import secrets

def random_key(n=8):
    return secrets.token_hex(n)
    
def key_hash(key, modulo, level=0):
    if isinstance(key, str):
        key = key.encode("utf-8")
    h = int.from_bytes(sha1(key))
    return (h >> level) % modulo
    
def to_str(x):
    if isinstance(x, memoryview):
        x = bytes(x)
    if isinstance(x, bytes):
        x = x.decode("utf-8")
    assert isinstance(x, str)
    return x
    
def to_bytes(x):
    if isinstance(x, str):
        x = x.encode("utf-8")
    assert isinstance(x, bytes)
    return x

