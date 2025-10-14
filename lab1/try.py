def div(a:int):
    try:
        result = 10 / a
    except ZeroDivisionError:
        print("Error: Cannot divide by zero!")
    else:
        print("No exception raised")
    finally:
        print("common try end")

div(10)
div(0)