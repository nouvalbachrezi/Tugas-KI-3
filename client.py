import socket
#mengirimkan pesan terenkripsi ke server
def send_message(client_socket, public_key, n, message):
    # Diasumsikan pesan adalah plaintext (dalam sistem nyata, enkripsi diperlukan)
    message_encoded = [pow(ord(ch), public_key, n) for ch in message]
    encrypted_message = ','.join(map(str, message_encoded))

    print(f"Ciphertext: {message_encoded}")

    client_socket.send(encrypted_message.encode())
#menerima dari server menerima data sari socket
def receive_message(client_socket, private_key, n):
    data = client_socket.recv(1024)
    if not data:
        return None

    # Asumsikan data yang diterima adalah ciphertext//Mengubah data yang diterima (ciphertext) menjadi daftar bilangan bulat.
    ciphertext = [int(byte) for byte in data.decode().split(',')]
    print(f"Ciphertext received from server: {ciphertext}")

    # Lakukan dekripsi
    decrypted_message = ''.join(chr(pow(ch, private_key, n)) for ch in ciphertext)
    print(f"Decrypted message from server: {decrypted_message}")

    return decrypted_message
#fugsi utama
#Membuat soket klien dan menghubungkannya ke alamat dan port tertentu (localhost:12345).

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 12345))

    # Terima kunci publik dari server
    public_key_data = client.recv(1024).decode().split(',')
    public_key = int(public_key_data[0])
    n = int(public_key_data[1])

    print(f"Received Public Key (e, n): ({public_key}, {n})")

    while True:
        #meneriam input
        message = input("Enter message to send (type 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        send_message(client, public_key, n, message)

        # Menerima balasan dari server
        received_message = receive_message(client, public_key, n)
        if received_message:
            print(f"Received message from server: {received_message}")

    client.close()

if __name__ == "__main__":
    start_client()

#catatan
#E_e (c)=m=c^(e ) mod n
#D_d (c)=m=c^(d ) mod n
#https://www.youtube.com/watch?v=2L-BzX1_i4o&t=559s