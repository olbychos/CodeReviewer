import os
import subprocess
import pathlib
from typing import List, Optional
from litellm import completion
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Constants and Configuration
LLM_PROVIDER = "openai"
LLM_MODEL = "gpt-4o-mini"
OUTPUT_DIR = pathlib.Path("code_review_output")
REPO_PATH = pathlib.Path("path/to/your/repo")
BRANCH_NAME = "your-branch-name"

SYSTEM_PROMPT = f"""
You are a helpful code reviewer tasked with providing concise and specific comments on a given git diff. Your goal is to identify potential issues, suggest improvements, and highlight good practices in the code changes.

To complete this task, follow these steps:

1. Carefully analyze the git diff, paying attention to:
   - Added, modified, and deleted lines of code
   - Changes in logic or functionality
   - Potential bugs or errors
   - Code style and formatting
   - Performance implications
   - Security concerns

2. When writing your comments, make sure they are:
   - Concise: Keep your comments brief and to the point
   - Specific: Reference exact lines or sections of code
   - Constructive: Offer suggestions for improvement when pointing out issues
   - Balanced: Highlight both positive aspects and areas for improvement

3. Organize your review comments as follows:
   - Start with a brief summary of the overall changes
   - Group related comments together
   - Use bullet points for individual comments
   - If applicable, prioritize comments based on their importance or impact

4. Include the following types of comments when relevant:
   - Potential bugs or logical errors
   - Suggestions for code optimization or simplification
   - Recommendations for improving readability or maintainability
   - Observations about adherence to coding standards or best practices
   - Questions about unclear code or design decisions
   - Positive feedback on well-implemented features or improvements

5. Avoid:
   - Nitpicking minor stylistic issues unless they significantly impact readability
   - Making assumptions about the broader context of the code without clear evidence
   - Using overly technical jargon without explanation

6. Format your review as follows:
   <review>
   [Your review comments here, following the guidelines above]
   </review>

Remember to maintain a professional and constructive tone throughout your review. Your goal is to help improve the code quality and support the developer's growth.
"""


class GitDiffTool:
    def run(self, repo_path: pathlib.Path, branch_name: str) -> Optional[str]:
        """Retrieves and saves the Git diff, handling different main branch names."""

        diff_file = OUTPUT_DIR / "diff.txt"
        try:
            # 1. Try getting the default branch name
            try:
                main_branch_process = subprocess.run(
                    ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
                    cwd=repo_path,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                main_branch = main_branch_process.stdout.strip().split("/")[-1]
            except subprocess.CalledProcessError:
                main_branch = "main" 

            # 2. Get the diff using the determined main branch
            diff_process = subprocess.run(
                ["git", "diff", main_branch, branch_name],
                cwd=repo_path,
                capture_output=True,
                text=True,
                check=True,
            )
            diff = diff_process.stdout

            with open(diff_file, "w") as f:
                f.write(diff)

            return str(diff_file)

        except subprocess.CalledProcessError as e:
            logger.error(f"Git diff failed: {e.stderr}")
            return None
        except ValueError as e:
            logger.error(f"Invalid input: {e}")
            return None



class CodeReviewAgent:
    def __init__(self, llm_model: str):
        self.llm_model = llm_model
        self.diff_tool = GitDiffTool()

    def review(self, repo_path: pathlib.Path, branch_name: str):
        """Performs the code review."""

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True) 

        diff_file_path = self.diff_tool.run(repo_path, branch_name)
        if not diff_file_path:
            return  

        with open(diff_file_path, "r") as f:
            diff = f.read()

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"```<git diff>\n{diff}\n<\git diff>```"},
        ]

        try:
            response = completion(
                messages=messages,
                model=self.llm_model,
                temperature=0.2,
                max_tokens=4000,
            )
            review_comments = response.choices[0].message.content

            comments_file = OUTPUT_DIR / "comments.txt"
            with open(comments_file, "w") as f:
                f.write(review_comments)

            logger.info(f"Code review comments saved to {comments_file}")

        except Exception as e:
            logger.error(f"Error generating or saving comments: {e}")



if __name__ == "__main__":
    agent = CodeReviewAgent(llm_model=LLM_MODEL)
    agent.review(REPO_PATH, BRANCH_NAME)