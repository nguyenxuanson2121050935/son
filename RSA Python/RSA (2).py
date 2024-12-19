from tkinter import Tk, Label, Entry, Button, Text, Scrollbar, filedialog, messagebox, StringVar, simpledialog
from sympy import isprime, gcd, mod_inverse
import os,random

# Tạo khóa RSA
def generate_keys(p, q):
    if not isprime(p) or not isprime(q):
        raise ValueError(" p hoặc q không phải là số nguyên tố.")
    n = p * q
    phi_n = (p - 1) * (q - 1)
    # Chọn e sao cho gcd(e, phi_n) = 1
    e = 2
    while e < phi_n:
        if gcd(e, phi_n) == 1:
            break
        e += 1
    d = mod_inverse(e, phi_n)  # Tính d
    return (e, n), (d, n)
def generate_random_prime():
    while True:
        num = random.randint(1000, 9999)  # Sinh số ngẫu nhiên trong khoảng từ 1000 đến 9999
        if isprime(num):  # Kiểm tra xem số này có phải là số nguyên tố không
            return num

# Hàm xử lý sự kiện khi nhấn nút "Random p, q"
def random_pq_handler():
    p = generate_random_prime()
    q = generate_random_prime()
    p_entry.delete(0, 'end')
    p_entry.insert(0, str(p))
    q_entry.delete(0, 'end')
    q_entry.insert(0, str(q))

# Chuyển đổi text sang danh sách byte
def text_to_bytes(text):
    return list(text.encode('utf-8'))

# Chuyển đổi byte về text
def bytes_to_text(byte_list):
    return bytes(byte_list).decode('utf-8')

# Mã hóa thông điệp
def encrypt(message, e, n):
    if n < 256:
        raise ValueError("Giá trị n quá nhỏ để mã hóa. Hãy chọn p, q lớn hơn.")
    byte_list = text_to_bytes(message)
    return [pow(byte, e, n) for byte in byte_list]

# Giải mã thông điệp
def decrypt(ciphertext, d, n):
    decrypted_bytes = [pow(byte, d, n) for byte in ciphertext]
    return bytes_to_text(decrypted_bytes)

# Đọc file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Ghi file mã hóa
def write_encrypted_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(' '.join(map(str, data)))

# Ghi file giải mã
def write_decrypted_file(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(data)

# Xử lý giao diện GUI
def generate_keys_handler():
    try:
        p = int(p_entry.get())
        q = int(q_entry.get())
        public_key, private_key = generate_keys(p, q)
        public_key_var.set(f"Khóa công khai: {public_key}")
        private_key_var.set(f"Khóa bí mật: {private_key}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
# Hàm xuất khóa vào file
def export_keys():
    try:
        public_key = public_key_var.get().split(": ")[1]
        private_key = private_key_var.get().split(": ")[1]

        # Đặt tên file xuất khóa
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            # Lưu khóa vào file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(f"Khóa công khai: {public_key}\n")
                file.write(f"Khóa bí mật: {private_key}\n")
            messagebox.showinfo("Thành công", f"Đã xuất khóa vào file: {file_path}")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def select_original_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.text")])
    if file_path:
        original_file_var.set(file_path)
        content = read_file(file_path)
        original_text.delete('1.0', 'end')
        original_text.insert('1.0', content)

def encrypt_file_handler():
    try:
        file_path = original_file_var.get()
        if not file_path or not os.path.exists(file_path):
            raise ValueError("Chưa chọn file gốc.")
        content = read_file(file_path)
        e, n = eval(public_key_var.get().split(": ")[1])
        encrypted_data = encrypt(content, e, n)
        encrypted_text.delete('1.0', 'end')
        encrypted_text.insert('1.0', " ".join(map(str, encrypted_data)))
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def save_encrypted_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        content = encrypted_text.get('1.0', 'end').strip()
        write_encrypted_file(file_path, map(int, content.split()))
        messagebox.showinfo("Thành công", f"Đã lưu file mã hóa: {file_path}")

def decrypt_file_handler():
    try:
        encrypted_content = encrypted_text.get('1.0', 'end').strip()
        if not encrypted_content:
            raise ValueError("Không có dữ liệu để giải mã.")
        ciphertext = list(map(int, encrypted_content.split()))
        d, n = eval(private_key_var.get().split(": ")[1])
        decrypted_data = decrypt(ciphertext, d, n)
        decrypted_text.delete('1.0', 'end')
        decrypted_text.insert('1.0', decrypted_data)
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))

