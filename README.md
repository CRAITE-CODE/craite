# CRAITE - Your Web3 AI CoPilot
CA: 2fSTec6ByDMo3V8MMehsGGgkBjNNh7ZfARAKcdqsbonk

![npm version](https://img.shields.io/npm/v/@craite/cli)
![PyPI version](https://img.shields.io/pypi/v/craite-sdk)
![Crates.io](https://img.shields.io/crates/v/craite)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

Create with conversation, not code. An open Web3 development framework with multi-language code generation, pluggable MCP tools, and community-driven knowledge expansion.

## 🚀 Quick Start

Choose your preferred language:

### JavaScript/TypeScript
```bash
npm install -g @craite/cli
craite init my-web3-project
```

### Python
```bash
pip install craite-sdk
craite-py generate "Create an ERC-20 token"
```

### Rust
```bash
cargo install craite --features cli
craite generate "Create a Solana program"
```

### Go
```bash
go install github.com/craite/craite-go/cmd/craite@latest
craite generate "Create a DeFi protocol"
```

## 📦 Packages & SDKs

### JavaScript/TypeScript Packages
- **[@craite/core](./packages/core)** - Core AI engine and LLM integration
- **[@craite/web3-tools](./packages/web3-tools)** - Web3 development utilities
- **[@craite/mcp-connectors](./packages/mcp-connectors)** - MCP tool integrations
- **[@craite/code-generator](./packages/code-generator)** - Code generation algorithms
- **[@craite/cli](./packages/cli)** - Command-line interface

### Language SDKs
- **[Python SDK](./sdks/python)** - Full-featured Python implementation
- **[Rust SDK](./sdks/rust)** - High-performance Rust implementation
- **[Go SDK](./sdks/go)** - Enterprise-ready Go implementation

## 🛠️ Features

### AI-Powered Code Generation
- Production-ready Web3 code in multiple languages
- Smart contract templates (Solidity, Rust, Move, Cairo)
- Frontend integration code
- Testing frameworks
- Trading bots and DeFi protocols

### 14+ MCP Tool Integrations
- OpenZeppelin contracts
- Solidity documentation
- Hardhat development
- Security auditing
- Gas optimization
- Solana development
- And more...

### Multi-Language Support
- **Solidity** - Ethereum smart contracts
- **Rust** - Solana, Near, CosmWasm
- **Python** - Trading bots, analytics
- **JavaScript/TypeScript** - dApps, Web3 integration
- **Go** - Backend services

### Flexible LLM Support
- OpenAI (GPT-4)
- Anthropic (Claude)
- Local LLM support
- Custom endpoints

## 📖 Documentation

Visit our [comprehensive documentation](./docs) for:
- [Getting Started Guide](./docs/getting-started.md)
- [API Reference](./docs/api-reference.md)
- [MCP Tools Guide](./docs/mcp-tools.md)
- [Examples](./docs/examples.md)

## 🔧 Development

### Prerequisites
- Node.js 18+ (for JS/TS packages)
- Python 3.8+ (for Python SDK)
- Rust 1.70+ (for Rust SDK)
- Go 1.21+ (for Go SDK)
- Git

### Setup

```bash
# Clone the repository
git clone https://github.com/craite/craite.git
cd craite

# Install all dependencies
make install

# Build all packages
make build

# Run tests
make test
```

### Project Structure
```
craite/
├── packages/          # JavaScript/TypeScript packages
├── sdks/             # Language-specific SDKs
│   ├── python/       # Python SDK
│   ├── rust/         # Rust SDK
│   └── go/           # Go SDK
├── examples/         # Usage examples
├── docker/           # Docker configurations
└── docs/            # Documentation
```

## 📝 Example Usage

### JavaScript/TypeScript
```javascript
import { CRAITE } from '@craite/core';

const craite = new CRAITE({
  apiKey: 'your-api-key',
  provider: 'openai'
});

const contract = await craite.generate({
  prompt: 'Create an ERC-20 token with mint and burn functions',
  language: 'solidity',
  mode: 'production'
});
```

### Python
```python
from craite import create_client

craite = create_client(api_key='your-api-key')

result = craite.generate(
    prompt='Create a Uniswap V3 arbitrage bot',
    language='python',
    mode='educational'
)
```

### Rust
```rust
use craite::{Craite, CraiteBuilder, GenerateOptions};

let craite = CraiteBuilder::new()
    .api_key("your-api-key")
    .build()?;

let result = craite.generate(GenerateOptions {
    prompt: "Create a Solana NFT program".to_string(),
    language: "rust".to_string(),
    ..Default::default()
}).await?;
```

### Go
```go
client := craite.NewClient(craite.Config{
    APIKey: "your-api-key",
})

result, _ := client.Generate(context.Background(), craite.GenerateOptions{
    Prompt:   "Create a cross-chain bridge",
    Language: "solidity",
})
```

## 🌟 Use Cases

- **Smart Contract Development**: Secure, optimized contracts for any blockchain
- **DApp Frontend**: Web3 connection and interaction code
- **Trading Bots**: Automated trading systems with risk management
- **DeFi Protocols**: Complex financial smart contracts
- **NFT Projects**: Marketplace and collection contracts
- **Cross-Chain**: Bridge contracts and multi-chain applications
- **Educational Learning**: Step-by-step blockchain development

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

CRAITE is open source software licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Website](https://craite.xyz)
- [Documentation](https://docs.craite.xyz/docs)
- [GitHub](https://github.com/CRAITE-CODE/craite)

---

**Note**: This project requires an API key from your chosen LLM provider (OpenAI, Anthropic, etc.) to function. See our [documentation](https://craite.xyz/docs) for setup instructions.

## 🚀 Update: Python SDK Now Functional!

The Python SDK (v1.0.2) has been updated. You can test it with:

```python
from craite import create_client

client = create_client('your-openai-api-key')
result = client.generate('Create an ERC-20 token')
print(result['code'])
```


## 📦 Published Packages

### NPM Packages
- CLI: [npmjs.com/package/@craite/cli](https://www.npmjs.com/package/@craite/cli)
- Core: [npmjs.com/package/@craite/core](https://www.npmjs.com/package/@craite/core)
- Web3 Tools: [npmjs.com/package/@craite/web3-tools](https://www.npmjs.com/package/@craite/web3-tools)
- MCP Connectors: [npmjs.com/package/@craite/mcp-connectors](https://www.npmjs.com/package/@craite/mcp-connectors)
- Code Generator: [npmjs.com/package/@craite/code-generator](https://www.npmjs.com/package/@craite/code-generator)

### Other Packages
- Python SDK: [pypi.org/project/craite-sdk](https://pypi.org/project/craite-sdk/)
- Rust Crate: [crates.io/crates/craite](https://crates.io/crates/craite)
- Go Module: `go get github.com/CRAITE-CODE/craite/sdks/go`
