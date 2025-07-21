use craite::create_client;
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
dotenv::dotenv().ok();
let api_key = std::env::var("CRAITE_API_KEY")?;
let client = create_client(&api_key);

let result = client
    .generate("Create a DAO contract with voting")
    .language("solidity")
    .await?;

println!("Generated contract:\n{}", result.code);

Ok(())
}
