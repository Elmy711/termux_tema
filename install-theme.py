#!/usr/bin/env python3
import os
import shutil
import subprocess
import urllib.request
import tarfile
from pathlib import Path

H=Path.home()
P=Path(os.getenv("PREFIX",
"/data/data/com.termux/files/usr"))

T=H/".termux"
F=H/".config/fish"
B=H/"bin"
C=H/".termux-themes"
FD=C/"fonts"
BK=H/".termux-backup"

CFG=F/"config.fish"
PR=F/"ELMY0711-prompt.fish"
FONT=T/"font.ttf"
COL=T/"colors.properties"
PROP=T/"termux.properties"

MAIN=H/"termux-theme.py"
CMD=B/"tema"

NF=("https://github.com/ryanoasis/"
    "nerd-fonts/releases/latest/download/")

THEMES={
"1":["Tokyo Night","Iosevka","regular",
["#f7768e","#73daca","#e0af68",
"#7aa2f7","#bb9af7","#7dcfff"]],

"2":["Dracula","VictorMono","italic",
["#002b36","#50fa7b","#f1fa8c",
"#bd93f9","#ff79c6","#8be9fd"]],

"3":["Nord","Hack","regular",
["#bf616a","#a3be8c","#ebcb8b",
"#81a1c1","#b48ead","#88c0d0"]],

"4":["Gruvbox","CascadiaCode","regular",
["#cc241d","#98971a","#d79921",
"#458588","#b16286","#689d6a"]],

"5":["Catppuccin","FiraCode","regular",
["#f38ba8","#a6e3a1","#f9e2af",
"#89b4fa","#f5c2e7","#94e2d5"]],

"6":["One Dark","Meslo","regular",
["#e06c75","#98c379","#e5c07b",
"#61afef","#c678dd","#56b6c2"]],

"7":["Cyberpunk","JetBrainsMono","regular",
["#ff0055","#00ff9c","#ffe600",
"#00aaff","#ff00ff","#00ffff"]],

"8":["Solarized","RobotoMono","regular",
["#002b36","#859900","#b58900",
"#268bd2","#d33682","#2aa198"]],

"9":["Everforest","UbuntuMono","regular",
["#002b36","#a7c080","#dbbc7f",
"#7fbbb3","#d699b6","#83c092"]],

"10":["Monokai","Mononoki","regular",
["#002b36","#a6e22e","#f4bf75",
"#66d9ef","#ae81ff","#a1efe4"]]
}

FONTS={
"Iosevka":("Iosevka",
"IosevkaNerdFont-Regular.ttf"),

"Hack":("Hack",
"HackNerdFont-Regular.ttf"),

"CascadiaCode":("CascadiaCode",
"CaskaydiaCoveNerdFont-Regular.ttf"),

"FiraCode":("FiraCode",
"FiraCodeNerdFont-Regular.ttf"),

"Meslo":("Meslo",
"MesloLGMNerdFont-Regular.ttf"),

"JetBrainsMono":("JetBrainsMono",
"JetBrainsMonoNerdFont-Regular.ttf"),

"RobotoMono":("RobotoMono",
"RobotoMonoNerdFont-Regular.ttf"),

"UbuntuMono":("UbuntuMono",
"UbuntuMonoNerdFont-Regular.ttf"),

"Mononoki":("Mononoki",
"MononokiNerdFont-Regular.ttf")
}


def setup():
    for d in (T,F,B,C,FD,BK):
        d.mkdir(parents=True,exist_ok=True)


def backup():
    for x in (CFG,COL,FONT,PROP):
        if x.exists():
            y=BK/x.name
            if not y.exists():
                shutil.copy2(x,y)


def write_colors(t):
    s=("background=#1e1e1e\n"
       "foreground=#ffffff\n"
       "cursor=#ffffff\n")

    for i,c in enumerate(t[3]):
        s+=f"color{i}={c}\n"

    COL.write_text(s)


def write_prompt(t):
    c1=t[3][0]

    s=f'''function fish_prompt
    set_color brblack
    echo -n (date "+%d %b %H:%M")
    echo ""

    set_color white
    echo -n "╭─"

    set_color {c1}
    echo -n "💖"

    set_color white
    echo -n "ELMY0711"

    set_color {c1}
    echo -n "💜"

    set_color white
    echo -n "─["

    set_color white
    echo -n (prompt_pwd)

    set_color white
    echo -n "]"
    echo ""

    set_color white
    echo -n "╰─> "

    set_color normal
end

function fish_right_prompt
end
'''

    PR.write_text(s)


