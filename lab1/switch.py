var = "abcdef"
boolean: bool = True

match var:
    case "abcdef":
        if boolean:
            print("match")
    case "qwerty" if boolean:
        pass
    case _:
        bool = False
