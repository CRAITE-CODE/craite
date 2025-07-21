#!/usr/bin/env python3
"""
CRAITE CLI - Command-line interface for CRAITE Python SDK
"""
import click
import os
import sys
import json
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.syntax import Syntax
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
import asyncio

from . import create_client, create_async_client
from .utils import save_code_to_file, format_solidity_code, format_python_code
from .mcp_tools import MCPToolRegistry

console = Console()


@click.group()
@click.version_option(version="1.0.0", prog_name="CRAITE")
def cli():
    """CRAITE - Elite Web3 Code Generator & AI Development Platform"""
    pass


@cli.command()
@click.argument("prompt")
@click.option("-l", "--language", default="solidity", help="Output language")
@click.option("-m", "--mode", default="production", type=click.Choice(["production", "educational"]))
@click.option("-o", "--output", help="Output file path")
@click.option("-t", "--tools", multiple=True, help="MCP tools to use")
@click.option("--api-key", envvar="OPENAI_API_KEY", help="API key for LLM provider")
@click.option("--provider", default="openai", help="LLM provider")
def generate(prompt: str, language: str, mode: str, output: Optional[str], tools: tuple, api_key: str, provider: str):
    """Generate code from a prompt"""
    
    if not api_key:
        console.print("[red]Error: API key is required. Set OPENAI_API_KEY or use --api-key[/red]")
        sys.exit(1)
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Generating code...", total=None)
        
        try:
            client = create_client(api_key, provider=provider)
            
            if tools:
                result = client.generate_with_tools(
                    prompt=prompt,
                    tools=list(tools),
                    language=language,
                    mode=mode
                )
                progress.update(task, description="Code generated with MCP tools!")
            else:
                result = client.generate(
                    prompt=prompt,
                    language=language,
                    mode=mode
                )
                progress.update(task, description="Code generated!")
        
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]")
            sys.exit(1)
    
    # Display result
    console.print("\n[bold green]Generated Code:[/bold green]")
    
    # Format code based on language
    code = result["code"]
    if language == "solidity":
        code = format_solidity_code(code)
    elif language == "python":
        code = format_python_code(code)
    
    syntax = Syntax(code, language, theme="monokai", line_numbers=True)
    console.print(syntax)
    
    # Show explanation if in educational mode
    if mode == "educational" and result.get("explanation"):
        console.print("\n[bold blue]Explanation:[/bold blue]")
        console.print(result["explanation"])
    
    # Show tools used
    if result.get("tools_used"):
        console.print(f"\n[bold yellow]MCP Tools Used:[/bold yellow] {', '.join(result['tools_used'])}")
    
    # Save to file if requested
    if output:
        filepath = save_code_to_file(code, output)
        console.print(f"\n[green]✓ Code saved to: {filepath}[/green]")


@cli.command()
@click.argument("contract-type", type=click.Choice(["ERC20", "ERC721", "ERC1155", "Governance"]))
@click.option("-n", "--name", default="MyContract", help="Contract name")
@click.option("-f", "--features", multiple=True, help="Contract features")
@click.option("-o", "--output", help="Output file path")
def scaffold(contract_type: str, name: str, features: tuple, output: Optional[str]):
    """Generate a smart contract scaffold using OpenZeppelin"""
    
    prompt = f"Create a {contract_type} contract named {name}"
    if features:
        prompt += f" with features: {', '.join(features)}"
    
    # Use the generate command with OpenZeppelin tool
    ctx = click.get_current_context()
    ctx.invoke(
        generate,
        prompt=prompt,
        language="solidity",
        mode="production",
        output=output,
        tools=("openzeppelin_contracts",)
    )


