use std::collections::HashMap;
use anyhow::Result;
use serde::{Deserialize, Serialize};

/// Result from MCP tool execution
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct MCPToolResult {
    pub success: bool,
    pub data: serde_json::Value,
    pub error: Option<String>,
    pub metadata: Option<HashMap<String, String>>,
}

/// Base trait for MCP tools
pub trait MCPTool: Send + Sync {
    fn name(&self) -> &str;
    fn description(&self) -> &str;
    fn execute(&self, params: &HashMap<String, serde_json::Value>) -> Result<MCPToolResult>;
}

/// OpenZeppelin contracts tool
pub struct OpenZeppelinTool {
    contracts: HashMap<String, ContractTemplate>,
}

#[derive(Debug, Clone)]
struct ContractTemplate {
    base: String,
    features: Vec<String>,
    template: String,
}

impl OpenZeppelinTool {
    pub fn new() -> Self {
        let mut contracts = HashMap::new();
        
        contracts.insert("ERC20".to_string(), ContractTemplate {
            base: "@openzeppelin/contracts/token/ERC20/ERC20.sol".to_string(),
            features: vec![
                "Mintable".to_string(),
                "Burnable".to_string(),
                "Pausable".to_string(),
                "Snapshot".to_string(),
                "Permit".to_string(),
            ],
            template: r#"
pragma solidity ^0.8.0;

import "{base}";
{imports}

contract {name} is ERC20{features} {
    constructor() ERC20("{token_name}", "{symbol}") {
        {constructor_body}
    }
    
    {functions}
}
"#.to_string(),
        });

        contracts.insert("ERC721".to_string(), ContractTemplate {
            base: "@openzeppelin/contracts/token/ERC721/ERC721.sol".to_string(),
            features: vec![
                "Enumerable".to_string(),
                "URIStorage".to_string(),
                "Burnable".to_string(),
                "Pausable".to_string(),
            ],
            template: "// ERC721 template".to_string(),
        });

        Self { contracts }
    }
}

impl MCPTool for OpenZeppelinTool {
    fn name(&self) -> &str {
        "openzeppelin_contracts"
    }

    fn description(&self) -> &str {
        "Access secure, audited smart contract templates from OpenZeppelin"
    }

