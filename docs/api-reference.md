API Reference
JavaScript/TypeScript
javascriptimport { CRAITE } from '@craite/core';

// Initialize CRAITE
const craite = new CRAITE({
  apiKey: 'your-api-key',
  provider: 'openai' // or any LLM provider
});

// Generate code
const code = await craite.generate({
  prompt: 'Create an ERC-20 token contract',
  language: 'solidity',
  mode: 'production' // or 'educational'
});
Python
pythonfrom craite import create_client

# Initialize client
craite = create_client(
    api_key='your-api-key',
    provider='openai'  # or 'anthropic', 'local', etc.
)

# Generate code
result = craite.generate(
    prompt='Create an ERC-20 token contract',
    language='solidity',
    mode='production'
)

# Async generation
import asyncio
from craite import create_async_client

async def generate_async():
    craite = create_async_client(api_key='your-api-key')
    result = await craite.generate_async(
        prompt='Create a DeFi protocol',
        language='solidity'
    )
Rust
rustuse craite::{Craite, CraiteBuilder, GenerateOptions, GenerationMode};

#[tokio::main]
async fn main() -> Result<()> {
    // Build client
    let craite = CraiteBuilder::new()
        .api_key("your-api-key")
        .provider(LLMProvider::OpenAI)
        .build()?;
    
    // Generate code
    let result = craite.generate(GenerateOptions {
        prompt: "Create a Solana NFT program".to_string(),
        language: "rust".to_string(),
        mode: GenerationMode::Production,
        ..Default::default()
    }).await?;
    
    println!("{}", result.code);
    Ok(())
}
Go
gopackage main

import (
    "context"
    "github.com/craite/craite-go"
)

func main() {
    // Create client
    client := craite.NewClient(craite.Config{
        APIKey:   "your-api-key",
        Provider: craite.OpenAI,
    })
    
    // Generate code
    result, err := client.Generate(context.Background(), craite.GenerateOptions{
        Prompt:   "Create an ERC-20 token",
        Language: "solidity",
        Mode:     craite.Production,
    })
    
    if err != nil {
        panic(err)
    }
    
    fmt.Println(result.Code)
}
Common Methods Across All SDKs
All SDKs provide these core methods:

generate() - Basic code generation
generateWithTools() - Generation with MCP tools
CLI commands:

generate - Generate code from prompt
scaffold - Create contract templates
analyze - Security and gas analysis
tools - List available MCP tools