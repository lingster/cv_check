import os
from PyPDF2 import PdfFileReader
import zipfile
import os
import re
import pdfreader 
from loguru import logger
import docx

import glob
import subprocess

#for doc in glob.iglob("*.doc"):
#    subprocess.call(['soffice', '--headless', '--convert-to', 'docx', doc])

# Re-initialize results list for Markdown table
markdown_table = ["| Filename | GitHub URL | Linkedin | ", "| --- | --- | --- |"]

unzip_dir = 'Applications'


def process_word(fn):
	# Open the Word document
    try:
        try:
            doc = docx.Document(fn)
        except Exception as ex:
            logger.error(f"{ex}: try converting")
            subprocess.call(['soffice', '--headless', '--convert-to', 'docx', fn])
            doc = docx.Document(fn)

        full_text = []

        # Loop through paragraphs 
        for para in doc.paragraphs:
            full_text.append(para.text)
            
        # Loop through tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    full_text.append(cell.text)
                    
        # Join all paragraphs and table texts
        full_text = '\n'.join(full_text)
        return full_text
    except Exception as ex:
        logger.error(ex)
        return ''

def process_pdf(fn):
	# Read PDF content
    try:
        logger.info(f'reading: {pdf_path}')
        pdf_reader = PdfFileReader(open(pdf_path, 'rb'))
        #pdf_reader = pdfreader.SimplePDFViewer(open(pdf_path, 'rb'))
        pdf_text = ''
        for page_num in range(pdf_reader.getNumPages()):
            page = pdf_reader.getPage(page_num)
            pdf_text += page.extractText()
        return pdf_text
    except:
        return ''

# Loop through unzipped PDF files
for root, dirs, files in os.walk(unzip_dir):
    for pdf_file in sorted(files):
        pdf_path = os.path.join(root, pdf_file)
        logger.info(f"processing {pdf_path}")
        if pdf_file.lower().endswith('.doc') or pdf_file.lower().endswith('docx'):
            text = process_word(pdf_path)
        elif not pdf_file.lower().endswith('.pdf'):
            continue  # Skip non-PDF files
        else:
            text = process_pdf(pdf_path)
        
        # Extract GitHub links, ignoring case
        gitlab = re.findall(r'gitlab\.com/[\w/-]+', text, re.IGNORECASE)
        bitbucket = re.findall(r'bitbucket\.com/[\w/-]+', text, re.IGNORECASE)
        github_links = re.findall(r'github\.com/[\w/-]+', text, re.IGNORECASE)
        linkedin = re.findall(r'linkedin\.com/[\w/-]+', text, re.IGNORECASE)
        if github_links or bitbucket or gitlab:
            repo = f"{ gitlab[0] if gitlab else '' } {bitbucket[0] if bitbucket else ''} {github_links[0] if github_links else ''}"
            markdown_table.append(f"| {pdf_file} | {repo} | {linkedin[0] if linkedin else ''} | ")

        #if github_links:
        #    print(github_links)
        #    for github_link in github_links:
        #        markdown_table.append(f"| {pdf_file} | {github_link} | | ")
        #if linkedin:
        #    print(linkedin)
        #    for linkedin in github_links:
        #        markdown_table.append(f"| {pdf_file} | | {linkedin} |")

# Join markdown table rows into a single string
markdown_table_str = '\n'.join(markdown_table)
print(markdown_table_str)


