primes = [2]

limit = int(input("enter a limit fo number of primes"))

for i in range(limit):
    if i < 2:
        pass
    else:
        for j in primes:
            if i % j == 0:
                # found prime 
                primes.append(i)
                break

print(primes)