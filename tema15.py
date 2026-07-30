import os
import subprocess
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
COLORS_PATH = f"{HOME}/.termux/colors.properties"
FONT_PATH = f"{HOME}/.termux/font.ttf"
FONT_CACHE = f"{HOME}/.termux/font_cache"
TMP_DIR = f"{HOME}/.termux/fonts_tmp"
ZSHRC_PATH = f"{HOME}/.zshrc"
TERMUX_PROPS = f"{HOME}/.termux/termux.properties"

CONFIG_CONTENT = 'extra-keys = [["ESC","python3 ","go","HOME","UP","END","PGUP","DEL"],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","PGDN","~"],["ls","cd ","clear","ENTER","pkg ","git pull","rm -rf","exit"]]'

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join([c*2 for c in h])
    if len(h)!= 6: h = 'FFFFFF'
    return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)

THEMES = {
    1: {"name": "Default Termux", "colors": {}, "font": "default"},
    2: {"name": "Termius Green", "colors": {"background":"#0d1117","foreground":"#00ff88","color0":"#0d1117","color1":"#ff5555","color2":"#00ff88","color3":"#f1fa8c","color4":"#00ffaa","color5":"#bd93f9","color6":"#00ff88","color7":"#f8f8f2","color8":"#44475a","color9":"#ff5555","color10":"#00ff88","color11":"#f1fa8c","color12":"#00ffaa","color13":"#bd93f9","color14":"#00ff88","color15":"#ffffff"}, "font": "MapleMono"},
    3: {"name": "Termius Nord", "colors": {"background":"#2E3440","foreground":"#D8DEE9","color0":"#3B4252","color1":"#BF616A","color2":"#A3BE8C","color3":"#EBCB8B","color4":"#81A1C1","color5":"#B48EAD","color6":"#88C0D0","color7":"#E5E9F0","color8":"#4C566A","color9":"#BF616A","color10":"#A3BE8C","color11":"#EBCB8B","color12":"#81A1C1","color13":"#B48EAD","color14":"#8FBCBB","color15":"#ECEFF4"}, "font": "ComicShannsMono"},
    4: {"name": "Dracula Pink", "colors": {"background":"#282A36","foreground":"#F8F8F2","color0":"#000","color1":"#FF79C6","color2":"#50FA7B","color3":"#F1FA8C","color4":"#BD93F9","color5":"#FF79C6","color6":"#8BE9FD","color7":"#BFBF","color8":"#4D4D4D","color9":"#FF92DF","color10":"#69FF94","color11":"#FFFFA5","color12":"#D6ACFF","color13":"#FF92DF","color14":"#A4FFFF","color15":"#FFFFFF"}, "font": "ZedMono"},
    5: {"name": "Cyberpunk Neon", "colors": {"background":"#0a0a0f","foreground":"#ff00ff","color0":"#0a0a0f","color1":"#ff0066","color2":"#00ffcc","color3":"#ffff00","color4":"#00aaff","color5":"#ff00ff","color6":"#00ff00","color7":"#ffffff","color8":"#222233","color9":"#ff0066","color10":"#00ffcc","color11":"#ffff00","color12":"#00aaff","color13":"#ff00ff","color14":"#00ff00","color15":"#ffffff"}, "font": "Monaspace"},
    6: {"name": "Gruvbox Black", "colors": {"background":"#000","foreground":"#EBDBB2","color0":"#000","color1":"#CC241D","color2":"#98971A","color3":"#D79921","color4":"#458588","color5":"#B16286","color6":"#689D6A","color7":"#A89984","color8":"#928374","color9":"#FB4934","color10":"#B8BB26","color11":"#FABD2F","color12":"#83A598","color13":"#D3869B","color14":"#8EC07C","color15":"#FDF4C1"}, "font": "VictorMono"},
    7: {"name": "Catppuccin Latte", "colors": {"background":"#EFF1F5","foreground":"#4C4F69","color0":"#CCD0DA","color1":"#D20F39","color2":"#40A02B","color3":"#DF8E1D","color4":"#1E66F5","color5":"#EA76B1","color6":"#179299","color7":"#5C5F77","color8":"#BCC0CC","color9":"#D20F39","color10":"#40A02B","color11":"#DF8E1D","color12":"#1E66F5","color13":"#EA76B1","color14":"#179299","color15":"#4C4F69"}, "font": "Hasklig"},
    8: {"name": "Tokyo Night Storm","colors": {"background":"#24283b","foreground":"#c0caf5","color0":"#1D202F","color1":"#f7768e","color2":"#9ece6a","color3":"#e0af68","color4":"#7aa2f7","color5":"#bb9af7","color6":"#7dcfff","color7":"#a9b1d6","color8":"#414868","color9":"#f7768e","color10":"#9ece6a","color11":"#e0af68","color12":"#7aa2f7","color13":"#bb9af7","color14":"#7dcfff","color15":"#c0caf5"}, "font": "BerkeleyMono"},
    9: {"name": "Everforest Ocean", "colors": {"background":"#2d353b","foreground":"#d3c6aa","color0":"#2d353b","color1":"#e67e80","color2":"#a7c080","color3":"#dbbc7f","color4":"#7fbbb3","color5":"#d699b6","color6":"#83c092","color7":"#d3c6aa","color8":"#475258","color9":"#e67e80","color10":"#a7c080","color11":"#dbbc7f","color12":"#7fbbb3","color13":"#d699b6","color14":"#83c092","color15":"#ffffff"}, "font": "CaskaydiaCove"},
    10: {"name": "Rosé Pine Dawn", "colors": {"background":"#faf4ed","foreground":"#575279","color0":"#f2e9e1","color1":"#b4637a","color2":"#286983","color3":"#ea9d34","color4":"#56949f","color5":"#907aa9","color6":"#d7827e","color7":"#575279","color8":"#9893a5","color9":"#b4637a","color10":"#286983","color11":"#ea9d34","color12":"#56949f","color13":"#907aa9","color14":"#d7827e","color15":"#575279"}, "font": "FantasqueSansMono"},
    11: {"name": "Kanagawa Wave", "colors": {"background":"#1F1F28","foreground":"#DCD7BA","color0":"#090618","color1":"#C34043","color2":"#76946A","color3":"#C0A36E","color4":"#7E9CD8","color5":"#957FB8","color6":"#6A9589","color7":"#C8C093","color8":"#727169","color9":"#E82424","color10":"#98BB6C","color11":"#E6C384","color12":"#7FB4CA","color13":"#938AA9","color14":"#7AA89F","color15":"#DCD7BA"}, "font": "GeistMono"},
    12: {"name": "Mystic Lavender", "colors": {"background":"#1a1625","foreground":"#e4d6f7","color0":"#1a1625","color1":"#ff79c6","color2":"#a5ff90","color3":"#f1fa8c","color4":"#8be9fd","color5":"#bd93f9","color6":"#ffb86c","color7":"#e4d6f7","color8":"#3d3754","color9":"#ff79c6","color10":"#a5ff90","color11":"#f1fa8c","color12":"#8be9fd","color13":"#bd93f9","color14":"#ffb86c","color15":"#ffffff"}, "font": "DepartureMono"},
    13: {"name": "Ayu Mirage", "colors": {"background":"#1F2430","foreground":"#CBCCC6","color0":"#1F2430","color1":"#FF6A6A","color2":"#BAE67E","color3":"#FFE66D","color4":"#5CCFE6","color5":"#B3A1E6","color6":"#95E6CB","color7":"#CBCCC6","color8":"#707A8C","color9":"#FF6A6A","color10":"#BAE67E","color11":"#FFE66D","color12":"#5CCFE6","color13":"#B3A1E6","color14":"#95E6CB","color15":"#FFFFFF"}, "font": "InputMono"},
    14: {"name": "Nord Frost", "colors": {"background":"#2E3440","foreground":"#ECEFF4","color0":"#3B4252","color1":"#BF616A","color2":"#A3BE8C","color3":"#EBCB8B","color4":"#81A1C1","color5":"#B48EAD","color6":"#88C0D0","color7":"#E5E9F0","color8":"#4C566A","color9":"#BF616A","color10":"#A3BE8C","color11":"#EBCB8B","color12":"#81A1C1","color13":"#B48EAD","color14":"#8FBCBB","color15":"#ECEFF4"}, "font": "BlexMono"},
    15: {"name": "Solarized Light", "colors": {"background":"#FDF6E3","foreground":"#657B83","color0":"#EEE8D5","color1":"#DC322F","color2":"#859900","color3":"#B58900","color4":"#268BD2","color5":"#D33682","color6":"#2AA198","color7":"#073642","color8":"#93A1A1","color9":"#CB4B16","color10":"#586E75","color11":"#657B83","color12":"#839496","color13":"#6C71C4","color14":"#93A1A1","color15":"#002B36"}, "font": "Lilex"},
}

