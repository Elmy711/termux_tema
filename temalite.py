#!/usr/bin/env python3
# TEMALITE - standalone Termux theme manager
import os, json, shutil, urllib.request, zipfile
from pathlib import Path

HOME=Path.home(); TERMUX=HOME/".termux"; COLORS=TERMUX/"colors.properties"
KEYS=TERMUX/"termux.properties"; FONT=TERMUX/"font.ttf"
BACKUP=TERMUX/"temalite-backup"; STATE=HOME/".temalite.json"

THEMES={
"Tokyo Night":["#16161e","#a9b1d6","#c0caf5","#283457","#c0caf5","#15161e","#f7768e","#41a6b5","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#787c99","#414868","#f7768e","#73daca","#ff9e64","#7aa2f7","#bb9af7","#7dcfff","#c0caf5"],
"Dracula":["#282a36","#f8f8f2","#f8f8f0","#44475a","#f8f8f2","#21222c","#ff5555","#50fa7b","#f1fa8c","#bd93f9","#ff79c6","#8be9fd","#f8f8f2","#6272a4","#ff6e6e","#69ff94","#ffffa5","#d6acff","#ff92df","#a4ffff","#ffffff"],
"Nord":["#2e3440","#d8dee9","#d8dee9","#434c5e","#eceff4","#3b4252","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#88c0d0","#e5e9f0","#4c566a","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#8fbcbb","#eceff4"],
"Gruvbox":["#282828","#ebdbb2","#ebdbb2","#504945","#fbf1c7","#282828","#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#a89984","#928374","#fb4934","#b8bb26","#fabd2f","#83a598","#d3869b","#8ec07c","#ebdbb2"],
"One Dark":["#282c34","#abb2bf","#528bff","#3e4451","#ffffff","#282c34","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#abb2bf","#5c6370","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#ffffff"],
"Catppuccin":["#1e1e2e","#cdd6f4","#f5e0e6","#45475a","#cdd6f4","#181825","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#bac2de","#585b70","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#a6adc8"],
"Monokai":["#272822","#f8f8f2","#f8f8f0","#49483e","#ffffff","#272822","#f92672","#a6e22e","#e6db74","#66d9ef","#ae81ff","#a1efe4","#f8f8f2","#75715e","#f92672","#a6e22e","#e6db74","#66d9ef","#ae81ff","#a1efe4","#f9f8f5"],
"Solarized Dark":["#002b36","#839496","#93a1a1","#073642","#eee8d5","#073642","#dc322f","#859900","#b58900","#268bd2","#d33682","#2aa198","#eee8d5","#586e75","#cb4b16","#586e75","#657b83","#839496","#6c71c4","#93a1a1","#fdf6e3"],
"Rose Pine":["#191724","#e0def4","#524f67","#26233a","#e0def4","#26233a","#eb6f92","#9ccfd8","#f6c177","#31748f","#c4a7e7","#ebbcba","#e0def4","#6e6a86","#eb6f92","#9ccfd8","#f6c177","#31748f","#c4a7e7","#ebbcba","#e0def4"],
"Everforest":["#2d353b","#d3c6aa","#d3c6aa","#475258","#d3c6aa","#475258","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#d3c6aa","#859289","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#e4e1cd"]}

THEME_FONTS=[("Tokyo Night","Iosevka"),("Dracula","VictorMono"),("Nord","JetBrainsMono"),("Gruvbox","Hack"),("One Dark","CascadiaCode"),("Catppuccin","FiraCode"),("Monokai","Inconsolata"),("Solarized Dark","IBM Plex Mono"),("Rose Pine","Noto Sans Mono"),("Everforest","UbuntuMono")]

FONTS={
"Iosevka":("https://github.com/be5invis/Iosevka/releases/latest/download/PkgTTF-Iosevka-31.0.0.zip","Iosevka-Regular.ttf"),
"VictorMono":("https://github.com/rubjo/victor-mono/releases/latest/download/VictorMonoAll.zip","VictorMono-Regular.ttf"),
"JetBrainsMono":("https://github.com/JetBrains/JetBrainsMono/releases/latest/download/JetBrainsMono-2.304.zip","JetBrainsMono-Regular.ttf"),
"Hack":("https://github.com/source-foundry/Hack/releases/latest/download/Hack-v3.003-ttf.zip","Hack-Regular.ttf"),
"CascadiaCode":("https://github.com/microsoft/cascadia-code/releases/latest/download/CascadiaCode-2407.24.zip","CascadiaCode.ttf"),
"FiraCode":("https://github.com/tonsky/FiraCode/releases/latest/download/Fira_Code_v6.2.zip","FiraCode-Regular.ttf"),
"Inconsolata":("https://github.com/googlefonts/Inconsolata/releases/latest/download/fonts.zip","Inconsolata-Regular.ttf"),
"IBM Plex Mono":("https://github.com/IBM/plex/releases/latest/download/TrueType.zip","IBMPlexMono-Regular.ttf"),
"Noto Sans Mono":("https://github.com/notofonts/latin-greek-cyrillic/releases/latest/download/NotoSansMono.zip","NotoSansMono-Regular.ttf"),
"UbuntuMono":("https://github.com/ubuntu/ubuntu-font-family/releases/latest/download/ubuntu-font-family-0.83.zip","UbuntuMono-R.ttf")}

