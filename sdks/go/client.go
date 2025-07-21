package craite

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "io"
    "net/http"
    "time"
)

// ApiClient handles HTTP communication with LLM providers
type ApiClient struct {
    httpClient *http.Client
    config     Config
}

// NewApiClient creates a new API client
func NewApiClient(config Config) *ApiClient {
    return &ApiClient{
        httpClient: &http.Client{
            Timeout: 30 * time.Second,
        },
        config: config,
    }
}

// Generate makes an API call to generate code
func (a *ApiClient) Generate(ctx context.Context, opts GenerateOptions) (*GenerateResult, error) {
    systemPrompt := a.buildSystemPrompt(opts.Mode)
    payload := a.buildPayload(opts, systemPrompt)
    
    req, err := http.NewRequestWithContext(ctx, "POST", a.getEndpoint(), bytes.NewBuffer(payload))
    if err != nil {
        return nil, fmt.Errorf("creating request: %w", err)
    }
    
    a.setHeaders(req)
    
    resp, err := a.httpClient.Do(req)
    if err != nil {
        return nil, fmt.Errorf("sending request: %w", err)
    }
    defer resp.Body.Close()
    
    if resp.StatusCode != http.StatusOK {
        body, _ := io.ReadAll(resp.Body)
        return nil, fmt.Errorf("API error %d: %s", resp.StatusCode, string(body))
    }
    
    var response map[string]interface{}
    if err := json.NewDecoder(resp.Body).Decode(&response); err != nil {
        return nil, fmt.Errorf("decoding response: %w", err)
    }
    
    return a.parseResponse(response, opts.Language)
}

func (a *ApiClient) buildSystemPrompt(mode Mode) string {
    base := `You are CRAITE, an elite Web3 code generator and AI development assistant. 
You specialize in blockchain development, smart contracts, dApps, DeFi protocols, and NFTs. 
Generate production-ready, secure, and optimized code following best practices.`
    
    switch mode {
    case Educational:
        return base + "\nProvide detailed explanations and comments to help the user learn."
    case Production:
        return base + "\nGenerate clean, production-ready code with minimal but essential comments."
    default:
        return base
    }
}

func (a *ApiClient) buildPayload(opts GenerateOptions, systemPrompt string) []byte {
    var payload interface{}
    
    switch a.config.Provider {
    case OpenAI:
        payload = map[string]interface{}{
            "model": a.config.Model,
            "messages": []map[string]string{
                {"role": "system", "content": systemPrompt},
                {"role": "user", "content": opts.Prompt},
            },
            "temperature": opts.Temperature,
            "max_tokens":  opts.MaxTokens,
        }
    case Anthropic:
        payload = map[string]interface{}{
            "model":       a.config.Model,
            "system":      systemPrompt,
            "messages":    []map[string]string{{"role": "user", "content": opts.Prompt}},
            "max_tokens":  opts.MaxTokens,
            "temperature": opts.Temperature,
        }
    default:
        payload = map[string]interface{}{
            "model":       a.config.Model,
            "prompt":      fmt.Sprintf("%s\n\n%s", systemPrompt, opts.Prompt),
            "temperature": opts.Temperature,
            "max_tokens":  opts.MaxTokens,
            "stream":      false,
        }
    }
    
    data, _ := json.Marshal(payload)
    return data
}

func (a *ApiClient) setHeaders(req *http.Request) {
    req.Header.Set("Content-Type", "application/json")
    
    switch a.config.Provider {
    case OpenAI:
        req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", a.config.APIKey))
    case Anthropic:
        req.Header.Set("x-api-key", a.config.APIKey)
        req.Header.Set("anthropic-version", "2023-06-01")
    }
}

func (a *ApiClient) getEndpoint() string {
    if a.config.Endpoint != "" {
        return a.config.Endpoint
    }
    
    switch a.config.Provider {
    case OpenAI:
        return "https://api.openai.com/v1/chat/completions"
    case Anthropic:
        return "https://api.anthropic.com/v1/messages"
    case Local:
        return "http://localhost:11434/api/generate"
    default:
        return "https://api.openai.com/v1/chat/completions"
    }
}

func (a *ApiClient) parseResponse(response map[string]interface{}, language string) (*GenerateResult, error) {
    var content string
    
    switch a.config.Provider {
    case OpenAI:
        if choices, ok := response["choices"].([]interface{}); ok && len(choices) > 0 {
            if msg, ok := choices[0].(map[string]interface{})["message"].(map[string]interface{}); ok {
                content, _ = msg["content"].(string)
            }
        }
    case Anthropic:
        if contentArray, ok := response["content"].([]interface{}); ok && len(contentArray) > 0 {
            if textContent, ok := contentArray[0].(map[string]interface{}); ok {
                content, _ = textContent["text"].(string)
            }
        }
    default:
        // Try common response formats
        if c, ok := response["response"].(string); ok {
            content = c
        } else if c, ok := response["content"].(string); ok {
            content = c
        }
    }
    
    code, explanation := extractCodeFromContent(content)
    
    return &GenerateResult{
        Code:        code,
        Language:    language,
        Explanation: explanation,
    }, nil
}