def protect_fish():
    CFG.touch()

    src="source ~/.config/fish/ELMY0711-prompt.fish"
    text=CFG.read_text()

    if src not in text:
        if text and not text.endswith("\n"):
            text+="\n"

        text+=(
            "\n# ELMY0711 THEME\n"
            +src+"\n"
        )

        CFG.write_text(text)


def write_keyboard():
    s='''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{"macro":"CTRL d","display":"exit"}]]\n'''

    PROP.write_text(s)


def write_command():
    s=f'''#!{P}/bin/bash
exec {P}/bin/python3 "$HOME/termux-theme.py" "$@"
'''

    CMD.write_text(s)
    CMD.chmod(0o755)


def extract(archive,directory):
    with tarfile.open(
        archive,"r:xz"
    ) as z:
        z.extractall(directory)


def find_font(directory,wanted):
    for f in directory.rglob("*.ttf"):
        if f.name.lower()==wanted.lower():
            return f

    key=wanted.lower()
    key=key.replace(".ttf","")

    for f in directory.rglob("*.ttf"):
        if key in f.name.lower():
            return f

    return None


def install_victor():
    d=FD/"VictorMono"
    d.mkdir(parents=True,exist_ok=True)

    url=NF+"VictorMono.tar.xz"
    arc=d/"VictorMono.tar.xz"

    wanted="VictorMonoNerdFontMono-Italic.ttf"
    out=d/wanted

    if not out.exists():
        print("Download VictorMono...")

        try:
            urllib.request.urlretrieve(
                url,arc
            )

            extract(arc,d)
            arc.unlink(missing_ok=True)

        except Exception as e:
            print(
                "! Download gagal:",
                e
            )
            return False

    if not out.exists():
        out=find_font(d,wanted)

    if not out:
        print(
            "! VictorMono italic "
            "tidak ditemukan"
        )
        return False

    shutil.copy2(out,FONT)

    print(
        "✓ Font:",
        out.name
    )

    return True


def install_font(name):
    if name=="VictorMono":
        return install_victor()

    archive,wanted=FONTS[name]

    d=FD/name
    d.mkdir(
        parents=True,
        exist_ok=True
    )

    arc=d/(archive+".tar.xz")
    out=d/wanted

    if not out.exists():
        print(
            "Download",
            name+"..."
        )

        try:
            urllib.request.urlretrieve(
                NF+archive+".tar.xz",
                arc
            )

            extract(arc,d)
            arc.unlink(
                missing_ok=True
            )

        except Exception as e:
            print(
                "! Download gagal:",
                e
            )
            return False

    if not out.exists():
        out=find_font(d,wanted)

    if not out:
        print(
            "! Font tidak ditemukan:",
            wanted
        )
        return False

    shutil.copy2(out,FONT)

    print(
        "✓ Font:",
        out.name
    )

    return True


def reload_termux():
    x=P/"bin/termux-reload-settings"

    if x.exists():
        subprocess.run(
            [str(x)],
            check=False
        )


def apply_theme(n):
    t=THEMES[n]

    print()
    print("Tema :",t[0])
    print("Font :",t[1])
    print("Style:",t[2])

    backup()
    write_colors(t)
    write_prompt(t)
    protect_fish()
    write_keyboard()
    write_command()

    if install_font(t[1]):
        print("✓ Font aktif")

    reload_termux()

    print()
    print("✓ Tema aktif")
    print("✓ Prompt aktif")
    print("✓ Keyboard aktif")
    print("✓ config.fish aman")


def menu():
    while True:
        os.system("clear")

        print("╭── ELMY0711 THEME ──╮")

        for n,t in THEMES.items():
            print(
                f"│ {n:>2}. "
                f"{t[0]:<15} │"
            )

        print("│ Q. keluar           │")
        print("╰─────────────────────╯")

        try:
            q=input(
                "Pilih: "
            ).strip().lower()

        except EOFError:
            print(
                "\nInput tidak tersedia."
            )
            print(
                "Jalankan: tema"
            )
            return

        except KeyboardInterrupt:
            print()
            return

        if q in THEMES:
            apply_theme(q)

            try:
                input("\nENTER...")
            except (EOFError,KeyboardInterrupt):
                return

        elif q=="q":
            return


def install():
    setup()
    backup()
    write_command()

    try:
        MAIN.write_text(
            Path(__file__).read_text()
        )

        print(
            "✓ ~/termux-theme.py dibuat"
        )

    except Exception as e:
        print(
            "! Gagal membuat "
            "termux-theme.py:",
            e
        )
        return

    apply_theme("1")

    print()
    print("✓ Installer selesai")
    print("Jalankan: exec fish")
    print("Menu tema: tema")


def main():
    setup()

    if not MAIN.exists():
        install()
        return

    menu()


if __name__=="__main__":
    main()
