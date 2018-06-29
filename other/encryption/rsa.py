#import sys


def generate_keys(prime1, prime2, prime3):

    #n is the public key
    n = prime1 * prime2
    totient = (prime1-1)*(prime2-1)
    e = 0
    d = 0
    #generating public exponent
    for i in range(1,totient):
        if totient / i == 1:
            e = i
            break

    for i in range(0,n):
        if ((i * e) % totient) == (1 % totient):
            d = i
            break

    print(n)
    print(e)
    print(d)
    return n, e, d


#mulinv(e, totient)
"""
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a,
        return (g, y - (b // a) * x, x)
    
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n
"""
def encrypt(message, exponent_e, key):
    return str(chr(ord(message)**public%key))

def decrypt(message, exponent_d, key):
    return str(chr(ord(message)**private%key))

public, key2, private = generate_keys(61,53,17)

message = input("enter message")
