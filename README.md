# Document Link Extractor

A Python script that extracts GitHub, GitLab, Bitbucket, and LinkedIn URLs from PDF and Word documents in a recruitment context.

## Overview

This tool processes documents (PDFs and Word files) in the `Applications` directory and extracts repository links and LinkedIn profiles, outputting the results in a markdown table format. It's designed for recruiters or HR teams to quickly identify candidates' online profiles and code repositories from submitted application documents.

## Features

- Processes PDF files using PyPDF2
- Processes Word documents (.doc/.docx) using python-docx
- Automatically converts .doc files to .docx using LibreOffice if needed
- Extracts URLs from:
  - GitHub repositories
  - GitLab repositories  
  - Bitbucket repositories
  - LinkedIn profiles
- Outputs results in markdown table format
- Handles text extraction from both document paragraphs and tables

## Requirements

- Python 3.x
- Required Python packages:
  - PyPDF2
  - python-docx
  - loguru
  - pdfreader
- LibreOffice (for .doc file conversion)

## Installation

```bash
# Install required packages
pip install PyPDF2 python-docx loguru pdfreader

# Or using pipenv (if Pipfile exists)
pipenv install
```

## Usage

1. Create an `Applications` directory in the same folder as the script
2. Place your PDF and Word document files in the `Applications` directory
3. Run the script:

```bash
python check_docs.py
```

### Example Command Line Usage

```bash
# Basic usage
python check_docs.py

# Using pipenv
pipenv run python check_docs.py
```

## Output

The script outputs a markdown table with the following columns:
- **Filename**: Name of the processed document
- **GitHub URL**: Any GitHub/GitLab/Bitbucket repository links found
- **LinkedIn**: LinkedIn profile URLs found

Example output:
```
| Filename | GitHub URL | Linkedin |
| --- | --- | --- |
| john_doe_cv.pdf | github.com/johndoe/portfolio | linkedin.com/in/johndoe |
| jane_smith_resume.docx | gitlab.com/janesmith/projects | linkedin.com/in/jane-smith |
```

## Directory Structure

```
.
   check_docs.py
   Applications/
      candidate1_cv.pdf
      candidate2_resume.docx
      candidate3_portfolio.doc
   README.md
```

## Error Handling

- If a Word document fails to open, the script attempts to convert it using LibreOffice
- PDF processing errors are logged but don't stop execution
- Files that can't be processed are skipped with error logging

## Limitations

- PDF text extraction quality depends on the PDF format (scanned images may not work well)
- Requires LibreOffice for .doc file conversion
- Only processes files in the `Applications` directory and its subdirectories