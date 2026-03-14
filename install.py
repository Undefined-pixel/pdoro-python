#!/usr/bin/env python3
"""
Installation script for pdoro - Pomodoro Timer
Installs pdoro as a global command-line tool
"""

import os
import sys
import shutil
import stat
import subprocess
from pathlib import Path

class PodoroInstaller:
    """Install pdoro as a global command."""
    
    def __init__(self):
        self.script_dir = Path(__file__).parent
        self.pdoro_py = self.script_dir / "pdoro.py"
        self.home = Path.home()
        self.local_bin = self.home / ".local" / "bin"
        self.pdoro_link = self.local_bin / "pdoro"
        
        # Farben
        self.GREEN = "\033[92m"
        self.RED = "\033[91m"
        self.BLUE = "\033[94m"
        self.YELLOW = "\033[93m"
        self.RESET = "\033[0m"
        self.BOLD = "\033[1m"
    
    def print_header(self, text: str):
        """Print colored header."""
        print(f"\n{self.BOLD}{self.BLUE}{'='*50}{self.RESET}")
        print(f"{text}")
        print(f"{self.BOLD}{self.BLUE}{'='*50}{self.RESET}\n")
    
    def print_success(self, text: str):
        """Print success message."""
        print(f"{self.GREEN}✅ {text}{self.RESET}")
    
    def print_error(self, text: str):
        """Print error message."""
        print(f"{self.RED}❌ {text}{self.RESET}")
    
    def print_info(self, text: str):
        """Print info message."""
        print(f"{self.BLUE}ℹ️  {text}{self.RESET}")
    
    def print_warning(self, text: str):
        """Print warning message."""
        print(f"{self.YELLOW}⚠️  {text}{self.RESET}")
    
    def check_pdoro_file(self) -> bool:
        """Check if pdoro.py exists."""
        self.print_info(f"Checking pdoro.py at {self.pdoro_py}")
        if not self.pdoro_py.exists():
            self.print_error(f"pdoro.py not found at {self.pdoro_py}")
            return False
        self.print_success("pdoro.py found")
        return True
    
    def create_local_bin(self) -> bool:
        """Create ~/.local/bin if it doesn't exist."""
        self.print_info(f"Checking ~/.local/bin directory...")
        try:
            self.local_bin.mkdir(parents=True, exist_ok=True)
            self.print_success(f"~/.local/bin ready")
            return True
        except Exception as e:
            self.print_error(f"Failed to create ~/.local/bin: {e}")
            return False
    
    def check_path_env(self) -> bool:
        """Check if ~/.local/bin is in PATH."""
        path_dirs = os.environ.get("PATH", "").split(":")
        if str(self.local_bin) in path_dirs:
            self.print_success("~/.local/bin is in PATH")
            return True
        else:
            self.print_warning(f"~/.local/bin is NOT in PATH")
            self.print_info("You may need to add this to your shell config:")
            print(f"{self.YELLOW}  export PATH=\"$HOME/.local/bin:$PATH\"{self.RESET}")
            return False
    
    def create_pdoro_executable(self) -> bool:
        """Create pdoro executable wrapper."""
        self.print_info(f"Creating pdoro executable...")
        
        # Create wrapper script
        wrapper_content = f"""#!/usr/bin/env python3
import sys
import os
os.chdir("{self.script_dir}")
sys.path.insert(0, "{self.script_dir}")
from pdoro import main
if __name__ == "__main__":
    main()
"""
        
        try:
            with open(self.pdoro_link, 'w') as f:
                f.write(wrapper_content)
            
            # Make it executable
            st = os.stat(self.pdoro_link)
            os.chmod(self.pdoro_link, st.st_mode | stat.S_IEXEC | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            
            self.print_success(f"pdoro executable created at {self.pdoro_link}")
            return True
        except Exception as e:
            self.print_error(f"Failed to create executable: {e}")
            return False
    
    def install_dependencies(self) -> bool:
        """Install required Python packages."""
        self.print_info("Installing required packages...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "rich", "-q"])
            self.print_success("Required packages installed")
            return True
        except Exception as e:
            self.print_warning(f"Failed to install packages: {e}")
            self.print_info("You may need to install 'rich' manually:")
            print(f"  {self.YELLOW}pip install rich{self.RESET}")
            return False
    
    def install(self):
        """Run the installation process."""
        self.print_header("🍅 Pomodoro Timer Installation")
        
        # Step 0: Install dependencies
        if not self.install_dependencies():
            return False
        
        # Step 1: Check pdoro.py
        if not self.check_pdoro_file():
            return False
        
        # Step 2: Create ~/.local/bin
        if not self.create_local_bin():
            return False
        
        # Step 3: Create executable
        if not self.create_pdoro_executable():
            return False
        
        # Step 4: Check PATH
        path_ok = self.check_path_env()
        
        # Summary
        self.print_header("Installation Summary")
        print(f"{self.GREEN}✅ pdoro has been installed!{self.RESET}\n")
        print(f"Location: {self.pdoro_link}")
        print(f"Source: {self.pdoro_py}\n")
        
        if path_ok:
            print(f"{self.GREEN}You can now run:{self.RESET}")
            print(f"  {self.BOLD}pdoro work{self.RESET}")
            print(f"  {self.BOLD}pdoro break{self.RESET}")
            print(f"  {self.BOLD}pdoro -h{self.RESET}\n")
        else:
            print(f"{self.YELLOW}To use pdoro from anywhere, add to your shell config:{self.RESET}")
            print(f"  {self.BOLD}export PATH=\"$HOME/.local/bin:$PATH\"{self.RESET}\n")
            print(f"Then restart your terminal or run:")
            print(f"  {self.BOLD}source ~/.bashrc{self.RESET}\n")
        
        return True


def main():
    """Main entry point."""
    installer = PodoroInstaller()
    success = installer.install()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
