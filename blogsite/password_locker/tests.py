from django.test import TestCase
from password_locker.utils import *


# Create your tests here.
p="abc@#012981~!"
g = generate_symmetric_key()
print(g)

s = encrypt_data(p,g)
print(s)
f = decrypt_data(s,g)
print(f)
print(f==p)