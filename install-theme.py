#!/usr/bin/env python3

import os
import shutil
import subprocess
import tarfile
import urllib.request
from pathlib import Path

HOME = Path.home()
PREFIX = Path(os.environ.get(
    "PREFIX",
    "/data/data/com.termux/files/usr"
))

TERMUX = HOME / ".termux"
FISH = HOME / ".config" / "fish"
BIN = HOME / "bin"

CACHE = HOME / ".termux-themes"
FONTS = CACHE / "fonts"
BACKUP = HOME / ".termux-backup"

CONFIG = FISH / "config.fish"
PROMPT = FISH / "ELMY0711-prompt.fish"

FONT = TERMUX / "font.ttf"
COLORS = TERMUX / "colors.properties"
PROPS = TERMUX / "termux.properties"

THEME_SCRIPT = HOME / "termux-theme.py"
TEMA = BIN / "tema"

NF = (
    "https://github.com/ryanoasis/"
    "nerd-fonts/releases/latest/download/"
)

THEMES = {
    "1": (
        "Tokyo Night",
        "Iosevka",
        "regular",
        "#1a1b26",
        "#a9b1d6",
        [
            "#15161e",
            "#f7768e",
            "#73daca",
            "#e0af68",
            "#7aa2f7",
            "#bb9af7",
            "#7dcfff",
            "#a9b1d6"
        ]
    ),

    "2": (
        "Dracula",
        "VictorMono",
        "italic",
        "#282a36",
        "#f8f8f2",
        [
            "#21222c",
            "#ff5555",
            "#50fa7b",
            "#f1fa8c",
            "#bd93f9",
            "#ff79c6",
            "#8be9fd",
            "#f8f8f2"
        ]
    ),

    "3": (
        "Nord",
        "Hack",
        "regular",
        "#2e3440",
        "#d8dee9",
        [
            "#3b4252",
            "#bf616a",
            "#a3be8c",
            "#ebcb8b",
            "#81a1c1",
            "#b48ead",
            "#88c0d0",
            "#e5e9f0"
        ]
    ),

    "4": (
        "Gruvbox",
        "CascadiaCode",
        "regular",
        "#282828",
        "#ebdbb2",
        [
            "#282828",
            "#cc241d",
            "#98971a",
            "#d79921",
            "#458588",
            "#b16286",
            "#689d6a",
            "#a89984"
        ]
    ),

    "5": (
        "Catppuccin",
        "FiraCode",
        "regular",
        "#1e1e2e",
        "#cdd6f4",
        [
            "#45475a",
            "#f38ba8",
            "#a6e3a1",
            "#f9e2af",
            "#89b4fa",
            "#f5c2e7",
            "#94e2d5",
            "#bac2de"
        ]
    ),

    "6": (
        "One Dark",
        "Meslo",
        "regular",
        "#282c34",
        "#abb2bf",
        [
            "#282c34",
            "#e06c75",
            "#98c379",
            "#e5c07b",
            "#61afef",
            "#c678dd",
            "#56b6c2",
            "#abb2bf"
        ]
    ),

    "7": (
        "Cyberpunk",
        "JetBrainsMono",
        "regular",
        "#090014",
        "#d8d8d8",
        [
            "#120024",
            "#ff0055",
            "#00ff9c",
            "#ffe600",
            "#00aaff",
            "#ff00ff",
            "#00ffff",
            "#d8d8d8"
        ]
    ),

    "8": (
        "Solarized",
        "RobotoMono",
        "regular",
        "#002b36",
        "#839496",
        [
            "#073642",
            "#dc322f",
            "#859900",
            "#b58900",
            "#268bd2",
            "#d33682",
            "#2aa198",
            "#eee8d5"
        ]
    ),

    "9": (
        "Everforest",
        "UbuntuMono",
        "regular",
        "#2d353b",
        "#d3c6aa",
        [
            "#343f44",
            "#e67e80",
            "#a7c080",
            "#dbbc7f",
            "#7fbbb3",
            "#d699b6",
            "#83c092",
            "#d3c6aa"
        ]
    ),

    "10": (
        "Monokai",
        "Mononoki",
        "regular",
        "#272822",
        "#f8f8f2",
        [
            "#272822",
            "#f92672",
            "#a6e22e",
            "#f4bf75",
            "#66d9ef",
            "#ae81ff",
            "#a1efe4",
            "#f8f8f2"
        ]
    )
}

