#!/bin/bash

# Assign arguments to variables
CONNECTION_STRING=$1
TABLE_NAME=$2

# Function to check if a table exists
create_table() {

  # Use connection string
  TABLE_EXISTS=$(psql "$CONNECTION_STRING" -tAc "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = '$TABLE_NAME');")

  if [ "$TABLE_EXISTS" = "f" ]; then
    echo "Table '$TABLE_NAME' does not exist. Creating it..."
    CREATE_TABLE_SQL="CREATE TABLE $TABLE_NAME (
      irn SERIAL PRIMARY KEY,
      department TEXT,
      taxon TEXT,
      taxon_id TEXT,
      accepted_name_usage_id INT,
      canonical_name TEXT,
      generic_name INT,
      specific_epithet TEXT,
      infraspecific_epithet TEXT,
      taxon_rank TEXT,
      kingdom TEXT,
      phylum TEXT,
      class TEXT,
      order TEXT,
      family TEXT,
      genus TEXT,
      vernacular_name TEXT,
      source TEXT,
      weight FLOAT

    );"

    psql "$CONNECTION_STRING" -c "$CREATE_TABLE_SQL"

    if [ $? -eq 0 ]; then
      echo "Table '$TABLE_NAME' created successfully."
    else
      echo "Error: Failed to create table '$TABLE_NAME'."
      exit 1
    fi
  else
    echo "Table '$TABLE_NAME' already exists."
  fi
}

create_table
