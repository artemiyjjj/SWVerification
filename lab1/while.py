a = True
b = 0

while a:
    b += 1
    if b != 10:
        continue
    else:
        a = False
else:
    print("Normal termination")

while not a:
    b -= 1
    if b == 0:
        break
else:
    print("Not normal execution")