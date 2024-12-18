"""
OpenAI Client Quickstart - A simplified, production-ready OpenAI client implementation.

This module provides functionality for:
1. Text completion with custom prompts
2. Image analysis
3. Email extraction
v4 - Added concurrent execution support
"""
import logging
import os
import time
from rich.logging import RichHandler
from rich.table import Table
from rich.console import Console
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, List, Dict, Callable
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial


# Load environment variables
load_dotenv()

# --------------------------------------------------------
# Global Configuration
# --------------------------------------------------------
DEFAULT_MODEL = "gpt-4o"  # Only use gpt-4o, gpt-4o-mini, or o1-mini, even for vision tasks
VISION_MODEL = "gpt-4o"
TEMPERATURE = 0.1  # Default to 0.0 or 0.1
MAX_TOKENS = 1000  # Maximum response length (1 to 4096)

ALLOWED_MODELS = ["gpt-4o", "gpt-4o-mini", "o1-mini"]

MAX_RETRIES = 3
BACKOFF_FACTOR = 2

RATE_LIMIT_PER_MINUTE = 200
RATE_LIMIT_PER_SECOND = 30

SYNC_OR_ASYNC = "async"  # "sync" or "async"

LOGGER_LEVEL = "INFO"  # Logging level for the application


# --------------------------------------------------------
# Global Configuration and Prompts
# --------------------------------------------------------

