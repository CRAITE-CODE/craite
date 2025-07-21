"""
MCP Tools implementation for CRAITE Python SDK
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import json
from dataclasses import dataclass


@dataclass
class MCPToolResult:
    """Result from MCP tool execution"""
    success: bool
    data: Any
    error: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BaseMCPTool(ABC):
    """Base class for MCP tools"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> MCPToolResult:
        """Execute the tool with given parameters"""
        pass
    
    def validate_params(self, params: Dict[str, Any], required: List[str]) -> bool:
        """Validate required parameters"""
        return all(param in params for param in required)


class OpenZeppelinTool(BaseMCPTool):
    """OpenZeppelin contracts tool"""
    
    def __init__(self):
        super().__init__(
            "openzeppelin_contracts",
            "Access secure, audited smart contract templates from OpenZeppelin"
        )
        self.contracts = {
            "ERC20": {
                "base": "@openzeppelin/contracts/token/ERC20/ERC20.sol",
                "features": ["Mintable", "Burnable", "Pausable", "Snapshot", "Permit"],
                "template": """
pragma solidity ^0.8.0;

import "{base}";
{imports}

contract {name} is ERC20{features} {{
    constructor() ERC20("{token_name}", "{symbol}") {{
        {constructor_body}
    }}
    
    {functions}
}}
"""
            },
            "ERC721": {
                "base": "@openzeppelin/contracts/token/ERC721/ERC721.sol",
                "features": ["Enumerable", "URIStorage", "Burnable", "Pausable"],
                "template": "// ERC721 template"
            },
            "ERC1155": {
                "base": "@openzeppelin/contracts/token/ERC1155/ERC1155.sol",
                "features": ["Supply", "Burnable", "Pausable"],
                "template": "// ERC1155 template"
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> MCPToolResult:
        """Generate OpenZeppelin contract template"""
        
        contract_type = params.get("contract_type", "ERC20")
        features = params.get("features", [])
        
        if contract_type not in self.contracts:
            return MCPToolResult(
                success=False,
                data=None,
                error=f"Unknown contract type: {contract_type}"
            )
        
        contract_info = self.contracts[contract_type]
        
        # Build imports
        imports = [f'import "{contract_info["base"]}";']
        feature_names = []
        
        for feature in features:
            if feature in contract_info["features"]:
                imports.append(
                    f'import "@openzeppelin/contracts/token/{contract_type}/'
                    f'extensions/{contract_type}{feature}.sol";'
                )
                feature_names.append(feature)
        
        return MCPToolResult(
            success=True,
            data={
                "contract_type": contract_type,
                "imports": imports,
                "features": feature_names,
                "template": contract_info["template"],
                "documentation": f"https://docs.openzeppelin.com/contracts/4.x/api/token/{contract_type.lower()}"
            }
        )


class SolidityDocsTool(BaseMCPTool):
    """Solidity documentation tool"""
    
    def __init__(self):
        super().__init__(
            "solidity_docs",
            "Access Solidity language documentation and best practices"
        )
        self.topics = {
            "basics": {
                "variables": "State variables, local variables, and global variables",
                "functions": "Function modifiers, visibility, and state mutability",
                "events": "Event declaration and emission",
                "errors": "Custom errors and revert statements"
            },
            "advanced": {
                "assembly": "Inline assembly and Yul",
                "storage": "Storage layout and optimization",
                "security": "Common vulnerabilities and mitigations",
                "patterns": "Design patterns and best practices"
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> MCPToolResult:
        """Retrieve Solidity documentation"""
        
        topic = params.get("topic", "basics")
        subtopic = params.get("subtopic")
        
        if topic not in self.topics:
            return MCPToolResult(
                success=False,
                data=None,
                error=f"Unknown topic: {topic}"
            )
        
        data = {
            "topic": topic,
            "content": self.topics[topic],
            "examples": self._get_examples(topic, subtopic),
            "references": [
                "https://docs.soliditylang.org/",
                "https://ethereum.org/en/developers/docs/smart-contracts/"
            ]
        }
        
        return MCPToolResult(success=True, data=data)
    
    def _get_examples(self, topic: str, subtopic: Optional[str]) -> Dict[str, str]:
        """Get code examples for topic"""
        examples = {
            "basics": {
                "variables": """
uint256 public totalSupply;  // State variable
function transfer(address to, uint256 amount) public {
    uint256 balance = balances[msg.sender];  // Local variable
    require(balance >= amount, "Insufficient balance");
    // msg.sender is a global variable
}
""",
                "functions": """
modifier onlyOwner() {
    require(msg.sender == owner, "Not the owner");
    _;
}

function mint(address to, uint256 amount) public onlyOwner {
    _mint(to, amount);
}
"""
            }
        }
        
        return examples.get(topic, {}).get(subtopic, {})


class SecurityAuditTool(BaseMCPTool):
    """Security audit tool"""
    
    def __init__(self):
        super().__init__(
            "security_audit",
            "Automated security checks and vulnerability detection"
        )
        self.vulnerabilities = {
            "reentrancy": {
                "severity": "high",
                "description": "External calls can re-enter the contract",
                "mitigation": "Use checks-effects-interactions pattern or ReentrancyGuard"
            },
            "overflow": {
                "severity": "medium",
                "description": "Arithmetic operations can overflow",
                "mitigation": "Use SafeMath or Solidity 0.8+ built-in checks"
            },
            "access_control": {
                "severity": "high",
                "description": "Missing or incorrect access control",
                "mitigation": "Implement proper role-based access control"
            }
        }
    
    def execute(self, params: Dict[str, Any]) -> MCPToolResult:
        """Run security analysis"""
        
        code = params.get("code", "")
        language = params.get("language", "solidity")
        
        # Simple pattern matching for demo
        issues = []
        
        if language == "solidity":
            if "call.value" in code or ".call{value:" in code:
                issues.append({
                    "type": "reentrancy",
                    "line": "N/A",
                    "severity": "high",
                    "message": "Potential reentrancy vulnerability detected"
                })
            
            if "tx.origin" in code:
                issues.append({
                    "type": "access_control",
                    "line": "N/A",
                    "severity": "medium",
                    "message": "tx.origin used for authentication"
                })
        
        return MCPToolResult(
            success=True,
            data={
                "issues": issues,
                "score": max(0, 100 - len(issues) * 20),
                "recommendations": self._get_recommendations(issues)
            }
        )
    
    def _get_recommendations(self, issues: List[Dict[str, Any]]) -> List[str]:
        """Get security recommendations"""
        recommendations = []
        
        for issue in issues:
            vuln_type = issue["type"]
            if vuln_type in self.vulnerabilities:
                recommendations.append(self.vulnerabilities[vuln_type]["mitigation"])
        
        return recommendations


class GasOptimizationTool(BaseMCPTool):
    """Gas optimization tool"""
    
    def __init__(self):
        super().__init__(
            "gas_optimization",
            "Analyze and optimize gas consumption"
        )
        self.optimizations = {
            "storage": [
                "Pack struct variables",
                "Use bytes32 instead of string for fixed data",
                "Cache storage variables in memory"
            ],
            "loops": [
                "Cache array length outside loops",
                "Use ++i instead of i++",
                "Avoid unbounded loops"
            ],
            "functions": [
                "Use external instead of public when possible",
                "Use calldata instead of memory for read-only data",
                "Short-circuit conditions"
            ]
        }
    
    def execute(self, params: Dict[str, Any]) -> MCPToolResult:
        """Analyze gas usage and suggest optimizations"""
        
        code = params.get("code", "")
        
        suggestions = []
        
        # Simple pattern matching
        if "string " in code:
            suggestions.append({
                "type": "storage",
                "suggestion": "Consider using bytes32 for fixed-length strings",
                "impact": "high"
            })
        
        if "for (" in code and ".length" in code:
            suggestions.append({
                "type": "loops",
                "suggestion": "Cache array length outside the loop",
                "impact": "medium"
            })
        
        return MCPToolResult(
            success=True,
            data={
                "suggestions": suggestions,
                "estimated_savings": f"{len(suggestions) * 1000} gas",
                "optimizations": self.optimizations
            }
        )


class MCPToolRegistry:
    """Registry for MCP tools"""
    
    def __init__(self):
        self.tools: Dict[str, BaseMCPTool] = {}
        self._register_default_tools()
    
    def _register_default_tools(self):
        """Register default MCP tools"""
        default_tools = [
            OpenZeppelinTool(),
            SolidityDocsTool(),
            SecurityAuditTool(),
            GasOptimizationTool()
        ]
        
        for tool in default_tools:
            self.register_tool(tool)
    
    def register_tool(self, tool: BaseMCPTool):
        """Register a new tool"""
        self.tools[tool.name] = tool
    
    def get_tool(self, name: str) -> Optional[BaseMCPTool]:
        """Get tool by name"""
        return self.tools.get(name)
    
    def list_tools(self) -> List[str]:
        """List all available tools"""
        return list(self.tools.keys())
    
    def enable_tool(self, name: str) -> bool:
        """Enable a tool (already registered by default)"""
        return name in self.tools
    
    def execute_tool(self, name: str, params: Dict[str, Any]) -> MCPToolResult:
        """Execute a tool by name"""
        tool = self.get_tool(name)
        if not tool:
            return MCPToolResult(
                success=False,
                data=None,
                error=f"Tool not found: {name}"
            )
        
        return tool.execute(params)