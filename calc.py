import operator


def evaluate(string: str):
    # remove all whitespace
    expression = "".join(string.split())
    expression = expression.replace('+-', '-').replace('--', '+')
    left = None
    oper = None
    right = None
    operators = {
        '*': operator.mul,
        '/': operator.truediv,
        '+': operator.add,
        '-': operator.sub
    }
    if expression.count('(') == 0 and expression.count(')') == 0:
        for char in expression:
            if char in operators:
                left, oper, right = expression.partition(char)
                if left.isdigit() and right.isdigit():
                    return operators[char](int(left), int(right))
    return None






tests = [
    ["1 + 1", 2],
    ["8/16", 0.5],
    ["3 -(-1)", 4],
    ["2 + -2", 0],
    ["10- 2- -5", 13],
    ["(((10)))", 10],
    ["3 * 5", 15],
    ["-7 * -(6 / 3)", 14]
]

for test in tests:
    print(evaluate(test[0]))