# Prompts for different tasks
@dataclass(frozen=True)
class PROMPTS:
    """
    Collection of system and user prompts organized by task.

    v1 - Initial implementation with validation
    v2 - Added detailed multiline prompts
    v3 - Added XML tags for structured prompts
    v4 - Reorganized by task [18-Dec-23]
    """

    # -------------------- General Task Prompts --------------------
    class General:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',  # Start system prompt
            '    <role>You are a helpful assistant focused on clear, accurate responses.</role>',  # Define role
            '</system_prompt>'
        ])
        USER: str = '<user_input>{user_prompt}</user_input>'

    # -------------------- Haiku Task [18-Dec-23] --------------------
    class Haiku:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',  # Start XML structure for consistent parsing
            '',  # Blank line for readability
            '    <role>',  # Role definition block
            '        You are a poetic assistant specializing in programming haikus.',  # Core identity
            '    </role>',  # Initially had issues with role confusion when combined with other tasks
            '',
            '    <guidelines>',  # Guidelines block - Added after seeing inconsistent outputs
            '        <style>',  # Style rules - Added [15-Dec-23] after seeing syllable count errors
            '            Create haikus that follow traditional rules:',
            '            - First line: 5 syllables',  # Explicit count after seeing 4-6 variations
            '            - Second line: 7 syllables',  # Most common error point in early tests
            '            - Third line: 5 syllables',  # Completing the traditional format
            '        </style>',
            '',
            '        <content>',  # Content guidelines - Added [16-Dec-23] after metaphor quality issues
            '            <focus>',  # Focus block - Ensures technical accuracy
            '                Focus on capturing complex programming concepts through metaphor.',  # Key requirement
            '            </focus>',
            '            <imagery>',  # Imagery block - Added after seeing too literal interpretations
            '                Use natural imagery to explain technical concepts.',  # Balance requirement
            '            </imagery>',
            '            <balance>',  # Balance block - Critical for maintaining both aspects
            '                Maintain a balance between technical accuracy and poetic beauty.',
            '            </balance>',
            '        </content>',
            '',
            '        <tone>',  # Tone specifications - Added [17-Dec-23] after seeing overly technical outputs
            '            <clarity>',  # Clarity block - Essential for understanding
            '                Keep the language clear yet evocative.',  # Dual requirement
            '            </clarity>',
            '            <impact>',  # Impact block - Added after seeing flat endings
            '                Aim for an "aha" moment in the final line.',  # Creates memorable endings
            '            </impact>',
            '        </tone>',
            '    </guidelines>',
            '',
            '</system_prompt>'
        ])
        USER: str = '<user_input>Write a haiku about recursion in programming.</user_input>'

    # -------------------- Vision Analysis Task --------------------
    class Vision:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',  # Start system prompt
            '    <role>You are a detail-oriented image analyst (that speaks concisely and clearly like a real human) with an eye for detail.</role>',  # Core role
            '    <analysis_framework>',  # Analysis structure
            '        <key_aspects>',  # Key elements to analyze
            '            <subject>Main focus and key elements</subject>',
            '            <action>Dynamic elements and movement</action>',
            '            <composition>Layout and visual hierarchy</composition>',  # Visual structure
            '            <lighting>Quality and direction of light</lighting>',
            '            <color>Dominant colors and their relationships</color>',
            '            <mood>Emotional impact and atmosphere</mood>',
            '        </key_aspects>',
            '        <response_structure>',  # Output organization
            '            <order>',
            '                <step_1>Main subject and immediate impact</step_1>',  # First impression
            '                <step_2>Technical details and composition</step_2>',  # Deep analysis
            '                <step_3>Mood and emotional resonance</step_3>',  # Emotional impact
            '            </order>',
            '        </response_structure>',
            '    </analysis_framework>',
            '</system_prompt>'
        ])
        USER: str = '<user_input>What\'s in this image? Describe the main elements, action, and mood.</user_input>'

    # -------------------- Email Extraction Task --------------------
    class Email:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',  # Start system prompt
            '    <role>You are a precise assistant that extracts email addresses from text.</role>',  # Core role
            '    <output_format>Always return valid email addresses in the specified JSON format.</output_format>',  # Format specification
            '</system_prompt>'
        ])
        USER: str = '<user_input>Extract email from: {text}</user_input>'

    # -------------------- Chain of Thought Task --------------------
    class COT:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',  # Start system prompt
            '    <task>',  # Task definition
            '        Chain of Thought Analysis for Complex Problem Solving',
            '        1. Analyze the problem components',
            '        2. Break down solution steps',
            '        3. Evaluate potential approaches',
            '        4. Synthesize final solution',
            '    </task>',
            '',  # Spacing for readability
            '    <variables>',  # Input variables
            '        <problem_statement>{problem}</problem_statement>',
            '        <context>{context}</context>',
            '        <constraints>{constraints}</constraints>',
            '    </variables>',
            '',  # Spacing for readability
            '    <general_instructions>',  # Core process
            '        1. Start with problem decomposition',
            '        2. List all assumptions',
            '        3. Consider edge cases',
            '        4. Document decision points',
            '        5. Validate solution against requirements',
            '    </general_instructions>',
            '',  # Spacing for readability
            '    <situational_instructions>',  # Context-specific guidance
            '        <case_simple>Focus on clarity over complexity</case_simple>',
            '        <case_complex>Break down into smaller sub-problems</case_complex>',
            '        <case_ambiguous>State assumptions explicitly</case_ambiguous>',
            '    </situational_instructions>',
            '',  # Spacing for readability
            '    <output_format>',  # Response structure
            '        You must strictly follow the OUTPUT_FORMAT, including all <sections>',
            '        <scratchpad>',
            '            <analysis>',
            '                - Problem understood: [yes/no]',
            '                - Edge cases considered: [yes/no]',
            '                - Assumptions documented: [yes/no]',
            '            </analysis>',
            '            <conclusion>',
            '                Explicitly reference instructions and context in explanation.',
            '            </conclusion>',
            '        </scratchpad>',
            '',  # Spacing for readability
            '        <classification>',
            '            Final solution approach selected',
            '        </classification>',
            '',  # Spacing for readability
            '        <categories>',
            '            [Primary category]',
            '            [Secondary category (if applicable)]',
            '        </categories>',
            '',  # Spacing for readability
            '        <justification>',
            '            [Brief explanation of solution approach, explicitly referencing instructions and context.]',
            '        </justification>',
            '    </output_format>',
            '</system_prompt>'
        ])
        USER: str = '<user_input>Analyze the following problem: {problem_text}</user_input>'

    # -------------------- Joke Task [18-Dec-23] --------------------
    class Joke:
        SYSTEM: str = '\n'.join([
            'you tell jokes about numbers'
        ])
        USER: str = 'your number is:{number}'

    # -------------------- Validations / EH --------------------
    @staticmethod
    def format_general(user_prompt: str) -> Dict[str, str]:
        """Format general prompt with validation."""
        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty")
        return {
            "system": PROMPTS.General.SYSTEM,
            "user": PROMPTS.General.USER.format(user_prompt=user_prompt)
        }

    @staticmethod
    def format_email(text: str) -> Dict[str, str]:
        """Format email extraction prompt with validation."""
        if not text.strip():
            raise ValueError("Text cannot be empty")
        return {
            "system": PROMPTS.Email.SYSTEM,
            "user": PROMPTS.Email.USER.format(text=text)
        }

    @staticmethod
    def format_cot(problem_text: str) -> Dict[str, str]:
        """Format COT analysis prompt with validation."""
        if not problem_text.strip():
            raise ValueError("Problem text cannot be empty")
        return {
            "system": PROMPTS.COT.SYSTEM,
            "user": PROMPTS.COT.USER.format(problem_text=problem_text)
        }

    @staticmethod
    def format_joke(number: int) -> Dict[str, str]:
        """Format joke prompt with validation."""
        return {
            "system": PROMPTS.Joke.SYSTEM,
            "user": PROMPTS.Joke.USER.format(number=number)
        }


