#!/usr/bin/env python3
import os, shutil, subprocess, urllib.request
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
CMD=B/"tema"

BASE=(
"https://raw.githubusercontent.com/"
"ryanoasis/nerd-fonts/v3.4.0/"
"patched-fonts/"
)

MAX=20*1024*1024

THEMES={
"1":[
"Tokyo Night","Terminess","regular","#1a1b26",
["#15161e","#f7768e","#73daca","#e0af68",
"#7aa2f7","#bb9af7","#7dcfff","#a9b1d6"]
],
"2":[
"Dracula","VictorMono","italic","#282a36",
["#21222c","#ff5555","#50fa7b","#f1fa8c",
"#bd93f9","#ff79c6","#8be9fd","#f8f8f2"]
],
"3":[
"Nord","Hack","regular","#2e3440",
["#3b4252","#bf616a","#a3be8c","#ebcb8b",
"#81a1c1","#b48ead","#88c0d0","#e5e9f0"]
],
"4":[
"Solarized","RobotoMono","regular","#002b36",
["#073642","#dc322f","#859900","#b58900",
"#268bd2","#d33682","#2aa198","#eee8d5"]
]
}

FONTS={
"Terminess":(
"TerminessNerdFont-Regular.ttf",
BASE+"Terminus/Regular/"
"TerminessNerdFont-Regular.ttf"
),
"VictorMono":(
"VictorMonoNerdFontMono-Italic.ttf",
BASE+"VictorMono/Italic/"
"VictorMonoNerdFontMono-Italic.ttf"
),
"Hack":(
"HackNerdFont-Regular.ttf",
BASE+"Hack/Regular/"
"HackNerdFont-Regular.ttf"
),
"RobotoMono":(
"RobotoMonoNerdFont-Regular.ttf",
BASE+"RobotoMono/Regular/"
"RobotoMonoNerdFont-Regular.ttf"
)
}


def setup():
    for d in (T,F,B,C,FD,BK):
        d.mkdir(
            parents=True,
            exist_ok=True
        )


def backup():
    for x in (CFG,COL,FONT,PROP):
        if x.exists():
            y=BK/x.name
            if not y.exists():
                shutil.copy2(x,y)


def colors(t):
    s=f"background={t[3]}\n"
    s+="foreground=#ffffff\n"
    s+="cursor=#ffffff\n"

    for i,c in enumerate(t[4]):
        s+=f"color{i}={c}\n"

    COL.write_text(s)


def prompt(t):
    c=t[4][1]

    s=f'''function fish_prompt
    set_color brblack
    echo -n (date "+%d %b %H:%M")
    echo ""

    set_color white
    echo -n "╭─"

    set_color {c}
    echo -n "💖"

    set_color white
    echo -n "ELMY0711"

    set_color {c}
    echo -n "💜"

    set_color white
    echo -n "─["

    echo -n (prompt_pwd)

    echo -n "]"
    echo ""

    echo -n "╰─> "
    set_color normal
end

function fish_right_prompt
end
'''

    PR.write_text(s)


def fish_source():
    CFG.touch()

    src=(
        "source ~/.config/fish/"
        "ELMY0711-prompt.fish"
    )

    text=CFG.read_text()

    if src in text:
        return

    if text and not text.endswith("\n"):
        text+="\n"

    text+=(
        "\n# ELMY0711 THEME\n"
        +src+"\n"
    )

    CFG.write_text(text)


def keyboard():
    s='''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{"macro":"CTRL d","display":"exit"}]]\n'''

    PROP.write_text(s)


def command():
    s=f'''#!{P}/bin/bash
exec {P}/bin/python3 "$HOME/temalite.py" "$@"
'''

    CMD.write_text(s)
    CMD.chmod(0o755)


def download_font(name):
    filename,url=FONTS[name]

    d=FD/name
    d.mkdir(
        parents=True,
        exist_ok=True
    )

    out=d/filename

    if out.exists():
        size=out.stat().st_size

        if 0<size<=MAX:
            shutil.copy2(out,FONT)

            print(
                f"✓ Cache: {name} "
                f"({size/1048576:.1f} MB)"
            )

            return True

        out.unlink()

    print("Download",name+"...")

    tmp=out.with_suffix(".download")

    try:
        req=urllib.request.Request(
            url,
            headers={
                "User-Agent":
                "Termux-Theme"
            }
        )

        with urllib.request.urlopen(
            req,
            timeout=60
        ) as r:

            size=r.headers.get(
                "Content-Length"
            )

            if size and int(size)>MAX:
                print("! Font >20 MB")
                return False

            total=0

            with open(tmp,"wb") as f:
                while True:
                    chunk=r.read(65536)

                    if not chunk:
                        break

                    total+=len(chunk)

                    if total>MAX:
                        print("! Font >20 MB")
                        tmp.unlink(
                            missing_ok=True
                        )
                        return False

                    f.write(chunk)

        if total<10000:
            print("! File font tidak valid")
            tmp.unlink(
                missing_ok=True
            )
            return False

        head=tmp.read_bytes()[:4]

        if head!=b"\x00\x01\x00\x00":
            print("! File bukan TTF")
            tmp.unlink(
                missing_ok=True
            )
            return False

        tmp.replace(out)

    except Exception as e:
        tmp.unlink(
            missing_ok=True
        )

        print(
            "! Download gagal:",
            e
        )

        return False

    mb=out.stat().st_size/1048576

    print(
        f"✓ Font: {filename} "
        f"({mb:.1f} MB)"
    )

    shutil.copy2(out,FONT)
    return True


def reload_termux():
    x=P/"bin/termux-reload-settings"

    if x.exists():
        subprocess.run(
            [str(x)],
            check=False
        )


def apply(n):
    t=THEMES[n]

    print()
    print("Tema :",t[0])
    print("Font :",t[1])
    print("Style:",t[2])

    backup()
    colors(t)
    prompt(t)
    fish_source()
    keyboard()
    command()

    if download_font(t[1]):
        print("✓ Font aktif")
    else:
        print("! Font gagal dipasang")

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
                f"│ {n}. {t[0]:<16}│"
            )

        print("│ Q. keluar          │")
        print("╰────────────────────╯")

        try:
            q=input(
                "Pilih: "
            ).strip().lower()

        except (EOFError,KeyboardInterrupt):
            print()
            return

        if q in THEMES:
            apply(q)

            try:
                input("\nENTER...")
            except (EOFError,KeyboardInterrupt):
                return

        elif q=="q":
            return


def main():
    setup()

    if not CFG.exists():
        CFG.touch()

    menu()


if __name__=="__main__":
    main()
