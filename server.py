import socket
from threading import Thread
import random
import math

#memeriksa apakah bilang prima
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, number // 2 + 1):
        if number % i == 0:
            return False
    return True

# menghasilkan bilangan prima acak dalam rentang tertentu    
def generate_prime(min_value, max_value):
    prime = random.randint(min_value, max_value)
    while not is_prime(prime):#Menggunakan fungsi is_prime untuk memeriksa apakah bilangan yang dihasilkan sudah merupakan bilangan prima atau tidak.
        prime = random.randint(min_value, max_value)
    return prime #jika tidak mengulang

#Fungsi ini menghitung invers modulo dari e dalam modulus phi
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d
    raise ValueError("mod_inverse does not exist")

#Fungsi ini menangani komunikasi dengan klien.
def handle_client(client_socket, private_key, n):
    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Asumsikan data yang diterima adalah ciphertext
        ciphertext = [int(byte) for byte in data.decode().split(',')]
        print(f"Ciphertext received from client: {ciphertext}")

        # Lakukan dekripsi
        decrypted_message = ''.join(chr(pow(ch, private_key, n)) for ch in ciphertext)
        print(f"Decrypted message: {decrypted_message}")

        # Balas pesan ke klien
        reply_message = input("Enter reply to send (type 'exit' to quit): ")
        if reply_message.lower() == 'exit':
            break

        send_message(client_socket, private_key, n, reply_message)

#Fungsi ini mengirim pesan terenkripsi ke klien.
def send_message(client_socket, private_key, n, message):
    # Diasumsikan pesan adalah plaintext (dalam sistem nyata, enkripsi diperlukan)
    #Mencetak pesan terenkripsi (dalam bentuk daftar bilangan bulat).
    message_encoded = [pow(ord(ch), private_key, n) for ch in message]
    encrypted_message = ','.join(map(str, message_encoded))

    print(f"Ciphertext: {message_encoded}")

    client_socket.send(encrypted_message.encode())

#Fungsi ini merupakan fungsi utama untuk menjalankan server.
def start_server():
   # Membuat soket server dan mendengarkan koneksi pada port 12345.
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 12345))
    server.listen(5)

    print("Server listening on port 12345...")
# enghasilkan dua bilangan prima acak, p dan q, dan menghitung modulus n dan totien phi_n.
    p, q = generate_prime(1000, 5000), generate_prime(1000, 5000)
    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(3, phi_n - 1)
    while math.gcd(e, phi_n) != 1:
        e = random.randint(3, phi_n - 1)

    d = mod_inverse(e, phi_n)

    print(f"Public Key (e, n): ({e}, {n})")

    while True:
        #Menerima koneksi dari klien, mengirimkan kunci publik ke klien, dan memulai thread baru untuk menangani komunikasi dengan klien.

        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")

        # Kirim kunci publik ke klien
        client_socket.send(f"{e},{n}".encode())

        # Mulai thread baru untuk menangani pesan klien
        client_thread = Thread(target=handle_client, args=(client_socket, d, n))
        client_thread.start()

if __name__ == "__main__":
    start_server()


#Angka 3 dipilih sebagai nilai minimum untuk e karena nilai e haruslah bilangan bulat positif yang relatif prima 