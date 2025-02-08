import sys
from os.path import exists
script, from_file, to_file = sys.argv
print("Appending from %s to %s..." % (from_file, to_file))
print("Checking input file existence...%s" % exists(from_file))
if not exists(from_file):
	print("The input file does not exist")
	sys.exit(1)
in_file = open(from_file, 'r')
indata = in_file.read()
print("The input file is %s characters long" % len(indata))
print("Checking output file existence...%s" % exists(to_file))
if not exists(to_file):
	print("The output file does not exist")
	sys.exit(1)
print("Type 'Y' to continue, 'N' to abort")
input_str = None
while input_str != 'Y':
	input_str = input(">: ")
	if input_str == 'N':
		sys.exit(0)
else:
	out_file = open(to_file,'a')
	out_file.write(2 * '\n' + indata)
	print("Done")
	out_file.close()
	in_file.close()
