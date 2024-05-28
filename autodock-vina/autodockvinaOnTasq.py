#!/usr/bin/env python3

import qarnot
import sys

# Create a connection
conn = qarnot.Connection('qarnot.conf')

# Create a task
task = conn.create_task('autodock_vina-demo', 'docker-batch', 1)

# Store if an error happened during the process
error_happened = False
try:
    # Create a resource bucket and add the content of resources_vina_qarnot into it
    input_bucket = conn.create_bucket('autodock_vina-demo-input')
    input_bucket.sync_directory('input/')

    # Attach the bucket to the task
    task.resources.append(input_bucket)

    # Create a result bucket and attach it to the task
    output_bucket = conn.create_bucket('autodock_vina-demo-output')
    task.results = output_bucket

    # Set the command to run when launching the container, by overriding a constant.
    # Task constants are the main way of controlling a task's behaviour
    task.constants['DOCKER_REPO'] = 'qarnotlab/autodock'
    task.constants['DOCKER_TAG'] = '1.1.2'
    task.constants['DOCKER_CMD'] = 'vina --config config.txt'

    # Submit the task to the API, that will launch it on the cluster
    task.submit()
 
    # Wait for the task to be finished, and monitor the progress of its
    # deployment
    last_state = ''
    done = False
    while not done:
        if task.state != last_state:
            last_state = task.state
            print('** {}'.format(last_state))
 
        # Wait for the task to complete, with a timeout of 5 seconds.
        # This will return True as soon as the task is complete, or False
        # after the timeout.
        done = task.wait(5)
 
        # Display fresh stdout / stderr
        sys.stdout.write(task.fresh_stdout())
        sys.stderr.write(task.fresh_stderr())
 
    # Display errors on failure
    if task.state == 'Failure':
        print('** Errors: %s' % task.errors[0])
        error_happened = True
    else:
        # Download results from output_bucket into given folder
        task.download_results('output')

finally:
    # Exit code in case of error
    if error_happened:
        sys.exit(1)