    fn execute(&self, params: &HashMap<String, serde_json::Value>) -> Result<MCPToolResult> {
        let contract_type = params
            .get("contract_type")
            .and_then(|v| v.as_str())
            .unwrap_or("ERC20");

        let features = params
            .get("features")
            .and_then(|v| v.as_array())
            .map(|arr| {
                arr.iter()
                    .filter_map(|v| v.as_str().map(String::from))
                    .collect::<Vec<_>>()
            })
            .unwrap_or_default();

        if let Some(template) = self.contracts.get(contract_type) {
            let mut imports = vec![format!(r#"import "{}";"#, template.base)];
            
            for feature in &features {
                if template.features.contains(feature) {
                    imports.push(format!(
                        r#"import "@openzeppelin/contracts/token/{}/extensions/{}{}.sol";"#,
                        contract_type, contract_type, feature
                    ));
                }
            }

            Ok(MCPToolResult {
                success: true,
                data: serde_json::json!({
                    "contract_type": contract_type,
                    "imports": imports,
                    "features": features,
                    "template": template.template,
                    "documentation": format!("https://docs.openzeppelin.com/contracts/4.x/api/token/{}", contract_type.to_lowercase())
                }),
                error: None,
                metadata: None,
            })
        } else {
            Ok(MCPToolResult {
                success: false,
                data: serde_json::Value::Null,
                error: Some(format!("Unknown contract type: {}", contract_type)),
                metadata: None,
            })
        }
    }
}

/// Security audit tool
pub struct SecurityAuditTool;

impl SecurityAuditTool {
    pub fn new() -> Self {
        Self
    }
}

impl MCPTool for SecurityAuditTool {
    fn name(&self) -> &str {
        "security_audit"
    }

    fn description(&self) -> &str {
        "Automated security checks and vulnerability detection"
    }

    fn execute(&self, params: &HashMap<String, serde_json::Value>) -> Result<MCPToolResult> {
        let code = params
            .get("code")
            .and_then(|v| v.as_str())
            .unwrap_or("");

        let language = params
            .get("language")
            .and_then(|v| v.as_str())
            .unwrap_or("solidity");

        let mut issues = Vec::new();

        if language == "solidity" {
            // Simple pattern matching for demonstration
            if code.contains("call.value") || code.contains(".call{value:") {
                issues.push(serde_json::json!({
                    "type": "reentrancy",
                    "severity": "high",
                    "message": "Potential reentrancy vulnerability detected"
                }));
            }

            if code.contains("tx.origin") {
                issues.push(serde_json::json!({
                    "type": "access_control",
                    "severity": "medium",
                    "message": "tx.origin used for authentication"
                }));
            }

            if code.contains("block.timestamp") {
                issues.push(serde_json::json!({
                    "type": "timestamp_dependence",
                    "severity": "low",
                    "message": "Block timestamp used, can be manipulated by miners"
                }));
            }
        }

        let score = (100_i32 - (issues.len() as i32 * 20)).max(0);

        Ok(MCPToolResult {
            success: true,
            data: serde_json::json!({
                "issues": issues,
                "score": score,
                "recommendations": Self::get_recommendations(&issues)
            }),
            error: None,
            metadata: None,
        })
    }
}

impl SecurityAuditTool {
    fn get_recommendations(issues: &[serde_json::Value]) -> Vec<String> {
        let mut recommendations = Vec::new();

        for issue in issues {
            if let Some(issue_type) = issue["type"].as_str() {
                match issue_type {
                    "reentrancy" => recommendations.push(
                        "Use checks-effects-interactions pattern or ReentrancyGuard".to_string()
                    ),
                    "access_control" => recommendations.push(
                        "Use msg.sender for authentication instead of tx.origin".to_string()
                    ),
                    "timestamp_dependence" => recommendations.push(
                        "Avoid using block.timestamp for critical logic".to_string()
                    ),
                    _ => {}
                }
            }
        }

        recommendations
    }
}

/// Gas optimization tool
pub struct GasOptimizationTool;

impl GasOptimizationTool {
    pub fn new() -> Self {
        Self
    }
}

impl MCPTool for GasOptimizationTool {
    fn name(&self) -> &str {
        "gas_optimization"
    }

    fn description(&self) -> &str {
        "Analyze and optimize gas consumption"
    }

    fn execute(&self, params: &HashMap<String, serde_json::Value>) -> Result<MCPToolResult> {
        let code = params
            .get("code")
            .and_then(|v| v.as_str())
            .unwrap_or("");

        let mut suggestions = Vec::new();

        // Simple pattern matching for common optimizations
        if code.contains("string ") && !code.contains("string memory") {
            suggestions.push(serde_json::json!({
                "type": "storage",
                "suggestion": "Consider using bytes32 for fixed-length strings",
                "impact": "high",
                "gas_saved": "~2000 per storage slot"
            }));
        }

        if code.contains("for (") && code.contains(".length") {
            suggestions.push(serde_json::json!({
                "type": "loops",
                "suggestion": "Cache array length outside the loop",
                "impact": "medium",
                "gas_saved": "~100 per iteration"
            }));
        }

        if code.contains("i++") {
            suggestions.push(serde_json::json!({
                "type": "loops",
                "suggestion": "Use ++i instead of i++ in loops",
                "impact": "low",
                "gas_saved": "~5 per iteration"
            }));
        }

        if code.contains("public") && !code.contains("external") {
            suggestions.push(serde_json::json!({
                "type": "functions",
                "suggestion": "Use external instead of public for functions not called internally",
                "impact": "medium",
                "gas_saved": "~200 per call"
            }));
        }

        let estimated_savings = suggestions.len() * 1000;

        Ok(MCPToolResult {
            success: true,
            data: serde_json::json!({
                "suggestions": suggestions,
                "estimated_total_savings": format!("{} gas", estimated_savings),
                "optimization_score": 100 - (suggestions.len() * 10)
            }),
            error: None,
            metadata: None,
        })
    }
}

/// MCP tool registry
pub struct MCPToolRegistry {
    tools: HashMap<String, Box<dyn MCPTool>>,
}

impl MCPToolRegistry {
    pub fn new() -> Self {
        let mut registry = Self {
            tools: HashMap::new(),
        };

        // Register default tools
        registry.register(Box::new(OpenZeppelinTool::new()));
        registry.register(Box::new(SecurityAuditTool::new()));
        registry.register(Box::new(GasOptimizationTool::new()));

        registry
    }

    pub fn register(&mut self, tool: Box<dyn MCPTool>) {
        self.tools.insert(tool.name().to_string(), tool);
    }

    pub fn get(&self, name: &str) -> Option<&dyn MCPTool> {
        self.tools.get(name).map(|t| t.as_ref())
    }

    pub fn list(&self) -> Vec<&str> {
        self.tools.keys().map(|s| s.as_str()).collect()
    }

    pub fn execute(
        &self,
        tool_name: &str,
        params: &HashMap<String, serde_json::Value>,
    ) -> Result<MCPToolResult> {
        if let Some(tool) = self.get(tool_name) {
            tool.execute(params)
        } else {
            Ok(MCPToolResult {
                success: false,
                data: serde_json::Value::Null,
                error: Some(format!("Tool not found: {}", tool_name)),
                metadata: None,
            })
        }
    }
}