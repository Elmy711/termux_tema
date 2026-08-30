#!/usr/bin/env python3
import os, shutil, subprocess, urllib.request, tarfile
from pathlib import Path

H=Path.home()
P=Path(os.getenv("PREFIX","/data/data/com.termux/files/usr"))
T=H/".termux"; F=H/".config/fish"; B=H/"bin"
C=H/".termux-themes"; FD=C/"fonts"; BK=H/".termux-backup"
CFG=F/"config.fish"; PR=F/"ELMY0711-prompt.fish"
FONT=T/"font.ttf"; COL=T/"colors.properties"
PROP=T/"termux.properties"; MAIN=H/"termux-theme.py"
CMD=B/"tema"

NF="https://github.com/ryanoasis/nerd-fonts/releases/latest/download/"

THEMES={
"1":["Tokyo Night","Iosevka","regular","#002b36","#a9b1d6",
["#15161e","#f7768e","#73daca","#e0af68","#7aa2f7","#bb9af7","#7dcfff","#a9b1d6"]],
"2":["Dracula","VictorMono","italic","#002b36","#f8f8f2",
["#21222c","#ff5555","#50fa7b","#f1fa8c","#bd93f9","#ff79c6","#8be9fd","#f8f8f2"]],
"3":["Nord","Hack","regular","#002b36","#d8dee9",
["#3b4252","#bf616a","#a3be8c","#ebcb8b","#81a1c1","#b48ead","#88c0d0","#e5e9f0"]],
"4":["Gruvbox","CascadiaCode","regular","#002b36","#ebdbb2",
["#282828","#cc241d","#98971a","#d79921","#458588","#b16286","#689d6a","#a89984"]],
"5":["Catppuccin","FiraCode","regular","#1e1e2e","#cdd6f4",
["#45475a","#f38ba8","#a6e3a1","#f9e2af","#89b4fa","#f5c2e7","#94e2d5","#bac2de"]],
"6":["One Dark","Meslo","regular","#282c34","#abb2bf",
["#282c34","#e06c75","#98c379","#e5c07b","#61afef","#c678dd","#56b6c2","#abb2bf"]],
"7":["Cyberpunk","JetBrainsMono","regular","#090014","#d8d8d8",
["#120024","#ff0055","#00ff9c","#ffe600","#00aaff","#ff00ff","#00ffff","#d8d8d8"]],
"8":["Solarized","RobotoMono","regular","#002b36","#839496",
["#073642","#dc322f","#859900","#b58900","#268bd2","#d33682","#2aa198","#eee8d5"]],
"9":["Everforest","UbuntuMono","regular","#2d353b","#d3c6aa",
["#343f44","#e67e80","#a7c080","#dbbc7f","#7fbbb3","#d699b6","#83c092","#d3c6aa"]],
"10":["Monokai","Mononoki","regular","#272822","#f8f8f2",
["#272822","#f92672","#a6e22e","#f4bf75","#66d9ef","#ae81ff","#a1efe4","#f8f8f2"]]
}

FONTS={
"Iosevka":("Iosevka","IosevkaNerdFont-Regular.ttf"),
"Hack":("Hack","HackNerdFont-Regular.ttf"),
"CascadiaCode":("CascadiaCode","CaskaydiaCoveNerdFont-Regular.ttf"),
"FiraCode":("FiraCode","FiraCodeNerdFont-Regular.ttf"),
"Meslo":("Meslo","MesloLGMNerdFont-Regular.ttf"),
"JetBrainsMono":("JetBrainsMono","JetBrainsMonoNerdFont-Regular.ttf"),
"RobotoMono":("RobotoMono","RobotoMonoNerdFont-Regular.ttf"),
"UbuntuMono":("UbuntuMono","UbuntuMonoNerdFont-Regular.ttf"),
"Mononoki":("Mononoki","MononokiNerdFont-Regular.ttf")
}

def setup():
    for d in(T,F,B,C,FD,BK): d.mkdir(parents=True,exist_ok=True)

def backup():
    for x in(CFG,COL,FONT,PROP):
        if x.exists():
            y=BK/x.name
            if not y.exists(): shutil.copy2(x,y)

def colors(t):
    p=t[5]
    s=f"background={t[3]}\nforeground={t[4]}\ncursor={t[4]}\n"
    s+="\n".join(f"color{i}={v}" for i,v in enumerate(p))+"\n"
    COL.write_text(s)

