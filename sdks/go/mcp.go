package craite

import (
    "encoding/json"
    "fmt"
    "strings"
)

// MCPToolResult represents the result of an MCP tool execution
type MCPToolResult struct {
    Success  bool                   `json:"success"`
    Data     interface{}            `json:"data"`
    Error    string                 `json:"error,omitempty"`
    Metadata map[string]interface{} `json:"metadata,omitempty"`
}

// MCPTool interface for all MCP tools
type MCPTool interface {
    Name() string
    Description() string
    Execute(params map[string]interface{}) MCPToolResult
}

// OpenZeppelinTool provides OpenZeppelin contract templates
type OpenZeppelinTool struct {
    contracts map[string]contractTemplate
}

type contractTemplate struct {
    Base     string
    Features []string
    Template string
}

// NewOpenZeppelinTool creates a new OpenZeppelin tool
func NewOpenZeppelinTool() *OpenZeppelinTool {
    contracts := make(map[string]contractTemplate)
    
    contracts["ERC20"] = contractTemplate{
        Base: "@openzeppelin/contracts/token/ERC20/ERC20.sol",
        Features: []string{"Mintable", "Burnable", "Pausable", "Snapshot", "Permit"},
        Template: `pragma solidity ^0.8.0;

import "{base}";
{imports}

contract {name} is ERC20{features} {
    constructor() ERC20("{token_name}", "{symbol}") {
        {constructor_body}
    }
    
    {functions}
}`,
    }
    
    contracts["ERC721"] = contractTemplate{
        Base: "@openzeppelin/contracts/token/ERC721/ERC721.sol",
        Features: []string{"Enumerable", "URIStorage", "Burnable", "Pausable"},
        Template: `// ERC721 template`,
    }
    
    contracts["ERC1155"] = contractTemplate{
        Base: "@openzeppelin/contracts/token/ERC1155/ERC1155.sol",
        Features: []string{"Supply", "Burnable", "Pausable", "URIStorage"},
        Template: `// ERC1155 template`,
    }
    
    return &OpenZeppelinTool{contracts: contracts}
}

func (o *OpenZeppelinTool) Name() string {
    return "openzeppelin_contracts"
}

func (o *OpenZeppelinTool) Description() string {
    return "Access secure, audited smart contract templates from OpenZeppelin"
}

func (o *OpenZeppelinTool) Execute(params map[string]interface{}) MCPToolResult {
    contractType, _ := params["contract_type"].(string)
    if contractType == "" {
        contractType = "ERC20"
    }
    
    features, _ := params["features"].([]string)
    
    template, exists := o.contracts[contractType]
    if !exists {
        return MCPToolResult{
            Success: false,
            Error:   fmt.Sprintf("Unknown contract type: %s", contractType),
        }
    }
    
    // Build imports
    imports := []string{fmt.Sprintf(`import "%s";`, template.Base)}
    validFeatures := []string{}
    
    for _, feature := range features {
        if contains(template.Features, feature) {
            imports = append(imports, fmt.Sprintf(
                `import "@openzeppelin/contracts/token/%s/extensions/%s%s.sol";`,
                contractType, contractType, feature,
            ))
            validFeatures = append(validFeatures, feature)
        }
    }
    
    return MCPToolResult{
        Success: true,
        Data: map[string]interface{}{
            "contract_type": contractType,
            "imports":       imports,
            "features":      validFeatures,
            "template":      template.Template,
            "documentation": fmt.Sprintf("https://docs.openzeppelin.com/contracts/4.x/api/token/%s", strings.ToLower(contractType)),
        },
    }
}

// SecurityAuditTool provides security analysis
type SecurityAuditTool struct{}

func NewSecurityAuditTool() *SecurityAuditTool {
    return &SecurityAuditTool{}
}

func (s *SecurityAuditTool) Name() string {
    return "security_audit"
}

func (s *SecurityAuditTool) Description() string {
    return "Automated security checks and vulnerability detection"
}

func (s *SecurityAuditTool) Execute(params map[string]interface{}) MCPToolResult {
    code, _ := params["code"].(string)
    language, _ := params["language"].(string)
    if language == "" {
        language = "solidity"
    }
    
    issues := []map[string]interface{}{}
    
    if language == "solidity" {
        // Simple pattern matching for common vulnerabilities
        if strings.Contains(code, "call.value") || strings.Contains(code, ".call{value:") {
            issues = append(issues, map[string]interface{}{
                "type":     "reentrancy",
                "severity": "high",
                "message":  "Potential reentrancy vulnerability detected",
            })
        }
        
        if strings.Contains(code, "tx.origin") {
            issues = append(issues, map[string]interface{}{
                "type":     "access_control",
                "severity": "medium",
                "message":  "tx.origin used for authentication",
            })
        }
        
        if strings.Contains(code, "block.timestamp") {
            issues = append(issues, map[string]interface{}{
                "type":     "timestamp_dependence",
                "severity": "low",
                "message":  "Block timestamp used, can be manipulated by miners",
            })
        }
        
        if strings.Contains(code, "delegatecall") {
            issues = append(issues, map[string]interface{}{
                "type":     "delegatecall",
                "severity": "high",
                "message":  "Delegatecall usage detected, ensure target is trusted",
            })
        }
    }
    
    score := 100 - len(issues)*20
    if score < 0 {
        score = 0
    }
    
    return MCPToolResult{
        Success: true,
        Data: map[string]interface{}{
            "issues":          issues,
            "score":           score,
            "recommendations": getSecurityRecommendations(issues),
        },
    }
}

