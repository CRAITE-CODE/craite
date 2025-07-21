# CRAITE Rust SDK

Web3 AI development in Rust.

## Installation

```toml
[dependencies]
craite = "1.0.0"
Usage
rustuse craite::create_client;

#[tokio::main]
async fn main() {
    let client = create_client("your-api-key");
    let result = client.generate("Create an ERC-20 token").await?;
    println!("{}", result.code);
}
