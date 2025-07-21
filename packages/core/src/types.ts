export interface CRAITEConfig {
    apiKey: string;
    provider?: 'openai' | 'anthropic' | 'cohere' | 'local' | string;
    model?: string;
    endpoint?: string;
    mcpTools?: string[];
    output?: {
      style?: 'concise' | 'educational';
      language?: string;
      saveToFile?: boolean;
    };
  }
  
  export interface GenerateOptions {
    prompt: string;
    language?: string;
    mode?: 'production' | 'educational';
    temperature?: number;
    maxTokens?: number;
  }
  
  export interface GenerateResult {
    code: string;
    language: string;
    explanation?: string;
    toolsUsed?: string[];
  }
  
  export interface MCPTool {
    name: string;
    description: string;
    execute: (params: any) => Promise<any>;
  }
  
  export interface LLMProvider {
    generate(options: GenerateOptions): Promise<{ code: string; explanation?: string }>;
  }
  
  export type CodeMode = 'production' | 'educational';
  
  export interface ToolResult {
    tool: string;
    success: boolean;
    data: any;
    error?: string;
  }
  
  export interface CodeSnippet {
    id: string;
    title: string;
    description: string;
    code: string;
    language: string;
    tags: string[];
    author?: string;
    credits?: number;
    public: boolean;
    created: Date;
    updated: Date;
  }