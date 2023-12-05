from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# print(key)
# # Load the secret key securely
# SECRET_KEY = Fernet.generate_key()
# print(SECRET_KEY)

# # Create an instance of the Fernet cipher
# cipher_suite = Fernet(SECRET_KEY)
# print(cipher_suite)

def fernet_encrypt_data(key,data):
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data.encode())
    return encrypted_data

def fernet_decrypt_data(key,encrypted_data):
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data).decode()
    return decrypted_data

