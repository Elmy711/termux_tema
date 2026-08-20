import os
import subprocess
import sys

HOME = os.path.expanduser("~")
COLORS_PATH = f"{HOME}/.termux/colors.properties"
FONT_PATH = f"{HOME}/.termux/font.ttf"
FONT_CACHE = f"{HOME}/.termux/font_cache"
TMP_DIR = f"{HOME}/.termux/fonts_tmp"
FISH_CONFIG_DIR = f"{HOME}/.config/fish"
FISH_CONFIG_PATH = f"{FISH_CONFIG_DIR}/config.fish"
TERMUX_PROPS = f"{HOME}/.termux/termux.properties"

# Tombol "tema" sekarang mengirim "tema" + ENTER (dengan \n)
CONFIG_CONTENT = 'extra-keys = [["bash ","python3 ","go run ","nano ","UP","END","PGUP","git clone "],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","curl -l ","node "],["ls","cd ","clear","ENTER","pkg install ","git pull","rm -rf ","exit"]]'

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def hex_to_rgb(h):
    h = h.lstrip('#')
    if len(h) == 3: h = ''.join([c*2 for c in h])
    if len(h)!= 6: h = 'FFFFFF'
    return int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)

THEMES = {
    1: {"name": "Default Termux", "colors": {
        "background": "#000000",
        "foreground": "#ffffff",
        "color0": "#000000",
        "color1": "#ff0000",
        "color2": "#00ff00",
        "color3": "#ffff00",
        "color4": "#0000ff",
        "color5": "#ff00ff",
        "color6": "#00ffff",
        "color7": "#ffffff",
        "color8": "#444444",
        "color9": "#ff0000",
        "color10": "#00ff00",
        "color11": "#ffff00",
        "color12": "#0000ff",
        "color13": "#ff00ff",
        "color14": "#00ffff",
        "color15": "#ffffff"
    }, "font": "default"},
    2: {"name": "Termius Nord", "colors": {"background":"#2E3440","foreground":"#D8DEE9","color0":"#3B4252","color1":"#BF616A","color2":"#A3BE8C","color3":"#EBCB8B","color4":"#81A1C1","color5":"#B48EAD","color6":"#88C0D0","color7":"#E5E9F0","color8":"#4C566A","color9":"#BF616A","color10":"#A3BE8C","color11":"#EBCB8B","color12":"#81A1C1","color13":"#B48EAD","color14":"#8FBCBB","color15":"#ECEFF4"}, "font": "JetBrainsMono"}, 
    3: {"name": "Dracula Pink", "colors": {"background":"#282A36","foreground":"#F8F8F2","color0":"#000","color1":"#FF79C6","color2":"#50FA7B","color3":"#F1FA8C","color4":"#BD93F9","color5":"#FF79C6","color6":"#8BE9FD","color7":"#BFBF","color8":"#4D4D4D","color9":"#FF92DF","color10":"#69FF94","color11":"#FFFFA5","color12":"#D6ACFF","color13":"#FF92DF","color14":"#A4FFFF","color15":"#FFFFFF"}, "font": "ZedMono"},
    4: {"name": "Cyberpunk Neon", "colors": {"background":"#0a0a0f","foreground":"#ff00ff","color0":"#0a0a0f","color1":"#ff0066","color2":"#00ffcc","color3":"#ffff00","color4":"#00aaff","color5":"#ff00ff","color6":"#00ff00","color7":"#ffffff","color8":"#222233","color9":"#ff0066","color10":"#00ffcc","color11":"#ffff00","color12":"#00aaff","color13":"#ff00ff","color14":"#00ff00","color15":"#ffffff"}, "font": "VictorMono"},  
    5: {"name": "Gruvbox Dark", "colors": {"background":"#282828","foreground":"#EBDBB2","color0":"#282828","color1":"#CC241D","color2":"#98971A","color3":"#D79921","color4":"#458588","color5":"#B16286","color6":"#689D6A","color7":"#A89984","color8":"#928374","color9":"#FB4934","color10":"#B8BB26","color11":"#FABD2F","color12":"#83A598","color13":"#D3869B","color14":"#8EC07C","color15":"#FDF4C1"}, "font": "FiraCode"},
    6: {"name": "Tokyo Night Storm","colors": {"background":"#24283b","foreground":"#c0caf5","color0":"#1D202F","color1":"#f7768e","color2":"#9ece6a","color3":"#e0af68","color4":"#7aa2f7","color5":"#bb9af7","color6":"#7dcfff","color7":"#a9b1d6","color8":"#414868","color9":"#f7768e","color10":"#9ece6a","color11":"#e0af68","color12":"#7aa2f7","color13":"#bb9af7","color14":"#7dcfff","color15":"#c0caf5"}, "font": "SourceCodePro"},  
    7: {"name": "Everforest Ocean", "colors": {"background":"#2d353b","foreground":"#d3c6aa","color0":"#2d353b","color1":"#e67e80","color2":"#a7c080","color3":"#dbbc7f","color4":"#7fbbb3","color5":"#d699b6","color6":"#83c092","color7":"#d3c6aa","color8":"#475258","color9":"#e67e80","color10":"#a7c080","color11":"#dbbc7f","color12":"#7fbbb3","color13":"#d699b6","color14":"#83c092","color15":"#ffffff"}, "font": "UbuntuMono"}, 
}

