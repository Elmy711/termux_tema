#!/data/data/com.termux/files/usr/bin/bash

echo "[+] Mulai bersihin Termux..."
sleep 1

# 1. Hapus semua file banner & login
rm -f ~/.termux-banner.txt 
rm -f ~/.termux-os-banner.sh
rm -f ~/login.sh 
rm -f ~/termux-login
rm -rf ~/.local/share/blesh

# 2. Bersihin .bashrc
sed -i '/banner/d' ~/.bashrc
sed -i '/login.sh/d' ~/.bashrc
sed -i '/password/d' ~/.bashrc
sed -i '/cat ~/.termux/d' ~/.bashrc
sed -i '/ble.sh/d' ~/.bashrc
sed -i '/neofetch/d' ~/.bashrc

# 3. Bersihin .zshrc
sed -i '/banner/d' ~/.zshrc
sed -i '/login.sh/d' ~/.zshrc
sed -i '/password/d' ~/.zshrc
sed -i '/cat ~/.termux/d' ~/.zshrc
sed -i '/ble.sh/d' ~/.zshrc
sed -i '/neofetch/d' ~/.zshrc

# 4. Tambahin prompt cantik + tanggal
cat >> ~/.bashrc << 'EOB'

# Prompt cantik polos
PS1='\[\e[0;90m\]\d \t\[\e[0m\]\n\[\e[1;32m\]┌─[\u@termux]\[\e[0m\]─[\[\e[1;34m\]\w\[\e[0m\]]\n\[\e[1;32m\]└─╼\[\e[0m\] ❯ '
EOB

# 5. Reload config
source ~/.bashrc

echo "[+] Selesai!"
echo "[+] Tutup dan buka ulang Termux buat cek"