FONTS = {
    "MapleMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Maple.zip",
    "ComicShannsMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/ComicShannsMono.zip",
    "ZedMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/ZedMono.zip",
    "Monaspace": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Monaspace.zip",
    "VictorMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/VictorMono.zip",
    "Hasklig": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Hasklig.zip",
    "BerkeleyMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/BerkeleyMono.zip",
    "CaskaydiaCove": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/CascadiaCode.zip",
    "FantasqueSansMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FantasqueSansMono.zip",
    "GeistMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/GeistMono.zip",
    "DepartureMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/DepartureMono.zip",
    "InputMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Input.zip",
    "BlexMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/BlexMono.zip",
    "Lilex": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/Lilex.zip"
}

PROMPT_ZSH = f'''
# PROMPT CUSTOM ELMY0711
autoload -U colors && colors
PROMPT='%F{{240}}%D{{%a %b %d %H:%M:%S}}%f
%F{{magenta}}┌─[%F{{red}}💖%F{{magenta}}💜%F{{cyan}}>%F{{cyan}}ELMY0711%F{{magenta}}]─[%F{{yellow}}%~%F{{magenta}}]%f
%F{{magenta}}└─%F{{green}}╼%f '
RPROMPT=''
'''

ALIAS_ZSH = f'''
# ALIAS TEMA TERMUX
alias tema='python {HOME}/termux_tema/tema15.py'
alias t='python {HOME}/termux_tema/tema15.py'
alias reload='source ~/.zshrc'
alias c='clear'
alias ll='ls -lah'
'''

