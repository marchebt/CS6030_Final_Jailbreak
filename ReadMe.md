
-----

# Python CSV Processing Utilities

This repository contains three Python scripts designed for CSV manipulation and automated LLM api prompting. All scripts require input CSV files to be present in the same directory for execution.

##  Prerequisites

You must have Python installed. The scripts rely on the widely used `pandas` library for data processing. The prompt_cycle script relies on the `google-genai` or `openai` library for automating prompts.

Install the required libraries using pip:

```bash
pip install pandas
pip install google-genai
pip install openai
```

-----

## 1\. `prompt_question_merger.py` (Cross-Join Combinator)

This script performs a **Cartesian Product (Cross-Join)** between two separate CSV files. It combines every row from the first file (questions) with every row from the second file (prompts) and inserts the question text into the prompt using a placeholder marker.

### Purpose

To generate all possible combinations of questions and prompts, and automatically populate the prompts. If you have $M$ questions and $N$ prompts, the output will have $M \times N$ rows.

### Configuration (Inside the Script)

| Variable | Description                                               | Example Value             |
| :--- |:----------------------------------------------------------|:--------------------------|
| `FILE_A_PATH` | Path to the CSV with the text to be inserted (Questions). | `'prompt_selection.csv'`  |
| `FILE_B_PATH` | Path to the CSV with the text template.                   | `'jailbreak-prompt.csv'`  |
| `OUTPUT_FILE_PATH` | The name for the resulting combined CSV file.             | `'prompt_collection.csv'` |
| `SOURCE_COLUMN` | The column in FILE A with the text to insert.             | `'prompt'`                |
| `PROMPT_COLUMN`| The column in FILE B with the text template.              | `'text'`                  |
| `PLACEHOLDER` | The exact marker string to be replaced in the prompts.    | `'[INSERT PROMPT HERE]'`  |

### How to Use

1.  **Prepare Data:**

    * Create `prompt_selection.csv` containing the text you want to insert.
    * Create `jailbreak-prompt.csv` containing the prompts that use the `PLACEHOLDER`.

2.  **Run:** Execute the script from your terminal:

    ```bash
    python prompt_question_merger.py
    ```

3.  **Result:** The output file (`prompt_collection.csv`) will be generated containing all combinations, with the final populated prompt in the `Final_Prompt` column.

-----

## 2\. `prompt_cycle.py` (One-to-One Alignment)

This script reads a single CSV file, reaches out to a Gemini Flash 2.5 API to process the question column as a prompt, and outputs the resulting response into a new 'Answer' column.
<br> Note, depending on your Google AI Studio Tier level, you will likely be rate limited depending on the number of rows/prompts. A workaround for this is to break the csv into multiple
<br> smaller csv files, run the script on the smaller files spaced out across multiple hours/days, and then merge the resulting files into one final collection.
<br> This script should easily be modifiable for use with other LLMs; simply change which library is imported, update the API_KEY to one from that organization, update what the 'client' 
<br> variable is set to based on the desired LLM API, and update the process_question function pass the prompt to the desired LLM API, and extract the text from the response.

### Purpose

To read the `Final_Prompt` column from a source file, reach out to an LLM API using `process_question()` and pass in the prompt, and place the result in the `Answer` column of the same row.

### Configuration (Inside the Script)

The following variables must be configured at the top of the file:

| Variable          | Description                                                 | Example Value                                                             |
|:------------------|:------------------------------------------------------------|:--------------------------------------------------------------------------|
| `INPUT_FILENAME`  | The name of the source CSV file.                            | `'prompt_collection.csv'`                                                 |
| `OUTPUT_FILENAME` | The name for the resulting CSV file.                        | `'response_collection.csv'`                                               |
| `API_KEY`         | The api key for Gemini, assuming Gemini is the desired LLM. | `<39 character string with unique chars, typically starting with AlzaSy>` |

### How to Use

1.  **Prepare Data:** Create your input file (e.g., `prompt_collection.csv`) with the required column (`Final_Prompt`). This can be generated using the prompt_question_merger.py script above.

2.  **Run:** Execute the script from your terminal:

    ```bash
    python prompt_cycle.py
    ```

3.  **Result:** The output file (`response_collection.csv`) will be generated with the new `Answer` column filled.

4. **Changing LLMs:** Placeholder code for accessing OpenAI's ChatGPT API is left in the file, commented out. This can be used to demonstrate the script can easily be tweaked to work with other LLMs.
-----

## 3\. `response_post_processing.py` (Substring Search and Categorization)

This script is designed to analyze text data within a single CSV column and flag (categorize) rows that contain specific target phrases. It is useful for identifying generic chatbot apologies, or specific error messages.
<br> Such generic apologies or error messages indicate the prompt did not successfully jailbreak the LLM's security provisions and generate a malicious response.

### Purpose

To load responses from a single input file and create a new column (`Jailbroken`) that flags a row as **`Flagged`** if the text in the `Answer` column contains any of the predefined substrings (case-insensitively). Otherwise, the row is marked as **`Clean`**.

### Configuration (Inside the Script)

| Variable | Description | Example Value |
| :--- | :--- | :--- |
| `INPUT_FILE_PATH` | Path to the source CSV file containing the responses. | `'response_collection.csv'` |
| `OUTPUT_FILE_PATH` | The name for the resulting processed CSV file. | `'response_processed.csv'` |
| `PROMPT_COLUMN` | The exact name of the column containing the text to be searched. **(Must exist in the input file)** | `'Answer'` |
| `PROCESS_COLUMN` | The name of the new column that will hold the flag (`Flagged` or `Clean`). | `'Jailbroken'` |
| `SEARCH_TEXTS` | A **Python list** of strings to search for within the `PROMPT_COLUMN`. The search is case-insensitive. | `['I cannot provide', 'I am sorry']` |

### How to Use

1.  **Prepare Data:** Ensure your input file (`response_collection.csv`) is present and contains the column specified by `PROMPT_COLUMN` (e.g., the `Answer` column).

2.  **Define Terms:** Update the `SEARCH_TEXTS` list with all the specific phrases you want to flag.

3.  **Run:** Execute the script from your terminal:

    ```bash
    python response_post_processing.py
    ```

4.  **Result:** The output file (`response_processed.csv`) will be generated, containing the original `Answer` column and the new `Jailbroken` flag column.

---