// GasOptimizationTool provides gas optimization suggestions
type GasOptimizationTool struct{}

func NewGasOptimizationTool() *GasOptimizationTool {
    return &GasOptimizationTool{}
}

func (g *GasOptimizationTool) Name() string {
    return "gas_optimization"
}

func (g *GasOptimizationTool) Description() string {
    return "Analyze and optimize gas consumption"
}

func (g *GasOptimizationTool) Execute(params map[string]interface{}) MCPToolResult {
    code, _ := params["code"].(string)
    
    suggestions := []map[string]interface{}{}
    
    // Pattern matching for common gas optimizations
    if strings.Contains(code, "string ") && !strings.Contains(code, "string memory") {
        suggestions = append(suggestions, map[string]interface{}{
            "type":       "storage",
            "suggestion": "Consider using bytes32 for fixed-length strings",
            "impact":     "high",
            "gas_saved":  "~2000 per storage slot",
        })
    }
    
    if strings.Contains(code, "for (") && strings.Contains(code, ".length") {
        suggestions = append(suggestions, map[string]interface{}{
            "type":       "loops",
            "suggestion": "Cache array length outside the loop",
            "impact":     "medium",
            "gas_saved":  "~100 per iteration",
        })
    }
    
    if strings.Contains(code, "i++") {
        suggestions = append(suggestions, map[string]interface{}{
            "type":       "loops",
            "suggestion": "Use ++i instead of i++ in loops",
            "impact":     "low",
            "gas_saved":  "~5 per iteration",
        })
    }
    
    if strings.Contains(code, "public") && !strings.Contains(code, "external") {
        suggestions = append(suggestions, map[string]interface{}{
            "type":       "functions",
            "suggestion": "Use external instead of public for functions not called internally",
            "impact":     "medium",
            "gas_saved":  "~200 per call",
        })
    }
    
    if strings.Contains(code, "storage") && strings.Contains(code, "=") {
        suggestions = append(suggestions, map[string]interface{}{
            "type":       "storage",
            "suggestion": "Minimize storage writes, batch updates when possible",
            "impact":     "high",
            "gas_saved":  "~5000-20000 per storage slot",
        })
    }
    
    estimatedSavings := len(suggestions) * 1000
    optimizationScore := 100 - len(suggestions)*10
    if optimizationScore < 0 {
        optimizationScore = 0
    }
    
    return MCPToolResult{
        Success: true,
        Data: map[string]interface{}{
            "suggestions":             suggestions,
            "estimated_total_savings": fmt.Sprintf("%d gas", estimatedSavings),
            "optimization_score":      optimizationScore,
        },
    }
}

// MCPToolRegistry manages all MCP tools
type MCPToolRegistry struct {
    tools map[string]MCPTool
}

// NewMCPToolRegistry creates a new tool registry with default tools
func NewMCPToolRegistry() *MCPToolRegistry {
    registry := &MCPToolRegistry{
        tools: make(map[string]MCPTool),
    }
    
    // Register default tools
    registry.Register(NewOpenZeppelinTool())
    registry.Register(NewSecurityAuditTool())
    registry.Register(NewGasOptimizationTool())
    
    return registry
}

func (r *MCPToolRegistry) Register(tool MCPTool) {
    r.tools[tool.Name()] = tool
}

func (r *MCPToolRegistry) Get(name string) (MCPTool, bool) {
    tool, exists := r.tools[name]
    return tool, exists
}

func (r *MCPToolRegistry) List() []string {
    names := make([]string, 0, len(r.tools))
    for name := range r.tools {
        names = append(names, name)
    }
    return names
}

func (r *MCPToolRegistry) Execute(toolName string, params map[string]interface{}) MCPToolResult {
    tool, exists := r.Get(toolName)
    if !exists {
        return MCPToolResult{
            Success: false,
            Error:   fmt.Sprintf("Tool not found: %s", toolName),
        }
    }
    
    return tool.Execute(params)
}

// Helper functions
func contains(slice []string, item string) bool {
    for _, s := range slice {
        if s == item {
            return true
        }
    }
    return false
}

func getSecurityRecommendations(issues []map[string]interface{}) []string {
    recommendations := []string{}
    
    for _, issue := range issues {
        issueType, _ := issue["type"].(string)
        switch issueType {
        case "reentrancy":
            recommendations = append(recommendations, "Use checks-effects-interactions pattern or ReentrancyGuard")
        case "access_control":
            recommendations = append(recommendations, "Use msg.sender for authentication instead of tx.origin")
        case "timestamp_dependence":
            recommendations = append(recommendations, "Avoid using block.timestamp for critical logic")
        case "delegatecall":
            recommendations = append(recommendations, "Ensure delegatecall targets are trusted and immutable")
        }
    }
    
    return recommendations
}