def prompt(t):
    p=t[5]; c1,c2,c3,c5,c6=p[1],p[2],p[3],p[5],p[6]
    s=f'''function fish_prompt
    set_color brblack
    echo -n (date "+%d %b %H:%M")
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
    echo -n "─["
    set_color {c3}
    echo -n (prompt_pwd)
    set_color {c5}
    echo -n "]"
    echo ""
    set_color {c5}
    echo -n "╰─"
    set_color {c2}
    echo -n "> "
    set_color normal
end
function fish_right_prompt
end
'''
    PR.write_text(s)

def fish_source():
    CFG.touch()
    src="source ~/.config/fish/ELMY0711-prompt.fish"
    s=CFG.read_text()
    if src not in s:
        if s and not s.endswith("\n"): s+="\n"
        CFG.write_text(s+"\n# ELMY0711 THEME\n"+src+"\n")

def keyboard():
    s='''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{"macro":"CTRL d","display":"exit"}]]\n'''
    PROP.write_text(s)

def command():
    s=f'''#!{P}/bin/bash
exec {P}/bin/python3 "$HOME/termux-theme.py" "$@"
'''
    CMD.write_text(s); CMD.chmod(0o755)

def extract(a,d):
    with tarfile.open(a,"r:xz") as z: z.extractall(d)

def findfont(d,want):
    for f in d.rglob("*.ttf"):
        if f.name.lower()==want.lower(): return f
    key=want.lower().replace(".ttf","").split("-")
    for f in d.rglob("*.ttf"):
        if all(k in f.name.lower() for k in key): return f
    return None

def victor():
    d=FD/"VictorMono"; d.mkdir(parents=True,exist_ok=True)
    a=d/"VictorMono.tar.xz"
    want="VictorMonoNerdFontMono-Italic.ttf"
    out=d/want
    if not out.exists():
        print("Download VictorMono...")
        try:
            urllib.request.urlretrieve(NF+"VictorMono.tar.xz",a)
            extract(a,d); a.unlink(missing_ok=True)
        except Exception as e:
            print("! Download gagal:",e); return False
    out=out if out.exists() else findfont(d,want)
    if not out:
        print("! VictorMono italic tidak ditemukan"); return False
    shutil.copy2(out,FONT)
    print("✓ Font:",out.name)
    return True

def font(name):
    if name=="VictorMono": return victor()
    archive,want=FONTS[name]
    d=FD/name; d.mkdir(parents=True,exist_ok=True)
    a=d/(archive+".tar.xz"); out=d/want
    if not out.exists():
        print("Download",name+"...")
        try:
            urllib.request.urlretrieve(NF+archive+".tar.xz",a)
            extract(a,d); a.unlink(missing_ok=True)
        except Exception as e:
            print("! Download gagal:",e); return False
    out=out if out.exists() else findfont(d,want)
    if not out:
        print("! Font tidak ditemukan:",want); return False
    shutil.copy2(out,FONT)
    print("✓ Font:",out.name)
    return True

def reload():
    x=P/"bin/termux-reload-settings"
    if x.exists(): subprocess.run([str(x)],check=False)

def apply(n):
    t=THEMES[n]
    print(f"\nTema : {t[0]}\nFont : {t[1]}\nStyle: {t[2]}")
    backup(); colors(t); prompt(t); fish_source()
    keyboard(); command(); font(t[1]); reload()
    print("\n✓ Tema aktif\n✓ Prompt aktif\n✓ Keyboard aktif\n✓ config.fish aman")

def menu():
    while True:
        os.system("clear")
        print("╭── ELMY0711 THEME ──╮")
        for n,t in THEMES.items(): print(f"│ {n:>2}. {t[0]:<15} │")
        print("│ Q. keluar           │")
        print("╰─────────────────────╯")
        try: q=input("Pilih: ").strip().lower()
        except KeyboardInterrupt: print(); return
        if q in THEMES:
            apply(q)
            try: input("\nENTER...")
            except KeyboardInterrupt: pass
        elif q=="q": return

def install():
    setup(); backup(); command()
    try:
        MAIN.write_text(Path(__file__).read_text())
        print("✓ ~/termux-theme.py dibuat")
    except Exception as e: print("! Gagal membuat termux-theme.py:",e)
    apply("1")
    print("\n✓ Installer selesai\n\nJalankan: exec fish\nPengaturan: tema")

def main():
    setup()
    if not MAIN.exists(): install()
    else: menu()

if __name__=="__main__":
    main()
