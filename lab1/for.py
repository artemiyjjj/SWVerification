
for i in range(0,5):
    print(i + " level")

for i in range(10, 20):
    for k in range(1,2):
        if k%2==0:
            break
        print(i + " " + k + "not broken")


for i in range(1, 10):
    pass

try:
    for i in range(5,10):
        if i == 7:
            raise StopIteration
except StopIteration:
    pass

for i in range(9, 15):
    print("if")
else:
    print("else")


def forloop():
    for i in range(10, 20):
        print(i)
        if i % 3 == 0:
            return

forloop()
