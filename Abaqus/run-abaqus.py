#!/usr/bin/env python3

# Import the Qarnot SDK
import qarnot

# Variables
task_name = 'Hello World Abaqus'

conn = qarnot.Connection(client_token='<<<MY_SECRET_TOKEN>>>')
task = conn.create_task('Hello world Abaqus', "abaqus", 1)
# Setting up task constants

task.constants['ABAQUS_LICENSE_IP'] = '<<<YOUR_LICENSE_IP>>>'
task.constants['ABAQUS_LICENSE_PORT'] = '<<<YOUR_LICENSE_PORT>>>'
task.constants['ABAQUS_VENDOR_PORT'] = '<<<YOUR_VENDOR_PORT>>>'

# Modify the custom_v6.env file
env_file_path = '/usr/SIMULIA/EstProducts/2021/linux_a64/SMA/site/custom_v6.env'
with open(env_file_path, 'r') as file:
    env_content = file.read()

env_content = env_content.replace('ABAQUS_LICENSE_PORT', task.constants.ABAQUS_LICENSE_PORT).replace('ABAQUS_LICENSE_IP', task.constants.ABAQUS_LICENSE_IP)

with open(env_file_path, 'w') as file:
    file.write(env_content)

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
task.run(output_dir="abaqus-results")
