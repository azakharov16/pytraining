from sys import argv, exit
script, filename = argv
print("Do you allow the script %s to erase the file %s ('Y'/'N')?" % (script, filename))
input_str = None
while input_str != 'Y':
	input_str = input(">: ")
	if input_str == 'N':
		exit(0)
else:
	print("Opening...")
	target = open(filename,'w')
	print("Truncating...")
	target.truncate()
	print("Fill three lines of new content (mind the ''!):")
	line1 = input("1 >: ")
	line2 = input("2 >: ")
	line3 = input("3 >: ")
	target.write(line1 + "\n" + line2 + "\n" + line3)
	print("Closing...")
	target.close()
