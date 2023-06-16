#!/bin/bash

first_names_file="l2-names/firstnames.txt"  # Path to the file containing first names
last_names_file="l2-names/last_names.txt"    # Path to the file containing last names
output_file="./students.csv"          # Output CSV file

# Generate a random 10-digit student ID
generate_student_id() {
  echo $((1000000000 + RANDOM % 9000000000))
}

# Generate a random grade between 0 and 100
generate_grade() {
  echo $((RANDOM % 101))
}

# Read first names and last names into arrays
readarray -t first_names < "$first_names_file"
readarray -t last_names < "$last_names_file"

# Shuffle the arrays randomly
shuf_first_names=($(shuf -e "${first_names[@]}"))
shuf_last_names=($(shuf -e "${last_names[@]}"))

# Number of records to generate
num_records=100

# Generate the CSV file
echo "Student,Student ID,Grade" > "$output_file"

for ((i=0; i<num_records; i++)); do
  # Select a random first name and last name
  first_name=${shuf_first_names[$((RANDOM % ${#shuf_first_names[@]}))]}
  last_name=${shuf_last_names[$((RANDOM % ${#shuf_last_names[@]}))]}

  # Generate a random student ID and grade
  student_id=$(generate_student_id)
  grade=$(generate_grade)

  # Append the record to the CSV file
  echo "$first_name $last_name,$student_id,$grade" >> "$output_file"
done

echo "CSV file generated: $output_file"
