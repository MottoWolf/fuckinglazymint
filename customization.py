import subprocess
import os
import shutil

PROFILE_SLUG = "ae050752-2571-438b-89db-827532378b8e"
PROFILE_PATH = f"/org/gnome/terminal/legacy/profiles:/:{PROFILE_SLUG}"
ZSH_CUSTOM = os.path.expanduser("~/.oh-my-zsh/custom")

def run(cmd, check=True):
    print(f"→ Running: {cmd}")
    subprocess.run(cmd, shell=True, check=check)

def write_dconf(path, value):
    run(f'dconf write "{PROFILE_PATH}/{path}" "{value}"')

def install_oh_my_zsh():
    if not os.path.isdir(os.path.expanduser("~/.oh-my-zsh")):
        run('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    else:
        print("✔ Oh My Zsh already installed")

def install_plugin(name, repo):
    dest = os.path.join(ZSH_CUSTOM, "plugins", name)
    if not os.path.isdir(dest):
        run(f"git clone {repo} {dest}")
    else:
        print(f"✔ {name} already installed")

def install_starship():
    if shutil.which("starship") is None:
        run("curl -sS https://starship.rs/install.sh | sh -s -- -y")
    else:
        print("✔ Starship already installed")

def install_btop():
    if shutil.which("btop") is None:
        run("sudo apt update && sudo apt install -y btop")
    else:
        print("✔ btop already installed")

def update_zshrc():
    zshrc = os.path.expanduser("~/.zshrc")
    with open(zshrc, "r") as f:
        lines = f.readlines()

    updated = []
    found_plugins = False
    found_theme = False
    starship_added = False

    for line in lines:
        if line.startswith("plugins="):
            updated.append("plugins=(git z sudo history zsh-autosuggestions zsh-syntax-highlighting)\n")
            found_plugins = True
        elif line.startswith("ZSH_THEME="):
            updated.append('ZSH_THEME=""\n')
            found_theme = True
        elif 'eval "$(starship init zsh)"' in line:
            updated.append(line)
            starship_added = True
        else:
            updated.append(line)

    if not found_plugins:
        updated.append("plugins=(git z sudo history zsh-autosuggestions zsh-syntax-highlighting)\n")
    if not found_theme:
        updated.append('ZSH_THEME=""\n')
    if not starship_added:
        updated.append('eval "$(starship init zsh)"\n')

    with open(zshrc, "w") as f:
        f.writelines(updated)
    print("✔ .zshrc updated")

def apply_tokyo_night_theme():
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

def main():
    apply_tokyo_night_theme()
    install_oh_my_zsh()
    install_plugin("zsh-autosuggestions", "https://github.com/zsh-users/zsh-autosuggestions")
    install_plugin("zsh-syntax-highlighting", "https://github.com/zsh-users/zsh-syntax-highlighting")
    install_starship()
    install_btop()
    update_zshrc()
    print("\n✅ All done! Open a new terminal or run: source ~/.zshrc")

if __name__ == "__main__":
    main()
    
