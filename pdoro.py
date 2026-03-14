#!/usr/bin/env python3
"""
🍅 Pomodoro Timer - Cool Edition
A stylish terminal-based Pomodoro timer with progress bar and notifications.
"""

import time
import sys
import signal
import argparse
from typing import Dict
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, MofNCompleteColumn
from rich.text import Text
from rich.align import Align

class PomodorTimer:
    """A cool Pomodoro timer with visual progress bar."""
    
    SESSIONS: Dict[str, int] = {
        "work": 45,
        "break": 10,
    }
    
    EMOJIS = {
        "work": "💼",
        "break": "☕",
        "done": "✅",
    }
    
    def __init__(self):
        self.session_type = None
        self.duration = 0
        self.console = Console()
    
    def format_time(self, seconds: int) -> str:
        """Convert seconds to MM:SS format."""
        mins, secs = divmod(seconds, 60)
        return f"{mins:02d}:{secs:02d}"
    
    def run(self, session_type: str) -> None:
        """Run the Pomodoro timer."""
        if session_type not in self.SESSIONS:
            self.console.print(f"[red]❌ Invalid session type![/red]")
            self.console.print(f"[cyan]Available: {', '.join(self.SESSIONS.keys())}[/cyan]")
            sys.exit(1)
        
        duration_minutes = self.SESSIONS[session_type]
        duration_seconds = duration_minutes * 60
        
        # Show header
        emoji = self.EMOJIS.get(session_type, "⏱️")
        title_text = f"{emoji}  {session_type.upper()} SESSION"
        panel = Panel(
            Align.center(f"[bold cyan]{title_text}[/bold cyan]"),
            border_style="bold cyan",
            padding=(1, 2),
        )
        self.console.print(panel)
        
        self.console.print(f"[bold]⏱️  Dauer:[/bold] {duration_minutes} Minuten")
        self.console.print(f"[yellow]⚠️  Drücke CTRL+C zum Beenden[/yellow]\n")
        
        start_time = time.time()
        
        def signal_handler(signum, frame):
            """Handle interrupt signal cleanly."""
            self.console.print("\n[yellow]⏸  Session abgebrochen![/yellow]\n")
            sys.exit(0)
        
        # Setup signal handler for CTRL+C
        signal.signal(signal.SIGINT, signal_handler)
        
        try:
            with Progress(
                TextColumn("[progress.description]{task.description}"),
                BarColumn(bar_width=40),
                TextColumn("[bold cyan]{task.fields[remaining]}[/bold cyan]"),
                console=self.console,
                transient=False,
            ) as progress:
                task = progress.add_task(
                    f"[bold cyan]🚀 Sitzung läuft[/bold cyan]",
                    total=duration_seconds,
                    remaining=self.format_time(duration_seconds)
                )
                
                while not progress.finished:
                    elapsed = int(time.time() - start_time)
                    remaining = max(0, duration_seconds - elapsed)
                    
                    if remaining <= 0:
                        progress.update(task, completed=duration_seconds, remaining=self.format_time(0))
                        break
                    
                    progress.update(task, completed=elapsed, remaining=self.format_time(remaining))
                    time.sleep(0.5)
        
        except Exception as e:
            self.console.print(f"[red]❌ Error: {e}[/red]\n")
            sys.exit(1)
        
        # Session complete
        complete_text = f"{self.EMOJIS['done']}  {session_type.upper()} SESSION ABGESCHLOSSEN!"
        complete_panel = Panel(
            Align.center(f"[bold green]{complete_text}[/bold green]"),
            border_style="bold green",
            padding=(1, 2),
        )
        self.console.print("\n")
        self.console.print(complete_panel)
        self.console.print("[bold green]🎉 Glückwunsch![/bold green]\n")


def main():
    """Main entry point with argument parser."""
    parser = argparse.ArgumentParser(
        prog="pdoro",
        description="🍅 Pomodoro Timer - A stylish terminal-based timer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  pdoro work              Start a 45-minute work session
  pdoro break             Start a 10-minute break session
  pdoro focus -d 90       Start a 90-minute custom session
  pdoro gym -d 60         Create your own custom session
        """
    )
    
    parser.add_argument(
        "session",
        metavar="SESSION",
        nargs="?",
        default=None,
        help="Session type (work, break) or custom name"
    )
    
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=None,
        metavar="MINUTES",
        help="Custom duration in minutes (overrides default)"
    )
    
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List all available sessions"
    )
    
    args = parser.parse_args()
    
    timer = PomodorTimer()
    
    # Show available sessions
    if args.list:
        timer.console.print("\n[bold]Available Sessions:[/bold]")
        for session, duration in timer.SESSIONS.items():
            emoji = timer.EMOJIS.get(session, '⏱️')
            timer.console.print(f"  [cyan]•[/cyan] [yellow]{session}[/yellow]: {duration} minutes {emoji}")
        timer.console.print()
        sys.exit(0)
    
    # Check if session is provided
    if args.session is None:
        timer.console.print("[red]❌ Please specify a session or use -l to list available sessions[/red]")
        sys.exit(1)
    
    # Run session with custom duration if provided
    if args.duration:
        timer.SESSIONS[args.session] = args.duration
    
    timer.run(args.session)


if __name__ == "__main__":
    main()
