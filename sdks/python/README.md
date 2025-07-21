# CRAITE Python SDK

Web3 AI development in Python.

## Installation

```bash
pip install craite-sdk
Quick Start
pythonfrom craite import create_client

# Initialize client
client = create_client("your-api-key")

# Generate smart contract
result = client.generate("Create an ERC-20 token with burn function")
print(result["code"])
Features

🚀 Simple API for Web3 code generation
🔧 Support for multiple LLM providers
🎯 14+ specialized MCP tools
📦 Multi-language output (Solidity, Rust, etc.)
⚡ Async support

Documentation
Full documentation at https://craite.xyz/docs
