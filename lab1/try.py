def div(a:int):
    try:
        result = 10 / a
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    else:
        print("No exception raised")
    finally:
        print("common try end")

div(div(100))
div(10)
div(0)

try:
    if div(10):
        pass
    else:
        print("not passed")
except:
    pass

try:
    pass
except IndentationError:
    pass
except:
    print("")

a = 2532526