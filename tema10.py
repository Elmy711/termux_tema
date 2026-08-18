#!/data/data/com.termux/files/usr/bin/env python
import os, shutil, urllib.request, zipfile

THEMES = {
    1: ("Cyberpunk","JetBrainsMono","regular","#090014","#00ffff",["#120024","#ff0055","#00ff9c","#ffe600","#00aaff","#ff00ff","#00ffff","#d8d8d8","#3b0057","#ff3366","#33ffbb","#ffff33","#33bbff","#ff33ff","#33ffff","#ffffff"]),
    2: ("Solarized","RobotoMono","regular","#002b36","#839496",["#073642","#dc322f","#859900","#b58900","#268bd2","#d33682","#2aa198","#eee8d5","#002b36","#cb4b16","#586e75","#657b83","#839496","#6c71c4","#93a1a1","#fdf6e3"]),
    3: ("Everforest","UbuntuMono","regular","#2d353b","#d3c6aa",["#343f44","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#d3c6aa","#475258","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#e9e8d2"]),
    4: ("Monokai","Mononoki","regular","#272822","#f8f8f2",["#272822","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f8f8f2","#75715e","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f9f8f5"]),

    # TAMBAHAN 3 TEMA BARU
    5: ("Dracula Pink","JetBrainsMono","regular","#282A36","#F8F8F2",["#000000","#FF79C6","#50FA7B","#F1FA8C","#BD93F9","#FF79C6","#8BE9FD","#BFBF","#4D4D4D","#FF92DF","#69FF94","#FFFFA5","#D6ACFF","#FF92DF","#A4FFFF","#FFFFFF"]),
    6: ("Tokyo Night","SourceCodePro","regular","#1a1b26","#c0caf5",["#1a1b26","#f7768e","#9ece6a","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#a9b1d6","#414868","#f7768e","#9ece6a","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#c0caf5"]),
    7: ("Catppuccin Mocha","CascadiaCode","regular","#1e1e2e","#cdd6f4",["#1e1e2e","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#bac2de","#585b70","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#a6adc8"])
}

FONT_URL = "https://github.com/ryanoasis/nerd-fonts/releases/latest/download/"

PROMPT_FISH = '''function fish_prompt
    set_color magenta
    echo -n '┌─'
    set_color red
    echo -n '💖'
    set_color magenta
    echo -n 'ELMY0711'
    set_color red
    echo -n '💜'
    set_color magenta
    echo -n '─['
    set_color yellow
    echo -n (prompt_pwd)
    set_color magenta
    echo ']'
    echo -n '└───'
    set_color green
    echo -n '╼ '
    set_color normal
end
'''

def download_font(name):
    print(f"[+] Download font {name}...")
    url = FONT_URL + name + ".zip"
    tmp = "/data/data/com.termux/files/usr/tmp"
    z = f"{tmp}/{name}.zip"
    d = f"{tmp}/font_{name}"
    os.system(f"mkdir -p {d}")
    try:
        urllib.request.urlretrieve(url, z)
        with zipfile.ZipFile(z,'r') as zf: zf.extractall(d)
        for r,_,fs in os.walk(d):
            for f in fs:
                if f.lower().endswith('.ttf'):
                    os.makedirs(os.path.expanduser("~/.termux"),exist_ok=True)
                    shutil.copy(os.path.join(r,f), os.path.expanduser("~/.termux/font.ttf"))
                    print(f"[+] Font {name} terpasang")
                    os.system(f"rm -rf {z} {d}"); return
    except Exception as e:
        print(f"[-] Gagal download font: {e}")
    os.system(f"rm -rf {z} {d}")

def apply_colors(name, bg, fg, colors):
    p = os.path.expanduser("~/.termux/colors.properties")
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f:
        f.write(f"background = {bg}\n")
        f.write(f"foreground = {fg}\n")
        for i,c in enumerate(colors):
            f.write(f"color{i} = {c}\n")
    print(f"[+] Tema {name} diterapkan")

def apply_prompt():
    p = os.path.expanduser("~/.config/fish/config.fish")
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: f.write(PROMPT_FISH)
    print("[+] Prompt Fish ELMY0711 diterapkan")

def reset_default():
    for p in ["~/.termux/colors.properties","~/.termux/font.ttf","~/.config/fish/config.fish","~/.termux/termux.properties"]:
        if os.path.exists(os.path.expanduser(p)): os.remove(os.path.expanduser(p))
    print("[+] Reset selesai")

def main():
    print("\n===💜 ELMY0711 TEMA10 FISH 💖===")
    print("0. Reset ke Default")
    for k,v in THEMES.items(): print(f"{k}. {v[0]} - Font: {v[1]}")
    p = input("\nPilih [0-7]: ")

    if p == '0': reset_default()
    else:
        p = int(p)
        name, font, _, bg, fg, colors = THEMES[p]
        apply_colors(name, bg, fg, colors)
        download_font(font)
        apply_prompt()
        # Biar warna kebaca
        with open(os.path.expanduser("~/.termux/termux.properties"),"w") as f:
            f.write("use-black-ui = false\nallow-external-apps = true\n")

    print("\n[Selesai] Force close Termux dari Recent Apps lalu buka lagi")
    print("Lalu: Tahan lama > Settings > Appearance > Font > pilih font.ttf")

if __name__=="__main__": main()
  
