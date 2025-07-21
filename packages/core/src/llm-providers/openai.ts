import axios from 'axios';
import { BaseLLMProvider } from './base';
import { GenerateOptions } from '../types';

export class OpenAIProvider extends BaseLLMProvider {
  private apiUrl: string;

  constructor(config: any) {
    super(config);
    this.apiUrl = config.endpoint || 'https://api.openai.com/v1/chat/completions';
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
          model: this.config.model || 'gpt-4',
          messages: [
            {
              role: 'system',
              content: this.buildSystemPrompt()
            },
            {
              role: 'user',
              content: formattedPrompt
            }
          ],
          temperature: options.temperature || 0.7,
          max_tokens: options.maxTokens || 2000
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.config.apiKey}`
          }
        }
      );

      const content = response.data.choices[0].message.content;
      return this.extractCodeFromResponse(content);
    } catch (error: any) {
      throw new Error(`OpenAI API error: ${error.message}`);
    }
  }
}