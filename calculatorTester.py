# -*- coding: utf-8 -*-
"""
I, Ibrahim Sydock, pledge  that  I  have  neither  given  nor  received  help  from  anyone  other  than  the 
instructor/TA for all program components included here!
"""

#For exiting cleanly
import sys
#For sin, log, etc. functions
import math
#For random num generation
import random

#constant variables
NUM_RANGE = 100
MAX_NUM_OF_TERMS = 8
MAX_NUM_OF_DECIMAL_PLACES = 5

'''operation methods'''
def add(num1, num2):
    return num1 + num2

def sub(num1, num2):
    return num1 - num2

def mul(num1, num2):
    return num1 * num2

def div(num1, num2):
    return num1 / num2

def cot(num):
    return math.cos(num) / math.sin(num)

def neg(num):
    return num * -1


"""Dictionary of value to operation/func method"""
operations = {
    '+' : add,
    '-' : sub,
    '*' : mul,
    '/' : div,
    '^' : math.pow,
    'u' : neg,
    's' : math.sin,
    't' : math.tan,
    'c' : math.cos,
    'o' : cot,
    'l' : math.log10,
    'e' : math.log
}

"""
Dictionary of an operation and it's precedence and associativity
Left is -1, Right is 1
"""
attributes = {
    '^' : (3, 1),
    '/' : (2, -1),
    '*' : (2, -1),
    '+' : (1, -1),
    '-' : (1, -1)
}

strt_paren = ['(', '{']
end_paren = [')', '}']

# valid operators & functions
ops = ['+','-','*','/','^']
fcs = ['u', 's', 't', 'c', 'o', 'l', 'e'] 
    
#returns true if the char can be converted into an int or float, otherwise return false
def is_num(char):
    try:
        int(char)
        return True
    except ValueError:
        try:
            float(char)
            return True
        except ValueError:
            return False

# returns number as a float or int using isinstance()
# assumes input is for a float or int
def get_num_type(num):
    if isinstance(num, int):
        return int(num)
    else:
        return float(num)
  

# Shunting Yard Algorithm to convert equation into postfix
def shunt(exp):
    ops_stk = [];
    output_que = [];
    for x in exp:
        # If a number, add to queue
        if is_num(x):
            output_que.append(x)
        # if a function, push to stack
        if x in fcs:
            ops_stk.append(x)
        # If an operator
        elif x in ops:
            # while the val on top is an operator,
            # AND has greater precedence OR same precedence and cur op is left-associative
            try:
                while ops_stk and ops_stk[-1] in ops and attributes[ops_stk[-1]][0] > attributes[x][0] or \
                          (attributes[ops_stk[-1]][0] == attributes[x][0] and attributes[x][1] == -1):
                    #pop from stack onto queue
                    output_que.append(ops_stk.pop())
            except Exception: pass #catching exception means stack val wasn't an op, so do nothing
            # push current op to stack
            ops_stk.append(x)
        # if left paren, push to stack
        elif x in strt_paren:
            ops_stk.append(x)
        # if right paren
        elif x in end_paren:
            #print("op stk before pop: ", ops_stk)
            #print("output que before pop: ", output_que)
            # while the top of the stack isn't a left paren
            while ops_stk and (not ops_stk[-1] in strt_paren):
                #pop ops from stack onto queue
                #print("pop: ", output_que.append(ops_stk.pop()))
                output_que.append(ops_stk.pop())
                
            #discard left paren    
            #print("discard: ", ops_stk.pop())
            ops_stk.pop()

            #if the top of the op stack is a func
            if ops_stk and ops_stk[-1] in fcs:
                #pop func to queue
                output_que.append(ops_stk.pop())
                
    #while there are ops on stack, pop to queue
    while ops_stk:
        output_que.extend(ops_stk.pop())
    
    # evaluates postfix notation
    for op in output_que:
        try:
            if is_num(op):
                ops_stk.append(op)
            elif op in fcs:
                #no stack means no real input
                if not ops_stk:
                    return '~Functions require input'
                num = get_num_type(ops_stk.pop())
                #print("evaluating: ", end='')
                #print(op)
                #print('with number: ', end='')
                #print(num)
                
                # log of <=0 is undefined
                if(num <= 0 and (op == 'e' or op == 'l')):
                    return '~The argument of a log function cannot be less than or equal to zero'
                
                # divide by zero error
                if(math.sin(num) == 0 and op == 'o'):
                    return '~The argument of a cotangent function had a value of sin() equal to zero'
                
                #print(operations[op](num))
                ops_stk.append(operations[op](num))
            else:
                # Ignores unary positives
                if not ops_stk or len(ops_stk) == 1: 
                    continue
                num2 = get_num_type(ops_stk.pop())
                num1 = get_num_type(ops_stk.pop())  
                
                #print("evaluating: ", end='')
                #print(num1, end = ' ')
                #print(op,  end = ' ')
                #print(num2)
                
                #Check for divide by zero
                if(num2 == 0 and op == '/'):
                    return '~Cannot divide by zero'
                
                #cannot calculate the exponent of a negative decimal in either place
                if(
                    op == '^'
                    and (
                    (num1 <= 0 and isinstance(num1, float))
                    or 
                    (num2 <= 0 and isinstance(num2, float)))
                    ):
                    return '~Unable to calculate the exponent with a negative decimal'
                
                #print(operations[op](num1, num2))
                
                ops_stk.append(operations[op](num1, num2))
        except OverflowError: 
            return'~Result is too big to compute'
        
    if not ops_stk:
        return '~Invalid Input'

    return get_num_type(ops_stk[-1])
        
    
