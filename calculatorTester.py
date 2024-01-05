# -*- coding: utf-8 -*-
"""
I, Ibrahim Sydock, pledge  that  I  have  neither  given  nor  received  help  from  anyone  other  than  the 
instructor/TA for all program components included here!
"""

#For exiting cleanly
import sys
#For random num generation
import random
#For python's eval to utilize math functions
import math
#For calculator usage
from calculator import Run_Calc 

#constant variables
NUM_RANGE = 100
MAX_NUM_OF_TERMS = 8
MAX_NUM_OF_DECIMAL_PLACES = 5



''' -----------------------------EQUATION GENERATION----------------------------- '''
def generate_equations(amount):
    
    #stat variables
    num_of_incorrect = 0
    num_of_correct = 0
    
    calc_valid_eq = 0
    eval_valid_eq = 0
    
    calc_acc = 0
    eval_acc = 0
    
    eq = ""
    eq_eval = "" #seperate equation string for eval() since it require different formatting for functions
    i = 0
    
    while(i < amount):
        
        #half of equations are incorrect
        CORRECT = i < amount/2            
        isInvalid = False
        
        terms = random.randint(1, MAX_NUM_OF_TERMS) # Rand number of terms in the equation
        
        num_stk = [] # stores all randomly generated terms in string form
        
        iTerm = 0
        
        '''' -----------------------------NUMBER GENERATOR----------------------------- '''
        while(iTerm < terms):
            num = random.randint(-NUM_RANGE, NUM_RANGE)
            
            '''coin flip if it is a decimal'''
            if(random.randint(0,1)):
                decPlaces = random.randint(1, MAX_NUM_OF_DECIMAL_PLACES)
                decNum = str(num) + "."
                
                iDec = 0
                
                '''' ----------------decimal generator---------------- '''
                while(iDec < decPlaces):
                    # making sure the last decimal place is never 0 if CORRECT
                    # wouldn't invalidate the equation but it looks nicer
                    if iDec == decPlaces - 1 and CORRECT:
                        decNum += str(random.randint(1, 9))
                    else:
                        decNum += str(random.randint(0, 9))
                        
                    # Chance to add an extra decimal place to the number to invalidate the equation
                    # chance is lessened the more decimal places there are
                    if not CORRECT and random.randint(0, decPlaces*2) == 0:
                        decNum += "."
                        isInvalid = True
                    
                    iDec += 1
                # decimal gen increment
                
                num_stk.append(decNum)
            else:
                num_stk.append(str(num))
            
            iTerm += 1
        # number gen increment     
            
        
        ''' -----------------------------OPERATOR & FUNCTION GENERATOR----------------------------- '''
        unclosedParenCount = 0
        onlyOps = False
        
        iOp = 0
        
        while(iOp < len(num_stk) ):
            
            OFIndex = 0 #which op/func if chosen
            n = num_stk[iOp] # number
            isLastNum = iOp == len(num_stk) - 1
            
            ''' ----------------Dice roll---------------- '''
            # Equation being incorrect will force the generator to choose any operation 
            # no matter the condition. Since this only gives the equation a chance of being incorrect,
            # isInvalid is not changed
            if(iOp == 0 and not isLastNum and CORRECT):
                # dont roll for paren if it is the first term, but not the only term
                # however this rule is ignored if it is being generated incorrectly
                # this gives the equation a chance to have incorrect usage of parenthesis
                OFIndex = random.randint(0,11)
            elif(isLastNum and CORRECT):
                OFIndex = random.randint(5,12) 
                #if there is only one term then only roll for functions and end paren
                # turns what a start paren index would be into a end paren index, 
                # as long as its not just the single term in the eq
                # this rule is ignored if it is being generated incorrectly
                # this gives a chance of invalid equation generation
                OFIndex = 13 if OFIndex == 12 and len(eq) > 1 else random.randint(5,11)
            elif(onlyOps and CORRECT): 
                # only operators if a parenthesis was added 
                # however this rule is ignored if the generated equation is incorrect
                # this itself won't make the equation wrong, but give it redundant parenthesis
                OFIndex = random.randint(0, 4)
            else:
                # otherwise roll for every option with the condition that 
                # an end paren will only generate if there is at least one unclosed paren
                # however this condition is ignored if it is being generated incorrectly
                # this gives the equation to have more of a chance to incorrectly use paren
                OFIndex = random.randint(0,13) if not CORRECT or unclosedParenCount > 0 else random.randint(0,12)
                
            #reset onlyOps
            onlyOps = False    
            
            #coin flip if the equation should finish up
            endEq = isLastNum and random.randint(0,1)
            
            
            ''' ----------------Appending---------------- '''
            if(not endEq):
                # adding func/op type
                # functions and paren force the same number to be iterated upon again
                # this allows for equations to generate nested functions
                # and have the equation divided by parenthesis if generated as such
                if(OFIndex == 0): #plus
                    eq += n + "+"
                    eq_eval += n + "+"
                elif(OFIndex == 1):   #minus
                    eq += n + "-"
                    eq_eval += n + "-"
                elif(OFIndex == 2):   #multiply
                    eq += n + "*"
                    eq_eval += n + "*"
                elif(OFIndex == 3):   #divide
                    eq += n + "/"
                    eq_eval += n + "/"
                elif(OFIndex == 4):   #exponent
                    eq += n + "^"
                    eq_eval += n + "^"
                elif(OFIndex == 5):   #sin(
                    eq += "sin("  
                    eq_eval += "math.sin("
                elif(OFIndex == 6):   #tan(
                    eq += "tan("  
                    eq_eval += "math.tan("
                elif(OFIndex == 7):   #cos(
                     eq += "cos("
                     eq_eval += "math.cos("
                elif(OFIndex == 8):   #cot(
                     eq += "cot("
                     eq_eval += "1/math.tan("
                elif(OFIndex == 9):   #log(
                     eq += "log("
                     eq_eval += "math.log10("
                elif(OFIndex == 10):  #ln(
                     eq += "ln("
                     eq_eval += "math.log("
                elif(OFIndex == 11):  #negate(
                     eq += "-("
                     eq_eval += "-("
                elif(OFIndex == 12):  #starting parenthesis (
                    # current number is instead fused with the paren
                    # this allows for an operation to be applied to it
                     num_stk[iOp] = "(" + n
                     onlyOps = True
                elif(OFIndex == 13):  #end parenthesis )
                    # if the last number, finish the equation
                    # otherwise fuse with the number so an operator may be used on it
                    if(isLastNum):
                        eq += n + ")"
                        eq_eval += n + ")"
                    else:
                        num_stk[iOp] = n + ")"
                        onlyOps = True
                        iOp -= 1     
                    
                    unclosedParenCount -= 1
                        
                # if the type of token being added is a func or start paren
                # the amount of unclosed parenthesis will increase
                # and the number will always be re-terated upon
                # end parenthesis slight differs with a condition
                if OFIndex >= 5 and OFIndex <= 12:
                    unclosedParenCount += 1
                    iOp -= 1
                        
            else:
                eq += n
                eq_eval += n
            
            iOp += 1
        # op & func gen increment
        
        ''' ----------------CLOSING PARENTHESIS---------------- '''
        while unclosedParenCount > 0:
            
            unclosedParenCount -= 1
            
            #chance to not add a closing paren if this equation is being generated incorrectly
            if not CORRECT and random.randint(0,1):
                isInvalid = True
                continue
                
            #otherwise close all leftover paren
            eq += ")"
            eq_eval += ")"
            
        # closing paren loop end
            
        '''    
        If the equation must be correct then it is necessary to test the generated eq
        to not cause a divide by zero, negative log input error, compute a result too big,
        or try to solve the exponent of a negative decimal
        this test will only be catching those errors
        if caught, the equation will be regenerated until it doesn't cause those errors.
        this shouldn't affect stats of this calculator vs eval as 
        the errors would mean the equation MUST be incorrect (assuming these errors are truly errors)
        this helps the generator not generate incorrect equations when they should be correct
        since the generator is unable to check for these errors as they can only be found during eval
        '''
        # Summary: Lets the calculator test for mathmatical flaws in the generated equations
        try:
            test = Run_Calc(eq)
            #print("test resulted: ", test)
            if isinstance(test, str) and ("zero" in test or "negative" in test or "compute" in test):
                if CORRECT:
                    eq = ""
                    eq_eval = ""
                    continue
        except Exception:
            pass      
            
        # if the equation hasn't been invalidated by chance
        # then purposefully invalidate equation with a string of nonsense
        ''' TODO check what caused isInvalid to be true when the "false" equation is actually valid '''
        if not CORRECT and not isInvalid:
            invalidation = "$#!blah!#$"
            eq += invalidation
            eq_eval += invalidation
        
        
        ''' -------------------------------Results and Testing------------------------------- '''
        
        print("\nEQUATION #", i+1, "----------------------------------------------\n")
        print('Valid?: ', CORRECT)
        
        #current equation count
        if CORRECT: num_of_correct += 1
        else: num_of_incorrect += 1
        
        # Giving equation to testers
        print("Generated: \n", eq, "\n")
        #print("Generated: \n", eq_eval, "\n")
        
        try:
            c = Run_Calc(eq)
            
            #if eq is correct and calc deemed it incorrect, then decrement valid count
            if not(isinstance(c, str) and '~' in c): 
                calc_valid_eq = calc_valid_eq + 1 if CORRECT else calc_valid_eq - 1
            else:
                calc_valid_eq = calc_valid_eq - 1 if CORRECT else calc_valid_eq + 1
                
            print("My calc result: ", c)
        except Exception as e:
            print("Calc Error: ", str(e))
            calc_valid_eq = calc_valid_eq - 1 if CORRECT else calc_valid_eq + 1
         
        # current calc acc, not printed if on final equation  
        calc_acc = (calc_valid_eq / (num_of_correct + num_of_incorrect)) * 100   
        
        print(">My calc has so far identified", calc_valid_eq, "equation(s) correctly")
        if i != amount - 1:
            print("\t Current accuracy: ", calc_acc, "%")
        
        print("\n")
        
        try:
            print("Python's eval result: ", eval(eq_eval)) 
            eval_valid_eq = eval_valid_eq + 1 if CORRECT else eval_valid_eq - 1
        except Exception as e:
            print("Eval Error: ", str(e))
            eval_valid_eq = eval_valid_eq - 1 if CORRECT else eval_valid_eq + 1
        
        # current eval acc, not printed if on final equation
        eval_acc = (eval_valid_eq / (num_of_correct + num_of_incorrect)) * 100
        
        print(">Python's eval has so far identified", eval_valid_eq, "equation(s) correctly")
        if i != amount - 1:
            print("\t Current accuracy: ", eval_acc, "%")
        
        eq = ""
        eq_eval = ""
        i += 1
    #equation gen increment

    
    ''' ---------------------CUMULATIVE STATS--------------------- '''
    # Accuracy
    #calc_acc = calculate_accuracy(calc_valid_eq, num_of_correct, num_of_incorrect) 
    #eval_acc = calculate_accuracy(eval_valid_eq, num_of_correct, num_of_incorrect)
    
    print("\n-------------------------------FINAL STATS-------------------------------\n")
    print("Incorrect number of eq generated: ", num_of_incorrect, " vs correct number of eq generated: ", num_of_correct, "\n")
    print("My calc identified", calc_valid_eq, "equation(s) correctly")
    print("\t Final Accuracy: ", calc_acc, "%")
    print("Python's eval() identified", eval_valid_eq, "equation(s) correctly")
    print("\t Final Accuracy: ", eval_acc, "%")
    

