#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Connect to the Qarnot platform
conn=qarnot.connection.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task("BLASTN-demo", "docker-batch", 1)

# Create an input bucket with the case files
input_bucket = conn.create_bucket("blastn-demo-input")
input_bucket.sync_directory("dataset-blastn")
task.resources.append(input_bucket)

# Create an output bucket
output_bucket = conn.create_bucket("blastn-demo-output")
task.results = output_bucket

# Give parameters regarding the Docker image to be used
task.constants["DOCKER_REPO"] = "ncbi/blast"
task.constants["DOCKER_TAG"] = "2.10.1"
task.constants['DOCKER_CMD'] = "./run_blastn.sh"

# Submit the task and download results
task.run(output_dir="output")
