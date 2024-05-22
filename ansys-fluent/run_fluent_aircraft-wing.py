#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Create a connection
conn = qarnot.connection.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task('fluent-aircraft', 'ansys-fluent', 2)

# Create and append input bucket
input_bucket = conn.retrieve_or_create_bucket("fluent-aircraft-input")
input_bucket.sync_directory("input")
task.resources.append(input_bucket)

# Create output bucket
task.results = conn.create_bucket("fluent-aircraft-output")

# Fluent Command
task.constants['FLUENT_CMD'] = "fluent -g 3ddp -t56 -i run.jou"
task.constants["DOCKER_TAG"] = "2023R2"

# Your license server informations
task.constants["QARNOT_SECRET__ANSYSLMD_LICENSE_IP"] = ""
task.constants["QARNOT_SECRET__ANSYSLMD_LICENSE_SERVER_PORT"] = ""

# Take a snapshot every 10 seconds
task.snapshot(10)

# Submit the task to the API, that will launch it on the cluster
task.submit()