# --------------------------------------------------------
# Logging Configuration
# --------------------------------------------------------
def setup_logging() -> logging.Logger:
    """Configure Rich logging with custom levels."""
    # Set root logger to DEBUG to capture all messages
    logging.basicConfig(
        level=getattr(logging, LOGGER_LEVEL),
        format="%(message)s",
        handlers=[
            RichHandler(
                rich_tracebacks=True,
                markup=True,
                log_time_format="[%X]"
            )
        ]
    )

    # Create logger
    logger = logging.getLogger(__name__)

    # Set OpenAI's logger to WARNING to reduce noise
    logging.getLogger("openai").setLevel(logging.WARNING)

    return logger


logger = setup_logging()


# --------------------------------------------------------
# Rate Limiting Implementation
# --------------------------------------------------------
class RateLimiter:
    """
    Rate limiter using token bucket algorithm.

    1. Track API calls per second and minute
    2. Enforce rate limits
    3. Handle backoff when limits are reached
    v2 - Improved rate limiting with better tracking
    """

    def __init__(self):
        """Initialize rate limiter with separate buckets for second and minute tracking."""
        self.per_second_calls = deque(maxlen=RATE_LIMIT_PER_SECOND)
        self.per_minute_calls = deque(maxlen=RATE_LIMIT_PER_MINUTE)
        self.total_waits = 0.0  # Track total wait time
        self.total_calls = 0  # Track total calls made

    def _clean_old_timestamps(self, timestamps: deque, window: timedelta):
        """Remove timestamps older than the window."""
        now = datetime.now()
        while timestamps and (now - timestamps[0]) > window:
            timestamps.popleft()

    def wait_if_needed(self):
        """Check rate limits and wait if necessary."""
        now = datetime.now()
        self.total_calls += 1

        # Clean up old timestamps
        self._clean_old_timestamps(self.per_second_calls, timedelta(seconds=1))
        self._clean_old_timestamps(self.per_minute_calls, timedelta(minutes=1))

        total_sleep_time = 0.0

        # Check second limit
        if len(self.per_second_calls) >= RATE_LIMIT_PER_SECOND:
            sleep_time = 1 - (now - self.per_second_calls[0]).total_seconds()
            if sleep_time > 0:
                logger.warning(f"⚠️  Rate limit reached (per second). Waiting {sleep_time:.2f}s")
                time.sleep(sleep_time)
                total_sleep_time += sleep_time

        # Check minute limit
        if len(self.per_minute_calls) >= RATE_LIMIT_PER_MINUTE:
            sleep_time = 60 - (now - self.per_minute_calls[0]).total_seconds()
            if sleep_time > 0:
                logger.warning(f"⚠️  Rate limit reached (per minute). Waiting {sleep_time:.2f}s")
                time.sleep(sleep_time)
                total_sleep_time += sleep_time

        # Record the call and update stats
        now = datetime.now()  # Update timestamp after potential sleep
        self.per_second_calls.append(now)
        self.per_minute_calls.append(now)
        self.total_waits += total_sleep_time

        # Log current status
        logger.debug(
            f"Rate limits: {len(self.per_second_calls)}/s, {len(self.per_minute_calls)}/min "
            f"(Total calls: {self.total_calls}, Total wait time: {self.total_waits:.2f}s)"
        )


