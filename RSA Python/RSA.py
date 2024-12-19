import tkinter as tk
from tkinter import messagebox
from sympy import isprime, gcd, mod_inverse

# Hàm tính toán khóa RSA
def generate_keys(p, q):
    if not isprime(p):
        raise ValueError(f"p = {p} không phải là số nguyên tố.")
    if not isprime(q):
        raise ValueError(f"q = {q} không phải là số nguyên tố.")

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Tự động chọn e
    e = 2
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            break
        e += 1

    # Tính d
    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)

# Hàm mã hóa
def encrypt(message, e, n):
    return pow(message, e, n)

# Hàm giải mã
def decrypt(ciphertext, d, n):
    return pow(ciphertext, d, n)

# Hàm xử lý khi nhấn nút "Tạo khóa"
def generate_keys_handler():
    try:
        # Lấy giá trị p và q từ giao diện
        p = int(p_entry.get())
        q = int(q_entry.get())

        # Tạo khóa
        public_key, private_key = generate_keys(p, q)

        # Hiển thị kết quả
        public_key_var.set(f"Khóa công khai: {public_key}")
        private_key_var.set(f"Khóa bí mật: {private_key}")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xử lý khi nhấn nút "Mã hóa"
def encrypt_handler():
    try:
        # Lấy thông tin từ giao diện
        message = int(message_entry.get())
        e, n = eval(public_key_var.get().split(": ")[1])

        # Mã hóa
        ciphertext = encrypt(message, e, n)
        encrypted_var.set(f"Bản mã: {ciphertext}")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Hàm xử lý khi nhấn nút "Giải mã"
def decrypt_handler():
    try:
        # Lấy thông tin từ giao diện
        ciphertext = int(ciphertext_entry.get())
        d, n = eval(private_key_var.get().split(": ")[1])

        # Giải mã
        decrypted_message = decrypt(ciphertext, d, n)
        decrypted_var.set(f"Thông điệp giải mã: {decrypted_message}")

    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

# Tạo giao diện
root = tk.Tk()
root.title("RSA Key Generation, Encryption, and Decryption")

# Nhập p và q
tk.Label(root, text="Nhập p:").pack()
p_entry = tk.Entry(root)
p_entry.pack()

tk.Label(root, text="Nhập q:").pack()
q_entry = tk.Entry(root)
q_entry.pack()

# Nút tạo khóa
generate_button = tk.Button(root, text="Tạo khóa", command=generate_keys_handler, bg="#007bff", fg="white")
generate_button.pack(pady=10)

# Hiển thị khóa
public_key_var = tk.StringVar()
tk.Label(root, textvariable=public_key_var).pack()

private_key_var = tk.StringVar()
tk.Label(root, textvariable=private_key_var).pack()

# Nhập thông điệp để mã hóa
tk.Label(root, text="Nhập thông điệp (số nguyên):").pack()
message_entry = tk.Entry(root)
message_entry.pack()

# Nút mã hóa
encrypt_button = tk.Button(root, text="Mã hóa", command=encrypt_handler, bg="#007bff", fg="white")
encrypt_button.pack(pady=10)

# Hiển thị bản mã
encrypted_var = tk.StringVar()
tk.Label(root, textvariable=encrypted_var).pack()

# Nhập bản mã để giải mã
tk.Label(root, text="Nhập bản mã (số nguyên):").pack()
ciphertext_entry = tk.Entry(root)
ciphertext_entry.pack()

# Nút giải mã
decrypt_button = tk.Button(root, text="Giải mã", command=decrypt_handler, bg="#28a745", fg="white")
decrypt_button.pack(pady=10)

# Hiển thị thông điệp giải mã
decrypted_var = tk.StringVar()
tk.Label(root, textvariable=decrypted_var).pack()

# Chạy ứng dụng
root.mainloop() 