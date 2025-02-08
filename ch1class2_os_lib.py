import os

print(os.getcwd())  # pwd
print(os.listdir(os.curdir))  # ls
os.mkdir('tempdir')  # mkdir
print('tempdir' in os.listdir(os.curdir))
os.rename('tempdir', 'junkdir')  # mv
os.rmdir('junkdir')  # rmdir

os.chdir('C://Users//andrey.zakharov//py_training//scripts')  # cd
print(os.getcwd())
os.chdir('C://Users//andrey.zakharov//PycharmProjects//training')

print(os.path.exists('junk.txt'))
print(os.path.isfile('junk.txt'))
print(os.path.isdir('junk.txt'))

print('junk.txt' in os.listdir(os.curdir))
total_path = os.path.abspath('junk.txt')
path_tuple = os.path.split(total_path)
print(path_tuple)
print(os.path.dirname(total_path))
print(os.path.basename(total_path))
print(os.path.splitext(os.path.basename(total_path)))

os.remove('junk.txt')  # rm

# Running an external command from shell:
os.system('start notepad')
# Note that this command passes its argument to cmd.exe, NOT PowerShell

# Generate a list of filenames in the directory tree:
for dirpath, dirnames, filenames in os.walk(os.curdir):
	for f in filenames:
		print(os.path.abspath(f))

