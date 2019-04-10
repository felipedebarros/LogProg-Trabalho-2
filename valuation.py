from parserfiles.parser import pyparsing_parse
import json

rawFrameHandler = open("frame.json", "r")
rawFrame = rawFrameHandler.read()
rawFrameHandler.close()

frame = json.loads(rawFrame)


def evaluate(formula, state = frame["initialstate"]):
    if(len(formula) == 1):
        if(formula in frame["symbols"]):
            if(state in frame["valuation"][formula]):
                return True
            else:
                return False
        else:
            return False
    elif(len(formula) == 2):
        if(formula[0] == "~"):
            return (not evaluate(formula[1], state))
        elif(formula[0] == "[]"):
            for neighboor in frame["relationships"][state]:
                if(evaluate(formula[1], neighboor) == False):
                    return False
            return True 
        elif(formula[0] == "<>"):
            for neighboor in frame["relationships"][state]:
                if(evaluate(formula[1], neighboor) == True):
                    return True
            return False 
        
    elif(len(formula) == 3):
        if(formula[1] == '&'):
            return (evaluate(formula[0], state) and evaluate(formula[2], state))
        if(formula[1] == '|'):
            return (evaluate(formula[0], state) or evaluate(formula[2], state))
        if(formula[1] == '->'):
            return ( (not evaluate(formula[0], state)) or evaluate(formula[2], state))

formula = pyparsing_parse(input("Formula: "))
print(evaluate(formula))