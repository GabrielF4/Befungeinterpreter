
import random as rand
from typing import Tuple

RIGHT = 1
DOWN = 2
LEFT = 3
UP = 4

def update_pointer_direction(row_pointer: int, col_pointer: int, pointer_direction: int) -> Tuple[int, int]:
    match pointer_direction:
            case 1:
                col_pointer += 1
            case 2:
                row_pointer += 1
            case 3:
                col_pointer -= 1
            case 4:
                row_pointer -= 1

    return row_pointer, col_pointer

def interpret(code):

    output: str = ""
    stack = []
    
    debug = False
    counter = 0

    defunge_arr = code.split("\n")

    row_pointer = 0
    col_pointer = 0
    pointer_direction = RIGHT
    push_mode = False

    while True:

        if debug:
            print(defunge_arr[row_pointer][col_pointer], stack)

        #Push mode is activated by '\'
        if push_mode:
            
            if defunge_arr[row_pointer][col_pointer] == '\"':
                push_mode = False
            else:
                stack.append(ord(defunge_arr[row_pointer][col_pointer]))
        else:

            #Add to the stack if it is a digit
            if defunge_arr[row_pointer][col_pointer].isdigit():
                stack.append(int(defunge_arr[row_pointer][col_pointer]))

            #Map sign to the right action according to the befunge rules
            match defunge_arr[row_pointer][col_pointer]:
                case '>':
                    pointer_direction = RIGHT
                case 'v':
                    pointer_direction = DOWN
                case '<':
                    pointer_direction = LEFT
                case '^':
                    pointer_direction = UP
                case '?':
                    pointer_direction = rand.choice([RIGHT, DOWN, LEFT, UP])
                case '+':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a + b)
                case '-':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(b - a)
                case '*':
                    a = stack.pop()
                    b = stack.pop()
                    stack.append(a * b)
                case '/':
                    a = stack.pop()
                    b = stack.pop()
                    if a == 0:
                        stack.append(0)
                    else:
                        stack.append(b // a)
                case '%':
                    a = stack.pop()
                    b = stack.pop()
                    if a == 0:
                        stack.append(0)
                    else:
                        stack.append(b % a)
                case '!':
                    a = stack.pop()
                    if a == 0:
                        stack.append(1)
                    else:
                        stack.append(0)
                case '`':
                    a = stack.pop()
                    b = stack.pop()
                    if b > a:
                        stack.append(1)
                    else:
                        stack.append(0)
                case '_':
                    temp = stack.pop()
                    if 0 == temp:
                        pointer_direction = RIGHT
                    else:
                        pointer_direction = LEFT
                case '|':
                    if stack.pop() == 0:
                        pointer_direction = DOWN
                    else:
                        pointer_direction = UP
                case '\"':
                    push_mode = True
                case ':':
                    if not stack:
                        stack.append(0)
                    else:
                        stack.append(stack[-1])
                case '\\':
                    if stack:
                        last = stack.pop()
                        if not stack:
                            stack.append(0)
                        second_last = stack.pop()
                        stack.append(last)
                        stack.append(second_last)
                case '$':
                    stack.pop()
                case '.':
                    output += str(stack.pop())
                case ',':
                    output += chr(stack.pop())
                case '#':
                    row_pointer, col_pointer = update_pointer_direction(row_pointer, col_pointer, pointer_direction)
                case 'p':
                    y = stack.pop()
                    x = stack.pop()
                    v = stack.pop()
                    defunge_arr[y] = defunge_arr[y][:x] + chr(v) + defunge_arr[y][x + 1:]
                case 'g':
                    y = stack.pop()
                    x = stack.pop()
                    stack.append(ord(defunge_arr[y][x]))
                case '@':
                    return output

        #Updating the pointer
        row_pointer, col_pointer = update_pointer_direction(row_pointer, col_pointer, pointer_direction)

        #Algorithm for wrapping around the 2d code
        if row_pointer + 1 > len(defunge_arr):
            row_pointer %= len(defunge_arr)
        elif row_pointer < 0:
            row_pointer = len(defunge_arr) + row_pointer
        elif col_pointer + 1 > len(defunge_arr[row_pointer]):
            col_pointer %= len(defunge_arr[row_pointer])
        elif col_pointer < 0:
            col_pointer = len(defunge_arr[row_pointer]) + col_pointer

        #Debug tool to control if code is stuck in infinite loop
        if debug:
            counter += 1
            if counter > 9000:
                print("Error! Code stuck in loop")
                break

if __name__ == "__main__":

    #The defunge code input
    defunge = '>987v>.v\nv456<  :\n>321 ^ _@'

    output = interpret(defunge)

    print(output)

    #>987v>.v
    #v456<  :
    #>321 ^ _@