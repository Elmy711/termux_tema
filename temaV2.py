import os, urllib.request, subprocess, glob
TERMUX_DIR = os.path.expanduser("~/.termux")
FONT_DIR = TERMUX_DIR
FONT_TTF = os.path.join(TERMUX_DIR, "font.ttf")

THEMES = {
    1: {"name": "Monokai Pro", "font": "FiraCode", "colors": {"background": "#2d2a2e", "foreground": "#fcfcfa", "color0": "#2d2a2e", "color1": "#ff6188", "color2": "#a9dc76", "color3": "#ffd866", "color4": "#78dce8", "color5": "#ab9df2", "color6": "#73d0ff", "color7": "#fcfcfa", "color8": "#727072", "color9": "#ff6188", "color10": "#a9dc76", "color11": "#ffd866", "color12": "#78dce8", "color13": "#ab9df2", "color14": "#73d0ff", "color15": "#ffffff"}},
    2: {"name": "Gruvbox Dark", "font": "JetBrainsMono", "colors": {"background": "#282828", "foreground": "#ebdbb2", "color0": "#282828", "color1": "#cc241d", "color2": "#98971a", "color3": "#d79921", "color4": "#458588", "color5": "#b16286", "color6": "#689d6a", "color7": "#ebdbb2", "color8": "#928374", "color9": "#fb4934", "color10": "#b8bb26", "color11": "#fabd2f", "color12": "#83a598", "color13": "#d3869b", "color14": "#8ec07c", "color15": "#fbf1c7"}},
    3: {"name": "Cyberpunk Neon", "font": "CascadiaCode", "colors": {"background": "#0a0a0f", "foreground": "#e0e0ff", "color0": "#1a1a2e", "color1": "#ff2d92", "color2": "#00ff88", "color3": "#ffdd00", "color4": "#00d4ff", "color5": "#bd00ff", "color6": "#00ffff", "color7": "#e0e0ff", "color8": "#3a3a5e", "color9": "#ff4da6", "color10": "#33ffaa", "color11": "#ffee33", "color12": "#33ddff", "color13": "#dd00ff", "color14": "#33ffff", "color15": "#ffffff"}},
    4: {"name": "Nord", "font": "Hack", "colors": {"background": "#2e3447", "foreground": "#eceff4", "color0": "#3b4252", "color1": "#bf616a", "color2": "#a3be8c", "color3": "#ebcb8b", "color4": "#81a1c1", "color5": "#b48ead", "color6": "#88c0d0", "color7": "#e5e9f0", "color8": "#4c566a", "color9": "#bf616a", "color10": "#a3be8c", "color11": "#ebcb8b", "color12": "#81a1c1", "color13": "#b48ead", "color14": "#8fbcbb", "color15": "#eceff4"}},
    5: {"name": "Catppuccin Mocha", "font": "VictorMono", "colors": {"background": "#1e1e2e", "foreground": "#cdd6f4", "color0": "#45475a", "color1": "#f38ba8", "color2": "#a6e3a1", "color3": "#f9e2af", "color4": "#89b4fa", "color5": "#f5c2e7", "color6": "#94e2d5", "color7": "#bac2de", "color8": "#585b70", "color9": "#f38ba8", "color10": "#a6e3a1", "color11": "#f9e2af", "color12": "#89b4fa", "color13": "#f5c2e7", "color14": "#94e2d5", "color15": "#a6adc8"}},
    6: {"name": "One Dark", "font": "FiraCode", "colors": {"background": "#282c34", "foreground": "#abb2bf", "color0": "#282c34", "color1": "#e06c75", "color2": "#98c379", "color3": "#e5c07b", "color4": "#61afef", "color5": "#c678dd", "color6": "#56b6c2", "color7": "#abb2bf", "color8": "#5c6370", "color9": "#e06c75", "color10": "#98c379", "color11": "#e5c07b", "color12": "#61afef", "color13": "#c678dd", "color14": "#56b6c2", "color15": "#ffffff"}},
    7: {"name": "Solarized Dark", "font": "JetBrainsMono", "colors": {"background": "#002b36", "foreground": "#839496", "color0": "#073642", "color1": "#dc322f", "color2": "#859900", "color3": "#b58900", "color4": "#268bd2", "color5": "#d33682", "color6": "#2aa198", "color7": "#eee8d5", "color8": "#002b36", "color9": "#cb4b16", "color10": "#586e75", "color11": "#657b83", "color12": "#839496", "color13": "#6c71c4", "color14": "#93a1a1", "color15": "#fdf6e3"}},
    8: {"name": "Tokyo Night", "font": "CascadiaCode", "colors": {"background": "#1a1b26", "foreground": "#c0caf5", "color0": "#1a1b26", "color1": "#f7768e", "color2": "#9ece6a", "color3": "#e0af68", "color4": "#7aa2f7", "color5": "#bb9af7", "color6": "#7dcfff", "color7": "#a9b1d6", "color8": "#414868", "color9": "#f7768e", "color10": "#9ece6a", "color11": "#e0af68", "color12": "#7aa2f7", "color13": "#bb9af7", "color14": "#7dcfff", "color15": "#c0caf5"}},
    9: {"name": "Palenight", "font": "Hack", "colors": {"background": "#292d3e", "foreground": "#a6accd", "color0": "#292d3e", "color1": "#f07178", "color2": "#c3e88d", "color3": "#ffcb6b", "color4": "#82aaff", "color5": "#c792ea", "color6": "#89ddff", "color7": "#a6accd", "color8": "#676e95", "color9": "#f07178", "color10": "#c3e88d", "color11": "#ffcb6b", "color12": "#82aaff", "color13": "#c792ea", "color14": "#89ddff", "color15": "#ffffff"}},
    10: {"name": "Dracula", "font": "VictorMono", "colors": {"background": "#282a36", "foreground": "#f8f8f2", "color0": "#21222c", "color1": "#ff5555", "color2": "#50fa7b", "color3": "#f1fa8c", "color4": "#bd93f9", "color5": "#ff79c6", "color6": "#8be9fd", "color7": "#f8f8f2", "color8": "#6272a4", "color9": "#ff5555", "color10": "#50fa7b", "color11": "#f1fa8c", "color12": "#bd93f9", "color13": "#ff79c6", "color14": "#8be9fd", "color15": "#ffffff"}}
}
FONT_URLS = {"FiraCode": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/FiraCode.tar.xz", "JetBrainsMono": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/JetBrainsMono.tar.xz", "CascadiaCode": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/CascadiaCode.tar.xz", "Hack": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/Hack.tar.xz", "VictorMono": "https://github.com/ryanoasis/nerd-fonts/releases/download/v3.2.1/VictorMono.tar.xz"}

def download_font(n):
    print(f"[+] Download {n}...")
    f = f"{FONT_DIR}/{n}.tar.xz"
    urllib.request.urlretrieve(FONT_URLS[n], f)
    subprocess.run(["tar","-xf",f,"-C",FONT_DIR])
    ttf = glob.glob(f"{FONT_DIR}/*.ttf")[0] # ambil file ttf pertama
    subprocess.run(["mv", ttf, FONT_TTF])
    subprocess.run(["rm", f])

def apply(t):
    with open(f"{TERMUX_DIR}/colors.properties","w") as f: [f.write(f"{k} = {v}\n") for k,v in THEMES[t]["colors"].items()]
    if os.path.exists(FONT_TTF): os.remove(FONT_TTF)
    download_font(THEMES[t]["font"]); subprocess.run(["termux-reload-settings"]); print(f"[SUKSES] {THEMES[t]['name']}")

def main():
    print("="*30); [print(f"{k}. {v['name']}") for k,v in THEMES.items()]; apply(int(input("Pilih: ")))
if __name__=="__main__": main()
