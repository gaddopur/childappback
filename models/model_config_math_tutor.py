"""
Configuration for Math Tutor AI model
Contains all model-related settings and prompts
"""

MODEL_NAME = "models/gemini-1.5-pro-001"

MODEL_CONFIG = {
    "temperature": 0.1,
    "top_p": 0.3,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

MATH_PROMPT_TEMPLATE = """Solve this mathematics problem for an Indian student. Follow these guidelines:

Problem: {problem}

Generate JSON strictly for your response these exact keys:
- "problem_analysis": Break down problem components
- "solution_strategies": List different approaches (up to 3)
- "mathematical_steps": Clean mathematical working with brief explanations in parentheses
- "detailed_explanations": Thorough reasoning for each logical step
- "common_mistakes": Common exam errors
- "answer": Final proven statement/result
- "key_topics": Relevant CBSE topics
- "diagram_search_queries": Query which can be searched on a the web to get most relevant image according to question and currently generated solution

Step Formatting Rules:
1. Each step must end with explanation in parentheses
2. Explanations should be 3-7 words long
3. Use this exact format: [operation] (reason)
4. Never number steps yourself
5. Include all algebraic manipulations

Step Development Rules:
1. Break down EVERY algebraic manipulation into individual steps
2. Show intermediate calculations for limit evaluations
3. Never combine multiple operations in one step
4. Include verification steps where applicable
5. For integrals:
   - Show term-by-term integration
   - Display limit substitution separately for each term
   - Show fraction simplification process

Rules:
1. For proofs:
   - Show ALL algebraic manipulations
   - State assumptions explicitly (like r ≠ 1)
   - Use ⇒ for logical implications
   - Include verification steps if applicable
2. Use × for multiplication, ÷ for division
3. Number steps only if showing multiple methods
4. Keep explanations under 15 words per step
5. Include 2-3 image search queries that would help find explanatory diagrams for this problem. Format queries as: [IMAGE_SEARCH: your search query]

Example Detailed Integration Response:
{{
    "problem_analysis": "Calculate definite integral of polynomial function",
    "solution_strategies": [
        "Direct Integration (Primary)",
        "Riemann Sum Approach",
        "Numerical Approximation"
    ],
    "mathematical_steps": [
        "Expand integrand: x² + x",
        "Split integral: ∫₀² x² dx + ∫₀² x dx",
        "Integrate x²: [x³/3] from 0 to 2",
        "Integrate x: [x²/2] from 0 to 2",
        "Calculate upper limit for x³/3: (2³)/3 = 8/3",
        "Calculate upper limit for x²/2: (2²)/2 = 4/2 = 2",
        "Sum upper limits: 8/3 + 2 = 8/3 + 6/3 = 14/3",
        "Verify lower limits: (0³)/3 + (0²)/2 = 0",
        "Final result: 14/3 - 0 = 14/3"
    ],
    "detailed_explanations": [
        "Separate polynomial into individual terms",
        "Apply linearity of integration",
        "Use power rule for x² integration",
        "Use power rule for x integration",
        "Substitute upper limit into cubic term",
        "Substitute upper limit into quadratic term",
        "Convert to common denominator for addition",
        "Confirm lower limit evaluation",
        "Combine all components for final answer"
    ],
    "common_mistakes": [
        "Forgetting to split terms before integration",
        "Errors in fraction addition",
        "Miscalculating exponents"
    ],
    "diagram_search_queries": [
            "perfect square number line diagram", 
            "quadratic equation graphical representation"
        ],
    "answer": "14/3",
    "key_topics": ["Integral Calculus", "Definite Integrals"]
}}"""

CLASSIFICATION_PROMPT_TEMPLATE = """Classify the user's message in this math conversation:
1 = New problem (complete question)
2 = Follow-up (about current problem)
3 = Unrelated (not math)

Rules:
1. Assume the message is a follow-up unless clearly an independent, new question.
2. Assume the message is related to math unless clearly irrelevant to math.
3. New problem - if contains a complete question with numbers, equations, or new context unrelated to the current discussion.
4. Follow-up - if it references the previous steps, asks "why", "how", or discusses specific parts of the current problem or solution.
5. Unrelated - for questions or statements that are clearly outside the scope of math.

Respond ONLY with 1, 2, or 3. No explanations.

Recent chat:
{history_snippet}

Current Query: {message}
Classification:"""
