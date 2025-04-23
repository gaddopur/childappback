import os
import re
import asyncio
import logging
import time
from threading import RLock
from typing import Optional, Tuple, List, Dict
from pydantic import BaseModel, Field
import google.generativeai as genai
from google.api_core import exceptions
from api_key_manager import APIKeyManager

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("math_solver_debug.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class MathSolution(BaseModel):
    """Pydantic model for structured math solution"""
    problem_analysis: str = Field(..., description="Initial breakdown of the problem")
    solution_strategy: str = Field(..., description="Chosen approach and reasoning")
    mathematical_steps: List[str] = Field(..., description="Concise mathematical steps only")
    detailed_explanations: List[str] = Field(..., description="Detailed reasoning behind steps")
    common_mistakes: List[str] = Field(..., description="Common exam mistakes")
    answer: str = Field(..., description="Final answer in plain format")
    key_topics: List[str] = Field(..., description="CBSE-relevant study topics")

    def formatted_output(self) -> str:
        """Generate student-friendly formatted string"""
        steps_str = "\n".join([f"Step {i+1}: {step}" for i, step in enumerate(self.mathematical_steps)])
        explanations_str = "\n\n".join(self.detailed_explanations)
        mistakes_str = "\n".join(f"✗ {mistake}" for mistake in self.common_mistakes)
        topics_str = "\n".join(f"• {topic}" for topic in self.key_topics)
        
        return f"""📚 Math Problem Solution 📚
        
🔍 Problem Analysis:
{self.problem_analysis}

🎯 Solution Strategy:
{self.solution_strategy}

🔢 Step-by-Step Solution:
{steps_str}

📖 Detailed Explanations:
{explanations_str}

❌ Common Mistakes:
{mistakes_str}

✅ Final Answer: {self.answer}

📚 Recommended Topics to Study:
{topics_str}"""

class MathValidationError(Exception):
    """Custom exception for invalid math problems."""
    pass

class MathSolver:
    """
    Math Problem Solver for Indian Curriculum
    
    Features:
    - Unicode-based mathematical notation
    - CBSE/State Board aligned explanations
    - Step-by-step solutions in simple English
    - Common Indian error patterns highlighted
    """
    
    def __init__(self, api_key_manager: APIKeyManager = None):
        self.api_key_manager = api_key_manager or APIKeyManager()
        self._lock = RLock()
        self.model_cache = {}
        self.model_config = {
            "temperature": 0.1,
            "top_p": 0.3,
            "top_k": 40,
            "max_output_tokens": 8192,
            "response_mime_type": "text/plain",
        }
        logger.info("Initializing MathSolver for Indian student needs")

    def _get_llm_response(self, prompt: str, max_retries: int) -> Optional[str]:
        """Robust LLM communication with retries."""
        logger.debug(f"Attempting LLM response generation (max retries: {max_retries})")
        
        for attempt in range(1, max_retries + 1):
            api_key = self.api_key_manager.get_available_key()
            if not api_key:
                logger.warning("No valid API keys available")
                continue

            try:
                logger.debug(f"Attempt {attempt} with key ending ...{api_key[-4:]}")
                model = self._get_model(api_key)
                if not model:
                    continue

                logger.info(f"Sending prompt to LLM:\n{prompt}")
                response = model.generate_content(
                    prompt, 
                    request_options={'timeout': 60}
                )
                self.api_key_manager.update_key_status(api_key, success=True)
                logger.debug("LLM response received successfully")
                return response.text

            except exceptions.ResourceExhausted as e:
                logger.warning(f"Rate limit exceeded: {str(e)}")
                self._handle_retry(api_key, attempt, max_retries, "API quota exceeded")
            except exceptions.GoogleAPIError as e:
                logger.error(f"API Error: {str(e)}")
                self._handle_retry(api_key, attempt, max_retries, str(e))
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                self._handle_retry(api_key, attempt, max_retries, "Generic error")

        logger.error(f"Failed after {max_retries} retries")
        return None

    def _handle_retry(self, api_key: str, attempt: int, max_attempts: int, error: str):
        """Enhanced retry handler with detailed logging"""
        logger.warning(f"Retry {attempt}/{max_attempts} | Error: {error}")
        self.api_key_manager.update_key_status(api_key, success=False)
        backoff_time = 2 ** attempt
        logger.info(f"Backing off for {backoff_time} seconds")
        time.sleep(backoff_time)

    def _get_model(self, api_key: str) -> Optional[genai.GenerativeModel]:
        """Retrieve or create configured Gemini model."""
        try:
            if api_key in self.model_cache:
                logger.debug(f"Using cached model for key ending ...{api_key[-4:]}")
                return self.model_cache[api_key]

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel(
                model_name="models/gemini-1.5-pro-001",
                generation_config=self.model_config
            )

            with self._lock:
                self.model_cache[api_key] = model

            logger.info(f"Created new model instance for key ending ...{api_key[-4:]}")
            return model

        except Exception as e:
            logger.error(f"Model creation failed: {str(e)}")
            return None

    def solve(self, problem: str, max_retries: int = 3) -> Optional[MathSolution]:
        """Main solving interface with enhanced logging."""
        logger.info(f"Received problem: {problem}")
        start_time = time.time()
        
        try:
            self._validate_math_problem(problem)
            prompt = self._build_indian_style_prompt(problem)
            
            logger.debug(f"Generated prompt:\n{prompt}")
            raw_response = self._get_llm_response(prompt, max_retries)
            
            if not raw_response:
                logger.error("No response received from LLM")
                return None
                
            logger.debug(f"Raw LLM response:\n{raw_response}")
            return self._parse_response(raw_response)

        except Exception as e:
            logger.error(f"Solving process failed: {str(e)}")
            return None
        finally:
            logger.info(f"Processing time: {time.time()-start_time:.2f} seconds")

        
    def _build_indian_style_prompt(self, problem: str) -> str:
        """Create structured prompt with output format"""
        return f"""Solve this mathematics problem for an Indian student. Follow these guidelines:

Problem: {problem}

Format your response as JSON with these exact keys:
- "problem_analysis": Break down problem components
- "solution_strategy": Explain chosen approach
- "mathematical_steps": Clean mathematical working with brief explanations in brackets
- "detailed_explanations": Reasoning behind each step
- "common_mistakes": Common exam errors
- "answer": Final answer
- "key_topics": Relevant CBSE topics

Rules:
1. Add short explanations in () after each mathematical step
2. Keep step explanations under 10 words
3. Use × for multiplication, ÷ for division
4. Number all steps sequentially
5. Final answer as comma-separated values

Example Response:
{{
    "problem_analysis": "Find positive integers n where n² + 20n is a perfect square",
    "solution_strategy": "Complete the square and factor analysis",
    "mathematical_steps": [
        "n² + 20n = m² (Let m be an integer)",
        "n² + 20n + 100 = m² + 100 (Add 100 to both sides)",
        "(n + 10)² = m² + 100 (Perfect square form)",
        "(n + 10)² - m² = 100 (Rearrange terms)",
        "(n + 10 + m)(n + 10 - m) = 100 (Factor difference of squares)",
        "Factor pairs: (1,100), (2,50), (4,25), (5,20), (10,10)",
        "Solve systems for each pair (Find n values)"
    ],
    "detailed_explanations": [
        "Set expression equal to perfect square k²",
        "Complete the square by adding 100 to both sides",
        "Apply difference of squares formula",
        "Find all factor pairs of constant term",
        "Solve resulting equations for each factor pair"
    ],
    "common_mistakes": [
        "Missing factor pairs",
        "Not verifying positive integer solutions"
    ],
    "answer": "5, 16, 24",
    "key_topics": ["Quadratic Equations", "Number Theory"]
}}"""

    def _parse_response(self, response: str) -> Optional[MathSolution]:
        """Parse and validate LLM response"""
        try:
            # Extract JSON from response
            json_str = re.search(r'\{.*\}', response, re.DOTALL).group()
            logger.debug(f"Extracted JSON: {json_str}")
            
            # Clean and validate
            cleaned_json = json_str.replace("\\n", "").strip()
            return MathSolution.model_validate_json(cleaned_json)
        
        except Exception as e:
            logger.error(f"Parsing failed: {str(e)}")
            return None

    def _extract_boxed_answer(self, text: str) -> str:
        """Extract LaTeX boxed answer with validation."""
        match = re.search(r"\\boxed{([^}]+)}", text)
        if not match:
            logger.warning("No boxed answer found in response")
            return "Answer not formatted properly"
        return f"\\boxed{{{match.group(1)}}}"

    def _validate_math_problem(self, problem: str):
        """Enhanced validation for Indian context."""
        if not problem:
            raise MathValidationError("Empty problem statement")
            
        if len(problem) > 2000:
            raise MathValidationError("Problem too long (max 2000 characters)")
            
        if not re.search(r"[०-९]|\b(प्रश्न|सिद्ध|हल|ज्ञात)\b", problem, re.IGNORECASE):
            logger.debug("No Indian language markers found, proceeding with English validation")
            
        math_triggers = r"\b(सिद्ध कीजिए|ज्ञात कीजिए|मान ज्ञात|रैखिक समीकरण)\b|[\+−×÷=π√]"  # Includes Indian operators
        if not re.search(math_triggers, problem, re.IGNORECASE | re.UNICODE):
            raise MathValidationError("Doesn't appear to be a valid math problem")

if __name__ == "__main__":
    solver = MathSolver()
    
    problem = """Find all positive integers n such that n² + 20n is a perfect square."""
    
    logger.info("Starting example problem solution")
    
    if solution := solver.solve(problem):
        print(solution.formatted_output())
    else:
        print("Solution failed")