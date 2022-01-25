import copy


# takes the expression as input and combines digits to integers and converts subtraction to addition of negative numbers returning the resulting expression
def convert_to_int(expression):
    converted = list()
    expression.append("e")
    i = 0
    # loop over the input
    while i < len(expression):
        # if it's - sign, check the sign before and append +, check for continuous numeric chars and append the whole negative number after
        if expression[i] == "-":
            temp = "-"
            if expression[i-1] == ")" or expression[i-1].isnumeric():
                if expression[i+1] != "(":
                    converted.append("+")
            j = i + 1
            while expression[j].isnumeric():
                temp = str(temp)
                temp = int(temp + expression[j])
                j += 1
            converted.append(temp)
            i = j

        # if it's numeric, check for continuous numeric chars and append the whole number as int
        elif expression[i].isnumeric():
            temp = int(expression[i])
            j = i + 1
            while expression[j].isnumeric():
                temp = str(temp)
                temp = int(temp + expression[j])
                j += 1
            converted.append(temp)
            i = j

        # if it's the end ("e") of string, do nothing
        elif expression[i] == "e":
            i += 1

        # if it's anything else, just append it
        else:
            converted.append(expression[i])
            i += 1
    return converted


# takes an expression cleaned of parentheses as input and returns the calculated result as output
def simple_solve(expression):
    inter = list()
    # iterates over the expression and does all multiplication and division while creating the intermediary expression
    for i in range(len(expression)):
        if expression[i] == "x":
            expression[i+1] = expression[i-1] * expression[i+1]
        elif expression[i] == "/":
            expression[i+1] = expression[i-1] / expression[i+1]
        elif expression[i] == "+" or expression[i] == "-":
            inter.extend(expression[i-1: i+1])
    inter.append(expression[-1])
    
    # iterates over the intermediary expression and calculates all the addition and substraction
    for i in range(len(inter)):
        if inter[i] == "+":
            inter[i+1] = inter[i-1] + inter[i+1]
        elif inter[i] == "-":
            inter[i+1] = inter[i-1] - inter[i+1]
        
    return inter[-1]


# takes the expression and recursively goes through the parentheses, sending the contents of the innermost one to the simple expression solver. Returns the final result
def high_level_solve(expression, start=0):
    expression.append("e")
    to_pop = list()
    for i in range(len(expression[start:])):
        if expression[start+i] == ")":
            to_pop.append(start+i)
            return (simple_solve(expression[start:start+i]), to_pop)
        elif expression[start+i] == "(":
            x, y = high_level_solve(expression, start+i+1)
            expression[start+i] = x
            for index in sorted(y, reverse=True):
                del expression[index]
            to_pop.append(start+i)
        elif expression[start+i] == "e":
            return (simple_solve(expression[start:start+i]), to_pop)
        else:
            to_pop.append(start+i)

# main solver method which takes the expression as input, calls the appropriate methods and returns the result
def solver(exp):
    exp = convert_to_int(exp)
    og_exp = copy.deepcopy(exp)
    result = high_level_solve(exp)[0]
    return og_exp, result