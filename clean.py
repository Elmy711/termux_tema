import os
import subprocess
import re

HOME = os.path.expanduser("~")
ZSHRC_PATH = f"{HOME}/.zshrc"
BASHRC_PATH = f"{HOME}/.bashrc"
COLORS_PATH = f"{HOME}/.termux/colors.properties"
FONT_PATH = f"{HOME}/.termux/font.ttf"
TERMUX_PROPS = f"{HOME}/.termux/termux.properties"
FONT_CACHE = f"{HOME}/.termux/font_cache"

def run(cmd):
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def clean_rc(path):
    if not os.path.exists(path): return
    print(f"[!] Bersihin {path}")
    with open(path, 'r') as f:
        lines = f.readlines()
    
    keywords = ['cowsay', 'figlet', 'lolcat', 'neofetch', 'banner', 'toilet', 'PROMPT CUSTOM', 'ALIAS TEMA', 'ELMY0711']
    new_lines = []
    for line in lines:
        if not any(k in line for k in keywords):
            new_lines.append(line)
    
    with open(path, 'w') as f:
        f.writelines(new_lines)
    
    # Kasih prompt default
    with open(path, 'a') as f:
        f.write('\nPROMPT="%F{green}%n@%m%f %F{blue}%~%f %# "\n')

def main():
    print("="*50)
    print(" CLEANUP FULL TERMUX - HAPUS SEMUA BANNER")
    print("="*50)

    print("\n[1/6] Hapus colors + font...")
    if os.path.exists(COLORS_PATH): os.remove(COLORS_PATH)
    if os.path.exists(FONT_PATH): os.remove(FONT_PATH)
    if os.path.exists(FONT_CACHE): run(f"rm -rf {FONT_CACHE}")

    print("[2/6] Reset keyboard ke default...")
    if os.path.exists(TERMUX_PROPS): os.remove(TERMUX_PROPS)

    print("[3/6] Bersihin .zshrc...")
    clean_rc(ZSHRC_PATH)

    print("[4/6] Bersihin .bashrc...")
    clean_rc(BASHRC_PATH)

    print("[5/6] Hapus folder tema umum...")
    run("rm -rf ~/termux_tema ~/tema-termux ~/termux-style")

    print("[6/6] Uninstall pkg banner populer...")
    run("pkg uninstall cowsay figlet lolcat toilet neofetch -y")

    print("\n" + "="*50)
    print(" SELESAI! Force close Termux lalu buka lagi")
    print("="*50)

if __name__ == "__main__": 
    confirm = input("Hapus SEMUA banner, tema, font, keyboard custom? [y/n]: ").lower()
    if confirm == 'y':
        main()
    else:
        print("Batal")
