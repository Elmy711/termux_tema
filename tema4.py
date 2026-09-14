#!/usr/bin/env python3
import os, shutil, subprocess
import urllib.request, tarfile
from pathlib import Path

H=Path.home()
P=Path(os.getenv(
    "PREFIX",
    "/data/data/com.termux/files/usr"
))

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

NF=(
    "https://github.com/ryanoasis/"
    "nerd-fonts/releases/latest/download/"
)

THEMES={
"1":[
    "Tokyo Night",
    "Iosevka",
    "regular",
    "#0a0a0a",
    ["#15161e","#f7768e","#73daca",
     "#e0af68","#7aa2f7","#bb9af7",
     "#7dcfff","#a9b1d6"]
],

"2":[
    "Dracula",
    "VictorMono",
    "italic",
    "#002b36",
    ["#21222c","#ff5555","#50fa7b",
     "#f1fa8c","#bd93f9","#ff79c6",
     "#8be9fd","#f8f8f2"]
],

"3":[
    "Nord",
    "Hack",
    "regular",
    "#000814",
    ["#3b4252","#bf616a","#a3be8c",
     "#ebcb8b","#81a1c1","#b48ead",
     "#88c0d0","#e5e9f0"]
],

"4":[
    "Solarized",
    "RobotoMono",
    "regular",
    "#002b36",
    ["#073642","#dc322f","#859900",
     "#b58900","#268bd2","#d33682",
     "#2aa198","#eee8d5"]
]
}

FONTS={
"Iosevka":(
    "Iosevka",
    "IosevkaNerdFont-Regular.ttf"
),

"Hack":(
    "Hack",
    "HackNerdFont-Regular.ttf"
),

"RobotoMono":(
    "RobotoMono",
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
    bg=t[3]
    p=t[4]

    s=f"background={bg}\n"
    s+="foreground=#ffffff\n"
    s+="cursor=#ffffff\n"

    for i,c in enumerate(p):
        s+=f"color{i}={c}\n"

    COL.write_text(s)


def prompt(t):
    p=t[4]

    c1=p[1]

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
exec {P}/bin/python3 "$HOME/termux-theme.py" "$@"
'''

    CMD.write_text(s)
    CMD.chmod(0o755)


def extract(archive,directory):
    with tarfile.open(
        archive,
        "r:xz"
    ) as z:
        z.extractall(directory)


def findfont(directory,wanted):
    for f in directory.rglob("*.ttf"):
        if f.name.lower()==wanted.lower():
            return f

    key=wanted.lower()
    key=key.replace(".ttf","")

    for f in directory.rglob("*.ttf"):
        if key in f.name.lower():
            return f

    return None


def victor():
    d=FD/"VictorMono"

    d.mkdir(
        parents=True,
        exist_ok=True
    )

    archive=d/"VictorMono.tar.xz"

    wanted=(
        "VictorMonoNerdFontMono-Italic.ttf"
    )

    out=d/wanted

    if not out.exists():
        print("Download VictorMono...")

        try:
            urllib.request.urlretrieve(
                NF+"VictorMono.tar.xz",
                archive
            )

            extract(
                archive,
                d
            )

            archive.unlink(
                missing_ok=True
            )

        except Exception as e:
            print(
                "! Download gagal:",
                e
            )
            return False

    if not out.exists():
        out=findfont(
            d,
            wanted
        )

    if not out:
        print(
            "! VictorMono italic "
            "tidak ditemukan"
        )
        return False

    shutil.copy2(
        out,
        FONT
    )

    print(
        "✓ Font:",
        out.name
    )

    return True


def font(name):
    if name=="VictorMono":
        return victor()

    archive,wanted=FONTS[name]

    d=FD/name

    d.mkdir(
        parents=True,
        exist_ok=True
    )

    a=d/(archive+".tar.xz")
    out=d/wanted

    if not out.exists():
        print(
            "Download",
            name+"..."
        )

        try:
            urllib.request.urlretrieve(
                NF+archive+".tar.xz",
                a
            )

            extract(
                a,
                d
            )

            a.unlink(
                missing_ok=True
            )

        except Exception as e:
            print(
                "! Download gagal:",
                e
            )
            return False

    if not out.exists():
        out=findfont(
            d,
            wanted
        )

    if not out:
        print(
            "! File font tidak ditemukan:",
            wanted
        )
        return False

    shutil.copy2(
        out,
        FONT
    )

    print(
        "✓ Font:",
        out.name
    )

    return True


def reload():
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

    ok=font(t[1])

    if ok:
        print("✓ Font aktif")
    else:
        print("! Font gagal dipasang")

    reload()

    print()
    print("✓ Tema aktif")
    print("✓ Prompt aktif")
    print("✓ Keyboard aktif")
    print("✓ config.fish aman")


def menu():
    while True:
        os.system("clear")

        print(
            "╭── ELMY0711 THEME ──╮"
        )

        for n,t in THEMES.items():
            print(
                f"│ {n}. {t[0]:<16}│"
            )

        print(
            "│ Q. keluar          │"
        )

        print(
            "╰────────────────────╯"
        )

        try:
            q=input(
                "Pilih: "
            ).strip().lower()

        except EOFError:
            print()
            print(
                "Input tidak tersedia."
            )
            print(
                "Jalankan: tema"
            )
            return

        except KeyboardInterrupt:
            print()
            return

        if q in THEMES:
            apply(q)

            try:
                input(
                    "\nENTER..."
                )

            except (
                EOFError,
                KeyboardInterrupt
            ):
                return

        elif q=="q":
            return


def install():
    setup()
    backup()
    command()

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

    apply("1")

    print()
    print(
        "✓ Installer selesai"
    )

    print()
    print(
        "Jalankan: exec fish"
    )

    print(
        "Pengaturan: tema"
    )


def main():
    setup()

    if not MAIN.exists():
        install()
        return

    menu()


if __name__=="__main__":
    main()