def save_decrypted_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        content = decrypted_text.get('1.0', 'end').strip()
        write_decrypted_file(file_path, content)
        messagebox.showinfo("Thành công", f"Đã lưu file giải mã: {file_path}")
# Hàm nhập khóa
def input_key():
    try:
        # Mở cửa sổ nhập khóa
        key_input = simpledialog.askstring("Nhập khóa", "Nhập khóa bí mật:")
        if key_input:
            private_key_var.set(f"Khóa bí mật : ({key_input})")
    except Exception as e:
        messagebox.showerror("Lỗi", str(e))
# Hàm nhập file mã hóa
def select_encrypted_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            # Đọc nội dung file
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()
            # Hiển thị nội dung vào ô text
            encrypted_text.delete('1.0', 'end')
            encrypted_text.insert('1.0', content)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể đọc file mã hóa: {e}")

# GUI
root = Tk()
root.title(" Mã hóa/Giải mã RSA Nhóm 2 ")
root.geometry("650x700")

# Tạo khóa
Label(root, text="Nhập p:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
p_entry = Entry(root)
p_entry.grid(row=0, column=1, padx=5, pady=5)

Label(root, text="Nhập q:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
q_entry = Entry(root)
q_entry.grid(row=1, column=1, padx=5, pady=5)
# Thêm nút Xuất khóa

Button(root, text="Tạo khóa", command=generate_keys_handler, bg="#007bff", fg="white").grid(row=0, column=2, pady=5, padx=5)
Button(root, text="Xuất khóa", command=export_keys, bg="#6f42c1", fg="white").grid(row=1, column=2, padx=5, pady=5)
Button(root, text="Random p, q", command=random_pq_handler, bg="#28a745", fg="white").grid(row=2, column=2, padx=5, pady=5)
public_key_var = StringVar()
Label(root, textvariable=public_key_var).grid(row=2, column=0, columnspan=3, sticky="w", padx=5, pady=5)

private_key_var = StringVar()
Label(root, textvariable=private_key_var).grid(row=3, column=0, columnspan=3, sticky="w", padx=5, pady=5)

# Chọn file gốc
original_file_var = StringVar()
Button(root, text="Chọn file gốc", command=select_original_file, bg="#6c757d", fg="white").grid(row=4, column=0, columnspan=2, padx=5, pady=5)

Label(root, text="Nội dung file gốc:").grid(row=5, column=0, sticky="w", padx=5)
original_text = Text(root, height=5, wrap="word")
original_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Mã hóa
Button(root, text="Mã hóa", command=encrypt_file_handler, bg="#007bff", fg="white").grid(row=7, column=0, columnspan=2, padx=5, pady=5)
Button(root, text="Lưu file mã hóa", command=save_encrypted_file, bg="#28a745", fg="white").grid(row=7, column=2, padx=5, pady=5)
# Thêm nút Nhập file mã hóa

Label(root, text="Nội dung file mã hóa:").grid(row=8, column=0, sticky="w", padx=5)
encrypted_text = Text(root, height=5, wrap="word")
encrypted_text.grid(row=9, column=0, columnspan=3, padx=5, pady=5)

# Giải mã
# Xắp xếp lại các nút trong dòng 10
Button(root, text="Giải mã", command=decrypt_file_handler, bg="#ffc107", fg="black").grid(row=10, column=0, padx=5, pady=5, sticky="w")
Button(root, text="Nhập khóa", command=input_key, bg="#ffc107", fg="black").grid(row=10, column=1, padx=5, pady=5, sticky="w")
Button(root, text="Nhập file mã hóa", command=select_encrypted_file, bg="#ffc107", fg="black").grid(row=10, column=2, padx=5, pady=5, sticky="w")
Button(root, text="Lưu file giải mã", command=save_decrypted_file, bg="#17a2b8", fg="white").grid(row=11, column=1, padx=5, pady=5, sticky="w")

Label(root, text="Nội dung file giải mã:").grid(row=12, column=0, sticky="w", padx=5)
decrypted_text = Text(root, height=5, wrap="word")
decrypted_text.grid(row=13, column=0, columnspan=3, padx=5, pady=5)

root.mainloop()
