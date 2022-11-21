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
            # while the top of the stack isn't a left paren
            while ops_stk and (not ops_stk[-1] in strt_paren):
                #pop ops from stack onto queue
                output_que.append(ops_stk.pop())
                
            #discard left paren    
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
                print("evaluating: ", end='')
                print(op)
                print('with number: ', end='')
                print(num)
                print(operations[op](num))
                ops_stk.append(operations[op](num))
            else:
                # Ignores unary positives
                if not ops_stk or len(ops_stk) == 1: 
                    continue
                num2 = get_num_type(ops_stk.pop())
                num1 = get_num_type(ops_stk.pop())  
                
                print("evaluating: ", end='')
                print(num1, end = ' ')
                print(op,  end = ' ')
                print(num2)
                
                #Check for divide by zero
                if(num2 == 0 and op == '/'):
                    return '~Cannot divide by zero'
                
                print(operations[op](num1, num2))
                
                ops_stk.append(operations[op](num1, num2))
        except OverflowError: 
            return'~Result is too big to compute'
        
    if not ops_stk:
        return '~Invalid Input'

    answer = ops_stk[-1]
    print("\n= ", end='') 
    if isinstance(answer, float):
        print("%.14f" % round(ops_stk[-1], 14))
    else:
        print(int(answer))
        
    
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
            # if the next key isn't a left paren or a digit, then something is wrong
            elif not_end and not chars[i+1] in strt_paren and not chars[i+1].isdigit(): return '~Invalid use of operations'
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
            new_exp.append(chars[i])
        # invalid token
        else: return '~Invalid input'
        
        #increment
        i += 1
      
    if right_paren != left_paren: return '~Mismatching parenthesis'
    if left_paren + right_paren == length: return '~Input requires numbers'
    
    print("validated exp: ", end="")
    print(new_exp)
    return new_exp

# Runs calculator and returns either evaluated expression or an error with '~' at the beginning
def test_calc(exp):
    #Get clean input with no white space
    exp = ''.join(exp.split())

    validated = validate(exp)
    
    #Returns a ~message if an error is occured
    if '~' in validated: return validated
    shunted = shunt(validate)
    return shunted

def generate_equations(amount):
    
    
    i = 0
    
    ''' EQUATION GENERATION '''
    while(i < amount):
        
        print("\nEQUATION #", i, "----------------------------------------------\n")
        
        #half of equations are incorrect
        CORRECT = i < amount/2
        
        terms = random.randint(1, 15) # Rand number of terms in the equation
        print("num of terms: ", terms, "\n")
        num_stk = [] # stores all randomly generated terms
        
        iTerm = 0
        
        '''' NUMBER GENERATOR '''
        while(iTerm < terms):
            num = random.randint(-999, 999)
            
            '''coin flip if it is a decimal'''
            if(random.randint(0,1)):
                decPlaces = random.randint(1, 6)
                decNum = str(num) + "."
                
                iDec = 0
                
                '''' decimal generator '''
                while(iDec < decPlaces):
                    # making sure the last decimal place is never
                    if iDec == decPlaces - 1:
                        decNum += str(random.randint(1, 9))
                    else:
                        decNum += str(random.randint(0, 9))
                    
                    iDec = iDec + 1
                    # decimal gen increment
                
                num_stk.append(float(decNum)) 
            else:
                num_stk.append(num)
            
            iTerm = iTerm + 1
            # number gen increment       
            
        print("stack: ", num_stk, "\n")
        
        ''' iterate thru num stack
            decide if there should be an operator next or an operation
        '''
        
        i = i + 1
        #equation gen increment
    ''' 
    Loop while i < amount
    Half of amount are sure to be incorrect equation
    Other half must be correctly formatted
    Generate random num of numbers to use in equation (0-10)
    Number has 50% chance to be be a whole number or decimal (rand number of decimals (0-5)) if not a zero
    Also 50% chance to be negative or positive if not a zero
    Correct:
        number of ops is no more than number of nums-1
        every open parenthesis has a closing parenthesis
        no number is divided by zero
        there can't be more than one consecutive operator (unless its a minus)
            
    Generation:
        equal chance of a number being affected by a function + beginning parenthesis, 
        is preceeded by a parenthesis (or followed by a parenthesis if there is a beginning one already),
        an operation
            
    Incorrect:
        equation contains random text
        decimals have multiple periods
    '''
    #pass to test_calc and eval()
    #print current stats
    '''
    Stats:
        Number of Correct vs Incorrect equations generated
        Number of correct equations found by calc and eval()
        Accuracy of calc
        Time taken for each to evaluate equation?
    '''
    #end loop
    #print final cumulative stats
    
# Main
if __name__ == '__main__':
    
    print("How many equations would you like to be generated?")
    
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