def preview_theme(num):
    theme = THEMES[num]
    print(f"\n{'='*40}")
    print(f" PREVIEW: {theme['name']}")
    print(f" Font: {theme['font']}")
    print(f"{'='*40}")
    if not theme["colors"]:
        print(" Ini tema default Termux")
        return
    c = theme["colors"]
    r1,g1,b1 = hex_to_rgb(c['color1']); r2,g2,b2 = hex_to_rgb(c['color2']); r3,g3,b3 = hex_to_rgb(c['color3'])
    r4,g4,b4 = hex_to_rgb(c['color4']); r5,g5,b5 = hex_to_rgb(c['color5']); r6,g6,b6 = hex_to_rgb(c['color6'])
    rb,gb,bb = hex_to_rgb(c['background']); rf,gf,bf = hex_to_rgb(c['foreground'])
    print(f" \033[38;2;{r1};{g1};{b1}m██ Merah\033[0m \033[38;2;{r2};{g2};{b2}m██ Hijau\033[0m \033[38;2;{r3};{g3};{b3}m██ Kuning\033[0m")
    print(f" \033[38;2;{r4};{g4};{b4}m██ Biru\033[0m \033[38;2;{r5};{g5};{b5}m██ Magenta\033[0m \033[38;2;{r6};{g6};{b6}m██ Cyan\033[0m")
    print(f" \033[48;2;{rb};{gb};{bb}m \033[0m Background \033[38;2;{rf};{gf};{bf}m██ Foreground\033[0m")
    print(f"{'='*40}")

