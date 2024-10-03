# AI-Powered Code Review Tool

This tool uses the power of Large Language Models (LLMs) to provide automated code reviews for your Git repositories.  It analyzes the diff between a specified branch and the main branch (usually `main` or `master`), generating insightful comments and suggestions for improvement.

## Features

* **Automated Code Review:**  Quickly get feedback on your code changes without manual intervention.
* **LLM-Powered Analysis:** Leverages the advanced reasoning capabilities of LLMs to identify potential issues, suggest improvements, and highlight good practices.
* **Clear and Concise Comments:**  Generates well-structured review comments formatted in Markdown for easy readability.
* **Customizable:**  Configure the LLM model, temperature, and maximum tokens to fine-tune the review process.
* **Easy to Use:** Simply provide the repository path and branch name to initiate the review.

## Requirements

* `litellm` library:  `pip install litellm`
* Git:  Make sure Git is installed and accessible in your environment.
* An API key for your chosen LLM provider (e.g., OpenAI).

## Installation

1. Clone this repository: `git clone <repository_url>`
2. Navigate to the project directory: `cd <project_directory>`
3. Install the required libraries: `pip install -r requirements.txt`

## Usage

1. **Configuration:**
   - Set the `LLM_PROVIDER` and `LLM_MODEL` variables in the script to your preferred provider and model.
   - Update `REPO_PATH` and `BRANCH_NAME` to point to your repository and the branch you want to review.
2. **Run the script:** `python code_review_agent.py` (replace `code_review_agent.py` with the actual script name).
3. **Review the output:** The generated code review comments will be saved in `code_review_output/comments.txt`. The raw diff will be saved in `code_review_output/diff.txt`.

## Example

```bash
# Set environment variables (recommended)
export LLM_PROVIDER="openai"
export OPENAI_API_KEY="your_openai_api_key" # Or other provider's key
export LLM_MODEL="gpt-4o" 

# Run the script
python code_review_agent.py  # Replace with your script name

# Provide repository path and branch name when prompted if not set as constants