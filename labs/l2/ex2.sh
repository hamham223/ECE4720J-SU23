#!/bin/bash

csv_file="students.csv"  # Path to the CSV file

# Extract student ID and grade from each line of the CSV file
awk -F',' '{ print $2 "\t" $3 }' "$csv_file"
