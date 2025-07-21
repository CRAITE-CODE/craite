import { CRAITEConfig, GenerateOptions, GenerateResult, MCPTool } from './types';
import { BaseLLMProvider } from './llm-providers/base';
import { OpenAIProvider } from './llm-providers/openai';
import { AnthropicProvider } from './llm-providers/anthropic';

export class CRAITE {
  private llmProvider: BaseLLMProvider;
  private mcpTools: Map<string, MCPTool> = new Map();
  private config: CRAITEConfig;

  constructor(config: CRAITEConfig) {
    this.config = config;
    this.llmProvider = this.initializeLLMProvider(config);
    
    // Initialize MCP tools if provided
    if (config.mcpTools) {
      this.initializeMCPTools(config.mcpTools);
    }
  }

  private initializeLLMProvider(config: CRAITEConfig): BaseLLMProvider {
    switch (config.provider || 'openai') {
      case 'openai':
        return new OpenAIProvider(config);
      case 'anthropic':
        return new AnthropicProvider(config);
      default:
        throw new Error(`Unsupported LLM provider: ${config.provider}`);
    }
  }

  private initializeMCPTools(toolNames: string[]) {
    // This would be implemented with actual MCP connector integration
    // For now, we'll stub it
    toolNames.forEach(toolName => {
      this.mcpTools.set(toolName, {
        name: toolName,
        description: `MCP tool: ${toolName}`,
        execute: async (__params: any) => {
          // Stub implementation
          return { success: true, data: {} };
        }
      });
    });
  }

  async generate(options: GenerateOptions): Promise<GenerateResult> {
    // Apply default mode if not specified
    const mode = options.mode || this.config.output?.style || 'production';
    
    // Prepare the prompt with mode context
    const enhancedPrompt = this.enhancePromptWithMode(options.prompt, mode);
    
    // Generate code using LLM provider
    const result = await this.llmProvider.generate({
      ...options,
      prompt: enhancedPrompt
    });

    return {
      code: result.code,
      language: options.language || 'javascript',
      explanation: mode === 'educational' ? result.explanation : undefined,
      toolsUsed: []
    };
  }

  async generateWithTools(options: GenerateOptions & { tools: string[] }): Promise<GenerateResult> {
    const toolsUsed: string[] = [];
    const toolResults: any[] = [];

    // Execute relevant MCP tools
    for (const toolName of options.tools) {
      const tool = this.mcpTools.get(toolName);
      if (tool) {
        const result = await this.useTool(toolName, { query: options.prompt });
        if (result) {
          toolResults.push(result);
          toolsUsed.push(toolName);
        }
      }
    }

    // Enhance prompt with tool results
    const enhancedPrompt = this.enhancePromptWithToolResults(
      options.prompt,
      toolResults
    );

    // Generate code with enhanced context
    const result = await this.generate({
      ...options,
      prompt: enhancedPrompt
    });

    return {
      ...result,
      toolsUsed
    };
  }

  async useTool(toolName: string, params: any): Promise<any> {
    const tool = this.mcpTools.get(toolName);
    if (!tool) {
      throw new Error(`MCP tool not found: ${toolName}`);
    }

    return await tool.execute(params);
  }

  registerTool(tool: MCPTool): void {
    this.mcpTools.set(tool.name, tool);
  }

  private enhancePromptWithMode(prompt: string, mode: string): string {
    const modeInstructions = {
      production: 'Generate production-ready code with minimal comments. Focus on efficiency and best practices.',
      educational: 'Generate code with detailed explanations, comments, and step-by-step guidance for learning.'
    };

    return `${modeInstructions[mode as keyof typeof modeInstructions] || ''}\n\n${prompt}`;
  }

  private enhancePromptWithToolResults(prompt: string, toolResults: any[]): string {
    if (toolResults.length === 0) return prompt;

    const context = toolResults
      .map(result => `Tool: ${result.tool}\nResult: ${JSON.stringify(result.data)}`)
      .join('\n\n');

    return `${prompt}\n\nAdditional context from MCP tools:\n${context}`;
  }

  // Utility methods
  getSupportedLanguages(): string[] {
    return ['javascript', 'typescript', 'solidity', 'python', 'rust'];
  }

  getAvailableTools(): string[] {
    return Array.from(this.mcpTools.keys());
  }

  getConfig(): CRAITEConfig {
    return { ...this.config };
  }
}