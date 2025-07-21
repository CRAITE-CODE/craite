📝 Example Usage
JavaScript/TypeScript
javascriptimport { CRAITE } from '@craite/core';

const craite = new CRAITE({
  apiKey: 'your-api-key',
  provider: 'openai'
});

const contract = await craite.generate({
  prompt: 'Create an ERC-20 token with mint and burn functions',
  language: 'solidity',
  mode: 'production'
});
Python
pythonfrom craite import create_client

craite = create_client(api_key='your-api-key')

result = craite.generate(
    prompt='Create a Uniswap V3 arbitrage bot',
    language='python',
    mode='educational'
)
Rust
rustuse craite::{Craite, CraiteBuilder, GenerateOptions};

let craite = CraiteBuilder::new()
    .api_key("your-api-key")
    .build()?;

let result = craite.generate(GenerateOptions {
    prompt: "Create a Solana NFT program".to_string(),
    language: "rust".to_string(),
    ..Default::default()
}).await?;
Go
goclient := craite.NewClient(craite.Config{
    APIKey: "your-api-key",
})

result, _ := client.Generate(context.Background(), craite.GenerateOptions{
    Prompt:   "Create a cross-chain bridge",
    Language: "solidity",
})
🌟 Use Cases

Smart Contract Development: Secure, optimized contracts for any blockchain
DApp Frontend: Web3 connection and interaction code
Trading Bots: Automated trading systems with risk management
DeFi Protocols: Complex financial smart contracts
NFT Projects: Marketplace and collection contracts
Cross-Chain: Bridge contracts and multi-chain applications
Educational Learning: Step-by-step blockchain development