'''' ------------------------------------------MAIN------------------------------------------ '''
if __name__ == '__main__':
    
    print("How many equations would you like to be generated?")
    print("\tNote 0: Python's eval() cannot interpret equations that use decimals ")
    print("\tto be evaluated as exponents, which this tester may generate")
    print("\t------------------------------------------")
    print("\tNote 1: these are the current values the equation generator is using: ")
    print("\t>NUM_RANGE =", NUM_RANGE, "- the limit of numbers generated between positive and negative.")
    print("\t>MAX_NUM_OF_TERMS =", MAX_NUM_OF_TERMS, "- the max amount of terms generated per equation.")
    print("\t>MAX_NUM_OF_DECIMAL_PLACES =", MAX_NUM_OF_DECIMAL_PLACES, "- the max amount of decimal places a decimal will generate with")
    print("\tThese constant values are hardcoded but can be manually changed if desired.")
    
    # get input and check that input is valid
    while(True):
        numOfEq = input("Input: ")
        try:
            numOfEq = int(numOfEq) # cast
            if numOfEq <= 0: raise ValueError() # number must be natural
            break
        except ValueError: #cast fail/<0
            print("\nPlease try again with a valid input.")
    
    #generate random expressions
    generate_equations(numOfEq)
    
    #end of program
    sys.exit(0)