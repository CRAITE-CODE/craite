"""CRAITE Client - AI-powered Web3 code generation"""
import os
from typing import Dict, Any, Optional

try:
    from openai import OpenAI
except ImportError:
    raise ImportError("Please install openai: pip install openai>=1.0.0")


class CRAITEClient:
    """Client for interacting with CRAITE code generation"""
    
    def __init__(self, api_key: str, provider: str = "openai", model: str = None):
        self.api_key = api_key
        self.provider = provider
        self.model = model or "gpt-4"
        
        if provider == "openai":
            self.client = OpenAI(api_key=api_key)
        else:
            raise ValueError(f"Provider {provider} not supported yet")
    
    def generate(self, prompt: str, language: str = "solidity", **options) -> Dict[str, Any]:
        """Generate Web3 code from a natural language prompt"""
        
        system_prompt = """You are CRAITE, an expert Web3 and blockchain code generator.
        Generate production-ready, secure, and optimized code.
        Include helpful comments but keep the code clean.
        For smart contracts, follow best security practices."""
        
        full_prompt = f"Generate {language} code for: {prompt}"
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": full_prompt}
                ],
                temperature=options.get("temperature", 0.7),
                max_tokens=options.get("max_tokens", 2000)
            )
            
            code = response.choices[0].message.content
            
            # Extract code from markdown if present
            if "```" in code:
                import re
                code_match = re.search(r'```[\w]*\n([\s\S]*?)\n```', code)
                if code_match:
                    code = code_match.group(1)
            
            return {
                "code": code,
                "language": language,
                "model": self.model,
                "explanation": "Generated successfully"
            }
            
        except Exception as e:
            return {
                "code": f"// Error generating code: {str(e)}",
                "language": language,
                "explanation": f"Failed to generate: {str(e)}"
            }


def create_client(api_key: str, provider: str = "openai", model: str = None) -> CRAITEClient:
    """Create a new CRAITE client instance"""
    return CRAITEClient(api_key, provider, model)


# Re-export for backward compatibility
NewClient = create_client
