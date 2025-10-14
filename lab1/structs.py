# common
myarr = [1,2,3]

# generators
genarr = [i for i in range(1, 4)]
print(genarr)


iterator = (i for i in myarr)
for i in iterator:
    print(i)


def generator(list):
    for i in list:
        yield i

gen = generator(myarr)
for i in gen:
    print(i)


def genPlusClosure():
    list = [i for i in range(1, 8)]
    def getNext():
        for i in list:
            yield i

for i in genPlusClosure():
    print(i)

