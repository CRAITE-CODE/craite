import { GenerateOptions, CRAITEConfig } from '../types';

export abstract class BaseLLMProvider {
  protected config: CRAITEConfig;

  constructor(config: CRAITEConfig) {
    this.config = config;
  }

  abstract generate(options: GenerateOptions): Promise<{
    code: string;
    explanation?: string;
  }>;

  protected buildSystemPrompt(): string {
    return `You are CRAITE, an elite Web3 code generator and AI development assistant. 
    You specialize in blockchain development, smart contracts, dApps, DeFi protocols, and NFTs.
    Generate production-ready, secure, and optimized code following best practices.`;
  }

  protected formatPrompt(userPrompt: string, mode: string): string {
    const modeInstructions = mode === 'educational' 
      ? 'Provide detailed explanations and comments to help the user learn.'
      : 'Generate clean, production-ready code with minimal but essential comments.';

    return `${this.buildSystemPrompt()}\n\n${modeInstructions}\n\nUser request: ${userPrompt}`;
  }

  protected extractCodeFromResponse(response: string): { code: string; explanation?: string } {
    // Basic implementation - can be overridden by specific providers
    const codeMatch = response.match(/```[\w]*\n([\s\S]*?)\n```/);
    
    if (codeMatch) {
      const code = codeMatch[1];
      const explanation = response.replace(codeMatch[0], '').trim();
      return { code, explanation: explanation || undefined };
    }

    // If no code blocks found, assume entire response is code
    return { code: response };
  }
}