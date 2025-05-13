import subprocess
import os
import shutil
from typing import List, Optional, Dict, Callable, Set
import curses
import sys

PROFILE_SLUG = "ae050752-2571-438b-89db-827532378b8e"
PROFILE_PATH = f"/org/gnome/terminal/legacy/profiles:/:{PROFILE_SLUG}"
ZSH_CUSTOM = os.path.expanduser("~/.oh-my-zsh/custom")

class InstallationStatus:
    def __init__(self):
        self.core_shell = all([
            os.path.isdir(os.path.expanduser("~/.oh-my-zsh")),
            shutil.which("starship") is not None
        ])
        self.zsh_plugins = all([
            os.path.isdir(os.path.join(ZSH_CUSTOM, "plugins", "zsh-autosuggestions")),
            os.path.isdir(os.path.join(ZSH_CUSTOM, "plugins", "zsh-syntax-highlighting"))
        ])
        self.btop = shutil.which("btop") is not None
        self.tokyo_night_theme = self._check_tokyo_night_theme()
        self.zshrc_configured = self._check_zshrc_config()

    def _check_tokyo_night_theme(self) -> bool:
        try:
            result = subprocess.run(
                ['dconf', 'read', f"{PROFILE_PATH}/background-color"],
                capture_output=True,
                text=True
            )
            return "'#1a1b26'" in result.stdout
        except:
            return False

    def _check_zshrc_config(self) -> bool:
        try:
            with open(os.path.expanduser("~/.zshrc"), "r") as f:
                content = f.read()
                return 'ZSH_THEME=""' in content and 'eval "$(starship init zsh)"' in content
        except:
            return False

