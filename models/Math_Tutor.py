
"""
Math Tutor Chatbot System

A comprehensive AI-powered math tutoring system with persistent session support.

Key Features:
- Step-by-step CBSE/State Board aligned solutions
- Multi-session support with automatic saving
- Session resume capability
- Interactive chat with diagram support

Usage Methods:
1. Command Line Interface:
   Basic usage:       python math_tutor.py
   Load session:      python math_tutor.py --session sessions/20240503-143000_abc123def456
   
2. API Integration:
   from math_tutor import MathChatbot
   
   # New session
   bot = MathChatbot()
   response = asyncio.run(bot.chat("new_session_id", "Solve x^2 + 5x = 0"))
   
   # Load existing session
   state = bot.load_session("sessions/20240503-143000_abc123def456") 
   response = asyncio.run(bot.chat(state.session_id, "Explain step 2"))

Session Management:
- Sessions auto-save to 'sessions/' directory
- Session folders contain:
  - chat.json: Full conversation history
  - session.json: Current problem state
  - diagrams/: Explanatory images
- To resume session: Use full session folder path
"""


import os
import re
import sys
from pathlib import Path
import asyncio
import logging
import time
from datetime import datetime
import json
import uuid
import argparse
import aiohttp
from typing import Optional, List, Dict
import requests
from ratelimit import limits, sleep_and_retry
from urllib.parse import urlparse
from pydantic import BaseModel, Field, field_serializer
from google.api_core import exceptions
from google import genai
from google.genai import types

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from childappback.settings import BASE_DIR
from models.api_key_manager import APIKeyManager

from models.model_config_math_tutor import (
    MODEL_CONFIG,
    MATH_PROMPT_TEMPLATE,
    CLASSIFICATION_PROMPT_TEMPLATE
)

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class MathSolution(BaseModel):
    """Pydantic model for structured math solution"""
    problem_analysis: str = Field(..., description="Initial breakdown of the problem")
    solution_strategies: List[str] = Field(..., description="Multiple approaches for solving")
    mathematical_steps: List[str] = Field(..., description="Concise mathematical steps only")
    detailed_explanations: List[str] = Field(..., description="Detailed reasoning behind steps")
    common_mistakes: List[str] = Field(..., description="Common exam mistakes")
    answer: str = Field(..., description="Final answer in plain format")
    key_topics: List[str] = Field(..., description="CBSE-relevant study topics")
    diagram_search_queries: List[str] = Field(default_factory=list, description="Search terms for finding explanatory diagrams")
    
    def formatted_output(self) -> str:
        """Generate student-friendly formatted string"""
        cleaned_steps = [
            re.sub(
                r'^(?:\[.*?\] |[➊-➒]+ |Step \d+[:\.]? |\d+\.\s+|•\s+)',  # Remove prefixes and action descriptions
                '', 
                step
            )
            for step in self.mathematical_steps
        ]
        
        # Format steps with clean numbering
        steps_str = "\n".join(
            [f"Step {i+1}: {step}" 
            for i, step in enumerate(cleaned_steps)]
        )
        topics_str = "\n".join(f"• {topic}" for topic in self.key_topics)
        primary_strategy = self.solution_strategies[0] if self.solution_strategies else ""
        other_strategies = self.solution_strategies[1:] if len(self.solution_strategies) > 1 else []

        # Start building the formatted string
        formatted = f"""📚 Math Problem Solution 📚

✅ Final Answer: {self.answer}
    
🔍 Problem Analysis:
{self.problem_analysis}

🎯 Solution Approach: {primary_strategy}

🔢 Step-by-Step Solution:
{steps_str}

📖 Step Explanations:
{chr(10).join(f"- {exp}" for exp in self.detailed_explanations)}

❌ Common Mistakes:
{chr(10).join(f"✗ {m}" for m in self.common_mistakes)}

🟢 Alternative Methods:
{chr(10).join(f"• {s}" for s in other_strategies) if other_strategies else "None"}

📚 Key Concepts:
{topics_str}"""
        
        return formatted


