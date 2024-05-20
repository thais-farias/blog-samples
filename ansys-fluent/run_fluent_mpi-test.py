#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Create a connection
conn = qarnot.connection.Connection(client_token='MY_SECRET_TOKEN')

# Create a task
task = conn.create_task('ansys-fluent-mpitest', 'ansys-fluent', 2)

# Fluent command based on this template : 'fluent 3ddp -t56 -i run.jou'
task.constants['FLUENT_CMD'] = "fluent 3ddp -mpitest -t56"

# Fluent tag version. E.g: latest, 2021R2, 2023R2, 2024R1, ...
task.constants["DOCKER_TAG"] = "2023R2"

# Submit the task to the API
task.submit()