def run(cmd: str, check: bool = True) -> None:
    """Execute a shell command and optionally check its return code.
    
    Args:
        cmd: The shell command to execute
        check: If True, raises CalledProcessError if command fails
    """
    print(f"→ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def write_dconf(path: str, value: str) -> None:
    """Write a value to dconf database.
    
    Args:
        path: The dconf path to write to
        value: The value to write
    """
    run(f'dconf write "{PROFILE_PATH}/{path}" "{value}"')

def install_core_shell() -> None:
    """Install core shell components (Git, Zsh, Oh My Zsh, Btop, Starship)."""
    # Install Git
    if shutil.which("git") is None:
        run("sudo apt update && sudo apt install -y git")
    else:
        print("✔ Git already installed")

    # Install Zsh
    if shutil.which("zsh") is None:
        run("sudo apt update && sudo apt install -y zsh")
    else:
        print("✔ Zsh already installed")

    # Install Oh My Zsh
    if not os.path.isdir(os.path.expanduser("~/.oh-my-zsh")):
        run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    else:
        print("✔ Oh My Zsh already installed")

    # Install btop
    if shutil.which("btop") is None:
        run("sudo apt update && sudo apt install -y btop")
    else:
        print("✔ btop already installed")

    # Install Starship
    if shutil.which("starship") is None:
        run("curl -sS https://starship.rs/install.sh | sh")
    else:
        print("✔ Starship already installed")

    # Configure Starship and theme in .zshrc
    zshrc = os.path.expanduser("~/.zshrc")
    with open(zshrc, "r") as f:
        lines = f.readlines()

    updated: List[str] = []
    starship_added = False
    theme_configured = False

    for line in lines:
        if line.startswith("ZSH_THEME="):
            updated.append('ZSH_THEME=""\n')
            theme_configured = True
        elif 'eval "$(starship init zsh)"' in line:
            updated.append(line)
            starship_added = True
        else:
            updated.append(line)

    if not theme_configured:
        updated.append('ZSH_THEME=""\n')
    if not starship_added:
        updated.append('eval "$(starship init zsh)"\n')

    with open(zshrc, "w") as f:
        f.writelines(updated)
    print("✔ Starship and theme configured in .zshrc")

def install_zsh_plugins() -> None:
    """Install Zsh plugins (autosuggestions and syntax highlighting) and configure them in .zshrc."""
    # Install plugins
    plugins = [
        ("zsh-autosuggestions", "https://github.com/zsh-users/zsh-autosuggestions"),
        ("zsh-syntax-highlighting", "https://github.com/zsh-users/zsh-syntax-highlighting")
    ]
    
    for name, repo in plugins:
        dest = os.path.join(ZSH_CUSTOM, "plugins", name)
        if not os.path.isdir(dest):
            run(f"git clone {repo} {dest}")
        else:
            print(f"✔ {name} already installed")

    # Update .zshrc with plugins
    zshrc = os.path.expanduser("~/.zshrc")
    with open(zshrc, "r") as f:
        lines = f.readlines()

    updated: List[str] = []
    found_plugins = False

    for line in lines:
        if line.startswith("plugins="):
            updated.append("plugins=(git zsh-autosuggestions zsh-syntax-highlighting)\n")
            found_plugins = True
        else:
            updated.append(line)

    if not found_plugins:
        updated.append("plugins=(git zsh-autosuggestions zsh-syntax-highlighting)\n")

    with open(zshrc, "w") as f:
        f.writelines(updated)
    print("✔ .zshrc updated with plugins")

def update_zshrc() -> None:
    """Update .zshrc with useful aliases."""
    zshrc = os.path.expanduser("~/.zshrc")
    with open(zshrc, "r") as f:
        lines = f.readlines()

    updated: List[str] = []
    aliases_added = False

    # Add aliases section
    aliases = """# Custom aliases
alias gh='history|grep'
alias top='btop'
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias .='pwd'
alias ..='cd ../'
alias ...='cd ../../'
alias ....='cd ../../../'
alias .....='cd ../../../../'
alias h='history'
alias mv='mv -i'
alias cp='cp -i'
alias ln='ln -i'
alias df='df -H'
alias du='du -ch'
alias tiempo="curl -s 'wttr.in/{Madrid}?format=3'"
alias python='python3'

"""

    for line in lines:
        if "# Custom aliases" in line:
            # Skip existing aliases section if found
            while line and not line.strip() == "":
                line = next(f, "")
            updated.append(aliases)
            aliases_added = True
        else:
            updated.append(line)

    if not aliases_added:
        updated.append(aliases)

    with open(zshrc, "w") as f:
        f.writelines(updated)
    print("✔ .zshrc updated with aliases")

def apply_tokyo_night_theme() -> None:
    """Apply Tokyo Night theme to the terminal."""
    print("🎨 Applying Tokyo Night theme...")
    write_dconf("use-theme-colors", "false")
    write_dconf("background-color", "'#1a1b26'")
    write_dconf("foreground-color", "'#c0caf5'")
    write_dconf("bold-color", "'#c0caf5'")
    write_dconf("bold-color-same-as-fg", "true")
    write_dconf("cursor-colors-set", "true")
    write_dconf("cursor-background-color", "'#c0caf5'")
    write_dconf("cursor-foreground-color", "'#1a1b26'")
    palette = """[
      '#15161E', '#f7768e', '#9ece6a', '#e0af68',
      '#7aa2f7', '#bb9af7', '#7dcfff', '#a9b1d6',
      '#414868', '#f7768e', '#9ece6a', '#e0af68',
      '#7aa2f7', '#bb9af7', '#7dcfff', '#c0caf5'
    ]"""
    write_dconf("palette", palette)
    print("✔ Tokyo Night theme applied")

def draw_menu(stdscr, selected_idx: int, status: InstallationStatus, selected_items: Set[int]) -> None:
    """Draw the installation menu with current status.
    
    Args:
        stdscr: Curses window object
        selected_idx: Currently selected menu item
        status: Current installation status
        selected_items: Set of indices of selected items
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    
    # Title
    title = "Fucking Lazy Debian - Installation Menu"
    stdscr.addstr(0, (w - len(title)) // 2, title, curses.A_BOLD)
    
    # Menu items with status
    menu_items = [
        ("Core Shell Setup (Git, Zsh, Oh My Zsh, Btop, Starship)", status.core_shell),
        ("Install Zsh Plugins (Autosuggestions, Syntax Highlighting) + Configure", status.zsh_plugins),
        ("Configure .zshrc (Theme + Aliases)", status.zshrc_configured),
        ("Tokyo Night Theme (Default Debian Terminal)", status.tokyo_night_theme)
    ]
    
    # Draw menu items
    for idx, (item, installed) in enumerate(menu_items):
        y = idx + 2
        if y < h - 4:  # Leave space for button and instructions
            # Status indicator
            if installed:
                status_text = "[INSTALLED]"
                status_attr = curses.A_BOLD | curses.color_pair(2)  # Green
            else:
                status_text = "[NOT INSTALLED]"
                status_attr = curses.color_pair(1)  # Red
            
            # Selection indicator
            if idx in selected_items:
                select_text = "●"
            else:
                select_text = "○"
            
            # Combine all parts
            item_text = f"{select_text} {item} {status_text}"
            
            # Apply appropriate attributes
            if idx == selected_idx:
                stdscr.addstr(y, 2, item_text, curses.A_REVERSE)
            else:
                stdscr.addstr(y, 2, item_text)
                # Add status text with color
                status_x = 2 + len(select_text) + len(item) + 2
                stdscr.addstr(y, status_x, status_text, status_attr)
    
    # Draw Install Selected button right after the last menu item
    button_y = len(menu_items) + 2
    button_text = "┌────────────────────┐"
    button_text2 = "│  Install Selected  │"
    button_text3 = "└────────────────────┘"
    
    if selected_idx == 4:  # Button is selected (now index 4 since we removed btop)
        stdscr.addstr(button_y, 2, button_text, curses.A_REVERSE)
        stdscr.addstr(button_y + 1, 2, button_text2, curses.A_REVERSE)
        stdscr.addstr(button_y + 2, 2, button_text3, curses.A_REVERSE)
    else:
        stdscr.addstr(button_y, 2, button_text)
        stdscr.addstr(button_y + 1, 2, button_text2)
        stdscr.addstr(button_y + 2, 2, button_text3)
    
    # Instructions
    instructions = "Use ↑↓ to move, SPACE to select, ENTER to install selected, q to quit"
    stdscr.addstr(h - 1, (w - len(instructions)) // 2, instructions)
    stdscr.refresh()

def main_menu() -> None:
    """Display and handle the main installation menu."""
    status = InstallationStatus()
    selected_items: Set[int] = set()
    
    def curses_main(stdscr):
        # Initialize colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
        
        curses.curs_set(0)  # Hide cursor
        selected_idx = 0
        while True:
            draw_menu(stdscr, selected_idx, status, selected_items)
            key = stdscr.getch()
            
            if key == curses.KEY_UP and selected_idx > 0:
                selected_idx -= 1
            elif key == curses.KEY_DOWN and selected_idx < 4:  # 4 menu items + button
                selected_idx += 1
            elif key == ord(' '):  # Spacebar
                if selected_idx < 4:  # Don't allow selecting the button
                    if selected_idx in selected_items:
                        selected_items.remove(selected_idx)
                    else:
                        selected_items.add(selected_idx)
            elif key == ord('\n'):  # Enter key
                if selected_idx == 4:  # Install Selected button
                    if selected_items:  # Only proceed if there are selected items
                        for idx in sorted(selected_items):
                            if idx == 0:  # Core Shell Setup
                                install_core_shell()
                                status.core_shell = True
                            elif idx == 1:  # Zsh Plugins
                                install_zsh_plugins()
                                status.zsh_plugins = True
                            elif idx == 2:  # Configure .zshrc
                                update_zshrc()
                                status.zshrc_configured = True
                            elif idx == 3:  # Tokyo Night Theme
                                apply_tokyo_night_theme()
                                status.tokyo_night_theme = True
                        selected_items.clear()
                else:
                    # Single item installation
                    if selected_idx == 0:  # Core Shell Setup
                        install_core_shell()
                        status.core_shell = True
                    elif selected_idx == 1:  # Zsh Plugins
                        install_zsh_plugins()
                        status.zsh_plugins = True
                    elif selected_idx == 2:  # Configure .zshrc
                        update_zshrc()
                        status.zshrc_configured = True
                    elif selected_idx == 3:  # Tokyo Night Theme
                        apply_tokyo_night_theme()
                        status.tokyo_night_theme = True
            elif key == ord('q'):
                break
    
    try:
        curses.wrapper(curses_main)
    except KeyboardInterrupt:
        pass
    finally:
        print("\n✅ Done! Open a new terminal or run: source ~/.zshrc")

if __name__ == "__main__":
    main_menu()
    
