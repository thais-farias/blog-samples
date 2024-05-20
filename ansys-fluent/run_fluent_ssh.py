#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Create a connection
conn = qarnot.connection.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task('fluent-aircraft-ssh', 'ansys-fluent-ssh', 2)

# Create, sync and link your Bucket
input_bucket = conn.retrieve_or_create_bucket("fluent-aircraft")
input_bucket.sync_directory("input")
task.resources.append(input_bucket)

# Fluent tag version. E.g: latest, 2021R2, 2023R2, 2024R1, ...
task.constants["DOCKER_TAG"] = "2023R2"

# Set your SSH key
task.constants["DOCKER_SSH"] = ""

# Set BATCH to true in order to initiate a batch launch with ssh connectivity
# task.constants["BATCH"] = "true"
# Fluent command based on this template : 'fluent 3ddp -t56 -i run.jou'
# task.constants['FLUENT_CMD'] = "fluent 3ddp -mpitest -t56"

# Your license server informations
task.constants["QARNOT_SECRET__ANSYSLMD_LICENSE_IP"] = ""
task.constants["QARNOT_SECRET__ANSYSLMD_LICENSE_SERVER_PORT"] = ""

# Submit the task to the API
task.submit()
