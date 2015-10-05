# Rodrigo Hernandez
# 48035611
# CompSci 169: Introduction to Optimization
# Homework 1

import sys
import math
import time

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

def stopCriteria(x1,x2,x3,abs_precision):
	'''
	Definition:
		Determines whether the stopping criteria is satisfied
	Arguments:
		x1(float): an integer representing a point
		x2(float): an integer representing a point
	Return:
		True if stopping criteria is satisfied, False otherwise
	'''

	rel_precision = math.sqrt(abs_precision)

	# This is the stopping criteria based on interval size

	return abs(x1 - x3) <= (rel_precision*abs(x2) + abs_precision )

def bracketMinimum(x1,step,gamma,func):
	'''
	Description:
		Brackets the minimum where [x1,x3] is the interval in which the minimum
		for function is located
	
	Arguments:
		x1(float): a starting point
		step(float): unit used in calculated second point
		gamma(float): the rate in which to use to find the third point
		func(function): function chosen to minimize

	Return:
		returns a tuple containing another two tuples, where the first one is
		all the points in which x1 < x2 < x3 and a second one with the values
		where all the points are  
	'''
	x2 = x1 + step

	f1 = func(x1)
	f2 = func(x2)

	if not (f2 <= f1):
		x1,x2,f1,f2 = x2,x1,f2,f1 #interchange both points
		step *= -1

	while(True):
		step *= gamma
		x3 = x2 + step
		f3 = func(x3)

		if(f3 > f2):
			break

		x1,x2 = x2,x3
		f1,f2 = f2,f3

	return ((x1,x2,x3),(f1,f2,f3))

def goldenSearch(start,step,func,max_iter):
	goldenRatio = (math.sqrt(5) - 1) / 2

	tol = findAbsMin()

	result = bracketMinimum(start,step,(1 / goldenRatio),func)
	x1,x2,x4 = result[0]
	f1,f2,f3 = result[1]

	x2 = (goldenRatio * x1) + ((1 - goldenRatio) * x4)
	x3 = ((1 - goldenRatio) * x1) + (goldenRatio * x4)
	f2 = func(x2)
	f3 = func(x3)
	count = 0

	while(abs(x2 - x3) > tol and count < max_iter):
		count+=1
		if(f2 < f3):
			x4 = x3
			x3 = x2
			f3 = f2
			x2 = goldenRatio * x1 + (1 - goldenRatio) * x4
			f2 = func(x2)
		else:
			x1 = x2
			x2 = x3
			f2 = f3
			x3 = (1 - goldenRatio) * x1 + goldenRatio * x4
			f3 = func(x3)

	print("Minimum is at point: ",x2,"with value of ", f2)
	print("\tNumber of Function calls: ",count)

def readFunction(fileName, funcName="function"):
	'''
	Description:
		Opens up the file specified, reads the function inside and arguments, 
		and returns a string representing executable python code. The file is 
		assumed to have a syntactically correct python representation of a 
		mathemical function.
	Arguments:
		fileName(string): the name of the file containing the desired function

	Returns:
		a string defining a python function named function that performs the 
		mathemical function in the specified file.
	Miscellanious:
		The file read should have the function in the first line and the
		arguments in the second line. The arguments should have the starting
		point first and the step second, seperated by a comma.


	'''

	function = "def function(x):\n\treturn float("

	with open(fileName) as f:
		function = function + f.readline().strip() + ")\n";
		args = f.readline().strip().split(";")
		function = function +  "start = " + args[0] \
					 + "\nstep = " + args[1]
	print(function)
	return function



def main():
	exec(readFunction("input.txt"),globals())
	
	max_iter = 10000

	for x1 in start:
		t0 = time.clock()
		goldenSearch(x1,step,function,max_iter)
		print("\t",time.clock() - t0," seconds wall time")
main()




