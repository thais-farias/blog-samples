#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Variables
task_name = 'Hello World Abaqus'

conn = qarnot.Connection(client_token='<<<MY_SECRET_TOKEN>>>')
task = conn.create_task('Hello world Abaqus', "abaqus", 1)

# Create input and output buckets
input_bucket = conn.create_bucket("abaqus-in")
input_bucket.sync_directory('input/')
task.resources.append(input_bucket)
task.results = conn.create_bucket('abaqus-out')

# Abaqus-specific commands for RoCE
run_computation='mpirun --allow-run-as-root --bind-to none --hostfile /job/mpihosts -x UCX_NET_DEVICES=mlx5_2:1 -x UCX_IB_TRAFFIC_CLASS=124 -x UCX_IB_SL=3 /root/abaqus'

# Run computation's input bucket file 
task.constants['DOCKER_CMD_MASTER'] = f'/bin/bash -c "/job/utils/setup_cluster abaqus job=elementradial.inp"'
task.constants['DOCKER_CMD_WORKER'] = '/bin/bash -c "/job/utils/setup_cluster"'


# Submit the task and download results
task.run(output_dir="abaqus-out")
