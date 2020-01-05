import argparse
import posixpath
import os
import platform
import tarfile
import sys
import subprocess
import shlex
import shutil
import stat
ARROW = '========>'

class BuildError(Exception):
	"""Something in Build.py went wrong."""
	def __init__(self, message=None):
		if message is None:
			# Default library error message
			message = "Something in Build.py went wrong."
		super().__init__(message)


def Execute_Shell(command):
	print('Executing: ' + command)
	p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	stdout_arr = []
	while p.poll() is None:
		try:
			line = p.stdout.readline().decode()[:-1]
		except Exception as ex:
			line = ''
		stdout_arr.append(line)
		if line:
			if line != '':
				print(line)
	stdout = ''.join(stdout_arr) or ''
	if p.returncode != 0:
		print('Error. Return code: ' + str(p.returncode) + '. Command: ' + command)
		raise BuildError
	return ''.join(stdout)

def main(raw_arguments):
	if platform.system() != 'Linux':
		raise BuildError('OS not detected as Linux. This service is Linux only.')
	argument_parser = argparse.ArgumentParser()
	argument_parser.add_argument('--build', action='store_true')
	argument_parser.add_argument('--run', action='store_true')
	argument_parser.add_argument('--start', action='store_true')
	argument_parser.add_argument('--kill', action='store_true')
	argument_parser.add_argument('--rm', action='store_true')
	argument_parser.add_argument('--rmi', action='store_true')
	argument_parser.add_argument('--test', action='store_true')

	parsed_arguments = shlex.split(raw_arguments)
	args, unknown = argument_parser.parse_known_args(parsed_arguments)
	if unknown:
		print('{} Warning: Unknown arguments: {}'.format(ARROW, str(unknown)))
	
	if args.build:
		print('{} Building image...'.format(ARROW))
		command = 'docker build -f build_tools/Dockerfile -t emailvalidator:latest .'
		Execute_Shell(command)
		print('{} Done building image.'.format(ARROW))
	if args.run:
		print('{} Running container...'.format(ARROW))
		command = 'docker run -d -p 127.0.0.1:8080:8080 -e PORT=8080 --name emailvalidator_container emailvalidator'
		Execute_Shell(command)
		print('{} Done running container.'.format(ARROW))
	if args.start:
		print('{} Starting container...'.format(ARROW))
		command = 'docker start emailvalidator_container'
		Execute_Shell(command)
		print('{} Done starting container.'.format(ARROW))
	if args.kill:
		print('{} Killing container...'.format(ARROW))
		command = 'docker kill emailvalidator_container'
		Execute_Shell(command)
		print('{} Done killing container.'.format(ARROW))
	if args.rm:
		print('{} Removing container...'.format(ARROW))
		command = 'docker rm emailvalidator_container'
		Execute_Shell(command)
		print('{} Done removing image.'.format(ARROW))
	if args.rmi:
		print('{} Removing image...'.format(ARROW))
		command = 'docker rmi emailvalidator'
		Execute_Shell(command)
		print('{} Done removing image.'.format(ARROW))
	if args.test:
		print('{} Running internal tests...'.format(ARROW))
		command = "docker exec emailvalidator_container /bin/bash -c 'python3 -m unittest tests/test_emailvalidator.py'"
		Execute_Shell(command)
		print('{} Done running internal tests.'.format(ARROW))
		print('{} Running external tests...'.format(ARROW))
		command = 'cd emailvalidator && python3 -m unittest tests/test_external.py'
		Execute_Shell(command)
		print('{} Done running internal tests.'.format(ARROW))



if __name__ == '__main__': main(' '.join(sys.argv[1:]))