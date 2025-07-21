//! CRAITE Rust SDK for Web3 AI Development

pub mod client;
pub mod mcp;

pub use client::{CraiteClient, CraiteConfig};
pub use mcp::MCPTool;

/// Create a new CRAITE client
pub fn create_client(api_key: &str) -> CraiteClient {
    CraiteClient::new(api_key)
}
