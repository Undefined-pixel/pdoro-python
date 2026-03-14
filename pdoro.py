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
import json
from pathlib import Path
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TextColumn, MofNCompleteColumn
from rich.text import Text
from rich.align import Align

class StatsManager:
    """Manage usage statistics for pdoro."""
    
    def __init__(self):
        self.stats_dir = Path.home() / ".local" / "share" / "pdoro"
        self.stats_file = self.stats_dir / "stats.json"
        self._ensure_stats_dir()
    
    def _ensure_stats_dir(self):
        """Create stats directory if it doesn't exist."""
        self.stats_dir.mkdir(parents=True, exist_ok=True)
    
    def get_today(self) -> str:
        """Get today's date as string (YYYY-MM-DD)."""
        return datetime.now().strftime("%Y-%m-%d")
    
    def load_stats(self) -> Dict:
        """Load stats from file."""
        if self.stats_file.exists():
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return self._default_stats()
        return self._default_stats()
    
    def _default_stats(self) -> Dict:
        """Return default stats structure."""
        return {
            "total_sessions": 0,
            "work_sessions": 0,
            "break_sessions": 0,
            "daily": {}
        }
    
    def save_stats(self, stats: Dict):
        """Save stats to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(stats, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save stats: {e}")
    
    def get_today_stats(self) -> Dict:
        """Get stats for today."""
        stats = self.load_stats()
        today = self.get_today()
        
        if today not in stats["daily"]:
            stats["daily"][today] = {
                "total": 0,
                "work": 0,
                "break": 0
            }
        
        return stats["daily"][today]
    
    def increment_session(self, session_type: str):
        """Increment counter for a completed session."""
        stats = self.load_stats()
        today = self.get_today()
        
        # Update total stats
        stats["total_sessions"] += 1
        if session_type in ["work", "break"]:
            stats[f"{session_type}_sessions"] += 1
        
        # Update daily stats
        if today not in stats["daily"]:
            stats["daily"][today] = {
                "total": 0,
                "work": 0,
                "break": 0
            }
        
        stats["daily"][today]["total"] += 1
        if session_type in ["work", "break"]:
            stats["daily"][today][session_type] += 1
        
        self.save_stats(stats)
    
    def get_stats(self) -> Dict:
        """Get current stats."""
        return self.load_stats()

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
        self.stats_manager = StatsManager()
    
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
        
        self.session_type = session_type
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
        
        # Show today's stats
        today_stats = self.stats_manager.get_today_stats()
        self.console.print(f"[cyan]📊 Heute: {today_stats['total']} Sessions ([yellow]{today_stats['work']}[/yellow] Arbeit, [green]{today_stats['break']}[/green] Pause)[/cyan]\n")
        
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
        # Increment and display stats
        self.stats_manager.increment_session(self.session_type)
        today_stats = self.stats_manager.get_today_stats()
        self.console.print(f"[cyan]📊 Heute insgesamt: {today_stats['total']} Sessions ([yellow]{today_stats['work']}[/yellow] Arbeit, [green]{today_stats['break']}[/green] Pause)[/cyan]\n")

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
    
    parser.add_argument(
        "-s", "--stats",
        action="store_true",
        help="Show usage statistics"
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
    
    # Show statistics
    if args.stats:
        stats = timer.stats_manager.get_stats()
        today_stats = timer.stats_manager.get_today_stats()
        today = timer.stats_manager.get_today()
        
        timer.console.print("\n[bold cyan]📊 Pomodoro Statistics[/bold cyan]")
        timer.console.print(f"  [bold]{today}[/bold]")
        timer.console.print(f"    [cyan]Sessions:[/cyan] {today_stats['total']}")
        timer.console.print(f"    [yellow]Work:[/yellow] {today_stats['work']}")
        timer.console.print(f"    [green]Break:[/green] {today_stats['break']}")
        timer.console.print(f"\n  [bold]All Time[/bold]")
        timer.console.print(f"    [cyan]Total Sessions:[/cyan] {stats['total_sessions']}")
        timer.console.print(f"    [yellow]Work Sessions:[/yellow] {stats.get('work_sessions', 0)}")
        timer.console.print(f"    [green]Break Sessions:[/green] {stats.get('break_sessions', 0)}\n")
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
