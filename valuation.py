from parser.parser import pyparsing_parse

op = ['~', '&', '|', '->']
v = dict([])

def evaluate(formula):
    if(len(formula) == 1):
        if(formula not in v):
            ev = input('Enter a value for "' + formula + '" (t/f): ')
            if(ev == 't' or ev == 'T'):
                ev = True
            elif (ev == 'f' or ev == 'F'):
                ev = False
            else:
                print('Not a valid value for "' + formula + '".')
            v[formula] = ev
        return v[formula]
    elif(len(formula) == 2 and formula[0] is '~'):
        return (not evaluate(formula[1]))
    elif(len(formula) == 3):
        if(formula[1] == '&'):
            return (evaluate(formula[0]) and evaluate(formula[2]))
        if(formula[1] == '|'):
            return (evaluate(formula[0]) or evaluate(formula[2]))
        if(formula[1] == '->'):
            return ( (not evaluate(formula[0])) or evaluate(formula[2]))

formula = pyparsing_parse(input("Formula: "))
print(evaluate(formula))