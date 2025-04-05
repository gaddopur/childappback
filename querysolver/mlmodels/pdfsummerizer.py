import google.generativeai as genai
from PyPDF2 import PdfReader

# Function to extract text from a PDF
def extract_pdf_text(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


# Main logic for summarization
def summarize_pdf(pdf_path):
    try:
        genai.configure(api_key="AIzaSyBOG0RJcwyQJQVFRvHtg5GzPl3_YUqrf-8")

        # Model generation configuration
        generation_config = {
            "temperature": 0,
            "top_p": 0.05,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            generation_config=generation_config,
        )

        # Extract text from PDF
        pdf_text = extract_pdf_text(pdf_path)
        print("Extracted PDF Text:")

        # Start a chat session
        chat_session = model.start_chat(
            history=[
                {"role": "user", "parts": [{"text": "You are a helpful assistant that summarizes documents, summe"}]}
            ]
        )

        # Send the extracted text to Gemini for summarization
        response = chat_session.send_message(pdf_text)  # Limit to 8000 tokens for safety
        input_tokens = response.usage_metadata.prompt_token_count
        output_tokens = response.usage_metadata.candidates_token_count
        print(f"Input tokens: {input_tokens}, Output tokens: {output_tokens}")
        print("\nSummarized Text:")
        print(response.text)

        return response.text, input_tokens, output_tokens

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    pdf_path = "~\Downloads/\10295939200002.pdf"
    print(pdf_path)
    response, input_tokens, output_tokens = summarize_pdf(pdf_path)
    