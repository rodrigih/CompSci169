##################################################
# Rodrigo Hernandez
# 48035611
# CompSci 169
##################################################

# The following program implements the conjugate gradient method for
# optimization
##
#The program takes two files
#   - The first file has the function that needs to be optimized written in 
#     correct python code
##
#   - The second file has the derivatives in respect to each variable. It also
#     contains a list containing these defined functions in a variable labeled
#     func_div as well as a starting point and the maximum number of iterations

import math
import re
import sys

import OneDimOptimizer

def findAbsMin():
    '''
    Description: 
        Finds the lowest number in which :
                1 + number > 1 
        holds true

    Return:
        smallest computable number
    '''
    minimum = 1

    while(1 + minimum > 1):
        minimum *= 0.1

    return minimum

def stoppingCriteria(func,x0,x1,abs_tol):
    '''
    Description:
        Determines whether the stopping criteria has been reached

    Arguments:
        func (function): a function that takes a vector x
        x0  (list): a list of floats representing vector
        x1 (list): a list of floatss representing a vector
        abs_tol (float): a number representing the absoulute tolerance

    Return:
        returns a boolean stating whether the stopping criteria has been reached
    '''
    rel_tol = math.sqrt(abs_tol)
    #print(abs(func(x1) - func(x0))," ",abs_tol + rel_tol * abs(func(x0)))

    return abs(func(x1) - func(x0)) <= abs_tol + rel_tol * abs(func(x0))

def calculateDirection(gradient,beta,direction):
    '''
    Description:
        Calculates the direction at the next iteration of the conjugate
        gradient method.

    Arguments:
        gradient (list): the gradient vector at the current iteration
        beta (float): beta used in the gradient descent method
        direction (list): the direction vector in which

    Return:
        returns the new direction calculated using gradient and old direction
    '''
    new_direction = list()

    for i in range(0,len(direction)):
        new_direction.append((gradient[i]) + ( beta * direction[i]))

    return new_direction

def calculateGradient(func_deriv,x):
    '''
    Description:
        Calculates the gradient at the next iteration of the conjugate 
        gradient method

    Arguments: 
        func_deriv (list): list of derivatives in respect to each variable 
                           of the original function
        x (float): the point in the current iteration

    Return:
        returns the new gradient calculated using the gradients of the function
    '''
    new_gradient = list()

    for i in range(len(func_deriv)):
        new_gradient.append(func_deriv[i](x) * -1)
    return new_gradient


def calculateX(x,alpha,direction):
    '''
    Description:
        Calculate the new point at the next iteration of the conjugate
        gradient method

    Arguments:
        x (list): a point vector in the current iteration of the conjugate
        alpha (float):  the minimum of the function f(x_k + alpha * d_k)
                        of the conjugate gradient method
        direction (list):  a vector representing the direction of the conjugate
                           gradient method
    
    Return:
        returns the new point calculated using the process described in the conjugate
        gradient method                        
    '''
    new_x = list()

    for i in range(0,len(x)):
        new_x.append(x[i] + alpha * direction[i])

    return new_x

def calculateBeta(current_grad,prev_grad):
    '''
    Description:
        Calculate the beta using the Fletcher-Reeves version of using the
        vector of the gradient calculated at vectors x_k and x_(k+1) of the
        conjugate gradient method

    Arguments:
        current_grad (list): a vector of the graident calculated using x_(k+1)
        prev_grad (list): a vector of the gradient calculated using x_k

    Returns:
        returns a float representing the value of beta using the
        Fletcher-Reeves formula
    '''
    current_grad_length = 0
    prev_grad_length = 0

    for i in range(0,len(current_grad)):
        current_grad_length += current_grad[i]**2
        prev_grad_length += prev_grad[i]**2

    return current_grad_length / prev_grad_length

def calculateAlpha(func_str,x,d):
    new_func = func_str.replace("function","alphaFunction")
    pattern = "var\[_\]" 

    for i in range(0,len(x)):
        replace = "( ({0}) + ({1} * var) )".format(x[i],d[i])
        new_func = re.sub(pattern.replace("_",str(i)),replace,new_func)

    exec(new_func,globals())

    return OneDimOptimizer.goldenSearch(0,10,alphaFunction,1000000) #change goldenSearch to return only minimum

def optimize(func,func_deriv,func_str,x0,max_iter):
    '''
    Description:
        Given a function and it's gradient, optimize function at dim iterations
        where dim is the number of dimensions
    
    Arguments:
        func (function): a function that needs to be optmimized
        func_grad (list): a list of functions representing the derivative in
                         repsects to the i-th variable, where i is the
                         position of the array plus 1
        x0 (list): a list of integers representing the starting point
        dim (int): the number of dimensions the equation has.

    Return:
        returns the minimum of the function
    '''

    minimum = findAbsMin()

    # These "previous" variables are var_k(i.e. x_k,d_k, and g_k)
    prev_x = x0
    prev_d = calculateGradient(func_deriv,x0) # Initial direction is just the 
                                              # gradient of the initial point
    prev_grad = prev_d
    
    # These "current" variable are var_(k+1) (i.e. x_(k+1), d_(k+1) 
    # and g_(k+1))
    # Initialize each current to prev for loop to calculate things correctly on
    # the first loop.
    current_x = prev_x
    current_d = prev_d
    current_grad = prev_grad
    
    count = 0

    while(True): 
        count+=1
        prev_x = current_x
        prev_d = current_d
        prev_grad = current_grad

        # make current variables current before computing new variables
        alpha = calculateAlpha(func_str,prev_x,prev_d)

        # Calculate new variables
        current_x = calculateX(prev_x,alpha,prev_d)
        current_grad = calculateGradient(func_deriv,current_x)
        beta = calculateBeta(current_grad,prev_grad)
        current_d = calculateDirection(current_grad ,beta,prev_d)
        if stoppingCriteria(func,prev_x,current_x,minimum) or count > max_iter:
            break
    print("Total CG iterations: ",count)
    return current_x 

def readFile(fileName):
    with open(fileName) as infile:
        return infile.read()

def checkArgs():
    '''
    Description:
        checks whether the correct number of arguments are given. If not, the
        program immediately exits with an error mesage
    '''
    if len(sys.argv) != 3 :
        sys.exit("Must include two files")

def getLength(x):
    '''
    Description:
        calculates the length of the vector x. To be used to calculate error
    '''
    total = 0
    for i in range(0,len(x)):
        total+= x[i]**2
    return math.sqrt(total)

def main():
    checkArgs()
    # Read file with function only
    func_str = readFile(sys.argv[1])
    exec(func_str,globals())
    # Next Read file, which has other information
    exec(readFile(sys.argv[2]),globals())

    point = optimize(function,func_deriv,func_str,start,max_iter)
    print("Minimum is at point: ",point)
    print("Length of vector is: ",getLength(point))
main()
