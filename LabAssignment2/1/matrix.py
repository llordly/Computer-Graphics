import numpy as np

# A
a = np.arange(2, 27)
print(a)

# B
M = a.reshape(5, 5)
print(M)

# C
M[1:4, 1:4] = np.zeros_like(M[1:4, 1:4])
print(M)

# D
M = M @ M
print(M)

# E
v = M[0, :]
print(np.sqrt(sum(v ** 2)))