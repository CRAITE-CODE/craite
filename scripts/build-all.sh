#!/bin/bash

# Build all CRAITE packages across all languages

set -e

echo "🔨 Building CRAITE packages..."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Build JavaScript/TypeScript packages
echo -e "${BLUE}Building JavaScript/TypeScript packages...${NC}"
npx lerna run build
echo -e "${GREEN}✓ JavaScript packages built${NC}"

# Build Python SDK
echo -e "${BLUE}Building Python SDK...${NC}"
cd sdks/python
python setup.py build
cd ../..
echo -e "${GREEN}✓ Python SDK built${NC}"

# Build Rust SDK
echo -e "${BLUE}Building Rust SDK...${NC}"
cd sdks/rust
cargo build --release --features cli
cd ../..
echo -e "${GREEN}✓ Rust SDK built${NC}"

# Build Go SDK
echo -e "${BLUE}Building Go SDK...${NC}"
cd sdks/go
go build -o bin/craite ./cmd/craite
cd ../..
echo -e "${GREEN}✓ Go SDK built${NC}"

echo -e "${GREEN}✨ All packages built successfully!${NC}"

# Create dist directory with all CLIs
echo -e "${YELLOW}Creating distribution directory...${NC}"
mkdir -p dist/cli

# Copy CLIs
cp packages/cli/bin/craite.js dist/cli/craite-js
cp sdks/rust/target/release/craite dist/cli/craite-rust
cp sdks/go/bin/craite dist/cli/craite-go

echo -e "${GREEN}✓ Distribution directory created at ./dist/cli${NC}"