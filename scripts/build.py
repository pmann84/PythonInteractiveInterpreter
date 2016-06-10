#!python34

from subprocess import Popen, PIPE

if __name__ == "__main__":
	# pyinstaller.exe --onefile --windowed --icon=..\\icons\\python.png --version-file=version.txt ..\\src\\pii.py

	# Create argument list for build
	pyinstaller_cmd = [ "pyinstaller.exe", 				# pyinstaller exe
						"--onefile", 					# bundle as one file
						"--windowed", 					# necessary for gui apps
						"--icon=..\\icons\\python.ico", # icon path
						#"--version-file=version.txt", 	# version information
						"--noupx",
						"--clean",						# clean install
						"..\\src\\pii.py" ]				# main script path

	p = Popen(pyinstaller_cmd, stdin=PIPE, stdout=PIPE)
	print p.communicate("n\n")[0]
