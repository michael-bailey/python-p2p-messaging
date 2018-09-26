#!/usr/bin/env python3

import sys

try:
    limit = int(sys.argv[1])
except:
    limit = int(input("enter a limit fo number of primes"))

prime = [True] * limit
prime[0] = prime[1] = False

file = open("primes.txt", "w")

for (i, isPrime) in enumerate(prime):
    if isPrime:
        print(i)
        file.write(str(i) + "\n")
        file.flush()
        for j in range(i*i, limit, i):
            prime[j] = False
            
file.close()
"""
for i in range(1,len(prime)-1):
    print
"""

