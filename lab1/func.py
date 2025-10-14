# Замыкания
print("====Closure====")
def closure(num: int):
    n = num
    def getN():
        return n

    return getN

func = closure(5)
print(func())


print("====Counter====")
def count():
    counter = 0

    def inc():
        nonlocal counter
        counter += 1
        return counter
    return inc

func = count()
for i in range(1,5):
    func()
print(func())

print("====List====")
def getFirstElem(list):
    l = list
    def _get_first():
        return l[0]
    return _get_first

list = ['apple', 'samsung', 'banana']
print(getFirstElem(list)())

print("====Lambda====")
def call(func):
    return lambda x: func(x)

to_str = call(str)
print(to_str(1110))