FONT_FILES = {
    "Iosevka": (
        "Iosevka.tar.xz",
        "Iosevka/Iosevka-Regular.ttf"
    ),

    "Hack": (
        "Hack.tar.xz",
        "Hack/Hack-Regular.ttf"
    ),

    "CascadiaCode": (
        "CascadiaCode.tar.xz",
        "CascadiaCode/CaskaydiaCoveNerdFont-Regular.ttf"
    ),

    "FiraCode": (
        "FiraCode.tar.xz",
        "FiraCode/FiraCodeNerdFont-Regular.ttf"
    ),

    "Meslo": (
        "Meslo.tar.xz",
        "Meslo/MesloLGMNerdFont-Regular.ttf"
    ),

    "JetBrainsMono": (
        "JetBrainsMono.tar.xz",
        "JetBrainsMono/JetBrainsMonoNerdFont-Regular.ttf"
    ),

    "RobotoMono": (
        "RobotoMono.tar.xz",
        "RobotoMono/RobotoMonoNerdFont-Regular.ttf"
    ),

    "UbuntuMono": (
        "UbuntuMono.tar.xz",
        "UbuntuMono/UbuntuMonoNerdFont-Regular.ttf"
    ),

    "Mononoki": (
        "Mononoki.tar.xz",
        "Mononoki/MononokiNerdFont-Regular.ttf"
    )
}


def setup():
    for d in (
        TERMUX,
        FISH,
        BIN,
        CACHE,
        FONTS,
        BACKUP
    ):
        d.mkdir(
            parents=True,
            exist_ok=True
        )


def backup():
    for src in (
        CONFIG,
        COLORS,
        FONT,
        PROPS
    ):
        if src.exists():
            dst = BACKUP / src.name

            if not dst.exists():
                shutil.copy2(
                    src,
                    dst
                )


def write_colors(theme):
    bg = theme[3]
    fg = theme[4]
    pal = theme[5]

    text = (
        f"background={bg}\n"
        f"foreground={fg}\n"
        f"cursor={fg}\n"
    )

    for i, color in enumerate(pal):
        text += (
            f"color{i}={color}\n"
        )

    COLORS.write_text(text)


def write_prompt(theme):
    pal = theme[5]

    c1 = pal[1]
    c2 = pal[2]
    c3 = pal[3]
    c5 = pal[5]
    c6 = pal[6]

    text = f'''function fish_prompt
    set_color {c6}
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

    PROMPT.write_text(text)


def protect_config():
    CONFIG.touch()

    marker = "# ELMY0711 THEME"
    source = (
        "source "
        "~/.config/fish/"
        "ELMY0711-prompt.fish"
    )

    text = CONFIG.read_text()

    if source not in text:
        if text and not text.endswith("\n"):
            text += "\n"

        text += (
            "\n"
            + marker
            + "\n"
            + source
            + "\n"
        )

        CONFIG.write_text(text)


def write_keyboard():
    text = '''extra-keys=[["bash ","python3 ","nano ","go run ","UP","END","PGUP","node "],["tema","CTRL","BKSP","LEFT","DOWN","RIGHT","git clone ","curl -i "],["ls ","cd ","clear ","ENTER","ping ","git pull ","rm -rf ",{"macro":"CTRL d","display":"exit"}]]
'''

    PROPS.write_text(text)


def write_command():
    script = f'''#!{PREFIX}/bin/bash
