#!/bin/bash

# Set default experiment name
experiment_name=${1:-gpt4omini}

dataset=${2:-tabfact}
# set default llm model
llm=${3:-gpt-4o-mini}
# llm=${3:-gpt-3.5-turbo}

# Create the output directory if it doesn't exist
output_dir="runs/${experiment_name}"
mkdir -p "$output_dir"

# Define the log file path
log_file="${output_dir}/app.log"

# Run the Python script and redirect output to the log file
echo "Running experiment with name: $experiment_name"
python test/main.py --dataset "$dataset" --experiment_name "$experiment_name" --llm "$llm">> "$log_file" 2>&1
echo "Logs are being written to $log_file"
