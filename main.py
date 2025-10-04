#!/usr/bin/env python3
"""
Alfred - Personal AI Assistant
Entry point for running Alfred in various modes (CLI, interactive, voice)

Author: San20506
Version: 0.1.0
"""

import argparse
import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.llm_brain import LLMBrain
from core.vector_memory import VectorMemory
from core.mcp_orchestrator import MCPOrchestrator
from utils.config_loader import ConfigLoader
from rich.console import Console
from rich.panel import Panel

console = Console()


def print_banner():
    """Print Alfred startup banner"""
    banner = """
     █████╗ ██╗     ███████╗██████╗ ███████╗██████╗ 
    ██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗
    ███████║██║     █████╗  ██████╔╝█████╗  ██║  ██║
    ██╔══██║██║     ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║
    ██║  ██║███████╗██║     ██║  ██║███████╗██████╔╝
    ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ 
    
    Your Personal AI Assistant v0.1.0
    """
    console.print(Panel(banner, style="bold cyan"))


async def run_cli_mode(config):
    """Run Alfred in CLI mode"""
    console.print("[bold green]Starting Alfred in CLI mode...[/bold green]")
    
    # Initialize components
    brain = LLMBrain(config)
    memory = VectorMemory(config)
    orchestrator = MCPOrchestrator(config, brain, memory)
    
    await orchestrator.start()
    
    console.print("[cyan]Alfred is ready! Type 'exit' to quit.[/cyan]\n")
    
    while True:
        try:
            user_input = console.input("[bold yellow]You:[/bold yellow] ")
            
            if user_input.lower() in ['exit', 'quit', 'bye']:
                console.print("[cyan]Goodbye! Alfred signing off.[/cyan]")
                break
            
            if not user_input.strip():
                continue
            
            # Process input through orchestrator
            response = await orchestrator.process(user_input)
            console.print(f"[bold green]Alfred:[/bold green] {response}\n")
            
        except KeyboardInterrupt:
            console.print("\n[cyan]Alfred interrupted. Goodbye![/cyan]")
            break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {e}")
    
    await orchestrator.stop()


async def run_interactive_mode(config):
    """Run Alfred in interactive mode with enhanced UI"""
    console.print("[bold green]Starting Alfred in Interactive mode...[/bold green]")
    # TODO: Implement enhanced interactive mode
    console.print("[yellow]Interactive mode not yet implemented. Falling back to CLI mode.[/yellow]")
    await run_cli_mode(config)


async def run_voice_mode(config):
    """Run Alfred in voice mode"""
    console.print("[bold green]Starting Alfred in Voice mode...[/bold green]")
    # TODO: Implement voice mode
    console.print("[yellow]Voice mode not yet implemented. Please check back later.[/yellow]")


async def run_daemon_mode(config):
    """Run Alfred as a background daemon"""
    console.print("[bold green]Starting Alfred in Daemon mode...[/bold green]")
    # TODO: Implement daemon mode
    console.print("[yellow]Daemon mode not yet implemented. Please check back later.[/yellow]")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Alfred - Your Personal AI Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        '--mode',
        choices=['cli', 'interactive', 'voice', 'daemon'],
        default='cli',
        help='Run mode for Alfred (default: cli)'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default='config/config.yaml',
        help='Path to configuration file (default: config/config.yaml)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug mode'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Alfred v0.1.0'
    )
    
    args = parser.parse_args()
    
    # Print banner
    print_banner()
    
    try:
        # Load configuration
        console.print(f"[cyan]Loading configuration from {args.config}...[/cyan]")
        config = ConfigLoader.load(args.config)
        
        if args.debug:
            config['debug_mode'] = True
            console.print("[yellow]Debug mode enabled[/yellow]")
        
        # Run in selected mode
        if args.mode == 'cli':
            asyncio.run(run_cli_mode(config))
        elif args.mode == 'interactive':
            asyncio.run(run_interactive_mode(config))
        elif args.mode == 'voice':
            asyncio.run(run_voice_mode(config))
        elif args.mode == 'daemon':
            asyncio.run(run_daemon_mode(config))
            
    except FileNotFoundError:
        console.print(f"[bold red]Error:[/bold red] Configuration file not found: {args.config}")
        console.print("[yellow]Please create a config file or specify a valid path.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]Fatal Error:[/bold red] {e}")
        if args.debug:
            import traceback
            console.print(traceback.format_exc())
        sys.exit(1)


if __name__ == "__main__":
    main()
