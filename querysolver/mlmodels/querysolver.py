import google.generativeai as genai



def answer_question_simple(question, api_key):
    """
    Answers a given question using the Gemini API in simple language.

    Parameters:
        question (str): The question to be answered.
        api_key (str): Your Gemini API key.

    Returns:
        str: The answer to the question.
    """
    try:
        # Configure the API
        genai.configure(api_key=api_key)

        # Model generation configuration
        generation_config = {
            "temperature": 0,
            "top_p": 0.05,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }

        # Initialize the Gemini model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash-8b",
            generation_config=generation_config,
        )

        # Build the prompt for a simple, understandable answer
        prompt = (
            f"Answer the following question in very simple words so that an school kid can understand it:\n"
            f"Question: {question}\n"
            f"Answer:"
        )

        # Generate the response
        response = model.generate_content(prompt)

        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"
    

    # Example usage
if __name__ == "__main__":
    question = "What is artificial intelligence?"
    answer = answer_question_simple(question)
    print(answer)


# querySolver()



# querySolverTest:
#  mock(model).generate_content("Answer the following question in very simple words so that an school kid can understand it:\nQuestion: What is artificial intelligence?\nAnswer:") >> "hello"