class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)

    @field_serializer('timestamp')
    def serialize_dt(self, dt: datetime, _info):
        return dt.isoformat()


class ConversationState(BaseModel):
    current_problem: Optional[str] = None
    current_problem_history: List[ChatMessage] = Field(default_factory=list)
    current_solution: Optional[MathSolution] = None
    history: List[ChatMessage] = []
    user_message_count: int = 0
    diagram_urls: List[str] = Field(default_factory=list)
    search_queries: List[str] = Field(default_factory=list)
    session_id: str
    session_path: str = Field(..., description="Persistent session storage path")

    def model_dump(self, **kwargs):
        return {
            "current_problem": self.current_problem,
            "current_solution": self.current_solution.model_dump() if self.current_solution else None,
            "history": [msg.model_dump() for msg in self.history],
            "diagram_urls": self.diagram_urls,
            "search_queries": self.search_queries,
            "user_message_count": self.user_message_count,
            "session_id": self.session_id,
            "session_path": self.session_path
        }

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
        self.model_config = MODEL_CONFIG
        self.image_search_config = {
            "google_cse_id": "34de7be9d41754f16",
            "google_api_key": "AIzaSyC_baCQhJhPf_2NicziOTx1bLPDsQg6n4E",
            "safe_search": "active",
            "img_size": "medium",
            "img_type": "clipart",
            "num_results": 3
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
                client = self._get_model(api_key)

                if not client:
                    continue

                generation_config = types.GenerateContentConfig(
                temperature=self.model_config["generation_config"]["temperature"],
                top_p=self.model_config["generation_config"]["top_p"],
                top_k=self.model_config["generation_config"]["top_k"],
                max_output_tokens=self.model_config["generation_config"]["max_output_tokens"],
                )

                logger.debug(f"Sending prompt to LLM:\n{prompt}")
                
                response = ""
                for chunk in client.models.generate_content_stream(
                    model=self.model_config["model"],
                    contents=[types.Content(role="user", parts=[types.Part.from_text(text=prompt)])],
                    config=generation_config,
                ):
                    if chunk.text:
                        response += chunk.text

                self.api_key_manager.update_key_status(api_key, success=True)
                logger.info("LLM response received successfully")
                return response

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

    def _get_model(self, api_key: str):
        """Retrieve or create configured Gemini model."""
        try:
            client = genai.Client(api_key=api_key)

            logger.info(f"Created new model instance for key ending ...{api_key[-4:]}")
            return client

        except Exception as e:
            logger.error(f"Client creation failed: {str(e)}")
            return None

    def solve(self, problem: str, max_retries: int = 3) -> Optional[MathSolution]:
        """Main solving interface with enhanced logging."""
        logger.info(f"Received problem: {problem}")
        start_time = time.time()
        
        try:
            prompt = self._build_indian_style_prompt(problem)
            
            logger.debug(f"Generated prompt")
            raw_response = self._get_llm_response(prompt, max_retries)
            
            if not raw_response:
                logger.error("No response received from LLM")
                return None
                
            logger.debug(f"Raw LLM response received")
            return self._parse_response(raw_response)

        except Exception as e:
            logger.error(f"Solving process failed: {str(e)}")
            return None
        finally:
            logger.info(f"Processing time: {time.time()-start_time:.2f} seconds")

        
    def _build_indian_style_prompt(self, problem: str) -> str:
        """Create structured prompt with output format"""
        return MATH_PROMPT_TEMPLATE.format(problem=problem)
    
    @sleep_and_retry
    @limits(calls=5, period=60)
    def _google_image_search(self, query: str) -> List[str]:
        """Use Google Custom Search JSON API for image search"""
        try:
            params = {
                "q": query,
                "cx": self.image_search_config["google_cse_id"],
                "key": self.image_search_config["google_api_key"],
                "searchType": "image",
                "safe": self.image_search_config["safe_search"],
                "imgSize": self.image_search_config["img_size"],
                "imgType": self.image_search_config["img_type"],
                "num": self.image_search_config["num_results"]
            }
            
            response = requests.get(
                "https://www.googleapis.com/customsearch/v1",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            
            return [
                item["link"] for item in response.json().get("items", [])
                if self.is_valid_url(item.get("link", ""))
            ][:3]

        except Exception as e:
            logger.error(f"Image search failed: {str(e)}")
            return []

    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Validate URL format and safety"""
        try:
            result = urlparse(url)
            return all([
                result.scheme in ["http", "https"],
                result.netloc,
                "://i.imgur.com/" not in url  # Block image hosting sites
            ])
        except:
            return False

    def _parse_response(self, response: str) -> Optional[MathSolution]:
        """Robust JSON parsing with error recovery"""
        try:
            # Improved JSON extraction with better error context
            json_str = response.strip()
            
            # 1. Handle code block responses
            if '```json' in json_str:
                json_str = re.search(r'```json(.*?)```', json_str, re.DOTALL).group(1)
            else:
                # 2. Handle partial JSON using more lenient pattern
                json_match = re.search(r'^\s*{(.*)}\s*$', json_str, re.DOTALL)
                if json_match:
                    json_str = json_match.group(0)
                else:
                    # 3. Attempt to complete truncated JSON
                    if not json_str.endswith('}'):
                        json_str = json_str.rsplit('}', 1)[0] + '}'
                    if not json_str.startswith('{'):
                        json_str = '{' + json_str.split('{', 1)[-1]

            # 4. Validate JSON structure before parsing
            logger.debug(f"Cleaned JSON string:\n{json_str}")
            
            # 5. Attempt validation with error recovery
            try:
                parsed = MathSolution.model_validate_json(json_str)
                return parsed
            except Exception as e:
                # 6. Fallback to partial validation
                logger.warning(f"Full validation failed, attempting partial recovery: {str(e)}")
                parsed_dict = json.loads(json_str)
                return MathSolution(**{
                    k: v for k, v in parsed_dict.items()
                    if k in MathSolution.model_fields
                })

        except json.JSONDecodeError as e:
            # 7. Enhanced error logging
            error_context = max(0, e.pos - 50)
            logger.error(
                f"JSON decoding failed at position {e.pos} (char {e.pos}):\n"
                f"Error context: {json_str[error_context:e.pos+50]}\n"
                f"Full response (500 chars): {response[:500]}"
            )
            return None
        except Exception as e:
            # 8. Final fallback with error context
            logger.error(
                f"Complete parsing failure: {str(e)}\n"
                f"Original response (500 chars): {response[:500]}"
            )
            return None

class MathChatbot(MathSolver):
    """
    Enhanced Math Solver with Chat capabilities
    Handles follow-up questions and maintains conversation context
    """
    
    def __init__(self, api_key_manager: APIKeyManager = None):
        super().__init__(api_key_manager)
        self.conversations: Dict[str, ConversationState] = {}
        os.makedirs("sessions", exist_ok=True)
        logger.info("MathChatbot initialized with conversation support")

    async def classify_query(self, message: str, state: ConversationState) -> int:
        """Returns classification (1=New, 2=Follow-up, 3=Unrelated)"""
        prompt = self._build_classification_prompt(message, state)
        response = await self.async_get_llm_response(prompt)


        logger.info(f"Classification response: {response}")
        
        try:
            return int(response.strip()[0])  # Get first character only
        except:
            logger.warning("Classification failed, using default")
            return 2    # Default to follow-up
        
    def _build_classification_prompt(self, message: str, state: ConversationState) -> str:
        history_snippet = "\n".join(
            f"{msg.role}: {msg.content}" 
            for msg in state.current_problem_history[-10:]  # Last 10 messages
        )
        return CLASSIFICATION_PROMPT_TEMPLATE.format(
            history_snippet=history_snippet,
            message=message
        )
        
    async def async_get_llm_response(self, prompt: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._get_llm_response, prompt, 2)
    
    def _create_session_folder(self, session_id: str) -> str:
        """Create session folder with timestamp and sanitized problem name"""
        try:
            sessions_dir = BASE_DIR / "sessions"
            
            # 1. Check for existing session folder
            existing_path = None
            if os.path.exists(sessions_dir):
                for folder in os.listdir(sessions_dir):
                    if folder.endswith(f"_{session_id}"):
                        existing_path = os.path.join(sessions_dir, folder)
                        break

            if existing_path:
                logger.info(f"Reusing existing session folder: {existing_path}")
                return existing_path
            # Create safe folder name
            timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
            folder_name = f"{timestamp}_{session_id}"
            folder_path = os.path.join("sessions", folder_name) 

            os.makedirs(folder_path, exist_ok=True)
            logger.info(f"Creating session logger folder for {folder_name}")

            return folder_path
        except FileExistsError:
            logger.warning(f"Session folder collision detected: {folder_path}")
        except Exception as e:
            logger.error(f"Folder creation failed: {str(e)}")
            return None

    def _save_exchange(self, state: ConversationState, 
                  class_prompt: str, class_response: str,
                  sol_prompt: str, sol_response: str):
        """Save complete exchange in one file"""
        
        # Then update the chat state
        self._save_chat_state(state)

        if not state.session_path:
            return
            
        filename = f"exchange_{state.user_message_count:03d}.txt"
        filepath = os.path.join(state.session_path, filename)
        
        content = f"""=== CLASSIFICATION PROMPT ===
{class_prompt}

=== CLASSIFICATION RESPONSE ===
{class_response}

=== SOLUTION PROMPT ===
{sol_prompt}

=== SOLUTION RESPONSE ===
{sol_response}"""
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            logger.error(f"Failed to save exchange: {str(e)}")

    def _download_images(self, urls: List[str], save_dir: Path) -> List[Path]:
        """Synchronous download with improved error handling"""
        saved_files = []
        for i, url in enumerate(urls[:3], 1):  # Limit to 3 images
            try:
                response = requests.get(url, timeout=15, stream=True)
                response.raise_for_status()
                
                # Verify image content
                content_type = response.headers.get('content-type', '')
                if 'image' not in content_type:
                    logger.warning(f"Skipped non-image content from {url}")
                    continue
                    
                # Generate safe filename
                ext = content_type.split('/')[-1].split('+')[0]  # Handle image/svg+xml
                filename = f"diagram_{i}.{ext}"
                file_path = save_dir / filename
                
                # Stream content to file
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                        
                saved_files.append(file_path)
                logger.debug(f"Saved image: {file_path}")

            except Exception as e:
                logger.error(f"Failed to download {url}: {str(e)}")
        
        return saved_files
        
    def _save_session_state(self, state: ConversationState):
        """Save current problem state separately from chat history"""
        try:
            session_data = {
                "session_id": state.session_id,
                "current_problem": state.current_problem,
                "current_solution": state.current_solution.model_dump() if state.current_solution else None,
                "current_problem_history": [msg.model_dump() for msg in state.current_problem_history],
                "diagram_urls": state.diagram_urls,
                "search_queries": state.search_queries,
                "created_at": datetime.now().isoformat()
            }
            
            session_file = os.path.join(state.session_path, "session.json")
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Session state save failed: {str(e)}")

    def _save_chat_state(self, state: ConversationState):
        """Save complete conversation history"""
        if not state.session_path:
            return
            
        try:
            chat_data = {
                "messages": [msg.model_dump() for msg in state.history],
                "session_id": state.session_id,
                "updated_at": datetime.now().isoformat()
            }
            
            chat_file = os.path.join(state.session_path, "chat.json")
            with open(chat_file, 'w', encoding='utf-8') as f:
                json.dump(chat_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            logger.error(f"Chat state save failed: {str(e)}")

    def load_session(self, session_path: str) -> ConversationState:
        """Load session with proper encoding and error handling"""
        try:
            # Convert to Path object and validate
            session_path = Path(session_path)
            if not session_path.exists():
                raise FileNotFoundError(f"Session directory {session_path} not found")
            
            # Normalize paths using BASE_DIR
            session_file = session_path / "session.json"
            chat_file = session_path / "chat.json"

            # Validate critical files exist
            if not session_file.exists():
                raise FileNotFoundError("session.json missing")
            if not chat_file.exists():
                raise FileNotFoundError("chat.json missing")

            # Load session data with UTF-8 encoding
            with open(session_file, 'r', encoding='utf-8') as f:
                session_data = json.load(f)

            # Load chat history with error handling
            try:
                with open(chat_file, 'r', encoding='utf-8') as f:
                    chat_data = json.load(f)
            except UnicodeDecodeError:
                # Fallback for corrupted files
                with open(chat_file, 'r', encoding='utf-8', errors='replace') as f:
                    chat_data = json.load(f)

            # Validate critical fields
            if not isinstance(session_data.get("session_id"), str):
                raise ValueError("Invalid session ID in file")

            return ConversationState(
                session_id=session_data["session_id"],
                session_path=str(session_path.absolute()),
                current_problem=session_data.get("current_problem"),
                current_solution=MathSolution(**session_data["current_solution"]) if session_data.get("current_solution") else None,
                diagram_urls=session_data.get("diagram_urls", []),
                search_queries=session_data.get("search_queries", []),
                user_message_count=len([m for m in chat_data.get("messages", []) if m.get("role") == "user"]),
                history=[ChatMessage(**msg) for msg in chat_data.get("messages", [])],
                current_problem_history=[ChatMessage(**msg) for msg in session_data.get("current_problem_history", [])]
            )
        except Exception as e:
            logger.error(f"Session load failed for {session_path}: {str(e)}")
            raise RuntimeError(f"Failed to load session: {str(e)}")

    def new_conversation(self, session_id: str) -> ConversationState:
        """Initialize with explicit session ID from main"""
        session_path = self._create_session_folder(session_id)
        if not session_path:
            raise RuntimeError("Failed to create session directory")
        
        # Ensure required subdirectories exist
        (Path(session_path) / "diagrams").mkdir(exist_ok=True)

        state = ConversationState(
            session_id=session_id,
            session_path=session_path,
            history=[],
            current_problem_history=[],
            diagram_urls=[],
            search_queries=[],
            user_message_count=0,
            current_problem=None,
            current_solution=None
        )
        self.conversations[session_id] = state
        logger.info(f"New session: {session_path}")
        return state

    async def chat(self, session_id: str, message: str) -> str:
        if session_id not in self.conversations:
            self.new_conversation(session_id)

        state = self.conversations[session_id]
        original_history = state.history.copy()
        
        try:
            # Add user message to history and increment counter
            user_msg = ChatMessage(role="user", content=message)
            state.history.append(user_msg)
            state.user_message_count += 1  # Increment for every user message
            
            self._save_chat_state(state)

            # Classify query using history up to but not including current message
            query_type = 1  # Default to new problem
            if len(original_history) > 0 or state.current_problem:
                query_type = await self.classify_query(message, state)
                logger.debug(f"Classification result: {query_type}")

            if query_type == 3:
                # Remove invalid message and persist
                state.history.remove(user_msg)
                state.user_message_count -= 1
                self._save_chat_state(state)
                return "Please ask math-related questions."

            if query_type == 1:
                class_prompt = self._build_classification_prompt(message, state)
                class_response = "1"

                # Create new state preserving existing history
                new_state = ConversationState(
                    session_id=state.session_id,
                    session_path=state.session_path,
                    user_message_count=state.user_message_count,
                    history=state.history,  # Maintain full history
                    current_problem_history=[user_msg],
                    current_problem=None,
                    current_solution=None,
                    diagram_urls=[],
                    search_queries=[]
                )
                self.conversations[session_id] = new_state
                state = new_state

                response = await self._handle_new_problem(state, message, class_prompt, class_response)
                return response

            if query_type == 2:
                if not state.current_problem:
                    assistant_msg = ChatMessage(
                        role="assistant",
                        content="Please first provide a complete math problem to solve."
                    )
                    state.history.append(assistant_msg)
                    self._save_chat_state(state)
                    return assistant_msg.content

                return await self._handle_followup(state, message)

            return "Unexpected query type. Please try again."

        except Exception as e:
            error_msg = f"Chat error: {str(e)}"
            logger.error(error_msg)
            self._save_chat_state(state)
            return "Sorry, I encountered an error. Please try again."


    async def _handle_new_problem(self, state: ConversationState, message: str, 
                            class_prompt: str, class_response: str) -> str:
        """Handle new problem with history context"""
        try:
            # Generate solution with full history context
            sol_prompt = self._build_indian_style_prompt(message)
            solution = await self.async_solve(message)

            if not solution:
                state.history.pop()  # Remove the user message if solution failed
                self._save_chat_state(state)
                return "I couldn't solve this problem. Please try again."

            # Update state with new solution
            state.current_problem = message
            state.current_solution = solution
            state.search_queries = solution.diagram_search_queries

            # Generate and store assistant response
            response = solution.formatted_output()
            response += "\n\nAsk me about:\n• Any specific step\n• Common mistakes\n• Related topics\n• Alternative methods"
            assistant_msg = ChatMessage(role="assistant", content=response)
            state.history.append(assistant_msg)
            state.current_problem_history.append(assistant_msg)

            # Persist state updates
            self._save_chat_state(state)
            self._save_session_state(state)

            # Save complete exchange with original history context
            self._save_exchange(
                state,
                class_prompt=class_prompt,
                class_response=class_response,
                sol_prompt=sol_prompt,
                sol_response=solution.model_dump_json()
            )

            # Start async processes after saving state
            if state.search_queries:
                asyncio.create_task(self._process_diagrams(state))

            return response

        except Exception as e:
            logger.error(f"New problem handling failed: {str(e)}")
            self._save_chat_state(state)
            return "Failed to process the problem. Please try again."

        
    async def _process_diagrams(self, state: ConversationState):
        """Enhanced image processing with detailed logging"""
        try:
            if not state.search_queries:
                logger.info("No search queries for diagrams")
                return

            logger.info(f"Starting image processing for {len(state.search_queries)} queries")
            diagram_dir = Path(state.session_path) / "diagrams"
            diagram_dir.mkdir(exist_ok=True)
            logger.debug(f"Image storage directory: {diagram_dir.absolute()}")

            saved_paths = []
            for i, query in enumerate(state.search_queries[:3], 1):
                try:
                    logger.debug(f"Processing query #{i}: {query}")
                    urls = await self.async_image_search(query)
                    logger.debug(f"Found {len(urls)} URLs for query: {query}")

                    for j, url in enumerate(urls[:2], 1):  # Top 2 results per query
                        try:
                            file_path = await self._download_and_save_image(
                                url=url,
                                query_idx=i,
                                result_idx=j,
                                save_dir=diagram_dir
                            )
                            if file_path:
                                saved_paths.append(str(file_path.relative_to(state.session_path)))
                                logger.info(f"Saved image: {file_path}")
                        except Exception as e:
                            logger.error(f"Failed to process {url}: {str(e)}")

                except Exception as e:
                    logger.error(f"Query processing failed for '{query}': {str(e)}")

            if saved_paths:
                state.diagram_urls = saved_paths
                self._save_session_state(state)
                logger.info(f"Saved {len(saved_paths)} images to session")

        except Exception as e:
            logger.error(f"Diagram processing failed: {str(e)}")
            logger.exception(e)

    async def async_image_search(self, query: str) -> List[str]:
        """Async wrapper for image search"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._google_image_search, query)

    async def _download_and_save_image(self, url: str, query_idx: int, result_idx: int, save_dir: Path) -> Optional[Path]:
        """Robust image download and save handler"""
        try:
            # Validate URL before processing
            if not self.is_valid_url(url):
                logger.warning(f"Skipping invalid URL: {url}")
                return None

            # Create unique filename
            sanitized_query = re.sub(r'\W+', '_', url)[:50]
            filename = f"query_{query_idx}_result_{result_idx}_{sanitized_query}.jpg"
            file_path = save_dir / filename

            # Configure request headers
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Referer": "https://www.google.com/"
            }

            # Download with timeout and streaming
            async with aiohttp.ClientSession() as session:
                async with session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)) as response:
                    if response.status != 200:
                        logger.warning(f"Invalid response {response.status} from {url}")
                        return None

                    content_type = response.headers.get('Content-Type', '')
                    if 'image' not in content_type:
                        logger.warning(f"Non-image content from {url}: {content_type}")
                        return None

                    # Read and save content
                    content = await response.read()
                    if not content:
                        logger.warning(f"Empty content from {url}")
                        return None

                    # Save to file
                    with open(file_path, 'wb') as f:
                        f.write(content)

                    logger.debug(f"Successfully saved {len(content)} bytes to {file_path}")
                    return file_path

        except Exception as e:
            logger.error(f"Failed to download {url}: {str(e)}")
            return None

    async def _handle_followup(self, state: ConversationState, message: str) -> str:
        try:
            # Build prompts with current history
            user_msg = ChatMessage(role="user", content=message)
            state.current_problem_history.append(user_msg)
            class_prompt = self._build_classification_prompt(message, state)
            prompt = self._build_followup_chat_prompt(state, message)
            
            # Get and process response
            raw_response = self._get_llm_response(prompt, max_retries=3)
            if not raw_response:
                raise ValueError("Empty LLM response")

            # Update conversation history
            assistant_msg = ChatMessage(role="assistant", content=raw_response)
            state.history.append(assistant_msg)
            state.current_problem_history.append(assistant_msg)
            self._save_chat_state(state)
            self._save_session_state(state)

            # Save exchange with current history context
            self._save_exchange(
                state,
                class_prompt=class_prompt,
                class_response="2",
                sol_prompt=prompt,
                sol_response=raw_response
            )

            return raw_response

        except Exception as e:
            logger.error(f"Follow-up handling failed: {str(e)}")
            self._save_chat_state(state)
            return "Error processing follow-up question. Please try again."
    
    def _build_followup_chat_prompt(self, state: ConversationState, message: str) -> str:
        # 1) Pre-build the snippets that contain backslashes
        history = "\n".join(
            f"{msg.role.upper()}: {msg.content}" 
            for msg in state.current_problem_history[-10:]
        )
        solution = state.current_solution.model_dump() if state.current_solution else {}
        # Add strategies to the prompt
        strategies = (
            "\n".join(state.current_solution.solution_strategies)
            if state.current_solution and state.current_solution.solution_strategies
            else ""
        )

        # 2) Build the final prompt without any backslashes inside {…}
        return (
            f"Available strategies:\n{strategies}\n"
            f"You're a math tutor. Current problem: {state.current_problem}\n"
            f"Conversation History:\n{history}\n"
            f"Student's query: {message}\n"
            f"Existing Solution Context:\n{json.dumps(solution, indent=2)}\n\n" +
            "Instructions:\n"
            "1. Maintain exact mathematical notation from previous steps\n"
            "2. Format exponents as x² not x^2\n"
            "3. Reference step numbers like 'Step 2'\n"
            "4. Keep explanations under 100 words\n"
            "5. Use brackets for brief explanations: (reason)\n"
            "6. Avoid markdown, use plain text with unicode\n"
            "7. Reference previous steps by number when applicable\n"
            "8. Add new steps with continuous numbering\n"
            "9. Explain changes from previous approaches clearly\n"
            "10. Use same formatting for equations and symbols\n"

            "Example Response Format:\n"
            "We add 100 to complete the square (Step 2). "
            "Half of 20 is 10, squared is 100. " 
            "This transforms the equation to (n + 10)² = k² + 100"
            "When explaining alternative approaches:\n"
            "1. Start with 'Alternative Approach: [Method Name]'\n"
            "2. Follow same structure as main solution\n"
            "3. Compare with previous methods\n"
            "Example Alternative Response Format:\n"
            "Alternative Approach: Factoring Method\n"
            "Step 1: Original equation: n² + 20n = k²\n"
            "Step 2: Rearrange as n² + 20n - k² = 0 (Quadratic in n)\n"
            "...\n"
            "Key Differences: This method focuses on...\n"
        )

    async def async_solve(self, problem: str) -> Optional[MathSolution]:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self.solve, problem)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='AI Math Tutor CLI',
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--session', type=str, 
        help='Full path to session folder to load\n'
             'Example: sessions/20240503-143000_abc123def456')
    args = parser.parse_args()

    bot = MathChatbot()
    
    print("""\nMath Tutor Bot - Commands:
    /new     - Start new session
    /load    - Load existing session (provide full path)
    /save    - Show current session path
    /exit    - Quit program""")

    # Session initialization
    if args.session:
        try:
            state = bot.load_session(args.session)
            current_session = state.session_id
            print(f"\nLoaded session: {state.session_path}")
            print(f"Previous messages: {len(state.history)}")
            print(f"Current problem: {state.current_problem[:50]}...")
        except Exception as e:
            print(f"\n⚠️ Load failed: {str(e)}")
            current_session = uuid.uuid4().hex
            print("Starting new session instead")
    else:
        current_session = uuid.uuid4().hex
    
    clean_session_id = re.sub(r'[^\w-]', '', current_session)[:32]

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break

            # Handle commands
            if user_input.startswith('/'):
                if user_input.lower() == '/new':
                    current_session = uuid.uuid4().hex
                    clean_session_id = re.sub(r'[^\w-]', '', current_session)[:32]
                    print(f"🆕 New session: {clean_session_id}")
                elif user_input.lower().startswith('/load'):
                    try:
                        _, session_path = user_input.split(maxsplit=1)
                        if not os.path.exists(session_path):
                            print(f"⚠️ Error: Session path {session_path} does not exist")
                            continue
                            
                        state = bot.load_session(session_path)
                        current_session = state.session_id
                        clean_session_id = re.sub(r'[^\w-]', '', current_session)[:32]
                        print(f"♻️ Loaded session from: {state.session_path}")
                        print(f"📜 History: {len(state.history)} messages")
                        print(f"🔢 Current problem: {state.current_problem[:60]+'...' if state.current_problem else 'None'}")
                        
                    except Exception as e:
                        print(f"⚠️ Load error: {str(e)}")
                        print("Hint: Use full path like 'sessions/20240503-143000_abc123def456'")
                elif user_input.lower() == '/save':
                    if clean_session_id in bot.conversations:
                        print(f"💾 Session path: {bot.conversations[clean_session_id].session_path}")
                continue
                
            response = asyncio.run(bot.chat(clean_session_id, user_input))
            print(f"\n📚 Tutor: {response}")

        except KeyboardInterrupt:
            break

    print("\n🧮 Conversation ended. Session ID:", clean_session_id)
    if clean_session_id in bot.conversations:
        print("💾 Saved at:", bot.conversations[clean_session_id].session_path)
