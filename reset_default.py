import os
import subprocess

HOME = os.path.expanduser("~")

PATHS = {
    "colors": f"{HOME}/.termux/colors.properties",
    "font": f"{HOME}/.termux/font.ttf", 
    "keyboard": f"{HOME}/.termux/termux.properties",
    "font_cache": f"{HOME}/.termux/font_cache",
    "zshrc": f"{HOME}/.zshrc",
    "bashrc": f"{HOME}/.bashrc"
}

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("="*40)
    print(" RESET TERMUX KE DEFAULT")
    print("="*40)

    # 1. Hapus warna custom
    print("[1/4] Hapus tema warna...")
    if os.path.exists(PATHS["colors"]): 
        os.remove(PATHS["colors"])
    
    # 2. Hapus font custom
    print("[2/4] Hapus font custom...")
    if os.path.exists(PATHS["font"]): 
        os.remove(PATHS["font"])
    if os.path.exists(PATHS["font_cache"]): 
        run(f"rm -rf {PATHS['font_cache']}")

    # 3. Hapus keyboard custom
    print("[3/4] Reset keyboard...")
    if os.path.exists(PATHS["keyboard"]): 
        os.remove(PATHS["keyboard"])

    # 4. Reset prompt zsh/bash ke default
    print("[4/4] Reset prompt...")
    for rc in [PATHS["zshrc"], PATHS["bashrc"]]:
        if os.path.exists(rc):
            # hapus banner & alias tema
            run(f"sed -i '/PROMPT CUSTOM ELMY0711/,+5d' {rc} 2>/dev/null")
            run(f"sed -i '/ALIAS TEMA TERMUX/,+6d' {rc} 2>/dev/null")
            run(f"sed -i '/cowsay/d; /figlet/d; /lolcat/d; /neofetch/d' {rc} 2>/dev/null")
            # set prompt default
            with open(rc, 'a') as f:
                f.write('\nPROMPT="%F{green}%n@%m%f %F{blue}%~%f %# "\n')

    print("\n" + "="*40)
    print(" SELESAI!")
    print(" 1. Force close Termux")
    print(" 2. Buka lagi")
    print(" Termux udah balik default")
    print("="*40)

if __name__ == "__main__":
    input("Tekan Enter untuk reset ke default... ")
    main()
