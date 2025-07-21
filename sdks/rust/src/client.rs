use crate::{GenerateOptions, GenerateResult, GenerationMode, LLMProvider};
use anyhow::{Context, Result};
use reqwest::{Client, header};
use serde_json::{json, Value};
use std::time::Duration;

/// HTTP client wrapper for API calls
pub struct ApiClient {
    client: Client,
    api_key: String,
    provider: LLMProvider,
    endpoint: String,
    model: String,
}

impl ApiClient {
    pub fn new(
        api_key: String,
        provider: LLMProvider,
        endpoint: Option<String>,
        model: String,
    ) -> Result<Self> {
        let mut headers = header::HeaderMap::new();
        headers.insert(
            header::CONTENT_TYPE,
            header::HeaderValue::from_static("application/json"),
        );

        match &provider {
            LLMProvider::OpenAI => {
                headers.insert(
                    header::AUTHORIZATION,
                    header::HeaderValue::from_str(&format!("Bearer {}", api_key))?,
                );
            }
            LLMProvider::Anthropic => {
                headers.insert(
                    "x-api-key",
                    header::HeaderValue::from_str(&api_key)?,
                );
                headers.insert(
                    "anthropic-version",
                    header::HeaderValue::from_static("2023-06-01"),
                );
            }
            _ => {}
        }

        let client = Client::builder()
            .default_headers(headers)
            .timeout(Duration::from_secs(30))
            .build()?;

        let endpoint = endpoint.unwrap_or_else(|| Self::default_endpoint(&provider));

        Ok(Self {
            client,
            api_key,
            provider,
            endpoint,
            model,
        })
    }

    fn default_endpoint(provider: &LLMProvider) -> String {
        match provider {
            LLMProvider::OpenAI => "https://api.openai.com/v1/chat/completions".to_string(),
            LLMProvider::Anthropic => "https://api.anthropic.com/v1/messages".to_string(),
            LLMProvider::Local => "http://localhost:11434/api/generate".to_string(),
            LLMProvider::Custom(url) => url.clone(),
        }
    }

    pub async fn generate(&self, options: &GenerateOptions) -> Result<GenerateResult> {
        let system_prompt = self.build_system_prompt(&options.mode);
        let payload = self.build_payload(options, &system_prompt)?;

        let response = self
            .client
            .post(&self.endpoint)
            .json(&payload)
            .send()
            .await
            .context("Failed to send request")?;

        if !response.status().is_success() {
            let error_text = response.text().await?;
            anyhow::bail!("API error: {}", error_text);
        }

        let response_data: Value = response.json().await?;
        self.parse_response(response_data, &options.language)
    }

    fn build_system_prompt(&self, mode: &GenerationMode) -> String {
        let base = "You are CRAITE, an elite Web3 code generator and AI development assistant. \
                   You specialize in blockchain development, smart contracts, dApps, DeFi protocols, and NFTs. \
                   Generate production-ready, secure, and optimized code following best practices.";

        match mode {
            GenerationMode::Educational => {
                format!("{}\nProvide detailed explanations and comments to help the user learn.", base)
            }
            GenerationMode::Production => {
                format!("{}\nGenerate clean, production-ready code with minimal but essential comments.", base)
            }
        }
    }

    fn build_payload(&self, options: &GenerateOptions, system_prompt: &str) -> Result<Value> {
        let payload = match &self.provider {
            LLMProvider::OpenAI => json!({
                "model": self.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": options.prompt}
                ],
                "temperature": options.temperature,
                "max_tokens": options.max_tokens
            }),
            LLMProvider::Anthropic => json!({
                "model": self.model,
                "system": system_prompt,
                "messages": [{"role": "user", "content": options.prompt}],
                "max_tokens": options.max_tokens,
                "temperature": options.temperature
            }),
            LLMProvider::Local | LLMProvider::Custom(_) => json!({
                "model": self.model,
                "prompt": format!("{}\n\n{}", system_prompt, options.prompt),
                "temperature": options.temperature,
                "max_tokens": options.max_tokens,
                "stream": false
            }),
        };

        Ok(payload)
    }

    fn parse_response(&self, response: Value, language: &str) -> Result<GenerateResult> {
        let content = match &self.provider {
            LLMProvider::OpenAI => response["choices"][0]["message"]["content"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            LLMProvider::Anthropic => response["content"][0]["text"]
                .as_str()
                .unwrap_or("")
                .to_string(),
            _ => response["response"]
                .as_str()
                .or_else(|| response["content"].as_str())
                .unwrap_or("")
                .to_string(),
        };

        let (code, explanation) = self.extract_code_from_content(&content);

        Ok(GenerateResult {
            code,
            language: language.to_string(),
            explanation,
            tools_used: vec![],
        })
    }

    fn extract_code_from_content(&self, content: &str) -> (String, Option<String>) {
        let code_regex = regex::Regex::new(r"```[\w]*\n([\s\S]*?)\n```").unwrap();
        
        if let Some(captures) = code_regex.captures(content) {
            let code = captures.get(1).map_or("", |m| m.as_str()).to_string();
            let mut explanation = content.to_string();
            
            // Remove all code blocks from explanation
            for cap in code_regex.captures_iter(content) {
                explanation = explanation.replace(&cap[0], "");
            }
            
            let explanation = explanation.trim().to_string();
            
            (code, if explanation.is_empty() { None } else { Some(explanation) })
        } else {
            (content.to_string(), None)
        }
    }
}