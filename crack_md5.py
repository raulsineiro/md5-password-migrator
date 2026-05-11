import hashlib
import os

# Indicamos tanto los archivos que necesitamos para el funcionamiento del script como los archivos salientes
PASSWORDS_FILE = "PASSWORDS.md"
WORDLIST_FILE  = "rockyou.txt"
PLAIN_FILE     = "plain.txt"
NEW_PASS_FILE  = "new_passwords.txt"
# ───────────────────────────────────────────────────────────

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def sha256_con_sal(password):
    sal = os.urandom(16).hex()          # sal aleatoria de 16 bytes
    hash_ = hashlib.sha256((sal + password).encode()).hexdigest()
    return f"{sal}:{hash_}"

# Cargamos los hashes MD5
with open(PASSWORDS_FILE, "r") as f:
    hashes = [line.strip() for line in f if line.strip()]

print(f"[*] {len(hashes)} hashes cargados")

# Intentamos revertirlos con rockyou.txt
revertidos = {}  # hash -> contraseña en plano

with open(WORDLIST_FILE, "r", encoding="latin-1") as f:
    for i, linea in enumerate(f):
        if i % 1_000_000 == 0:
            print(f"[*] {i:,} palabras probadas, {len(revertidos)} hashes revertidos...")

        palabra = linea.strip()
        h = md5(palabra)
        if h in set(hashes) and h not in revertidos:
            revertidos[h] = palabra
            print(f"[+] Encontrado: {h} → {palabra}")

        # Parar si ya revertimos todos
        if len(revertidos) == len(set(hashes)):
            break

print(f"\n[✓] Total revertidos: {len(revertidos)} de {len(set(hashes))} hashes únicos")

# Generamos los archivos plain.txt y new_passwords.txt
with open(PLAIN_FILE, "w") as f_plain, open(NEW_PASS_FILE, "w") as f_new:
    for hash_ in hashes:
        if hash_ in revertidos:
            plain = revertidos[hash_]
            f_plain.write(plain + "\n")
            f_new.write(sha256_con_sal(plain) + "\n")
        else:
            f_plain.write("\n")
            f_new.write("\n")

print(f"[✓] plain.txt y new_passwords.txt generados")