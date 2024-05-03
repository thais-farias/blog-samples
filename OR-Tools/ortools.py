#!/usr/bin/env python3

import sys
import qarnot

# Create a connection
conn = qarnot.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task('ortools-demo', 'docker-batch', 1)

# Store if an error happened
error_happened = False
try:
	# Create a resource bucket and add iput files 
	input_bucket = conn.create_bucket('ortools-demo-input')
	input_bucket.sync_directory('or-tools-examples/input_CP/')

	# Attach the bucket to the task
	task.resources.append(input_bucket)

	# Create a result bucket and attach it to the task
	output_bucket = conn.create_bucket('ortools-demo-output')
	task.results = output_bucket
	task.results_blacklist = "__pycache__"

	# Set the command to run when launching the container, by overriding a constant.
	# Task constants are the main way of controlling a task's behaviour
	task.constants['DOCKER_REPO'] = 'qarnotlab/ortools'
	task.constants['DOCKER_TAG'] = '9.5'
	task.constants['DOCKER_CMD'] = "python3 run_optimization.py"

	# Submit the task to the API, that will launch it on the cluster
	task.submit()

	# Wait for the task to be finished, and monitor the progress of its deployment
	last_state = ''
	done = False
	while not done:
		if task.state != last_state:
			last_state = task.state
			print("** {}".format(last_state))

		# Wait for the task to complete, with a timeout of 5 seconds.
		# This will return True as soon as the task is complete, or False
		# after the timeout.
		done = task.wait(5)

		# Display fresh stdout / stderr
		sys.stdout.write(task.fresh_stdout())
		sys.stderr.write(task.fresh_stderr())

	# Display errors on failure
	if task.state == 'Failure':
		print("** Errors: %s" % task.errors[0])
		error_happened = True
	else:
		task.download_results('output')

finally:
	# Exit code in case of error
	if error_happened:
		sys.exit(1)
