from parserfiles.parser import parse
import json

rawFrameHandler = open("frame.json", "r")
rawFrame = rawFrameHandler.read()
rawFrameHandler.close()

frame = json.loads(rawFrame)

def updateFrame(formula):
    for state in frame["states"]:
        if (evaluate(formula, state) == False):
            removeState(state)
    print ("Frame depois: ", frame)
    



def removeState(state):
    frame["states"].remove(state)
    for modeRelationships in frame["relationships"]:
        if(state in frame["relationships"][modeRelationships]):
            del frame["relationships"][modeRelationships][state]
        for originStateRelationships in frame["relationships"][modeRelationships]:
            if(state in frame["relationships"][modeRelationships][originStateRelationships]):
                frame["relationships"][modeRelationships][originStateRelationships].remove(state)
    for symbol in frame["valuation"]:
        if(state in frame["valuation"][symbol]):
            frame["valuation"][symbol].remove(state)


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
        if(formula[1] == '[]'):
            mode = formula[0]
            for neighboor in frame["relationships"][mode][state]:
                if(evaluate(formula[2], neighboor) == False):
                    return False
            return True
        if(formula[1] == '<>'):
            mode = formula[0]
            for neighboor in frame["relationships"][mode][state]:
                if(evaluate(formula[2], neighboor) == True):
                    return True
            return False

        if(formula[1] == '&'):
            return (evaluate(formula[0], state) and evaluate(formula[2], state))
        if(formula[1] == '|'):
            return (evaluate(formula[0], state) or evaluate(formula[2], state))
        if(formula[1] == '->'):
            return ( (not evaluate(formula[0], state)) or evaluate(formula[2], state))

formula = parse(input("Formula: "))
if(formula[1] == "{}"):
    print ("Frame atual: ", frame)
    updateFrame(formula[0])
#    evaluate(formula[2])
#else:
#    evaluate(formula)

# print(evaluate(formula))
#print(formula)