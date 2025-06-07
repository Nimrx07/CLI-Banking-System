#!/bin/bash

#README: Run this by typing "bash daily.sh [day]" where [day] is the day of the week (numbered 0 to 6).
# For the first day's sessions you would type "bash daily.sh 0" and then increment by one each time.
# 
# In order to work this requires the text files to be located in the proper file structure.
# Input session files NEED to be located in a 'sessions' subdirectory for this shell script to find them. 
# Each file has to be named according to the format "day0_session1.txt" representing the first
# session of day 0, incrementing the numbers for each day and for each session of that day.
# Current accounts files MUST be located in a subdirectory called 'accounts'. Each text file in
# that folder follows the naming convention "current_dayx" where x is the day expressed as a number (0-6)
# Both this and the weekly script were functioning fine on my system so feel free to reach out to me
# (Adam Peltenburg) if you're encountering any issues.


DAY=$1

# Define paths
CURRENT_ACCOUNTS="accounts/current_day${DAY}.txt"
MERGED_TX="output/merged_day${DAY}.txt"
MASTER_ACCOUNTS="output/master_day${DAY}.txt"
NEXT_CURRENT_ACCOUNTS="accounts/current_day$((DAY + 1)).txt"

# Ensure output directory exists
mkdir -p output

# Clear merged file
> "$MERGED_TX"

echo "=== Running Day $DAY ==="

# Process each session file
for SESSION in sessions/day${DAY}_session*.txt; do
  SESSION_NAME=$(basename "$SESSION" .txt)
  echo "Running front end with $SESSION"

  # Front end writes to temp_tx.txt
  python front_end.py temp_tx.txt "$CURRENT_ACCOUNTS" < "$SESSION"
  
  # Append to merged transaction file
  cat temp_tx.txt >> "$MERGED_TX"
done

# Call the backend processor
echo "Running back end for Day $DAY"
python backend.py "$CURRENT_ACCOUNTS" "$MERGED_TX" "$MASTER_ACCOUNTS" "$NEXT_CURRENT_ACCOUNTS"

# Clean up temp file
rm temp_tx.txt
