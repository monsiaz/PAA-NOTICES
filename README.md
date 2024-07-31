
# Product Information Extractor and SERP Analyzer

## Overview

This Python project is designed to extract product information from a given URL, perform a search using the SerpAPI, and analyze the search results. The project includes functionality to extract the product name, search for related questions, prices, and ratings, and present this information in a structured table format. The results can be saved to a JSON file for further analysis.

## Features

- **Product Name Extraction**: Automatically extracts the product name from the provided URL.
- **SERP Search**: Uses SerpAPI to perform a search based on the extracted product name.
- **Data Extraction**: Extracts related questions, prices, and ratings from the SERP results.
- **Data Analysis**: Calculates the average price and average rating based on the extracted data.
- **Data Presentation**: Displays the extracted and calculated information in a structured table format.
- **Data Storage**: Saves the SERP results to a JSON file for future reference.

## Prerequisites

Before running this project, ensure you have the following installed:

- Python 3.x
- Required Python packages: `requests`, `serpapi`, `json`, `pandas`, `tabulate`

You can install the required Python packages using the following command:

\`\`\`bash
pip install requests serpapi pandas tabulate
\`\`\`

## Setup

1. **Clone the Repository**:

    \`\`\`bash
    git clone https://github.com/your-username/your-repository.git
    cd your-repository
    \`\`\`

2. **Store Your API Key**:
    - Create a file named `keys.txt` in the project directory.
    - Add your SerpAPI key in the following format:

    \`\`\`plaintext
    api_key = "your_serpapi_key"
    \`\`\`

3. **Configure .gitignore**:
    Ensure that `keys.txt` is added to your `.gitignore` file to prevent it from being tracked by Git:

    \`\`\`plaintext
    # Ignore the API key file
    keys.txt
    \`\`\`

## Usage

1. **Extract Product Name and Perform Search**:
    - Modify the URL in the `main` function of `script.py` to the URL of the product you want to analyze.
    - Run the script:

    \`\`\`bash
    python script.py
    \`\`\`

2. **View Results**:
    - The script will print the product name, related questions, average price, and average rating.
    - SERP results will be saved to `serp_results.json`.

## Script Explanation

### `script.py`

- **Imports**: The script imports necessary libraries for HTTP requests, JSON handling, data manipulation, and display.
- **Function Definitions**:
  - `extract_product_name(url)`: Extracts the product name from the given URL using a HTTP GET request.
  - `search_product_on_serpapi(product_name, api_key)`: Performs a SERP search using SerpAPI and returns the results.
  - `extract_serp_info(serp_results)`: Extracts related questions, prices, and ratings from the SERP results.
  - `calculate_averages(prices, ratings, reviews_count)`: Calculates average price and average rating.
  - `save_serp_results(serp_results, filename)`: Saves SERP results to a JSON file.
  - `print_serp_info_as_table(related_questions, prices, avg_price, avg_rating, reviews_count)`: Displays the extracted and calculated information in a table format.

- **Main Execution**:
  - The script extracts the product name from the provided URL.
  - Reads the API key from `keys.txt`.
  - Performs a SERP search using the extracted product name and API key.
  - Extracts related questions, prices, and ratings from the search results.
  - Calculates average price and average rating.
  - Saves the SERP results to a JSON file.
  - Displays the information in a structured table format.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- This project uses the [SerpAPI](https://serpapi.com/) to retrieve search results.
- Data manipulation and presentation are facilitated by the `pandas` and `tabulate` libraries.

## Contributing

Contributions are welcome! Please read the [CONTRIBUTING](CONTRIBUTING.md) guidelines for more information.
