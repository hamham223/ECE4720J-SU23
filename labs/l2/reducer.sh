#!/bin/bash

# Read pairs from standard input
while IFS=$'\t' read -r student_id grades; do
  # Split the grades into an array
  IFS=',' read -ra grade_array <<< "$grades"

  # Find the maximum grade in the array
  max_grade=$(printf '%s\n' "${grade_array[@]}" | sort -nr | head -n 1)

  # Output the student ID and the maximum grade
  echo "$student_id $max_grade"

done

# To use this program:

# Save the script to a file named reducer.
# Make the script executable by running chmod +x reducer.
# Prepare input data in the format of student ID followed by a tab-separated list of grades, 
# e.g., 1234567890<TAB>80,75,90.
# Pipe the input data to the reducer program, e.g., cat input.txt | ./reducer.
# The program will process the input pairs, find the maximum grade for each student, and output the results in the format studentID<TAB>maxGrade on the standard output.