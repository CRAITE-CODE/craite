package main

import (
    "context"
    "encoding/json"
    "fmt"
    "io/ioutil"
    "os"
    "path/filepath"
    "strings"
    
    "github.com/craite/craite-go"
    "github.com/joho/godotenv"
    "github.com/spf13/cobra"
    "github.com/fatih/color"
)

var (
    // Global flags
    apiKey   string
    provider string
    model    string
    
    // Color printers
    greenBold  = color.New(color.FgGreen, color.Bold).SprintFunc()
    redBold    = color.New(color.FgRed, color.Bold).SprintFunc()
    yellowBold = color.New(color.FgYellow, color.Bold).SprintFunc()
    cyanBold   = color.New(color.FgCyan, color.Bold).SprintFunc()
    dimmed     = color.New(color.Faint).SprintFunc()
)

func main() {
    // Load .env file if present
    godotenv.Load()
    
    var rootCmd = &cobra.Command{
        Use:   "craite",
        Short: "CRAITE - Elite Web3 Code Generator & AI Development Platform",
        Long:  `CRAITE is a sophisticated Web3-focused AI development platform that combines advanced code generation capabilities with comprehensive blockchain development resources.`,
        Version: "1.0.0",
    }
    
    // Global flags
    rootCmd.PersistentFlags().StringVar(&apiKey, "api-key", os.Getenv("OPENAI_API_KEY"), "API key for LLM provider")
    rootCmd.PersistentFlags().StringVar(&provider, "provider", "openai", "LLM provider (openai, anthropic, local)")
    rootCmd.PersistentFlags().StringVar(&model, "model", "gpt-4", "Model to use")
    
    // Add commands
    rootCmd.AddCommand(generateCmd())
    rootCmd.AddCommand(scaffoldCmd())
    rootCmd.AddCommand(analyzeCmd())
    rootCmd.AddCommand(toolsCmd())
    rootCmd.AddCommand(initCmd())
    
    if err := rootCmd.Execute(); err != nil {
        fmt.Println(redBold("Error:"), err)
        os.Exit(1)
    }
}

func generateCmd() *cobra.Command {
    var (
        language string
        mode     string
        output   string
        tools    []string
    )
    
    cmd := &cobra.Command{
        Use:   "generate [prompt]",
        Short: "Generate code from a prompt",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            if apiKey == "" {
                fmt.Println(redBold("Error:"), "API key is required. Set OPENAI_API_KEY or use --api-key")
                os.Exit(1)
            }
            
            prompt := args[0]
            fmt.Println(greenBold("Generating code..."))
            
            config := craite.Config{
                APIKey:   apiKey,
                Provider: parseProvider(provider),
                Model:    model,
                MCPTools: tools,
            }
            
            client := craite.NewClient(config)
            
            opts := craite.GenerateOptions{
                Prompt:      prompt,
                Language:    language,
                Mode:        parseMode(mode),
                Temperature: 0.7,
                MaxTokens:   2000,
            }
            
            ctx := context.Background()
            
            var result *craite.GenerateResult
            var err error
            
            if len(tools) > 0 {
                result, err = client.GenerateWithTools(ctx, opts, tools)
            } else {
                result, err = client.Generate(ctx, opts)
            }
            
            if err != nil {
                fmt.Println(redBold("Error:"), err)
                os.Exit(1)
            }
            
            fmt.Println("\n" + greenBold("Generated Code:"))
            fmt.Println(strings.Repeat("─", 50))
            fmt.Println(result.Code)
            
            if result.Explanation != "" && mode == "educational" {
                fmt.Println("\n" + cyanBold("Explanation:"))
                fmt.Println(result.Explanation)
            }
            
            if len(result.ToolsUsed) > 0 {
                fmt.Printf("\n%s %s\n", yellowBold("MCP Tools Used:"), strings.Join(result.ToolsUsed, ", "))
            }
            
            if output != "" {
                if err := ioutil.WriteFile(output, []byte(result.Code), 0644); err != nil {
                    fmt.Println(redBold("Error saving file:"), err)
                    os.Exit(1)
                }
                fmt.Printf("\n%s %s\n", greenBold("✓ Code saved to:"), output)
            }
        },
    }
    
    cmd.Flags().StringVarP(&language, "language", "l", "solidity", "Output language")
    cmd.Flags().StringVarP(&mode, "mode", "m", "production", "Generation mode (production/educational)")
    cmd.Flags().StringVarP(&output, "output", "o", "", "Output file path")
    cmd.Flags().StringSliceVarP(&tools, "tools", "t", []string{}, "MCP tools to use")
    
    return cmd
}

func scaffoldCmd() *cobra.Command {
    var (
        name     string
        features []string
        output   string
    )
    
    cmd := &cobra.Command{
        Use:   "scaffold [contract-type]",
        Short: "Generate a smart contract scaffold",
        Args:  cobra.ExactArgs(1),
        ValidArgs: []string{"ERC20", "ERC721", "ERC1155"},
        Run: func(cmd *cobra.Command, args []string) {
            contractType := args[0]
            
            prompt := fmt.Sprintf("Create a %s contract named %s", contractType, name)
            if len(features) > 0 {
                prompt += fmt.Sprintf(" with features: %s", strings.Join(features, ", "))
            }
            
            // Reuse generate logic
            fmt.Printf("%s %s contract...\n", greenBold("Scaffolding"), contractType)
            
            // Would implement similar to generate command
        },
    }
    
    cmd.Flags().StringVarP(&name, "name", "n", "MyContract", "Contract name")
    cmd.Flags().StringSliceVarP(&features, "features", "f", []string{}, "Contract features")
    cmd.Flags().StringVarP(&output, "output", "o", "", "Output file path")
    
    return cmd
}

