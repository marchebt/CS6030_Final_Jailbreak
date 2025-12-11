import csv
import os
from google import genai
# import openai

# --- Configuration ---
INPUT_FILENAME = 'prompt_collection.csv'
OUTPUT_FILENAME = 'response_collection.csv'
API_KEY = '<><><>>'   #Do not upload

client = genai.Client(api_key=API_KEY)
# openai.api_key = API_KEY

def process_question(question_text):
    """This function takes the question text and passes it to the Gemini API to receive a response."""

    response = client.models.generate_content(model="gemini-2.5-flash", contents=f"{question_text}")
    answer = f"{response.text}"
    # response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"{question_text}"}])
    # answer = response['choices'][0]['message']['content']

    return answer

def process_csv(input_file, output_file):
    """Reads input_file, processes the question column, and writes to output_file."""

    # Check if the input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return

    processed_rows = []

    try:
        # 1. Read the input CSV
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.reader(infile)

            # Read the header row separately (assuming the first row is a header)
            try:
                header = next(reader)
                # Add the new 'Answer' column header if it doesn't exist
                if len(header) < 4:
                    header.append('Answer')
                else:
                    # Rename the third column to 'Answer' if it was placeholder/empty
                    header[3] = 'Answer'
                processed_rows.append(header)
            except StopIteration:
                print("The input file is empty.")
                return

            # Process the remaining data rows
            print(f"Processing data from '{input_file}'...")
            for row in reader:
                # Ensure the row has at least 2 columns (ID, Question)
                if len(row) < 3:
                    print(f"Skipping malformed row: {row}")
                    continue

                # Pull the question from the third column (index 2)
                question = row[2]

                # Process the question to get the answer text
                answer = process_question(question)

                # Prepare the row for writing
                new_row = row[:] # Copy the existing row data

                # Either add the answer as a fourth column, or replace the existing fourth column
                if len(new_row) < 4:
                    new_row.append(answer)
                else:
                    new_row[3] = answer # Place the new answer in the 4th column (index 3)

                processed_rows.append(new_row)

    except Exception as e:
        print(f"An error occurred during file reading/processing: {e}")
        return

    # 2. Write the output CSV
    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(processed_rows)

        print(f" Successfully wrote {len(processed_rows) - 1} data rows to '{output_file}'")
    except Exception as e:
        print(f"An error occurred during file writing: {e}")

# --- Execution ---
if __name__ == "__main__":
    process_csv(INPUT_FILENAME, OUTPUT_FILENAME)