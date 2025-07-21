#[derive(Debug, Clone)]
pub struct MCPTool {
    pub name: String,
    pub description: String,
}

impl MCPTool {
    pub fn new(name: &str, description: &str) -> Self {
        Self {
            name: name.to_string(),
            description: description.to_string(),
        }
    }
}
