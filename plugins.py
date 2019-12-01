import string
import random
import hashlib

def uuid(size = 32, chars = string.ascii_uppercase + string.digits ):
	return ''.join(random.choice(chars) for _ in range(size))

def encrypt_string(hash_string):
	sha_signature = hashlib.sha256(hash_string.encode()).hexdigest()
	return sha_signature