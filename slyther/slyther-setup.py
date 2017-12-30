import cx_Freeze
import os
os.environ['TCL_LIBRARY'] = "C:\\Python34\\tcl\\tcl8.6"
os.environ['TK_LIBRARY'] = "C:\\Python34\\tcl\\tcl8.6"

executables = [cx_Freeze.Executable("slyther.py")]

cx_Freeze.setup(
	name = "Slyther",
	options = {"build_exe" : {"packages":["pygame"],"include_files":["apple.png","snakehead.png"]}},
	description = "Apple and Snake",
	executables = executables
	)