FONTS = {
    "JetBrainsMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/JetBrainsMono.zip", 
    "ZedMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/ZedMono.zip",
    "VictorMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/VictorMono.zip",
    "FiraCode": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/FiraCode.zip",  
    "SourceCodePro": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/SourceCodePro.zip",
    "UbuntuMono": "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/UbuntuMono.zip"  
}

ALIAS_FISH = f'''
# BEGIN ALIAS TEMA TERMUX
alias tema='python {HOME}/termux_tema/temafish.py'
alias t='python {HOME}/termux_tema/temafish.py'
alias reload='source ~/.config/fish/config.fish'
# END ALIAS TEMA TERMUX
'''

def generate_fish_prompt(colors):
    if not colors:
        colors = {
            "background": "#000000",
            "foreground": "#ffffff",
            "color0": "#000000",
            "color1": "#ff0000",
            "color2": "#00ff00",
            "color3": "#ffff00",
            "color4": "#0000ff",
            "color5": "#ff00ff",
            "color6": "#00ffff",
            "color7": "#ffffff",
            "color8": "#444444",
            "color9": "#ff0000",
            "color10": "#00ff00",
            "color11": "#ffff00",
            "color12": "#0000ff",
            "color13": "#ff00ff",
            "color14": "#00ffff",
            "color15": "#ffffff"
        }
    c1 = colors.get('color1', '#ff0000')
    c2 = colors.get('color2', '#00ff00')
    c3 = colors.get('color3', '#ffff00')
    c4 = colors.get('color4', '#0000ff')
    c5 = colors.get('color5', '#ff00ff')
    c6 = colors.get('color6', '#00ffff')
    fg = colors.get('foreground', '#ffffff')
    bg = colors.get('background', '#000000')

    prompt = f'''
# BEGIN PROMPT CUSTOM ELMY0711
function fish_prompt
    set_color {c6}
    echo -n (date "+%b %d %H:%M:%S")
    echo ""
    set_color {c5}
    echo -n "╭─"
    set_color {c1}
    echo -n "💖"
    set_color {c5}
    echo -n "ELMY0711"
    set_color {c1}
    echo -n "💜"
    set_color {c5}
    echo -n " _["
    set_color {c3}
    echo -n (prompt_pwd)
    set_color {c5}
    echo -n "]"
    echo ""
    set_color {c5}
    echo -n "╰─"
    set_color {c2}
    echo -n "╼ "
    set_color normal
end
function fish_right_prompt
end
# END PROMPT CUSTOM ELMY0711
'''
    return prompt