def validate(exp):
    #get exp string into an array of chars for easy iteration
    chars = list(exp)
    length = len(chars)
    new_exp = []
    i = 0;
    start = 0;
    negate = False
    
    left_paren = 0
    right_paren = 0
    
    while i < length:
        # if a digit, loop until a non-digit is found to get the entire number/decimal
        if chars[i].isdigit():
            start = i
            while i < length and (chars[i].isdigit() or chars[i] == '.'):
                i += 1
                
            #check for invalid decimal value
            num = chars[start:i]
            dec = 0
            for c in num:
                if c == '.': dec += 1
                if dec > 1: return '~Invalid decimal number'
            
            #remove leading zeros
            num = (''.join(num)).lstrip('0')
            # An empty string means there were only zeros
            if not num: num = 0
            
            new_exp.append(num)
            if negate:
                negate = False
                new_exp.append(')')
            i -= 1
        # if char is a potential beginning of sin, cot, etc, then check if the rest of the func is there
        # otherwise an invalid function is present
        elif chars[i] in 'sctl':
            if i + 2 >= length: return '~Invalid input'
            #convert function to one char value
            func = ''.join(chars[i:i+3])
            nat = ''.join(chars[i:i+2])
            func_to_token = ''
            
            if func == "sin": func_to_token = 's'
            elif func == 'tan': func_to_token = 't'
            elif func == 'cos': func_to_token = 'c'
            elif func == 'cot': func_to_token = 'o'
            elif func == 'log': func_to_token = 'l'
            elif nat == 'ln': func_to_token = 'e'
            else: return '~Invalid Input'
                
            new_exp.append(func_to_token)
            
            #make sure to change index based on if a 3 or 2 letter func was used
            if nat == 'ln': i+= 1
            else: i += 2
        # Converting a minus if:
        elif chars[i] == '-':
            not_end = i != length-1 #prevents calls of i+1 when that would be out of bounds
            # at the start of the expression, then it is unary 
            #(unary minus is given parenthesis to cover a number since it is treated as a func like "sin()")
            if i == 0: 
                new_exp.append('u')
                if not_end and chars[i+1] != '(':
                    new_exp.append('(')
                    negate = True
            # there is another minus, then convert to binary plus
            elif not_end and chars[i+1] == '-':
                i += 1
                new_exp.append('+')
            # the previous key is an operator or starting paren, then it is unary
            elif not_end and chars[i-1] in ops or chars[i-1] in strt_paren: 
                new_exp.append('u')
                if chars[i+1] != '(':
                    new_exp.append('(')
                    negate = True
            # if the next key isn't a left paren, function or a digit, then something is wrong
            elif not_end and not chars[i+1] in strt_paren and not chars[i+1].isdigit() and not chars[i+1] in fcs: 
                return '~Invalid use of operations'
            # otherwise it is binary minus
            else: new_exp.append(chars[i])
        # if an operation check if there is another operation ahead (ignores minus since it could be unary)
        elif chars[i] in ops:
            if i != length-1 and chars[i+1] in ops and chars[i+1] != '-': return '~Invalid use of operators'
            new_exp.append(chars[i])
        # if a paren keep count
        elif chars[i] in strt_paren: 
            left_paren += 1
            new_exp.append(chars[i])
        elif chars[i] in end_paren: 
            right_paren += 1
            
            # if a start paren has never existed then adding an end paren invalidates this equation
            if left_paren < right_paren: return '~Cannot end a parenthesis group if it was never opened'
            
            new_exp.append(chars[i])
            
        # invalid token
        else: return '~Invalid input'
        
        #increment
        i += 1
      
    if right_paren != left_paren: return '~Mismatching parenthesis'
    if left_paren + right_paren == length: return '~Input requires numbers'
    
    #print("validated exp: ", end="")
    #print(new_exp)
    return new_exp

# Runs calculator and returns either evaluated expression or an error string with '~' at the beginning
def test_calc(exp):

    validated = validate(exp)
    
    #Returns a ~message if an error is occured
    if '~' in validated: return validated
    return shunt(validated)

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
            
            
        print("stack: ", num_stk, "\n")
        
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
                     eq_eval += "math.cot("
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
            
            
        # If the equation must be correct then it is necessary to test the generated eq
        # to not cause a divide by zero, negative log input error, compute a result too big,
        # or try to solve the exponent of a negative decimal
        # this test will only be catching those errors
        # if caught, the equation will be regenerated until it doesn't cause those errors.
        # this shouldn't affect stats of this calculator vs eval as 
        # the errors would mean the equation MUST be incorrect (assuming these errors are truly errors)
        # this helps the generator not generate incorrect equations when they should be correct
        # since the generator is unable to check for these errors as they can only be found during eval
        try:
            test = test_calc(eq)
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
            eq += "&|@,#`$~"    
            eq_eval += "(b#$!&?"
        
        
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
            c = test_calc(eq)
            
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

    
    ''' ---------------------CUMULATiVE STATS--------------------- '''
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
    print("\tNote that Python's eval() cannot interpret equations that use either cot() ")
    print("\tor decimals for exponents which this tester may generate")
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