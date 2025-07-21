use craite::create_client;
#[tokio::test]
async fn test_client_creation() {
let client = create_client("test-key");
assert_eq!(client.api_key(), "test-key");
}
