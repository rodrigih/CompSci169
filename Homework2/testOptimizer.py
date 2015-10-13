import optimizer

def safeAssert(correct,actual,functionName):
	try:
		assert(correct == actual)
	except(AssertionError):
		print(functionName + " failed")
		print("Ouput was: ",actual,", should have been: ",correct)

# This is an example function of 2 dimensions along with it's
# derivatives

def function(x1,x2):
	return x1**2 + 2 * x2**2

def function_derivative_1(x):
	return 2 * x

def function_derivative_2(x):
	return 4 * x

derivatives = [function_derivative_1,function_derivative_2]

# Test functions are below
def testCalculateDirection():
	gradient = [8,16]
	beta = 0.5
	direction = [-2,6]

	correct = [-9,-13]
	actual = optimizer.calculateDirection(gradient,beta,direction)
	
	safeAssert(correct,actual,"testCalculateDirection")

def testCalculateGradient():
	x = [7,3]
	correct = [14,12]
	actual = optimizer.calculateGradient(derivatives,x)

	safeAssert(correct,actual,"testCalculateGradient")

def testCalculateAlpha():
	x = [0.7384615,-0.0461538]
	d = [-1.54508,0.09656]

	string = "def function(var):\n\treturn var[0]**2 + 4 * var[1]**2"

	print(optimizer.calculateAlpha(string,x,d))



def testCalculateBeta():
	g1 = [2,3]
	g2 = [-2,-3]

	correct = 1
	actual = optimizer.calculateBeta(g1,g2)

	safeAssert(correct,actual,"testCalculateBeta")

def testCalculateX():
	x = [1,-1]
	alpha = 2
	direction = [5,10]

	correct = [11,19]
	actual = optimizer.calculateX(x,alpha,direction)

	safeAssert(correct,actual,"testCalculateX")

def testReadFile():
	exec(optimizer.readFile("input1.txt"),globals())
	print(start)
	print(function(start))

def testAll():	
	testCalculateDirection()
	testCalculateGradient()
	testCalculateAlpha()
	testCalculateBeta()
	testCalculateX()
	#testReadFile()

testAll()