def ensure():
    TERMUX.mkdir(parents=True,exist_ok=True); BACKUP.mkdir(parents=True,exist_ok=True)
def backup(p):
    if p.exists() and not (BACKUP/p.name).exists(): shutil.copy2(p,BACKUP/p.name)
def write_theme(name):
    keys="background foreground cursor selection-background selection-foreground black red green yellow blue magenta cyan white bright-black bright-red bright-green bright-yellow bright-blue bright-magenta bright-cyan bright-white".split()
    backup(COLORS); COLORS.write_text("\n".join(f"{k}={v}" for k,v in zip(keys,THEMES[name]))+"\n")
def write_keys():
    backup(KEYS)
    KEYS.write_text("# TEMALITE\nextra-keys = [[\"ESC\",\"TAB\",\"CTRL\",\"ALT\",\"UP\",\"END\",\"PGUP\"],[\"HOME\",\"LEFT\",\"DOWN\",\"RIGHT\",\"PGDN\",\"ENTER\",\"~\"],[\"CTRL\",\"C\",\"CTRL\",\"D\",\"CTRL\",\"L\",\"CTRL\",\"Z\",\"|\"]]\n")
def write_prompt():
    d=HOME/".config/fish/functions"; d.mkdir(parents=True,exist_ok=True); p=d/"fish_prompt.fish"; backup(p)
    p.write_text('function fish_prompt\n    set_color cyan\n    echo (date "+%a %d %b %H:%M:%S")\n    set_color magenta\n    echo "╭─["(prompt_pwd)"]"\n    set_color cyan\n    echo -n "╰─❯ " \n    set_color normal\nend\n')
def font(name):
    cache=HOME/".cache/temalite"; cache.mkdir(parents=True,exist_ok=True); arc=cache/(name.replace(" ","_")+".zip"); ext=cache/(name.replace(" ","_")+"_x"); url,want=FONTS[name]
    try:
        print("  ↓",name); urllib.request.urlretrieve(url,arc)
        if ext.exists(): shutil.rmtree(ext)
        ext.mkdir(); zipfile.ZipFile(arc).extractall(ext); fs=list(ext.rglob("*.ttf"))
        t=next((x for x in fs if x.name.lower()==want.lower()),None) or next((x for x in fs if "regular" in x.stem.lower() and "italic" not in x.stem.lower()),None) or (fs[0] if fs else None)
        if not t: print("  ! TTF tidak ditemukan"); return False
        if FONT.exists(): backup(FONT)
        shutil.copy2(t,FONT); print("  ✓",t.name); return True
    except Exception as e: print("  ! Font gagal:",e); return False
def apply(theme,f):
    ensure(); write_theme(theme); write_keys(); write_prompt(); ok=font(f); STATE.write_text(json.dumps({"theme":theme,"font":f}))
    print("\n✓ Tema aktif :",theme); print("✓ Font        :",f if ok else "gagal"); print("✓ Keyboard aktif"); print("✓ Fish prompt aktif"); print("✓ config.fish aman"); print("\nTutup lalu buka kembali Termux.")
def restore():
    if not BACKUP.exists(): print("! Belum ada backup."); return
    for n in ("colors.properties","termux.properties","font.ttf"):
        s=BACKUP/n; d=TERMUX/n
        if s.exists(): shutil.copy2(s,d); print("✓ restored",n)
    s=BACKUP/"fish_prompt.fish"; d=HOME/".config/fish/functions/fish_prompt.fish"
    if s.exists(): d.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(s,d); print("✓ restored fish_prompt.fish")
def main():
    ensure()
    while True:
        print("\n╭─ TEMALITE\n╰─ Standalone Termux Theme Manager\n")
        for i,(t,f) in enumerate(THEME_FONTS,1): print(f" {i:2}. {t:<16} {f}")
        print("  0. Keluar\n  b. Restore backup\n")
        c=input("Pilih [0-10]: ").strip().lower()
        if c=="0": return
        if c=="b": restore(); continue
        if c.isdigit() and 1<=int(c)<=10: t,f=THEME_FONTS[int(c)-1]; print(f"\nMengaktifkan {t} + {f}..."); apply(t,f)
        else: print("! Pilihan tidak valid.")
if __name__=="__main__":
    try: main()
    except KeyboardInterrupt: print("\nDibatalkan.")
