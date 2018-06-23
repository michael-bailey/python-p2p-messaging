def generate_keys(prime1, prime2, prime3):
    public_key_n = prime1 * prime2
    phi = (prime1-1)*(prime2-1)
    if prime3 >= phi :
        print("third number wont work")
        return
    public_key_e = prime3
    private_key_d = mulinv(public_key_e, phi)
    print(public_key_n)
    print(public_key_e)
    print(private_key_d)
    return public_key_n public_key_e private_key_d

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
    
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def encrypt(message, public_expo, public_mod):
    return message**public_expo%public_mod

def decrypt(c, d, n):
    return c**d%n


a, b, c = generate_keys(2, 5, 3)

encrypt
