import axios from 'axios';
import { BaseLLMProvider } from './base';
import { GenerateOptions } from '../types';

export class AnthropicProvider extends BaseLLMProvider {
  private apiUrl: string;

  constructor(config: any) {
    super(config);
    this.apiUrl = config.endpoint || 'https://api.anthropic.com/v1/messages';
  }

  async generate(options: GenerateOptions): Promise<{
    code: string;
    explanation?: string;
  }> {
    const mode = options.mode || 'production';
    const formattedPrompt = this.formatPrompt(options.prompt, mode);

    try {
      const response = await axios.post(
        this.apiUrl,
        {
          model: this.config.model || 'claude-3-opus-20240229',
          system: this.buildSystemPrompt(),
          messages: [{
            role: 'user',
            content: formattedPrompt
          }],
          max_tokens: options.maxTokens || 2000,
          temperature: options.temperature || 0.7
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'x-api-key': this.config.apiKey,
            'anthropic-version': '2023-06-01'
          }
        }
      );

      const content = response.data.content[0].text;
      return this.extractCodeFromResponse(content);
    } catch (error: any) {
      throw new Error(`Anthropic API error: ${error.message}`);
    }
  }
}