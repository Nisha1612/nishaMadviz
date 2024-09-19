from transformers import BartTokenizer, BartForConditionalGeneration
import PyPDF2

# Load BART model and tokenizer
tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')

# Function to summarize a single chunk of text
def summarize_text_chunk(text_chunk):
    inputs = tokenizer.encode("summarize: " + text_chunk, return_tensors="pt", max_length=1024, truncation=True)
    summary_ids = model.generate(inputs, max_length=150, min_length=40, length_penalty=2.0, num_beams=4, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

# Function to handle large PDFs by chunking long texts
def summarize_pdf(file_path, chunk_size=1024):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()

    # Tokenize and break text into chunks of approximately chunk_size tokens
    text_chunks = []
    tokens = tokenizer.encode(text)
    for i in range(0, len(tokens), chunk_size):
        chunk_tokens = tokens[i:i + chunk_size]
        text_chunk = tokenizer.decode(chunk_tokens, skip_special_tokens=True)
        text_chunks.append(text_chunk)

    # Summarize each chunk and combine the results
    final_summary = ""
    for chunk in text_chunks:
        chunk_summary = summarize_text_chunk(chunk)
        final_summary += chunk_summary + " "
    
    return final_summary.strip()
