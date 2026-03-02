import hashlib
import random

p = 23        
g = 6         

# Private keys (secret)
bob_private = random.randint(1,10)
alice_private = random.randint(1,10)

# Public keys
bob_public = pow(g, bob_private, p)
alice_public = pow(g, alice_private, p)

# Shared secret computation
bob_secret = pow(alice_public, bob_private, p)
alice_secret = pow(bob_public, alice_private, p)

print("Bob Secret:", bob_secret)
print("Alice Secret:", alice_secret)

# Message
M = "Hello Alice"

# Bob computes hash
data = M + str(bob_secret)
bob_hash = hashlib.sha256(data.encode()).hexdigest()

print("Bob Hash:", bob_hash)

# Alice verifies hash
verify_data = M + str(alice_secret)
alice_hash = hashlib.sha256(verify_data.encode()).hexdigest()

print("Alice Hash:", alice_hash)

if bob_hash == alice_hash:
    print("Message Verified ")
else:
    print("Message Altered ")