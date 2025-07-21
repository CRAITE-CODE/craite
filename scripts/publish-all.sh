#!/bin/bash

# Publish all CRAITE packages to their respective registries

set -e

echo "📦 Publishing CRAITE packages..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Check if user is logged in to npm
echo -e "${BLUE}Checking npm authentication...${NC}"
if ! npm whoami > /dev/null 2>&1; then
    echo -e "${RED}Error: Not logged in to npm. Run 'npm login' first.${NC}"
    exit 1
fi
echo -e "${GREEN}✓ npm authenticated${NC}"

# Publish JavaScript packages
echo -e "${BLUE}Publishing JavaScript packages to npm...${NC}"
npx lerna publish --yes
echo -e "${GREEN}✓ JavaScript packages published${NC}"

# Publish Python package
echo -e "${BLUE}Publishing Python SDK to PyPI...${NC}"
cd sdks/python

# Check if twine is installed
if ! command -v twine &> /dev/null; then
    echo "Installing twine..."
    pip install twine
fi

# Build and upload
rm -rf dist build *.egg-info
python setup.py sdist bdist_wheel
twine upload dist/*
cd ../..
echo -e "${GREEN}✓ Python SDK published${NC}"

# Publish Rust crate
echo -e "${BLUE}Publishing Rust SDK to crates.io...${NC}"
cd sdks/rust

# Check if user is logged in to crates.io
if ! cargo login --list | grep -q "token"; then
    echo -e "${RED}Error: Not logged in to crates.io. Run 'cargo login' first.${NC}"
    exit 1
fi

cargo publish
cd ../..
echo -e "${GREEN}✓ Rust SDK published${NC}"

# Tag for Go module
echo -e "${BLUE}Creating tags for Go module...${NC}"
VERSION=$(cat sdks/go/go.mod | grep "module" | cut -d'/' -f3 | cut -d' ' -f1)
git tag -a "sdks/go/v1.0.0" -m "Release Go SDK v1.0.0"
git push origin "sdks/go/v1.0.0"
echo -e "${GREEN}✓ Go module tagged${NC}"

echo -e "${GREEN}✨ All packages published successfully!${NC}"
echo -e "${YELLOW}Package locations:${NC}"
echo "  npm: @craite/core, @craite/web3-tools, @craite/mcp-connectors, @craite/code-generator, @craite/cli"
echo "  PyPI: craite-sdk"
echo "  crates.io: craite"
echo "  Go: github.com/craite/craite-go"