func analyzeCmd() *cobra.Command {
    var (
        security bool
        gas      bool
    )
    
    cmd := &cobra.Command{
        Use:   "analyze [file]",
        Short: "Analyze a smart contract",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            file := args[0]
            
            code, err := ioutil.ReadFile(file)
            if err != nil {
                fmt.Println(redBold("Error reading file:"), err)
                os.Exit(1)
            }
            
            fmt.Printf("%s %s\n", cyanBold("Analyzing:"), file)
            fmt.Println(strings.Repeat("─", 50))
            
            registry := craite.NewMCPToolRegistry()
            
            if security {
                fmt.Println("\n" + redBold("Security Analysis:"))
                
                result := registry.Execute("security_audit", map[string]interface{}{
                    "code":     string(code),
                    "language": "solidity",
                })
                
                if result.Success {
                    data := result.Data.(map[string]interface{})
                    fmt.Printf("Score: %v/100\n", data["score"])
                    
                    if issues, ok := data["issues"].([]interface{}); ok && len(issues) > 0 {
                        fmt.Println("\nIssues found:")
                        for _, issue := range issues {
                            if issueMap, ok := issue.(map[string]interface{}); ok {
                                fmt.Printf("  • %s (%s): %s\n",
                                    issueMap["type"],
                                    issueMap["severity"],
                                    issueMap["message"])
                            }
                        }
                    } else {
                        fmt.Println(greenBold("✓ No security issues found!"))
                    }
                }
            }
            
            if gas {
                fmt.Println("\n" + yellowBold("Gas Optimization:"))
                
                result := registry.Execute("gas_optimization", map[string]interface{}{
                    "code": string(code),
                })
                
                if result.Success {
                    data := result.Data.(map[string]interface{})
                    fmt.Printf("Optimization Score: %v/100\n", data["optimization_score"])
                    fmt.Printf("Estimated Savings: %v\n", data["estimated_total_savings"])
                    
                    if suggestions, ok := data["suggestions"].([]interface{}); ok && len(suggestions) > 0 {
                        fmt.Println("\nSuggestions:")
                        for _, suggestion := range suggestions {
                            if suggMap, ok := suggestion.(map[string]interface{}); ok {
                                fmt.Printf("  • %s: %s (Impact: %s)\n",
                                    suggMap["type"],
                                    suggMap["suggestion"],
                                    suggMap["impact"])
                            }
                        }
                    } else {
                        fmt.Println(greenBold("✓ Code is well optimized!"))
                    }
                }
            }
        },
    }
    
    cmd.Flags().BoolVar(&security, "security", true, "Run security audit")
    cmd.Flags().BoolVar(&gas, "gas", true, "Run gas optimization")
    
    return cmd
}

func toolsCmd() *cobra.Command {
    return &cobra.Command{
        Use:   "tools",
        Short: "List available MCP tools",
        Run: func(cmd *cobra.Command, args []string) {
            fmt.Println(cyanBold("Available MCP Tools:"))
            fmt.Println(strings.Repeat("─", 50))
            
            tools := []struct {
                name string
                desc string
            }{
                {"openzeppelin_contracts", "OpenZeppelin contract templates"},
                {"solidity_docs", "Solidity documentation and best practices"},
                {"hardhat_dev", "Hardhat development environment"},
                {"foundry_toolkit", "Foundry smart contract toolkit"},
                {"web3js_integration", "Web3.js integration helpers"},
                {"moralis_api", "Moralis Web3 infrastructure"},
                {"solana_development", "Solana program development"},
                {"binance_trading", "Binance trading APIs"},
                {"hyperliquid_dex", "Hyperliquid DEX integration"},
                {"security_audit", "Automated security analysis"},
                {"gas_optimization", "Gas usage optimization"},
                {"bitquery_analytics", "Blockchain data analytics"},
                {"axiom_protocol", "Zero-knowledge proofs"},
                {"erc_standards", "ERC token standards"},
            }
            
            for _, tool := range tools {
                fmt.Printf("  %s - %s\n", greenBold(tool.name), tool.desc)
            }
        },
    }
}

func initCmd() *cobra.Command {
    var template string
    
    cmd := &cobra.Command{
        Use:   "init [project-name]",
        Short: "Create a new Web3 project",
        Args:  cobra.ExactArgs(1),
        Run: func(cmd *cobra.Command, args []string) {
            projectName := args[0]
            
            fmt.Printf("%s %s project: %s\n", greenBold("Creating"), template, projectName)
            
            // Create project structure
            dirs := []string{
                filepath.Join(projectName, "contracts"),
                filepath.Join(projectName, "scripts"),
                filepath.Join(projectName, "test"),
                filepath.Join(projectName, "docs"),
            }
            
            for _, dir := range dirs {
                if err := os.MkdirAll(dir, 0755); err != nil {
                    fmt.Println(redBold("Error creating directory:"), err)
                    os.Exit(1)
                }
            }
            
            // Create basic files
            // ... implementation
            
            fmt.Println(greenBold("✓ Project created!"))
            fmt.Println("\n" + cyanBold("Next steps:"))
            fmt.Printf("  cd %s\n", projectName)
            fmt.Println("  go mod init")
            fmt.Println("  craite generate \"Create an ERC20 token\"")
        },
    }
    
    cmd.Flags().StringVarP(&template, "template", "t", "basic", "Project template")
    
    return cmd
}

// Helper functions
func parseProvider(p string) craite.Provider {
    switch p {
    case "openai":
        return craite.OpenAI
    case "anthropic":
        return craite.Anthropic
    case "local":
        return craite.Local
    default:
        return craite.OpenAI
    }
}

func parseMode(m string) craite.Mode {
    switch m {
    case "educational":
        return craite.Educational
    default:
        return craite.Production
    }
}