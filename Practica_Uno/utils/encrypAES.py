# pip -m install pycryptodome
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def encode (key, text):
    cipher = AES.new(key, AES.MODE_CBC)
    text_bytes = cipher.encrypt(pad(text.encode(), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    text_encrypted = base64.b64encode(text_bytes).decode('utf-8')
    return iv, text_encrypted

def decode(key,iv,text_encrypted):
    iv_bytes=base64.b64decode(iv)
    text_encrypted_bytes = base64.b64decode(text_encrypted)
    cipher_decode = AES.new(key, AES.MODE_CBC, iv_bytes)
    text_bytes = unpad(cipher_decode.decrypt(text_encrypted_bytes), AES.block_size)
    return text_bytes.decode('utf-8')

def getKey(size):
    return get_random_bytes(size)

def saludar ():
    return "hello from encryp AES"