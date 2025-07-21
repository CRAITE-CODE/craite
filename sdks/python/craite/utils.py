"""
Utility functions for CRAITE Python SDK
"""
import re
import os
from typing import List, Dict, Any, Optional
import hashlib
import json
from datetime import datetime


def extract_code_blocks(content: str) -> List[Dict[str, Any]]:
    """Extract code blocks from markdown content"""
    pattern = r'```(\w*)\n([\s\S]*?)\n```'
    matches = re.finditer(pattern, content)
    
    blocks = []
    for match in matches:
        blocks.append({
            "language": match.group(1) or "plaintext",
            "code": match.group(2),
            "full_match": match.group(0)
        })
    
    return blocks


def validate_api_key(api_key: str) -> bool:
    """Validate API key format"""
    if not api_key:
        raise ValueError("API key is required")
    
    if len(api_key) < 20:
        raise ValueError("API key appears to be invalid")
    
    return True


def save_code_to_file(
    code: str,
    filename: str,
    directory: str = "generated",
    add_timestamp: bool = True
) -> str:
    """Save generated code to file"""
    
    # Create directory if it doesn't exist
    os.makedirs(directory, exist_ok=True)
    
    # Add timestamp if requested
    if add_timestamp:
        base, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base}_{timestamp}{ext}"
    
    filepath = os.path.join(directory, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
    
    return filepath


def format_solidity_code(code: str) -> str:
    """Basic Solidity code formatting"""
    # Add proper indentation
    lines = code.split('\n')
    formatted_lines = []
    indent_level = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Decrease indent for closing braces
        if stripped.startswith('}'):
            indent_level = max(0, indent_level - 1)
        
        # Add indentation
        if stripped:
            formatted_lines.append('    ' * indent_level + stripped)
        else:
            formatted_lines.append('')
        
        # Increase indent for opening braces
        if stripped.endswith('{'):
            indent_level += 1
    
    return '\n'.join(formatted_lines)


def format_python_code(code: str) -> str:
    """Format Python code using black if available"""
    try:
        import black
        return black.format_str(code, mode=black.Mode())
    except ImportError:
        # If black is not installed, return as-is
        return code


def estimate_gas_cost(code: str, network: str = "ethereum") -> Dict[str, Any]:
    """Estimate gas cost for smart contract deployment"""
    
    # Simple estimation based on code size and complexity
    base_gas = 21000
    code_size_gas = len(code.encode()) * 68  # Approximate gas per byte
    
    # Count operations for complexity
    complexity_multiplier = 1.0
    
    if "for (" in code or "while (" in code:
        complexity_multiplier += 0.3
    
    if "mapping" in code:
        complexity_multiplier += 0.2
    
    if "require(" in code or "assert(" in code:
        complexity_multiplier += 0.1 * code.count("require(")
    
    estimated_gas = int((base_gas + code_size_gas) * complexity_multiplier)
    
    # Gas prices (example values)
    gas_prices = {
        "ethereum": {"slow": 20, "standard": 30, "fast": 40},  # Gwei
        "polygon": {"slow": 30, "standard": 35, "fast": 40},
        "bsc": {"slow": 3, "standard": 5, "fast": 7}
    }
    
    network_prices = gas_prices.get(network, gas_prices["ethereum"])
    
    return {
        "estimated_gas": estimated_gas,
        "gas_prices_gwei": network_prices,
        "estimated_cost_eth": {
            speed: (estimated_gas * price) / 1e9
            for speed, price in network_prices.items()
        }
    }


def generate_contract_hash(code: str) -> str:
    """Generate a hash for contract code"""
    return hashlib.sha256(code.encode()).hexdigest()


def parse_constructor_args(code: str) -> List[Dict[str, str]]:
    """Parse constructor arguments from Solidity code"""
    constructor_pattern = r'constructor\s*\((.*?)\)'
    match = re.search(constructor_pattern, code, re.DOTALL)
    
    if not match:
        return []
    
    args_str = match.group(1)
    args = []
    
    # Simple parsing - would need more robust parser for production
    for arg in args_str.split(','):
        arg = arg.strip()
        if arg:
            parts = arg.split()
            if len(parts) >= 2:
                args.append({
                    "type": parts[0],
                    "name": parts[-1]
                })
    
    return args


def create_deployment_script(
    contract_name: str,
    constructor_args: List[Dict[str, str]],
    network: str = "hardhat"
) -> str:
    """Generate deployment script for smart contract"""
    
    args_params = ", ".join([arg["name"] for arg in constructor_args])
    args_comments = "\n".join([
        f"    // {arg['name']}: {arg['type']}"
        for arg in constructor_args
    ])
    
    script = f"""const hre = require("hardhat");

async function main() {{
    console.log("Deploying {contract_name}...");
    
    // Get constructor arguments
{args_comments}
    const constructorArgs = [{args_params}];
    
    // Deploy contract
    const Contract = await hre.ethers.getContractFactory("{contract_name}");
    const contract = await Contract.deploy(...constructorArgs);
    
    await contract.deployed();
    
    console.log("{contract_name} deployed to:", contract.address);
    
    // Verify on Etherscan (if not local network)
    if (network.name !== "hardhat" && network.name !== "localhost") {{
        console.log("Waiting for confirmations...");
        await contract.deployTransaction.wait(5);
        
        console.log("Verifying contract...");
        await hre.run("verify:verify", {{
            address: contract.address,
            constructorArguments: constructorArgs,
        }});
    }}
}}

main()
    .then(() => process.exit(0))
    .catch((error) => {{
        console.error(error);
        process.exit(1);
    }});
"""
    
    return script


def validate_web3_address(address: str, network: str = "ethereum") -> bool:
    """Validate blockchain address format"""
    
    if network in ["ethereum", "bsc", "polygon"]:
        # EVM-compatible address
        if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
            return False
        return True
    
    elif network == "solana":
        # Solana address (base58)
        if not re.match(r'^[1-9A-HJ-NP-Za-km-z]{32,44}$', address):
            return False
        return True
    
    return False


def create_test_template(
    contract_name: str,
    language: str = "javascript"
) -> str:
    """Generate test template for smart contract"""
    
    if language == "javascript":
        return f"""const {{ expect }} = require("chai");
const {{ ethers }} = require("hardhat");

describe("{contract_name}", function () {{
    let contract;
    let owner;
    let addr1;
    let addr2;
    
    beforeEach(async function () {{
        [owner, addr1, addr2] = await ethers.getSigners();
        
        const Contract = await ethers.getContractFactory("{contract_name}");
        contract = await Contract.deploy();
        await contract.deployed();
    }});
    
    describe("Deployment", function () {{
        it("Should set the right owner", async function () {{
            expect(await contract.owner()).to.equal(owner.address);
        }});
    }});
    
    describe("Transactions", function () {{
        it("Should transfer tokens between accounts", async function () {{
            // Add your test logic here
        }});
        
        it("Should fail if sender doesn't have enough tokens", async function () {{
            // Add your test logic here
        }});
    }});
}});
"""
    
    elif language == "python":
        return f"""import pytest
from brownie import {contract_name}, accounts, reverts

@pytest.fixture
def contract():
    return accounts[0].deploy({contract_name})

def test_deployment(contract):
    assert contract.owner() == accounts[0]

def test_transfer(contract):
    # Add your test logic here
    pass

def test_insufficient_balance(contract):
    # Add your test logic here
    with reverts("Insufficient balance"):
        # Transaction that should fail
        pass
"""
    
    return ""


# Blockchain-specific utilities
def get_chain_id(network: str) -> int:
    """Get chain ID for network"""
    chain_ids = {
        "ethereum": 1,
        "goerli": 5,
        "sepolia": 11155111,
        "polygon": 137,
        "mumbai": 80001,
        "bsc": 56,
        "bsc-testnet": 97,
        "arbitrum": 42161,
        "optimism": 10,
        "avalanche": 43114
    }
    
    return chain_ids.get(network, 1)


def format_wei_to_ether(wei_value: int) -> str:
    """Convert Wei to Ether with proper formatting"""
    ether = wei_value / 1e18
    return f"{ether:.6f} ETH"