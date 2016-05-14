from pympler import asizeof
import random
import resource

mem_usage = []
list_sizes = []

b = bytearray()

for i in range(0,4):
    for j in range(2,15):
        b.append(j<<2 | i)

min_piles = 52
max_piles = 0

for i in range(1,100000):
    l = []
    l.append(bytearray())
    index = 0
    for j in b:
        if random.random() > 0:
            # create new byte array and advance index
            l.append(bytearray())
            index += 1
        l[index].append(j)

    #print l
    list_sizes.append(asizeof.asizeof(l))
    mem_usage.append(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    max_piles = len(l) if len(l) > max_piles else max_piles
    min_piles = len(l) if len(l) < min_piles else min_piles


list_sizes.sort()
print list_sizes[0], list_sizes[-1]
print min_piles, max_piles
#print mem_usage