@cli.command()
@click.argument("file", type=click.Path(exists=True))
@click.option("--security/--no-security", default=True, help="Run security audit")
@click.option("--gas/--no-gas", default=True, help="Run gas optimization")
def analyze(file: str, security: bool, gas: bool):
    """Analyze a smart contract for security and gas optimization"""
    
    with open(file, "r") as f:
        code = f.read()
    
    registry = MCPToolRegistry()
    results = {}
    
    console.print(f"\n[bold]Analyzing: {file}[/bold]\n")
    
    if security:
        with console.status("Running security audit..."):
            security_tool = registry.get_tool("security_audit")
            if security_tool:
                result = security_tool.execute({"code": code, "language": "solidity"})
                results["security"] = result
    
    if gas:
        with console.status("Running gas optimization analysis..."):
            gas_tool = registry.get_tool("gas_optimization")
            if gas_tool:
                result = gas_tool.execute({"code": code})
                results["gas"] = result
    
    # Display results
    if "security" in results and results["security"].success:
        data = results["security"].data
        console.print("[bold red]Security Analysis:[/bold red]")
        console.print(f"Score: {data['score']}/100")
        
        if data["issues"]:
            table = Table(title="Security Issues")
            table.add_column("Type", style="cyan")
            table.add_column("Severity", style="magenta")
            table.add_column("Message", style="yellow")
            
            for issue in data["issues"]:
                table.add_row(issue["type"], issue["severity"], issue["message"])
            
            console.print(table)
            
            console.print("\n[bold]Recommendations:[/bold]")
            for rec in data["recommendations"]:
                console.print(f"• {rec}")
        else:
            console.print("[green]✓ No security issues found![/green]")
    
    if "gas" in results and results["gas"].success:
        data = results["gas"].data
        console.print("\n[bold yellow]Gas Optimization:[/bold yellow]")
        console.print(f"Optimization Score: {data['optimization_score']}/100")
        console.print(f"Estimated Savings: {data['estimated_total_savings']}")
        
        if data["suggestions"]:
            table = Table(title="Optimization Suggestions")
            table.add_column("Type", style="cyan")
            table.add_column("Suggestion", style="yellow")
            table.add_column("Impact", style="magenta")
            table.add_column("Gas Saved", style="green")
            
            for suggestion in data["suggestions"]:
                table.add_row(
                    suggestion["type"],
                    suggestion["suggestion"],
                    suggestion["impact"],
                    suggestion.get("gas_saved", "N/A")
                )
            
            console.print(table)
        else:
            console.print("[green]✓ Code is well optimized![/green]")


@cli.command()
def tools():
    """List available MCP tools"""
    registry = MCPToolRegistry()
    tools_list = registry.list_tools()
    
    table = Table(title="Available MCP Tools")
    table.add_column("Tool Name", style="cyan", no_wrap=True)
    table.add_column("Description", style="yellow")
    
    for tool_name in tools_list:
        tool = registry.get_tool(tool_name)
        if tool:
            table.add_row(tool.name, tool.description)
    
    console.print(table)


@cli.command()
@click.argument("prompts-file", type=click.Path(exists=True))
@click.option("-o", "--output-dir", default="generated", help="Output directory")
@click.option("--api-key", envvar="OPENAI_API_KEY", help="API key for LLM provider")
def batch(prompts_file: str, output_dir: str, api_key: str):
    """Generate multiple code files from a JSON file of prompts"""
    
    if not api_key:
        console.print("[red]Error: API key is required. Set OPENAI_API_KEY or use --api-key[/red]")
        sys.exit(1)
    
    with open(prompts_file, "r") as f:
        prompts = json.load(f)
    
    if not isinstance(prompts, list):
        console.print("[red]Error: Prompts file must contain a JSON array[/red]")
        sys.exit(1)
    
    async def process_batch():
        client = create_async_client(api_key)
        results = await client.generate_batch_async(prompts)
        
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        for i, (prompt_data, result) in enumerate(zip(prompts, results)):
            filename = prompt_data.get("filename", f"generated_{i}.{result['language']}")
            filepath = Path(output_dir) / filename
            
            with open(filepath, "w") as f:
                f.write(result["code"])
            
            console.print(f"[green]✓ Generated: {filepath}[/green]")
    
    with console.status(f"Processing {len(prompts)} prompts..."):
        asyncio.run(process_batch())
    
    console.print(f"\n[bold green]✓ Batch generation complete! Files saved to: {output_dir}[/bold green]")


def main():
    """Main entry point"""
    cli()


if __name__ == "__main__":
    main()