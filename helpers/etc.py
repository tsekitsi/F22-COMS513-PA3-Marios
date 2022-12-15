from os.path import basename, dirname, join
from os import getcwd, chdir, devnull
import subprocess
import time

from diff_match_patch import diff_match_patch

def compile_temp():
	subprocess.call(['gcc', '-o', 'test/temp', 'test/temp.c'], stderr=open(devnull, 'wb'))
	

def is_faulty(filepath):
	# Runs the binary* at @filepath through the script
	# "test/modified/detect_segfault.sh" and returns
	# False if "139" is in the output, otherwise returns
	# True (*so prereq to have the program compiled).
	path_to_sh = join(dirname(filepath), 'detect_segfault.sh') # => prereq: "detect_segfault.sh" must be in the same dir as the test program
	result = subprocess.run([path_to_sh, filepath], stdout=subprocess.PIPE).stdout.decode('utf-8') # https://stackoverflow.com/a/4760517
	return '139' in result


def extract_changes_between_files(file1, file2):
	# Returns str of diff between file1 and file2.
	with open(file1, 'r') as f1:
		file1_str = f1.read()
		with open(file2, 'r') as f2:
			file2_str = f2.read()

			dmp = diff_match_patch()
			patches = dmp.patch_make(file1_str, file2_str)
			return patches


def patch_to_new_file(patches, file):
	with open(file, 'r') as f:
		text = f.read()
		dmp = diff_match_patch()
		new_text, _ = dmp.patch_apply(patches, text)
		with open('test/temp.c', 'w') as g:
			g.write(new_text)
