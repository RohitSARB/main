def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Invalid Expression"