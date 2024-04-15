#!/usr/bin/env python3

import qarnot

# Create a connection

# Create a task
task = conn.create_task('md-gromacs', 'docker-batch', 1)

# Create a resource bucket and add iput files 
input_bucket = conn.create_bucket('md-gromacs-input')
input_bucket.sync_directory('input/')

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
output_bucket = conn.create_bucket('md-gromacs-output')
task.results = output_bucket

# Set the command to run when launching the container, by overriding a constant.
# Task constants are the main way of controlling a task's behaviour
task.constants['DOCKER_REPO'] = 'qarnotlab/gromacs'
task.constants['DOCKER_TAG'] = '2021.2'
task.constants['DOCKER_CMD'] = 'sh -c "./run_md.sh 2>&1 | tee output.log"'

# Submit the task to the Api, that will launch it on the cluster
task.submit()
