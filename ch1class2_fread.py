from sys import argv
# File modes:
# 'r': reading mode (file will not be altered)
# 'w': writing mode (writing into file [partly] erases its content)
# 'a': append mode (writing into file does not erase its content)
# 'r+': read and write
# 'rb', 'wb': binary modes (for pickle files)

script, filename = argv
input_file = open(filename,'r')
print("Script %s running..." % script)
print("Opening file: %s" % filename)
print(input_file.read())
input_file.seek(0)
print("Now choose the position from 0 to %d to read from" % len(input_file.read()))
n = int(input(">: "))
input_file.seek(n)
print(input_file.read())
input_file.close()