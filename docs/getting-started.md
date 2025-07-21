Getting Started
Creating Your Account

Visit the CRAITE platform
Connect with your Web3 wallet or email
Complete your profile setup
Receive 850 starter credits

Understanding Credits

Earning Credits: Share code snippets that others purchase
Using Credits: Generate code, access premium snippets
Credit Values:

Basic queries: 1-5 credits
Complex code generation: 10-50 credits
Premium marketplace snippets: Variable pricing




Chat Interface
Starting a Conversation

Click "New" to start a fresh conversation
Type your Web3 development query
CRAITE will respond with code or educational content

Chat Modes
Direct Code Mode:

Provides production-ready code
Minimal explanations
Optimized for experienced developers

Educational Mode:

Step-by-step explanations
Best practices included
Perfect for learning

Example Queries

"Build a python script that connects to Ethereum"
"Create an ERC-20 token contract"
"How do I optimize gas fees?"
"Build a DeFi lending protocol"


Code Library
Saving Snippets

Generate code through chat
Click the snippet to view details
Select "Save to Library"
Add tags and description

Managing Your Library

Private Snippets: Only visible to you
Public Snippets: Available in marketplace
Categories: Python, Solidity, JavaScript, etc.
Search: Find snippets by language or keyword

Code Preview
Each snippet shows:

Language type
Creation date
Preview of first few lines
Credit value (if monetized)


Marketplace
Browsing Code

Navigate to the Market tab
Filter by:

All: View everything
Smart Contracts: Solidity code
Frontend: Web3 integration code


Sort by popularity, price, or rating

Purchasing Snippets

Click "Preview" to see code sample
Check the credit cost
Click "Buy Now" to purchase
Code is added to your library

Selling Your Code

Create high-quality code snippets
Set as "Public" in library
Add comprehensive description
Set credit price (1-100 credits)
Earn credits when others purchase

Quality Guidelines

Code must be functional and tested
Include clear comments
No malicious or harmful code
Original work only


Profile & Credits
Profile Overview

Username: Your display name
Credits: Current balance
Created: Snippets you've made
Saved: Your code library
Earned: Credits from sales
Reputation: Community rating (1-5)

Quick Actions

Buy More Credits: Purchase additional credits
View Analytics: Track your snippet performance
Account Settings: Manage preferences


Installation
Prerequisites

For JavaScript/TypeScript: Node.js 18+ and npm/yarn
For Python: Python 3.8+ and pip
For Rust: Rust 1.70+ and cargo
For Go: Go 1.21+
Git installed
API key from your LLM provider (OpenAI, Anthropic, etc.)

Quick Start
Choose your preferred language:
JavaScript/TypeScript
bash# Install globally
npm install -g @craite/cli

# Or with yarn
yarn global add @craite/cli

# Initialize a new project
craite init my-web3-project
cd my-web3-project
npm run dev
Python
bash# Install from PyPI
pip install craite-sdk

# Or install with extras for trading
pip install craite-sdk[trading]

# Use the CLI
craite-py generate "Create an ERC-20 token"
Rust
bash# Add to your project
cargo add craite

# Or install CLI globally
cargo install craite --features cli

# Use the CLI
craite generate "Create a Solana program"
Go
bash# Install the module
go get github.com/craite/craite-go

# Or install CLI
go install github.com/craite/craite-go/cmd/craite@latest

# Use the CLI
craite generate "Create a DeFi protocol"
Language-Specific Package Installation
JavaScript/TypeScript Packages
bash# Core AI engine
npm install @craite/core

# Web3 development tools
npm install @craite/web3-tools

# MCP connectors
npm install @craite/mcp-connectors

# Code generator
npm install @craite/code-generator
Python SDK
bash# Basic installation
pip install craite-sdk

# With specific extras
pip install craite-sdk[trading]  # Trading bot features
pip install craite-sdk[solana]   # Solana development
pip install craite-sdk[dev]      # Development tools
Rust Crate
toml# In Cargo.toml
[dependencies]
craite = "1.0"

# With CLI feature
craite = { version = "1.0", features = ["cli"] }
Go Module
go// In your Go code
import "github.com/craite/craite-go"

// Or use go get
go get github.com/craite/craite-go@latest

Configuration
Environment Setup
Create a .env file in your project root:
env# Required
OPENAI_API_KEY=your-api-key-here

# Optional - Use any LLM provider
LLM_PROVIDER=openai # or anthropic, cohere, local
LLM_MODEL=gpt-4 # or your preferred model
LLM_API_ENDPOINT=https://api.openai.com/v1 # for custom endpoints

# MCP Tools Configuration (Optional)
ENABLE_MCP_TOOLS=true
MCP_TOOLS_PATH=./mcp-tools
Configuration File
Create craite.config.js:
javascriptmodule.exports = {
  // LLM Configuration
  llm: {
    provider: process.env.LLM_PROVIDER || 'openai',
    model: process.env.LLM_MODEL || 'gpt-4',
    apiKey: process.env.OPENAI_API_KEY,
    endpoint: process.env.LLM_API_ENDPOINT
  },
  
  // MCP Tools to enable
  mcpTools: [
    'openzeppelin_contracts',
    'solidity_docs',
    'hardhat_dev',
    'foundry_toolkit',
    'web3js_integration',
    'moralis_api',
    'solana_development',
    'binance_trading',
    'hyperliquid_dex',
    'security_audit',
    'gas_optimization',
    'bitquery_analytics',
    'axiom_protocol',
    'erc_standards'
  ],
  
  // Output preferences
  output: {
    style: 'concise', // or 'educational'
    language: 'javascript', // default output language
    saveToFile: true
  }
}