import os
import subprocess

HOME = os.path.expanduser("~")
ZSHRC_PATH = f"{HOME}/.zshrc"
COLORS_PATH = f"{HOME}/.termux/colors.properties"
FONT_PATH = f"{HOME}/.termux/font.ttf"
TERMUX_PROPS = f"{HOME}/.termux/termux.properties"
FONT_CACHE = f"{HOME}/.termux/font_cache"

def run(cmd):
    print(f"[!] {cmd}")
    subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    print("="*50)
    print(" CLEANUP TEMA TERMUX")
    print("="*50)

    # 1. HAPUS COLORS + FONT
    print("\n[1/5] Hapus colors dan font...")
    if os.path.exists(COLORS_PATH): os.remove(COLORS_PATH)
    if os.path.exists(FONT_PATH): os.remove(FONT_PATH)
    if os.path.exists(FONT_CACHE): run(f"rm -rf {FONT_CACHE}")

    # 2. HAPUS KEYBOARD CUSTOM
    print("[2/5] Reset keyboard ke default...")
    if os.path.exists(TERMUX_PROPS): os.remove(TERMUX_PROPS)

    # 3. HAPUS PROMPT + ALIAS LAMA DI ZSHRC
    print("[3/5] Bersihin .zshrc...")
    run("sed -i '/PROMPT CUSTOM ELMY0711/,+5d' ~/.zshrc 2>/dev/null")
    run("sed -i '/ALIAS TEMA TERMUX/,+6d' ~/.zshrc 2>/dev/null")
    
    # Balikin prompt default zsh
    run("echo 'PROMPT=\"%F{green}%n@%m%f %F{blue}%~%f %# \"' >> ~/.zshrc")

    # 4. HAPUS FOLDER TEMA
    print("[4/5] Hapus folder tema lama...")
    run("rm -rf ~/termux_tema")

    # 5. RELOAD ZSH
    print("[5/5] Reload zsh...")
    run("source ~/.zshrc")

    print("\n" + "="*50)
    print(" SELESAI! TERMUX SUDAH KEMBALI DEFAULT")
    print(" Force close Termux lalu buka lagi")
    print("="*50)

if __name__ == "__main__": 
    confirm = input("Yakin mau hapus semua tema & banner? [y/n]: ").lower()
    if confirm == 'y':
        main()
    else:
        print("Batal").
