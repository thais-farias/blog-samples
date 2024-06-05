#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Connect to the Qarnot platform
conn = qarnot.Connection(client_token='<<<MY_SECRET_TOKEN>>>')

# Create a task
task = conn.create_task('Hello world Abaqus', "abaqus", 1)

# Create input and output buckets
input_bucket = conn.create_bucket("abaqus-in")
input_bucket.sync_directory('taylor3d')
task.resources.append(input_bucket)
task.results = conn.create_bucket('abaqus-out')


# Submit the task and download results
task.run(output_dir="abaqus-out")
