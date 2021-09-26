import random

x = [1, 2, 3, 4, 5]

def func():
    a = random.sample(x, 3)
    return a

a = func()

a[0] = 5

print(a)
print(x)