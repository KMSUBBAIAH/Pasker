from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=7680,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def serialize_private_key(private_key):
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

def serialize_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

def deserialize_private_key(serialized_key):
    return serialization.load_pem_private_key(
        serialized_key,
        password=None,
        backend=default_backend()
    )

def deserialize_public_key(serialized_key):
    return serialization.load_pem_public_key(serialized_key, backend=default_backend())

def rsa_encrypt_data(data, public_key):
    encoded_data = base64.b64encode(data.encode()) 
    ciphertext = public_key.encrypt(
        encoded_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def rsa_decrypt_data(ciphertext, private_key):
    try:
        encoded_data = private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Unpad the data after decryption
        decoded_data = base64.b64decode(encoded_data)

        return decoded_data.decode()
    except ValueError as e:
        return None


import random
import string

def generate_secure_password():
    length = 32  # You can adjust the length as needed
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    punctuation = string.punctuation
    each = int(length/4)
    password = []
    # Fill the remaining characters randomly
    password.extend([random.choice(lowercase_letters) for _ in range(each)])
    password.extend([random.choice(uppercase_letters) for _ in range(each)])
    password.extend([random.choice(digits) for _ in range(each)])
    password.extend([random.choice(punctuation) for _ in range(each)])
    # Shuffle the password to mix the characters
    random.shuffle(password)
    return ''.join(password)
