Assignment Details Clear
Your assignment is as follows:
You need to come up with an algorithm that works which can take the following PDF and extract key information from the same for an investor looking to evaluate the company. The investor looks at key elements such as future growth prospects, key changes in the business, key triggers, important information that might have a material effect on next year's earnings and growth. 


In this assignment you are free to use the GPT algorithm and API's of your choice. You are free to use any python libraries and packages to achieve this task. The code should be well documented and cleanly written. 

Length of code is not important, its quality is. Also the quality of the output is important. The code should work across other documents of the same kind and should preferably not have any hard coded logic within it. 

You will need to submit your code as a Google collab link (Please ensure the Google collab link is visible to public for anyone who has the link).


Please use the below link to access the document that needs to be summarized:

[doc link](https://drive.google.com/file/d/1jguXFqGgYkbeF5X9jFJ4ts50m-VJ1rCu/view?usp=sharing)


# Document Summarization and Key Business Information Extraction Pipeline

## ✅ My Approach
## Overview

This pipeline summarizes large documents and extracts key business information relevant to investors. The solution leverages two models:
- **Summarization Model**: `allenai/led-base-16384` for summarizing large chunks of text.
- **Information Extraction Model**: `Gemma-2-2b-it` for identifying key business information from the summarized text.

The workflow divides the document into manageable sections, summarizes each section individually, and consolidates the results for a final business analysis.

---

## Step-by-Step Architecture

### Step 1: Document Chunking

- **Purpose**: Handle large documents that exceed the input capacity of the summarization model.
- **Process**:
  - Split the document into **chunks of up to 2000 words each**.
  - Each chunk is processed independently to avoid memory overload and improve model efficiency.
- **Implementation**:
  - Use a text-processing function to divide the document based on sentence or paragraph boundaries, ensuring coherent chunks.

---

### Step 2: Chunk-wise Summarization with `allenai/led-base-16384`

- **Purpose**: Generate summaries for each document chunk.
- **Model**: `allenai/led-base-16384` (Longformer Encoder-Decoder model) optimized for long input sequences.
- **Process**:
  - Pass each chunk (2000 words max) into the model to obtain a summary.
  - Store each chunk’s summary in a list or concatenate into a single text.
- **Implementation**:
  - Use a loop to feed each chunk into the summarization model.
  - Capture and save each summarized output.

---

### Step 3: Combine Summaries

- **Purpose**: Consolidate individual chunk summaries for a coherent, reduced representation of the entire document.
- **Process**:
  - Concatenate all chunk summaries.
  - Optionally, re-run the combined text through the summarization model for further condensation.
- **Implementation**:
  - Combine summaries into a single string for downstream processing.

---

### Step 4: Key Business Information Extraction with `Gemma-2-2b-it`

- **Purpose**: Extract key information useful to investors.
  - Focus on specific points:
    - **Future Growth Prospects**
    - **Key Changes in Business**
    - **Key Triggers**
    - **Material Impacts on Earnings and Growth**
- **Model**: `Gemma-2-2b-it`, a GPT-based model fine-tuned for business text analysis.
- **Process**:
  - Pass the combined summary into `Gemma-2-2b-it` using a custom prompt to extract the targeted information.
  - The output is a structured set of bullet points relevant to investors.
- **Prompt Design**:
  - Use a clear and specific prompt instructing the model to extract and organize the output according to investor interests.

---

## Final Output

- **Format**: A bullet-point summary of key business insights.
- **Content**: Structured to address investor priorities with insights on growth, strategic changes, potential triggers, and material impacts.
- **Usage**: Final output serves as a concise business overview, suitable for investor evaluation and decision-making.

---

## Summary of the Workflow

1. **Chunk Document** → **Summarize Each Chunk** → **Combine Summaries**
2. **Summarized Document** → **Extract Key Business Information**
3. **Final Output**: Key business insights in investor-focused bullet points.

---

## Advantages of This Approach

- **Efficiently Handles Large Texts**: Chunking allows summarization of documents that exceed the model’s input length.
- **Targeted Business Insights**: Extraction model focuses on specific investor needs, making the final output highly relevant for evaluation.

