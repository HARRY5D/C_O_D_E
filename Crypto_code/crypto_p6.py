"""
1️⃣ Why RSA is used for key distribution instead of sending AES key directly?

Ans:
AES key sent in plaintext can be intercepted by attackers.
RSA encrypts the AES key using receiver’s public key.
Only the receiver can decrypt it using their private key.
Thus the secret key remains secure during transmission.

2️⃣ How hybrid cryptography improves security & performance?

Ans:
RSA is secure but slow for large data.
AES is fast but needs secure key exchange.

Hybrid approach uses:
RSA → secure key distribution
AES → fast data encryption
Gives both security and efficiency.

"""


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# ===== Step 1: Generate RSA keys for Alice & Bob =====
alice_key = RSA.generate(2048)
alice_public = alice_key.publickey()

bob_key = RSA.generate(2048)
bob_public = bob_key.publickey()

# ===== Step 2: Key Distribution Server generates AES-256 key =====
aes_key = get_random_bytes(32)   # 256-bit key
print("Generated AES Key:", aes_key.hex())

# ===== Step 3: Encrypt AES key using Bob's RSA public key =====
rsa_cipher = PKCS1_OAEP.new(bob_public)
encrypted_key = rsa_cipher.encrypt(aes_key)
print("\nEncrypted AES Key sent to Bob.")

# ===== Step 4: Bob decrypts AES key =====
rsa_decipher = PKCS1_OAEP.new(bob_key)
bob_aes_key = rsa_decipher.decrypt(encrypted_key)
print("Bob received AES key:", bob_aes_key.hex())

# ===== Step 5: Encrypt message using AES =====
message = b"Hello Bob Secure Message"

cipher_aes = AES.new(bob_aes_key, AES.MODE_CBC)
ciphertext = cipher_aes.encrypt(pad(message, AES.block_size))

print("\nEncrypted Message:", ciphertext.hex())

# ===== Step 6: Bob decrypts message =====
decipher = AES.new(bob_aes_key, AES.MODE_CBC, cipher_aes.iv)
plaintext = unpad(decipher.decrypt(ciphertext), AES.block_size)

print("Decrypted Message:", plaintext.decode())

