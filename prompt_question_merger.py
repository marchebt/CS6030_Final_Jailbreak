import pandas as pd

# --- Configuration ---
FILE_A_PATH = 'prompt_selection.csv'  # Contains the question string to be inserted
FILE_B_PATH = 'jailbreak-prompt.csv' # Contains the prompts with the placeholder
OUTPUT_FILE_PATH = 'prompt_collection.csv'

# Define the columns and placeholder
SOURCE_COLUMN = 'prompt'       # Column in FILE A with the text to insert
PROMPT_COLUMN = 'text'   # Column in FILE B with the text placeholder
PLACEHOLDER = '[INSERT PROMPT HERE]' # The specific string to be replaced in the prompt

def create_cartesian_product_and_replace():
    """
    Creates a Cartesian product (cross-join) between two DataFrames,
    then replaces a placeholder in the prompt column with the question text.
    """
    try:
        # --- Step 1. Read the two CSV files into DataFrames ---
        df_a = pd.read_csv(FILE_A_PATH)[[SOURCE_COLUMN]]
        df_b = pd.read_csv(FILE_B_PATH)[[PROMPT_COLUMN]]

        print(f"Loaded {len(df_a)} unique questions (A) and {len(df_b)} unique templates (B).")

    except FileNotFoundError as e:
        print(f"Error: One of the input files was not found. Please check the path: {e}")
        return

    except KeyError as e:
        print(f"Error: A required column ('{e}') was not found. Please check your column names.")
        return

    # --- Step 2: Create the Cartesian Product (Cross Join) ---

    # Add a temporary 'key' column with a shared value to both DataFrames, and then merge on that key.
    df_a['key'] = 1
    df_b['key'] = 1

    # Merge on the common 'key' column to create all combinations
    merged_df = pd.merge(
        df_a,
        df_b,
        on='key',
        how='outer'
    ).drop('key', axis=1) # Remove the temporary key column

    # Calculate and display the expected total rows
    expected_rows = len(df_a) * len(df_b)
    print(f"Created a Cartesian Product with {len(merged_df)} rows (Expected: {expected_rows}).")

    # --- Step 3: Perform the String Replacement ---

    # Create the final column by replacing the placeholder
    merged_df['Final_Prompt'] = merged_df.apply(
        lambda r: r[PROMPT_COLUMN].replace(PLACEHOLDER, r[SOURCE_COLUMN]),
        axis=1
    )

    # 4. Save the Result
    # Order the columns for a clean output: Question, Prompt, Final Result
    final_output_cols = [SOURCE_COLUMN, PROMPT_COLUMN, 'Final_Prompt']
    merged_df[final_output_cols].to_csv(OUTPUT_FILE_PATH, index=False)

    print(f"\n Success! All {len(merged_df)} combined rows saved to '{OUTPUT_FILE_PATH}'")


# --- Execute the function ---
if __name__ == "__main__":
    create_cartesian_product_and_replace()