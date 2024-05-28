#!/usr/bin/env python3

import qarnot

# Create a connection
conn = qarnot.Connection(client_token="MY_SECRET_TOKEN")

# Create a task
task = conn.create_task('Hello World - Hashcat', 'docker-nvidia-batch', 1)

# Create a resource bucket and add input files 
input_bucket = conn.create_bucket('hashcat-in')
input_bucket.sync_directory('input/')

# Attach the bucket to the task
task.resources.append(input_bucket)

# Create a result bucket and attach it to the task
task.results =conn.create_bucket('hashcat-out')

# Set the command to run when launching the container, by overriding a constant.
# Task constants are the main way of controlling a task's behaviour
task.constants['DOCKER_REPO'] = 'qarnotlab/hashcat'
task.constants['DOCKER_TAG'] = 'latest'

# Hashcat command to pass. Too many possibilities to pass 
task.constants['HASHCAT_CMD'] = '/opt/hashcat/hashcat.bin --backend-ignore-opencl --optimized-kernel-enable --workload-profile 4 --hash-type 0 --attack-mode 0 --outfile /job/cracked.txt /job/target_hashes.txt /job/wordslist.txt'
task.constants['DOCKER_CMD'] = '/bin/bash /opt/wrapper.sh "${HASHCAT_CMD}"'

# Submit the task
task.run(output_dir = "hashcat-results")
