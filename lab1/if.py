if True and not True == False:
    print("True")
    3 + 2

a = "true"
b = False

if a and not b or not a and b or a or b:
    print("Also True")
    a = "bool"
elif not a:
    print("Also False")
else:
    print("Not calculated")

a = "new" if not b else "old"