def preview_theme(num):
    theme = THEMES[num]
    print(f"\n{'='*20}")
    print(f" PREVIEW: {theme['name']}")
    print(f" Font: {theme['font']}")
    print(f"{'='*20}")
    if not theme["colors"]:
        print(" tema default Termux")
        return
    c = theme["colors"]
    r1,g1,b1 = hex_to_rgb(c['color1']); r2,g2,b2 = hex_to_rgb(c['color2']); r3,g3,b3 = hex_to_rgb(c['color3'])
    r4,g4,b4 = hex_to_rgb(c['color4']); r5,g5,b5 = hex_to_rgb(c['color5']); r6,g6,b6 = hex_to_rgb(c['color6'])
    rb,gb,bb = hex_to_rgb(c['background']); rf,gf,bf = hex_to_rgb(c['foreground'])
    print(f" \033[38;2;{r1};{g1};{b1}m█ Merah\033[0m \033[38;2;{r2};{g2};{b2}m█ Hijau\033[0m \033[38;2;{r3};{g3};{b3}m█ Kuning\033[0m")
    print(f" \033[38;2;{r4};{g4};{b4}m█ Biru\033[0m \033[38;2;{r5};{g5};{b5}m█ Magenta\033[0m \033[38;2;{r6};{g6};{b6}m█ Cyan\033[0m")
    print(f" \033[48;2;{rb};{gb};{bb}m \033[0m Background \033[38;2;{rf};{gf};{bf}m█ Foreground\033[0m")
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
    run(f"rm -rf {TMP_DIR}")

def setup_keyboard():
    print("Setting up keyboard...")
    os.makedirs(f"{HOME}/.termux", exist_ok=True)
    with open(TERMUX_PROPS, "w") as f:
        f.write(CONFIG_CONTENT)

def strip_function_block(lines, func_name):
    result = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip() == f"function {func_name}":
            i += 1
            while i < n and lines[i].strip() != "end":
                i += 1
            i += 1
            continue
        result.append(lines[i])
        i += 1
    return result

def purge_managed_fish_content(lines):
    lines = strip_function_block(lines, "fish_prompt")
    lines = strip_function_block(lines, "fish_right_prompt")
    cleaned = []
    for line in lines:
        s = line.strip()
        if s.startswith("#") and ("ELMY0711" in s or "TEMA TERMUX" in s):
            continue
        if s.startswith("alias tema=") or s.startswith("alias t=") or s.startswith("alias reload="):
            continue
        cleaned.append(line)
    return cleaned

def apply_prompt_fish(colors):
    os.makedirs(FISH_CONFIG_DIR, exist_ok=True)
    if not os.path.exists(FISH_CONFIG_PATH):
        open(FISH_CONFIG_PATH, "a").close()

    with open(FISH_CONFIG_PATH, "r") as f:
        lines = f.readlines()

    lines = purge_managed_fish_content(lines)

    while lines and lines[-1].strip() == "":
        lines.pop()

    prompt_code = generate_fish_prompt(colors)

    with open(FISH_CONFIG_PATH, "w") as f:
        f.writelines(lines)
        f.write("\n")
        f.write(prompt_code)
        f.write(ALIAS_FISH)

def apply_theme(num):
    theme = THEMES[num]
    print(f"\nApplying: {theme['name']} - {theme['font']}")
    if theme["colors"]:
        with open(COLORS_PATH, "w") as f:
            for k, v in theme["colors"].items(): f.write(f"{k} {v}\n")
    else:
        if os.path.exists(COLORS_PATH): os.remove(COLORS_PATH)
    download_font(theme["font"])
    apply_prompt_fish(theme["colors"])
    setup_keyboard()
    print("\nSelesai... Exit lalu buka lagi")

def get_input(prompt):
    try:
        return input(prompt).strip()
    except EOFError:
        return ""

def main():
    print("Cek deps...")
    run("pkg install curl unzip fish -y")
    run("chsh -s fish 2>/dev/null")

    os.makedirs(FONT_CACHE, exist_ok=True)

    while True:
        print("\n===💜  ELMY0711 TEMAFISH 💖===")
        for k, v in THEMES.items(): print(f"{k}. {v['name']:<20} - {v['font']}")

        pilih_input = get_input("\nPilih [1-7]  q untuk keluar: ")
        if pilih_input.lower() == 'q':
            print("Keluar")
            sys.exit(0)
        if not pilih_input.isdigit():
            print("Input harus angka 1-7 atau q")
            continue

        pilih = int(pilih_input)
        if pilih in THEMES:
            preview_theme(pilih)
            y = get_input("\nTerapkan tema ? [y/n]: ").lower()
            if y == 'y':
                apply_theme(pilih)
                break
            else:
                print("Batal. Pilih lagi")
        else:
            print("Nomor tidak ada. Pilih 1-7")

if __name__ == "__main__": main()
