# Uncomment this to install the packages (run in terminal)
#!pip install -U -q PyMuPDF transformers 
import os
import fitz  # PyMuPDF
import re    # For cleaning text
import json
import torch # For using 'cuda'
from transformers import pipeline # For using the transformer models from HF hub
from IPython.display import Markdown, display # For displaying the Final output in a structured format

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        text += page.get_text("text")
    # Post-process text to remove excessive whitespace
    lines = text.split('\n')
    lines = [line.strip() for line in lines if line.strip()]
    formatted_text = '\n'.join(lines)
    return formatted_text

def clean_extracted_text(pdf_path):
    extracted_text = extract_text_from_pdf(pdf_path)
    # Remove non-alphanumeric characters except for common punctuation and newlines
    text = re.sub(r'[^A-Za-z0-9\s,.\'@|\-\n]', '', extracted_text)
    # Remove extra spaces
    text = re.sub(r'\s+', ' ', text)
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    # Strip leading and trailing spaces and newlines
    text = text.strip()
    return text

# Function to split text into chunks of max 2000 words
def split_text_into_chunks(text, max_words=2000):
    words = text.split()
    total_words = len(words)
    print(f"Total words in document: {total_words}")

    # Calculate the number of chunks
    chunks = []
    for i in range(0, total_words, max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
    
    print(f"Total number of chunks created: {len(chunks)}")
    return chunks

# Initialize the Hugging Face summarization pipeline
summarizer = pipeline("summarization", model="allenai/led-base-16384")

# Summarization function for each chunk
def summarize_text_chunks(chunks):
    summarized_text = ""
    for idx, chunk in enumerate(chunks):
        print(f"Summarizing chunk {idx + 1}...")
        summary = summarizer(chunk, max_length=80, do_sample=False)
        summarized_text += summary[0]['summary_text'] + "\n"  # Add a newline between summaries

    return summarized_text


# Main process to clean text, split, and summarize
def process_pdf_for_summarization(pdf_path):
    # Extract and clean text from PDF
    text = clean_extracted_text(pdf_path)
    
    # Split text into manageable chunks of 2000 words
    text_chunks = split_text_into_chunks(text, max_words=2000)
    
    # Summarize each chunk and combine the results
    complete_summary = summarize_text_chunks(text_chunks)
    return complete_summary

# Run the function and print the complete summary
pdf_path = 'doc.pdf'  # Uplod the document and pass the file path (in this case passing the file name as the file is in same directory)
output_summary = process_pdf_for_summarization(pdf_path)
print("Output Summary 👇",'\n',output_summary)

from huggingface_hub import login   
login("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")
print("Logged in to Hugging Face Hub!")

pipe2 = pipeline(
    "text-generation",
    model="google/gemma-2-2b-it",
    model_kwargs={"torch_dtype": torch.bfloat16},
    device="cuda",
)

messages = [
    {"role": "user",
    "content": f"""Context:\n {output_summary}\n Instructions:\n Based on the above context, please extract and organize the key information an investor would need to evaluate this company in proper markdown format. Present the information in bullet points, focusing on:
    Future growth prospects: Any trends, opportunities, or strategies that suggest growth potential for the company.
    Key changes in the business: Significant changes in business operations, structure, or strategy.
    Key triggers: Events or factors that could impact the company’s performance or market position.
    Material impacts on earnings and growth: Important details that could significantly affect next year’s financial performance. """
    },
]

outputs = pipe2(messages, max_new_tokens=1024)
assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
display(Markdown(assistant_response))