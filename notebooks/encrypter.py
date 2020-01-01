# %pip install pycryptodome
from Crypto import Random
from Crypto.Cipher import AES
import ipywidgets as widgets
from IPython.display import display
import base64

encryptionKey = widgets.Password(description="Password:")

textToEncrypt = widgets.Text(description="Encrypt:")
doEncrypt = widgets.Button(description="Do Encryption")
encryptedOutput = widgets.Output()

#textToDecrypt = widgets.Text(description="Decrypt:")
#doDecrypt = widgets.Button(description="Do Decryption")
#decryptedOutput = widgets.Output()

def pad(s):
    return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

def expandKey(s, newSize):
    return (s*(int(newSize/len(s))+1))[0:newSize]

def encrypt(message, key, key_size=32):
    xkey = expandKey(key, key_size).encode('utf-8')
    bmessage = pad(message.encode('utf-8'))
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(xkey, AES.MODE_CBC, iv)
    encrypted = iv + cipher.encrypt(bmessage)
    return base64.encodebytes(encrypted).decode('utf-8').rstrip()

def decrypt(ciphertext, key = "usePassword", key_size=32):
    if key is "usePassword":
        key = encryptionKey.value
    xkey = expandKey(key, key_size).encode('utf-8')
    ciphertext = base64.decodebytes(ciphertext.encode('utf-8'))
    iv = ciphertext[:AES.block_size]
    cipher = AES.new(xkey, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext[AES.block_size:])
    return plaintext.rstrip(b"\0").decode('utf-8')

def on_encrypt_clicked(b):
    with encryptedOutput:
        print( "Replace string '{}' in your notebook with the below:\n decrypt('{}')\n".format(textToEncrypt.value,encrypt(message = textToEncrypt.value, key = encryptionKey.value) ))

def on_decrypt_clicked(b):
    with decryptedOutput:
        print(decrypt(ciphertext = textToDecrypt.value, key = encryptionKey.value))

doEncrypt.on_click(on_encrypt_clicked)
#doDecrypt.on_click(on_decrypt_clicked)

display(encryptionKey)
display(textToEncrypt)
display(doEncrypt, encryptedOutput)
#display(textToDecrypt)
#display(doDecrypt, decryptedOutput)