exec {PREFIX}/bin/python3 "$HOME/termux-theme.py" "$@"
'''

    TEMA.write_text(script)
    TEMA.chmod(0o755)


def install_fish():
    if shutil.which("fish"):
        return True

    pkg = PREFIX / "bin" / "pkg"

    if not pkg.exists():
        return False

    print("Install Fish...")

    subprocess.run(
        [
            str(pkg),
            "install",
            "fish",
            "-y"
        ],
        check=False
    )

    return shutil.which("fish") is not None


def extract(archive, directory):
    with tarfile.open(
        archive,
        "r:xz"
    ) as tar:
        tar.extractall(
            directory
        )


def install_victor():
    d = FONTS / "VictorMono"

    d.mkdir(
        parents=True,
        exist_ok=True
    )

    url = (
        "https://github.com/ryanoasis/"
        "nerd-fonts/releases/latest/download/"
        "VictorMono.tar.xz"
    )

    arc = d / "VictorMono.tar.xz"

    out = d / (
        "VictorMonoNerdFontMono-Italic.ttf"
    )

    if not out.exists():
        print(
            "Download Victor Mono..."
        )

        try:
            urllib.request.urlretrieve(
                url,
                arc
            )

            extract(
                arc,
                d
            )

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
        for f in d.rglob("*.ttf"):
            n = f.name.lower()

            if (
                "victormono" in n
                and "italic" in n
                and "mono" in n
                and "propo" not in n
            ):
                out = f
                break

    if not out.exists():
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


def install_font(name):
    if name == "VictorMono":
        return install_victor()

    archive_name, path = FONT_FILES[name]

    d = FONTS / name

    d.mkdir(
        parents=True,
        exist_ok=True
    )

    archive = d / archive_name
    target = d / Path(path).name

    if not target.exists():
        print(
            "Download",
            name + "..."
        )

        try:
            urllib.request.urlretrieve(
                NF + archive_name,
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

    if not target.exists():
        print(
            "! File font tidak ditemukan:",
            path
        )

        return False

    shutil.copy2(
        target,
        FONT
    )

    print(
        "✓ Font:",
        target.name
    )

    return True


def reload_termux():
    cmd = PREFIX / (
        "bin/termux-reload-settings"
    )

    if cmd.exists():
        subprocess.run(
            [str(cmd)],
            check=False
        )


def apply_theme(number):
    theme = THEMES[number]

    print()
    print("Tema :", theme[0])
    print("Font :", theme[1])
    print("Style:", theme[2])

    backup()

    write_colors(theme)
    write_prompt(theme)
    protect_config()
    write_keyboard()
    write_command()

    ok = install_font(
        theme[1]
    )

    if ok:
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

        print(
            "╭── ELMY0711 THEME ──╮"
        )

        for n, theme in THEMES.items():
            print(
                f"│ {n:>2}. "
                f"{theme[0]:<15} │"
            )

        print(
            "│ Q. keluar           │"
        )

        print(
            "╰─────────────────────╯"
        )

        try:
            choice = input(
                "Pilih: "
            ).strip().lower()

        except KeyboardInterrupt:
            print()
            return

        if choice in THEMES:
            apply_theme(choice)

            try:
                input("\nENTER...")

            except KeyboardInterrupt:
                pass

        elif choice == "q":
            return


def install():
    print()
    print(
        "╭─────────────────────╮"
    )
    print(
        "│ ELMY0711 THEME      │"
    )
    print(
        "│ INSTALLER           │"
    )
    print(
        "╰─────────────────────╯"
    )
    print()

    setup()
    backup()

    if not install_fish():
        print(
            "! Fish tidak tersedia"
        )

    write_command()

    if not THEME_SCRIPT.exists():
        try:
            source = Path(
                __file__
            ).read_text()

            THEME_SCRIPT.write_text(
                source
            )

        except Exception:
            pass

    apply_theme("1")

    print()
    print(
        "✓ ~/termux-theme.py dibuat"
    )
    print(
        "✓ Installer selesai"
    )
    print()
    print(
        "Restart Fish:"
    )
    print(
        "  exec fish"
    )
    print()
    print(
        "Pengaturan tema:"
    )
    print(
        "  tema"
    )
    print()


def main():
    setup()

    if not THEME_SCRIPT.exists():
        install()
    else:
        menu()


if __name__ == "__main__":
    main()
