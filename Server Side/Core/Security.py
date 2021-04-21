import hashlib

def md5_hash(string):
    return hashlib.md5(string.encode()).hexdigest()