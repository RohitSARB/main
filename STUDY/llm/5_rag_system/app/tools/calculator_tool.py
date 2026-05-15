def calculate(expression):

    try:
        return str(eval(expression))
    except Exception:
        return "Error in calculation"