# --------------------------------------------------------
# OpenAI Client Implementation
# --------------------------------------------------------
class OAI:
    """
    OpenAI client implementation with retry logic, rate limiting, and concurrent execution.

    1. Handle API interactions with retries
    2. Implement rate limiting
    3. Process responses concurrently
    v4 - Added concurrent execution support
    """

    def __init__(self, api_key: Optional[str] = None, max_workers: int = 5):
        """
        Initialize client with API key, rate limiter, and thread pool.

        Args:
            api_key: Optional API key (defaults to environment variable)
            max_workers: Maximum number of concurrent threads (default: 5)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.client = OpenAI(api_key=self.api_key)
        self.rate_limiter = RateLimiter()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def _retry_with_backoff(self, func: Callable, *args, **kwargs) -> Optional[str]:
        """Retry function with exponential backoff."""
        for attempt in range(MAX_RETRIES):
            try:
                # Wait for rate limit if needed
                self.rate_limiter.wait_if_needed()

                # Attempt the API call
                return func(*args, **kwargs)

            except Exception as e:
                if attempt == MAX_RETRIES - 1:
                    logger.error(f"Final retry attempt failed: {str(e)}")
                    return None

                backoff_time = BACKOFF_FACTOR ** attempt
                logger.warning(f"Attempt {attempt + 1} failed: {str(e)}. Retrying in {backoff_time}s...")
                time.sleep(backoff_time)

        return None

    def complete(
        self,
        messages: List[Dict[str, str]],
        model: str = DEFAULT_MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ) -> Optional[str]:
        """Send completion request to OpenAI API with retry logic."""
        if model not in ALLOWED_MODELS and model != VISION_MODEL:
            raise ValueError(f"Model must be one of: {ALLOWED_MODELS} or {VISION_MODEL}")

        def _make_request():
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content

        return self._retry_with_backoff(_make_request)

    def complete_batch(
        self,
        batch_messages: List[List[Dict[str, str]]],
        model: str = DEFAULT_MODEL,
        temperature: float = TEMPERATURE,
        max_tokens: int = MAX_TOKENS,
    ) -> List[Optional[str]]:
        """
        Process multiple completion requests concurrently.

        Args:
            batch_messages: List of message lists for each completion
            model: Model to use for completions
            temperature: Temperature setting
            max_tokens: Maximum tokens per response

        Returns:
            List of completion results in the same order as inputs
        """
        # Create partial function with fixed parameters
        complete_func = partial(
            self.complete,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # Submit all tasks to the executor
        future_to_messages = {
            self.executor.submit(complete_func, messages): i
            for i, messages in enumerate(batch_messages)
        }

        # Collect results in order
        results = [None] * len(batch_messages)
        for future in as_completed(future_to_messages):
            index = future_to_messages[future]
            try:
                results[index] = future.result()
            except Exception as e:
                logger.error(f"Request {index} failed: {str(e)}")
                results[index] = None

        return results

    def create_haiku_batch(self, count: int) -> List[Optional[str]]:
        """Generate multiple haikus concurrently."""
        messages = [
            {"role": "system", "content": PROMPTS.Haiku.SYSTEM},
            {"role": "user", "content": PROMPTS.Haiku.USER}
        ]
        batch_messages = [messages] * count
        return self.complete_batch(batch_messages)

    def create_haiku(self) -> Optional[str]:
        """Generate a programming haiku."""
        messages = [
            {"role": "system", "content": PROMPTS.Haiku.SYSTEM},
            {"role": "user", "content": PROMPTS.Haiku.USER}
        ]
        return self.complete(messages)

    def describe_image(self, image_url: str) -> Optional[str]:
        """Analyze an image."""
        messages = [
            {"role": "system", "content": PROMPTS.Vision.SYSTEM},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPTS.Vision.USER},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
        return self.complete(messages, model=VISION_MODEL)

    def extract_email(self, text: str) -> Optional[str]:
        """Extract email addresses from text."""
        formatted = PROMPTS.format_email(text)
        messages = [
            {"role": "system", "content": formatted["system"]},
            {"role": "user", "content": formatted["user"]}
        ]
        return self.complete(messages)

    def tell_joke(self, number: int) -> Optional[str]:
        """Generate a programming joke."""
        formatted = PROMPTS.format_joke(number)
        messages = [
            {"role": "system", "content": formatted["system"]},
            {"role": "user", "content": formatted["user"]}
        ]
        return self.complete(messages)

    def tell_jokes_batch(self, start_number: int, count: int) -> List[Optional[str]]:
        """Generate multiple jokes concurrently."""
        batch_messages = [
            [
                {"role": "system", "content": PROMPTS.Joke.SYSTEM},
                {"role": "user", "content": PROMPTS.Joke.USER.format(number=i)}
            ]
            for i in range(start_number, start_number + count)
        ]
        return self.complete_batch(batch_messages)


# --------------------------------------------------------
# Example Usage
# --------------------------------------------------------
if __name__ == "__main__":
    # Test image URL that works
    TEST_IMAGE_URL = "https://img.freepik.com/premium-photo/lion-runs-through-water-splashing-with-every-step_36682-244775.jpg?w=2000"

    logger.info("[bold green]Starting OpenAI Quickstart Demo[/bold green]")

    try:
        # Initialize client with 3 workers for regular demos
        client = OAI(max_workers=3)

        # Regular demos
        logger.info("\n[yellow]1. Regular Demos[/yellow]")

        # Test haiku generation
        logger.info("\n[cyan]Testing haiku generation:[/cyan]")
        if result := client.create_haiku():
            logger.info(f"[magenta]{result}[/magenta]")

        # Test image description
        logger.info("\n[cyan]Testing image description:[/cyan]")
        if result := client.describe_image(TEST_IMAGE_URL):
            logger.info(f"[magenta]{result}[/magenta]")

        # Test email extraction
        logger.info("\n[cyan]Testing email extraction:[/cyan]")
        if result := client.extract_email("Contact us at support@example.com"):
            logger.info(f"[magenta]{result}[/magenta]")

        # Threaded demo with jokes
        TOTAL_JOKES = 500
        logger.info(f"\n[yellow]2. Threaded Demo - Generating {TOTAL_JOKES} Jokes[/yellow]")

        # Initialize client with more workers for batch processing
        threaded_client = OAI(max_workers=10)

        # Record start time
        start_time = time.time()

        # Generate jokes concurrently
        results = threaded_client.tell_jokes_batch(1, TOTAL_JOKES)

        # Calculate total time
        total_time = time.time() - start_time

        # Calculate stats
        success_count = sum(1 for r in results if r is not None)

        # Display results
        # Create and populate rich table with jokes
        table = Table(title="Generated Jokes", show_header=True, header_style="bold cyan")
        table.add_column("#", justify="right", style="cyan")
        table.add_column("Joke", style="magenta")

        for i, result in enumerate(results, 1):
            if result:
                table.add_row(str(i), result)

        # Display the table using console to properly render the table
        console = Console()
        console.print(table)

        logger.info("\n[bold cyan]Async Processing Stats[/bold cyan]")
        logger.info(f"Total time: {total_time:.2f}s")
        logger.info(f"Successful requests: {success_count}/{TOTAL_JOKES}")
        logger.info(f"Average time per request: {total_time/TOTAL_JOKES:.2f}s")
        logger.info(f"Requests per second: {TOTAL_JOKES/total_time:.2f}")

        # Display rate limiter stats
        logger.info(f"Total wait time: {threaded_client.rate_limiter.total_waits:.2f}s")
        logger.info(f"Effective throughput: {TOTAL_JOKES/(total_time - threaded_client.rate_limiter.total_waits):.2f} req/s")

    except Exception as e:
        logger.error(f"[bold red]Demo failed:[/bold red] {str(e)}")
    finally:
        logger.info("[bold green]Demo completed[/bold green]")
