"""
CRAITE Python Client - Core implementation
"""
import os
import json
import asyncio
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
import aiohttp
import requests
from .mcp_tools import MCPToolRegistry
from .utils import extract_code_blocks, validate_api_key


@dataclass
class ClientConfig:
    """Configuration for CRAITE client"""
    api_key: str
    provider: str = "openai"
    model: str = "gpt-4"
    endpoint: Optional[str] = None
    timeout: int = 30
    max_retries: int = 3
    mcp_tools: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        validate_api_key(self.api_key)


class CraiteClient:
    """Main CRAITE client for synchronous operations"""
    
    def __init__(self, config: Union[ClientConfig, Dict[str, Any]]):
        if isinstance(config, dict):
            config = ClientConfig(**config)
        self.config = config
        self.mcp_registry = MCPToolRegistry()
        self._setup_mcp_tools()
        
    def _setup_mcp_tools(self):
        """Initialize MCP tools"""
        for tool_name in self.config.mcp_tools:
            self.mcp_registry.enable_tool(tool_name)
    
    def generate(
        self,
        prompt: str,
        language: str = "python",
        mode: str = "production",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate code synchronously"""
        
        # Build request
        system_prompt = self._build_system_prompt(mode)
        payload = self._build_payload(
            prompt, system_prompt, temperature, max_tokens, **kwargs
        )
        
        # Make request
        headers = self._get_headers()
        endpoint = self._get_endpoint()
        
        response = requests.post(
            endpoint,
            headers=headers,
            json=payload,
            timeout=self.config.timeout
        )
        response.raise_for_status()
        
        # Parse response
        result = self._parse_response(response.json(), language)
        
        # Add mode-specific processing
        if mode == "educational":
            result["explanation"] = self._enhance_explanation(result.get("explanation", ""))
        
        return result
    
    def generate_with_tools(
        self,
        prompt: str,
        tools: List[str],
        language: str = "python",
        mode: str = "production",
        **kwargs
    ) -> Dict[str, Any]:
        """Generate code using specific MCP tools"""
        
        # Execute MCP tools
        tool_results = []
        for tool_name in tools:
            if tool_name in self.config.mcp_tools:
                tool = self.mcp_registry.get_tool(tool_name)
                if tool:
                    result = tool.execute({"prompt": prompt, "language": language})
                    tool_results.append({
                        "tool": tool_name,
                        "result": result
                    })
        
        # Enhance prompt with tool results
        enhanced_prompt = self._enhance_prompt_with_tools(prompt, tool_results)
        
        # Generate with enhanced context
        result = self.generate(
            enhanced_prompt,
            language=language,
            mode=mode,
            **kwargs
        )
        
        result["tools_used"] = tools
        result["tool_results"] = tool_results
        
        return result
    
    def _build_system_prompt(self, mode: str) -> str:
        """Build system prompt based on mode"""
        base = """You are CRAITE, an elite Web3 code generator and AI development assistant.
You specialize in blockchain development, smart contracts, dApps, DeFi protocols, and NFTs.
Generate production-ready, secure, and optimized code following best practices."""
        
        mode_instructions = {
            "production": "Generate clean, production-ready code with minimal but essential comments.",
            "educational": "Provide detailed explanations, comments, and learning resources to help the user understand the code.",
            "debug": "Generate code with extensive debugging output and error handling.",
            "optimize": "Focus on gas optimization, performance, and efficiency."
        }
        
        return f"{base}\n\n{mode_instructions.get(mode, mode_instructions['production'])}"
    
    def _build_payload(
        self,
        prompt: str,
        system_prompt: str,
        temperature: float,
        max_tokens: int,
        **kwargs
    ) -> Dict[str, Any]:
        """Build request payload based on provider"""
        
        if self.config.provider == "openai":
            return {
                "model": self.config.model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
        elif self.config.provider == "anthropic":
            return {
                "model": self.config.model,
                "system": system_prompt,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
                **kwargs
            }
        elif self.config.provider == "local":
            return {
                "model": self.config.model,
                "prompt": f"{system_prompt}\n\n{prompt}",
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": False,
                **kwargs
            }
        else:
            # Custom provider
            return {
                "prompt": prompt,
                "system": system_prompt,
                "temperature": temperature,
                "max_tokens": max_tokens,
                **kwargs
            }
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        headers = {
            "Content-Type": "application/json"
        }
        
        if self.config.provider in ["openai", "anthropic"]:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        elif self.config.provider == "anthropic":
            headers["x-api-key"] = self.config.api_key
            headers["anthropic-version"] = "2023-06-01"
        
        return headers
    
    def _get_endpoint(self) -> str:
        """Get API endpoint"""
        if self.config.endpoint:
            return self.config.endpoint
        
        endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "anthropic": "https://api.anthropic.com/v1/messages",
            "local": "http://localhost:11434/api/generate",
            "ollama": "http://localhost:11434/api/generate",
            "llamacpp": "http://localhost:8080/completion"
        }
        
        return endpoints.get(self.config.provider, "http://localhost:8080/generate")
    
    def _parse_response(self, response_data: Dict[str, Any], language: str) -> Dict[str, Any]:
        """Parse API response"""
        content = ""
        
        if self.config.provider == "openai":
            content = response_data["choices"][0]["message"]["content"]
        elif self.config.provider == "anthropic":
            content = response_data["content"][0]["text"]
        elif self.config.provider in ["local", "ollama"]:
            content = response_data.get("response", response_data.get("content", ""))
        else:
            # Try common response formats
            content = (
                response_data.get("content") or
                response_data.get("response") or
                response_data.get("text") or
                response_data.get("output", "")
            )
        
        # Extract code blocks and explanation
        code_blocks = extract_code_blocks(content)
        
        if code_blocks:
            code = code_blocks[0]["code"]
            explanation = content
            for block in code_blocks:
                explanation = explanation.replace(block["full_match"], "")
            explanation = explanation.strip()
        else:
            code = content
            explanation = None
        
        return {
            "code": code,
            "language": language,
            "explanation": explanation,
            "raw_response": content
        }
    
    def _enhance_prompt_with_tools(
        self,
        prompt: str,
        tool_results: List[Dict[str, Any]]
    ) -> str:
        """Enhance prompt with MCP tool results"""
        if not tool_results:
            return prompt
        
        enhanced = f"{prompt}\n\n### Additional Context from MCP Tools:\n\n"
        
        for result in tool_results:
            tool_name = result["tool"]
            tool_data = result["result"]
            enhanced += f"**{tool_name}**:\n"
            
            if isinstance(tool_data, dict):
                for key, value in tool_data.items():
                    enhanced += f"- {key}: {value}\n"
            else:
                enhanced += f"{tool_data}\n"
            
            enhanced += "\n"
        
        return enhanced
    
    def _enhance_explanation(self, explanation: str) -> str:
        """Enhance explanation for educational mode"""
        if not explanation:
            return ""
        
        enhancements = [
            "\n\n### Key Concepts:",
            "- Always validate inputs in smart contracts",
            "- Use established patterns and standards (ERC-20, ERC-721, etc.)",
            "- Consider gas optimization in your implementation",
            "- Test thoroughly on testnets before mainnet deployment",
            "\n### Additional Resources:",
            "- OpenZeppelin Documentation: https://docs.openzeppelin.com/",
            "- Ethereum Developer Resources: https://ethereum.org/developers/",
            "- Security Best Practices: https://consensys.github.io/smart-contract-best-practices/"
        ]
        
        return explanation + "\n".join(enhancements)


class AsyncCraiteClient(CraiteClient):
    """Asynchronous CRAITE client"""
    
    async def generate_async(
        self,
        prompt: str,
        language: str = "python",
        mode: str = "production",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        **kwargs
    ) -> Dict[str, Any]:
        """Generate code asynchronously"""
        
        system_prompt = self._build_system_prompt(mode)
        payload = self._build_payload(
            prompt, system_prompt, temperature, max_tokens, **kwargs
        )
        
        headers = self._get_headers()
        endpoint = self._get_endpoint()
        
        async with aiohttp.ClientSession() as session:
            async with session.post(
                endpoint,
                headers=headers,
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            ) as response:
                response.raise_for_status()
                data = await response.json()
                
        result = self._parse_response(data, language)
        
        if mode == "educational":
            result["explanation"] = self._enhance_explanation(result.get("explanation", ""))
        
        return result
    
    async def generate_batch_async(
        self,
        prompts: List[Dict[str, Any]],
        max_concurrent: int = 5
    ) -> List[Dict[str, Any]]:
        """Generate multiple code snippets concurrently"""
        
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def generate_with_semaphore(prompt_data):
            async with semaphore:
                return await self.generate_async(**prompt_data)
        
        tasks = [generate_with_semaphore(p) for p in prompts]
        return await asyncio.gather(*tasks)


# Factory functions
def create_client(api_key: str, **kwargs) -> CraiteClient:
    """Create a synchronous CRAITE client"""
    config = ClientConfig(api_key=api_key, **kwargs)
    return CraiteClient(config)


def create_async_client(api_key: str, **kwargs) -> AsyncCraiteClient:
    """Create an asynchronous CRAITE client"""
    config = ClientConfig(api_key=api_key, **kwargs)
    return AsyncCraiteClient(config)