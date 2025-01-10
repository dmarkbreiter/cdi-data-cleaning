#!/bin/bash

# Check if enough arguments are provided
if [ "$#" -lt 3 ] && [ "$#" -ne 2 ]; then
  echo "Usage: $0 <connection_string> <table_name> <csv_file_path>"
  echo "Example: $0 postgresql://postgres:postgres@127.0.0.1:54322/postgres ./file.csv"
  exit 1
fi

# Assign arguments to variables
CONNECTION_STRING=$1
TABLE_NAME=$2
CSV_FILE=$3
USE_CONNECTION_STRING=true

# Declare columns
COLUMNS="\"irn\", \"emuGuuid\", \"dateEmuRecordModified\", \"catalogueNumber\", \"department\", \"basisOfRecord\", \"taxonIRN\", \"taxon\", \"taxonRank\", \"taxonID\", \"vernacularName\", \"typeStatus\", \"sex\", \"caste\", \"lifeStage\", \"side\", \"element\", \"localityIRN\", \"locality\""

# Check if the CSV file exists
if [ ! -f "$CSV_FILE" ]; then
  echo "Error: CSV file '$CSV_FILE' does not exist."
  exit 1
fi

# Function to check if a table exists
check_and_create_table() {
  if [ "$USE_CONNECTION_STRING" = true ]; then
    # Use connection string
    TABLE_EXISTS=$(psql "$CONNECTION_STRING" -tAc "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = '$TABLE_NAME');")
  else
    # Use individual connection details
    TABLE_EXISTS=$(psql -h "$HOST" -p "$PORT" -d "$DATABASE" -U "$USER" -tAc "SELECT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = '$TABLE_NAME');")
  fi

  if [ "$TABLE_EXISTS" = "f" ]; then
    echo "Table '$TABLE_NAME' does not exist. Creating it..."
    CREATE_TABLE_SQL="CREATE TABLE $TABLE_NAME (
      irn SERIAL PRIMARY KEY,
      emu_guid TEXT,
      date_emu_record_modified DATE,
      catalogue_number TEXT,
      department TEXT,
      basis_of_record TEXT,
      taxon_irn INT,
      type_status TEXT,
      sex TEXT,
      caste TEXT,
      life_stage TEXT,
      side TEXT,
      element TEXT,
      locality_irn INT,
      locality TEXT
    );"

    if [ "$USE_CONNECTION_STRING" = true ]; then
      psql "$CONNECTION_STRING" -c "$CREATE_TABLE_SQL"
    else
      psql -h "$HOST" -p "$PORT" -d "$DATABASE" -U "$USER" -c "$CREATE_TABLE_SQL"
    fi

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

check_and_create_table

# Execute the \COPY command
if [ "$USE_CONNECTION_STRING" = true ]; then
  # Use the connection string
  echo "Using connection string: $CONNECTION_STRING"
  psql "$CONNECTION_STRING" -c "\COPY $TABLE_NAME FROM '$CSV_FILE' WITH DELIMITER ',' CSV HEADER QUOTE '\"' ENCODING 'UTF8'"
else
  # Use individual connection details
  psql -h "$HOST" -p "$PORT" -d "$DATABASE" -U "$USER" -c "\COPY $TABLE_NAME ($COLUMNS) FROM '$CSV_FILE' WITH DELIMITER ',' CSV HEADER QUOTE '\"' ENCODING 'UTF8'"
fi

# Check if the command succeeded
if [ $? -eq 0 ]; then
  echo "CSV file '$CSV_FILE' successfully uploaded to table '$TABLE_NAME'."
else
  echo "Error: Failed to upload CSV file to table '$TABLE_NAME'."
fi