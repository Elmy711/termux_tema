import os

HOME = os.path.expanduser("~")
FISH_CONFIG_PATH = f"{HOME}/.config/fish/config.fish"


def strip_function_block(lines, func_name):
    """Buang blok 'function <func_name> ... end' di manapun ditemukan,
    termasuk sisa dari versi script lama yang formatnya beda."""
    result = []
    i = 0
    n = len(lines)
    while i < n:
        if lines[i].strip() == f"function {func_name}":
            i += 1
            while i < n and lines[i].strip() != "end":
                i += 1
            i += 1  # lewati baris "end"-nya juga
            continue
        result.append(lines[i])
        i += 1
    return result


def purge_managed_fish_content(lines):
    """Bersihin semua jejak konfigurasi ELMY0711 (versi lama maupun baru)."""
    lines = strip_function_block(lines, "fish_prompt")
    lines = strip_function_block(lines, "fish_right_prompt")
    cleaned = []
    for line in lines:
        s = line.strip()
        if s.startswith("#") and ("ELMY0711" in s or "TEMA TERMUX" in s):
            continue
        if s.startswith("alias tema=") or s.startswith("alias t=") or s.startswith("alias reload="):
            continue
        cleaned.append(line)
    return cleaned


def main():
    if not os.path.exists(FISH_CONFIG_PATH):
        print(f"Gak ada file di {FISH_CONFIG_PATH}, gak ada yg perlu dibersihin.")
        return

    with open(FISH_CONFIG_PATH, "r") as f:
        lines = f.readlines()

    print(f"Baris sebelum dibersihin: {len(lines)}")

    cleaned = purge_managed_fish_content(lines)
    while cleaned and cleaned[-1].strip() == "":
        cleaned.pop()

    with open(FISH_CONFIG_PATH, "w") as f:
        f.writelines(cleaned)
        if cleaned:
            f.write("\n")

    print(f"Baris sesudah dibersihin: {len(cleaned)}")
    print(f"Selesai. {FISH_CONFIG_PATH} sekarang bersih dari sisa konfigurasi lama.")
    print("Jalankan tema7.py lagi buat nulis ulang prompt & alias yang baru.")


if __name__ == "__main__":
    main()