def download_font(font_name):
    if font_name == "default":
        if os.path.exists(FONT_PATH): os.remove(FONT_PATH)
        return
    cache_file = f"{FONT_CACHE}/{font_name}.ttf"
    if os.path.exists(cache_file):
        print(f"Pakai font dari cache: {font_name}")
        run(f"cp {cache_file} {FONT_PATH}")
        return
    print(f"Download font {font_name}...")
    os.makedirs(FONT_CACHE, exist_ok=True)
    os.makedirs(TMP_DIR, exist_ok=True)
    url = FONTS[font_name]
    zip_file = f"{TMP_DIR}/{font_name}.zip"
    run(f"curl -L {url} -o {zip_file}")
    run(f"unzip -o {zip_file} '*.ttf' -d {TMP_DIR}")
    ttf_files = [f for f in os.listdir(TMP_DIR) if f.endswith('.ttf')]
    if ttf_files:
        run(f"mv {TMP_DIR}/{ttf_files[0]} {cache_file}")
        run(f"cp {cache_file} {FONT_PATH}")
        run(f"chmod 600 {FONT_PATH}")
    run(f"rm -rf {TMP_DIR}")

def setup_keyboard():
    print("Setting up keyboard...")
    os.makedirs(f"{HOME}/.termux", exist_ok=True)
    with open(TERMUX_PROPS, "w") as f:
        f.write(CONFIG_CONTENT)

def apply_prompt():
    # hapus blok lama biar gak numpuk
    run("sed -i '/PROMPT CUSTOM ELMY0711/,+5d' ~/.zshrc 2>/dev/null")
    run("sed -i '/ALIAS TEMA TERMUX/,+7d' ~/.zshrc 2>/dev/null")
    # tambahin yang baru
    with open(ZSHRC_PATH, "a") as f:
        f.write(PROMPT_ZSH)
        f.write(ALIAS_ZSH)

def apply_theme(num):
    theme = THEMES[num]
    print(f"\nApplying: {theme['name']} - {theme['font']}")
    if theme["colors"]:
        with open(COLORS_PATH, "w") as f:
            for k, v in theme["colors"].items(): f.write(f"{k} {v}\n")
    else:
        if os.path.exists(COLORS_PATH): os.remove(COLORS_PATH)
    download_font(theme["font"])
    apply_prompt()
    setup_keyboard()
    print("\nSelesai! Force close Termux dari recent apps lalu buka lagi")

def get_input(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""

def main():
    print("Cek deps...")
    run("pkg install curl unzip zsh -y")
    run("chsh -s zsh 2>/dev/null")
    os.makedirs(FONT_CACHE, exist_ok=True)

    while True:
        print("\n=== TEMA TERMUX 15 PACK + KEYBOARD ELMY ===")
        for k, v in THEMES.items(): print(f"{k:2}. {v['name']:<20} - {v['font']}")

        pilih_input = get_input("\nPilih nomor [1-15] atau q untuk keluar: ")
        if pilih_input.lower() == 'q':
            print("Keluar")
            sys.exit(0)
        if not pilih_input.isdigit():
            print("Input harus angka 1-15 atau q")
            continue

        pilih = int(pilih_input)
        if pilih in THEMES:
            preview_theme(pilih)
            y = get_input("\nTerapkan tema ini? [y/n]: ").lower()
            if y == 'y':
                apply_theme(pilih)
                break
            else:
                print("Batal. Pilih lagi ya")
        else:
            print("Nomor tidak ada. Pilih 1-15")

if __name__ == "__main__": main()
