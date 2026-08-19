import os
import urllib.request
import subprocess

# Folder termux
TERMUX_DIR = os.path.expanduser("~/.termux")
FONT_DIR = TERMUX_DIR
FONT_TTF = os.path.join(TERMUX_DIR, "font.ttf")

# List Tema - Dracula Pink udah dihapus
THEMES = {
    1: {
        "name": "Monokai Pro",
        "colors": {
            "background": "#2d2a2e", "foreground": "#fcfcfa",
            "color0": "#2d2a2e", "color1": "#ff6188", "color2": "#a9dc76", "color3": "#ffd866",
            "color4": "#78dce8", "color5": "#ab9df2", "color6": "#73d0ff", "color7": "#fcfcfa",
            "color8": "#727072", "color9": "#ff6188", "color10": "#a9dc76", "color11": "#ffd866",
            "color12": "#78dce8", "color13": "#ab9df2", "color14": "#73d0ff", "color15": "#ffffff"
        },
        "font": "FiraCode"
    },
    2: {
        "name": "Gruvbox Dark",
        "colors": {
            "background": "#282828", "foreground": "#ebdbb2",
            "color0": "#282828", "color1": "#cc241d", "color2": "#98971a", "color3": "#d79921",
            "color4": "#458588", "color5": "#b16286", "color6": "#689d6a", "color7": "#ebdbb2",
            "color8": "#928374", "color9": "#fb4934", "color10": "#b8bb26", "color11": "#fabd2f",
            "color12": "#83a598", "color13": "#d3869b", "color14": "#8ec07c", "color15": "#fbf1c7"
        },
        "font": "JetBrainsMono"
    },
    3: { 
        "name": "Cyberpunk Neon",
        "colors": {
            "background": "#0a0a0f", "foreground": "#e0e0ff",
            "color0": "#1a1a2e", "color1": "#ff2d92", "color2": "#00ff88", "color3": "#ffdd00",
            "color4": "#00d4ff", "color5": "#bd00ff", "color6": "#00ffff", "color7": "#e0e0ff",
            "color8": "#3a3a5e", "color9": "#ff4da6", "color10": "#33ffaa", "color11": "#ffee33",
            "color12": "#33ddff", "color13": "#dd00ff", "color14": "#33ffff", "color15": "#ffffff"
        },
        "font": "CascadiaCode"
    },
    4: {
        "name": "Nord",
        "colors": {
            "background": "#2e3447", "foreground": "#eceff4",
            "color0": "#3b4252", "color1": "#bf616a", "color2": "#a3be8c", "color3": "#ebcb8b",
            "color4": "#81a1c1", "color5": "#b48ead", "color6": "#88c0d0", "color7": "#e5e9f0",
            "color8": "#4c566a", "color9": "#bf616a", "color10": "#a3be8c", "color11": "#ebcb8b",
            "color12": "#81a1c1", "color13": "#b48ead", "color14": "#8fbcbb", "color15": "#eceff4"
        },
        "font": "Hack"
    },
    5: {
        "name": "Catppuccin Mocha",
        "colors": {
            "background": "#1e1e2e", "foreground": "#cdd6f4",
            "color0": "#45475a", "color1": "#f38ba8", "color2": "#a6e3a1", "color3": "#f9e2af",
            "color4": "#89b4fa", "color5": "#f5c2e7", "color6": "#94e2d5", "color7": "#bac2de",
            "color8": "#585b70", "color9": "#f38ba8", "color10": "#a6e3a1", "color11": "#f9e2af",
            "color12": "#89b4fa", "color13": "#f5c2e7", "color14": "#94e2d5", "color15": "#a6adc8"
        },
        "font": "VictorMono"
    }
}

FONT_URLS = {
    "FiraCode": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/FiraCode.tar.xz",
    "JetBrainsMono": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.tar.xz",
    "CascadiaCode": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/CascadiaCode.tar.xz",
    "Hack": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.tar.xz",
    "VictorMono": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/VictorMono.tar.xz"
}

def download_font(font_name):
    print(f"[+] Download {font_name} Nerd Font...")
    url = FONT_URLS[font_name]
    font_file = os.path.join(FONT_DIR, f"{font_name}.tar.xz")
    urllib.request.urlretrieve(url, font_file)
    
    print("[+] Extract font...")
    subprocess.run(["tar", "-xf", font_file, "-C", FONT_DIR])
    subprocess.run(["mv", f"{FONT_DIR}/{font_name}NerdFont-Regular.ttf", FONT_TTF])
    subprocess.run(["rm", font_file])
    print("[+] Font berhasil diinstall")

def apply_theme(theme_id):
    theme = THEMES[theme_id]
    colors_path = os.path.join(TERMUX_DIR, "colors.properties")
    
    print(f"[+] Menerapkan tema: {theme['name']}")
    with open(colors_path, "w") as f:
        for key, value in theme["colors"].items():
            f.write(f"{key} = {value}\n")
    
    if os.path.exists(FONT_TTF):
        os.remove(FONT_TTF)
    download_font(theme["font"])
    subprocess.run(["termux-reload-settings"])
    print("\n[SUKSES] Tema diterapkan!")
    print("Force close Termux dari recent apps lalu buka lagi")

def main():
    print("="*35)
    print("     TEMA TERMUX V2 - PRO       ")
    print("="*35)
    for k, v in THEMES.items():
        print(f"{k}. {v['name']} + {v['font']}")
    print("")
    
    try:
        pilih = int(input("Pilih tema [1-5]: "))
        if pilih in THEMES:
            apply_theme(pilih)
        else:
            print("Pilihan tidak ada")
    except:
        print("Input salah")

if __name__ == "__main__":
    main()
