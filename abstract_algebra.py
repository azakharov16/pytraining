def tetration(a, b):
	if type(b) != int:
		raise ValueError
	elif b == 0:
		return 1
	else:
   		return a ** tetration(a, b - 1)
		
def pentation(a, b):
	if type(b) != int:
		raise ValueError
	elif b == 0:
		return 1
	else:
		return tetration(a, pentation(a, b - 1))
		
def hyper(a, b, n):
	if type(n) != int or type(b) != int:
		raise ValueError
	elif b == 0:
		return 1
	elif n == 1:
		return a + b
	elif n == 2:
		return a * b
	elif n == 3:
		return a ** b
	else:
		return hyper(a, hyper(a, b - 1, n), n - 1)
		

print tetration(3,3)
print tetration(3,2)
print pentation(2,2)
print pentation(2,3)

print hyper(3,3,3)
print hyper(3,3,4)
print hyper(3,2,4)
print hyper(2,2,5)
print hyper(2,3,5)


