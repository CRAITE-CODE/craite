"""Example: Generate a DeFi trading bot using CRAITE"""

import os
from dotenv import load_dotenv
from craite import create_client

load_dotenv()

def main():
    # Initialize client
    client = create_client(
        api_key=os.getenv("CRAITE_API_KEY"),
        provider="openai"
    )
    
    # Generate trading bot code
    result = client.generate(
        prompt="Create a Uniswap V3 arbitrage bot",
        language="solidity",
        options={
            "mode": "production",
            "include_tests": True
        }
    )
    
    print("Generated trading bot:")
    print(result["code"])
    
    # Save to file
    with open("trading_bot.sol", "w") as f:
        f.write(result["code"])

if __name__ == "__main__":
    main()
