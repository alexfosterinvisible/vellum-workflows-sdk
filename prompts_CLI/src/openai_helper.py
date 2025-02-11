"""
OpenAI Documentation Helper - Uses OpenAI to provide intelligent responses about Vellum documentation.

This module provides functionality to:
1. Query documentation using natural language - [OpenAI completion endpoint] - [90% complete]
2. Get relevant code examples - [Semantic search in docs] - [TODO]
3. Troubleshoot common issues - [Pattern matching with learnings] - [TODO]

Run this file directly to see example queries and responses.

v5 - Added MD file crawler, LLM call logging, and rich table output
"""

import os
import json
from typing import Optional, List, Dict, Set
from dataclasses import dataclass
from openai import OpenAI
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import partial
from pathlib import Path
import fnmatch


# --------------------------------------------------------
# Global Configuration
# --------------------------------------------------------
GLOBAL_VARS = {
    # -------------------- Model Configuration --------------------
    "MODEL": "gpt-4o-mini",  # Default model
    "VISION_MODEL": "gpt-4o",  # Model for image analysis
    "TEMPERATURE": 0.1,  # Low temperature for factual responses
    "MAX_TOKENS": 1000,  # Maximum response length
    "ALLOWED_MODELS": ["gpt-4o", "gpt-4o-mini", "o1-mini"],

    # -------------------- Documentation Files --------------------
    "DOC_FILES": [
        "docs/learnings/README.md",
        "docs/learnings/1_quick_reference.md",
        "docs/learnings/2_technical_details.md",
        "docs/learnings/3_troubleshooting.md",
        "docs/client_sdk/1_introduction.md",
        "docs/client_sdk/2_authentication.md",
        "docs/client_sdk/3_prompts.md",
        "docs/workflow_sdk/1_workflow.md",
        "docs/workflow_sdk/2_workflows2.md",
        "docs/workflow_sdk/3_configuration.md",
        "docs/workflow_sdk/5_CLI.md",
        "prompts_CLI/README.md"
    ],

    # -------------------- Rate Limiting --------------------
    "RATE_LIMIT_PER_MINUTE": 200,  # Maximum API calls per minute
    "RATE_LIMIT_PER_SECOND": 30,   # Maximum API calls per second
    "MAX_RETRIES": 3,              # Maximum retry attempts
    "BACKOFF_FACTOR": 2,           # Exponential backoff multiplier

    # -------------------- Concurrency Settings --------------------
    "MAX_WORKERS": 50,             # Maximum concurrent threads
    "SYNC_OR_ASYNC": "async",      # "sync" or "async" operation mode

    # -------------------- Timeouts --------------------
    "LLM_TIMEOUT": 30,             # Timeout for individual LLM calls (seconds)
    "TOTAL_TIMEOUT": 120,          # Total operation timeout (seconds)

    # -------------------- Logging --------------------
    "LOGGER_LEVEL": "INFO",        # Logging level for the application

    # -------------------- Confidence Scoring --------------------
    "CONFIDENCE_RUBRIC": {
        "direct_answer": "Does the text directly answer the query? (yes/no)",
        "relevant_context": "Does the text provide relevant context? (yes/no)",
        "code_examples": "Does the text contain relevant code examples? (yes/no)",
        "up_to_date": "Does the information appear current? (yes/no)",
        "implementation_details": "Does it provide implementation details? (yes/no)"
    },

    # -------------------- Response Formats --------------------
    "JSON_SCHEMA": {
        "doc_search": {
            "type": "object",
            "properties": {
                "relevant_text": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of relevant quotes from the document"
                },
                "confidence_scores": {
                    "type": "object",
                    "properties": {
                        "direct_answer": {"type": "string", "enum": ["yes", "no"]},
                        "relevant_context": {"type": "string", "enum": ["yes", "no"]},
                        "code_examples": {"type": "string", "enum": ["yes", "no"]},
                        "up_to_date": {"type": "string", "enum": ["yes", "no"]},
                        "implementation_details": {"type": "string", "enum": ["yes", "no"]}
                    }
                },
                "summary": {"type": "string"}
            }
        },
        "synthesizer": {
            "type": "object",
            "properties": {
                "answer": {"type": "string"},
                "quotes": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source": {"type": "string"},
                            "relevance": {"type": "string"},
                            "is_code": {"type": "boolean"}
                        }
                    }
                },
                "context": {"type": ["string", "null"]},
                "confidence": {
                    "type": "object",
                    "properties": {
                        "answer_quality": {"type": "string", "enum": ["high", "medium", "low"]},
                        "source_quality": {"type": "string", "enum": ["high", "medium", "low"]},
                        "completeness": {"type": "string", "enum": ["high", "medium", "low"]},
                        "code_examples": {"type": "string", "enum": ["high", "medium", "low", "none"]}
                    }
                }
            }
        }
    }
}


def find_md_files(start_path: str = ".") -> List[str]:
    """
    Find all .md files in the repository, respecting .gitignore.

    1. Read .gitignore patterns
    2. Walk directory tree
    3. Filter files based on patterns
    4. Return relative paths
    v1 - Initial implementation
    """
    md_files = []
    gitignore_patterns = set()

    # Read .gitignore if it exists
    gitignore_path = os.path.join(start_path, '.gitignore')
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            gitignore_patterns = {line.strip() for line in f if line.strip() and not line.startswith('#')}

    def is_ignored(path: str) -> bool:
        """Check if path matches any gitignore pattern."""
        path = os.path.normpath(path)
        for pattern in gitignore_patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False

    # Walk directory tree
    for root, dirs, files in os.walk(start_path):
        # Remove ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]

        # Find .md files
        for file in files:
            if file.endswith('.md'):
                full_path = os.path.join(root, file)
                if not is_ignored(full_path):
                    # Convert to relative path
                    rel_path = os.path.relpath(full_path, start_path)
                    md_files.append(rel_path)

    return sorted(md_files)  # Sort for consistent ordering


# --------------------------------------------------------
# Structured Prompts
# --------------------------------------------------------
@dataclass(frozen=True)
class PROMPTS:
    """Collection of system and user prompts for documentation querying."""

    class DocSearch:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',
            '    <role>You analyze documentation to find relevant information and return JSON.</role>',
            '    <task>',
            '        1. Read the provided documentation section',
            '        2. Evaluate relevance to the query',
            '        3. Extract key information and quotes',
            '        4. Score confidence based on rubric',
            '    </task>',
            '    <output_format>',
            '        You must return a valid JSON object with this exact schema:',
            '        {',
            '            "relevant_text": ["quote1", "quote2", "quote3"],',
            '            "confidence_scores": {',
            '                "direct_answer": "yes/no",',
            '                "relevant_context": "yes/no",',
            '                "code_examples": "yes/no",',
            '                "up_to_date": "yes/no",',
            '                "implementation_details": "yes/no"',
            '            },',
            '            "summary": "Brief summary text"',
            '        }',
            '    </output_format>',
            '</system_prompt>'
        ])
        USER: str = '<user_input>Query: {query}\n\nDocumentation section:\n{doc_content}\n\nRespond with JSON.</user_input>'

    class Synthesizer:
        SYSTEM: str = '\n'.join([
            '<system_prompt>',
            '    <role>You synthesize information from multiple documentation sources and return JSON.</role>',
            '    <task>',
            '        1. Review all source responses',
            '        2. Identify most relevant information',
            '        3. Combine insights coherently',
            '        4. Include key quotes and code examples',
            '        5. Separate code examples from text quotes',
            '    </task>',
            '    <output_format>',
            '        You must return a valid JSON object with this exact schema:',
            '        {',
            '            "answer": "Brief 2-3 sentence answer",',
            '            "quotes": [',
            '                {',
            '                    "text": "Quote text or code block (include ```language for code)",',
            '                    "source": "File path",',
            '                    "relevance": "Why this quote/code is relevant",',
            '                    "is_code": true/false',
            '                }',
            '            ],',
            '            "context": "Additional context or null if none needed",',
            '            "confidence": {',
            '                "answer_quality": "high/medium/low",',
            '                "source_quality": "high/medium/low",',
            '                "completeness": "high/medium/low",',
            '                "code_examples": "high/medium/low/none"',
            '            }',
            '        }',
            '    </output_format>',
            '    <guidelines>',
            '    1. For code examples, always wrap in ```language blocks',
            '    2. Include command-line examples with ```bash',
            '    3. Include Python examples with ```python',
            '    4. Keep code examples focused and minimal',
            '    5. Ensure code examples are properly formatted',
            '    </guidelines>',
            '</system_prompt>'
        ])
        USER: str = '<user_input>Query: {query}\n\nSource responses:\n{responses}\n\nRespond with JSON.</user_input>'


@dataclass
class DocQuery:
    """Information about a documentation query."""
    query: str
    context: Optional[str] = None
    max_tokens: int = 150
    temperature: float = 0.7


class OpenAIHelper:
    """Main class for OpenAI-powered documentation assistance."""

    def __init__(self, api_key: Optional[str] = None, testing: bool = False, use_md_crawler: bool = True):
        """
        Initialize the OpenAI helper.

        1. Load environment variables
        2. Initialize OpenAI client
        3. Set up console for output
        4. Initialize thread pool for parallel queries
        5. Find markdown files if crawler enabled
        v5 - Added markdown file crawler option
        """
        self.console = Console()
        self.testing = testing
        self.executor = ThreadPoolExecutor(max_workers=GLOBAL_VARS["MAX_WORKERS"])
        self.llm_call_count = 0

        try:
            # Load environment variables if no API key provided
            if not api_key:
                api_key = os.environ.get('OPENAI_API_KEY')

            if not api_key:
                self.console.print("[red]No API key found. Please set OPENAI_API_KEY in Replit Secrets.[/red]")
                self.console.print("To add your API key:")
                self.console.print("1. Click Tools > Secrets")
                self.console.print("2. Add OPENAI_API_KEY with your API key")
                raise ValueError("Missing OPENAI_API_KEY")

            # Initialize OpenAI client
            self.client = OpenAI(api_key=api_key)

            # Test the API key unless in testing mode
            if not testing:
                self._test_api_key()

            # Update doc files list if crawler is enabled
            if use_md_crawler:
                md_files = find_md_files()
                if md_files:
                    GLOBAL_VARS["DOC_FILES"] = md_files
                    self.console.print(f"[grey50]Found {len(md_files)} markdown files in repository[/grey50]")

        except Exception as e:
            self.console.print(f"[red]Error initializing OpenAI helper: {str(e)}[/red]")
            raise

    def _test_api_key(self) -> None:
        """Test the API key with a minimal query."""
        try:
            self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hi"}],
                max_tokens=5
            )
        except Exception as e:
            raise ValueError(f"Failed to validate OpenAI API key: {str(e)}")

    def _read_doc_file(self, file_path: str) -> str:
        """Read a documentation file."""
        try:
            with open(file_path, 'r') as f:
                return f.read()
        except Exception as e:
            self.console.print(f"[red]Error reading {file_path}: {str(e)}[/red]")
            return ""

    def _log_llm_call(self, purpose: str) -> None:
        """Log an LLM API call."""
        self.llm_call_count += 1
        self.console.print(f"[grey50]#{self.llm_call_count} LLM Call: {purpose}[/grey50]")

    def _query_single_doc(self, query: str, doc_content: str, file_path: str) -> Dict:
        """
        Query a single documentation file and get confidence scores.

        1. Format messages
        2. Make API call with timeout
        3. Parse and return response
        v4 - Removed schema validation, using basic JSON format
        """
        try:
            messages = [
                {"role": "system", "content": PROMPTS.DocSearch.SYSTEM},
                {"role": "user", "content": PROMPTS.DocSearch.USER.format(
                    query=query,
                    doc_content=doc_content
                )}
            ]

            self._log_llm_call(f"Analyzing {os.path.basename(file_path)}")

            # Make API call with timeout
            response = self.client.with_options(timeout=GLOBAL_VARS["LLM_TIMEOUT"]).chat.completions.create(
                model=GLOBAL_VARS["MODEL"],
                messages=messages,
                temperature=GLOBAL_VARS["TEMPERATURE"],
                max_tokens=GLOBAL_VARS["MAX_TOKENS"],
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except TimeoutError:
            self.console.print(f"[red]Timeout analyzing {file_path}[/red]")
            return {
                "relevant_text": [],
                "confidence_scores": {k: "no" for k in GLOBAL_VARS["CONFIDENCE_RUBRIC"]},
                "summary": f"Error: Timeout analyzing document"
            }
        except json.JSONDecodeError:
            self.console.print(f"[red]Invalid JSON response from {file_path}[/red]")
            return {
                "relevant_text": [],
                "confidence_scores": {k: "no" for k in GLOBAL_VARS["CONFIDENCE_RUBRIC"]},
                "summary": f"Error: Invalid response format"
            }
        except Exception as e:
            self.console.print(f"[red]Error querying {file_path}: {str(e)}[/red]")
            return {
                "relevant_text": [],
                "confidence_scores": {k: "no" for k in GLOBAL_VARS["CONFIDENCE_RUBRIC"]},
                "summary": f"Error: {str(e)}"
            }

    def _synthesize_responses(self, query: str, doc_responses: List[Dict]) -> Dict:
        """
        Synthesize responses from multiple documentation sources.

        1. Format messages
        2. Make API call with timeout
        3. Parse and return response
        v4 - Removed schema validation, using basic JSON format
        """
        try:
            messages = [
                {"role": "system", "content": PROMPTS.Synthesizer.SYSTEM},
                {"role": "user", "content": PROMPTS.Synthesizer.USER.format(
                    query=query,
                    responses=json.dumps(doc_responses, indent=2)
                )}
            ]

            self._log_llm_call("Synthesizing responses")

            # Make API call with timeout
            response = self.client.with_options(timeout=GLOBAL_VARS["LLM_TIMEOUT"]).chat.completions.create(
                model=GLOBAL_VARS["MODEL"],
                messages=messages,
                temperature=GLOBAL_VARS["TEMPERATURE"],
                max_tokens=GLOBAL_VARS["MAX_TOKENS"],
                response_format={"type": "json_object"}
            )

            return json.loads(response.choices[0].message.content)

        except TimeoutError:
            self.console.print("[red]Timeout synthesizing responses[/red]")
            return {
                "answer": "Error: Timeout synthesizing responses",
                "quotes": [],
                "context": None,
                "confidence": {
                    "answer_quality": "low",
                    "source_quality": "low",
                    "completeness": "low",
                    "code_examples": "none"
                }
            }
        except json.JSONDecodeError:
            self.console.print("[red]Invalid JSON response from synthesis[/red]")
            return {
                "answer": "Error: Invalid response format",
                "quotes": [],
                "context": None,
                "confidence": {
                    "answer_quality": "low",
                    "source_quality": "low",
                    "completeness": "low",
                    "code_examples": "none"
                }
            }
        except Exception as e:
            self.console.print(f"[red]Error synthesizing responses: {str(e)}[/red]")
            return {
                "answer": f"Error synthesizing responses: {str(e)}",
                "quotes": [],
                "context": None,
                "confidence": {
                    "answer_quality": "low",
                    "source_quality": "low",
                    "completeness": "low",
                    "code_examples": "none"
                }
            }

    def query_docs_parallel(self, query: str) -> Dict:
        """
        Query all documentation files in parallel and synthesize results.

        1. Read all documentation files
        2. Query each file in parallel
        3. Collect and score responses
        4. Synthesize final response
        v3 - Added timeouts and simultaneous querying
        """
        try:
            # Read all documentation files simultaneously
            with ThreadPoolExecutor(max_workers=GLOBAL_VARS["MAX_WORKERS"]) as file_executor:
                file_futures = {
                    file_executor.submit(self._read_doc_file, file_path): file_path
                    for file_path in GLOBAL_VARS["DOC_FILES"]
                }

                doc_contents = {}
                for future in as_completed(file_futures, timeout=GLOBAL_VARS["TOTAL_TIMEOUT"]):
                    file_path = file_futures[future]
                    try:
                        content = future.result()
                        if content:  # Only store non-empty content
                            doc_contents[file_path] = content
                    except Exception as e:
                        self.console.print(f"[red]Error reading {file_path}: {str(e)}[/red]")

            # Query each file in parallel
            with ThreadPoolExecutor(max_workers=GLOBAL_VARS["MAX_WORKERS"]) as query_executor:
                query_futures = {
                    query_executor.submit(self._query_single_doc, query, content, file_path): file_path
                    for file_path, content in doc_contents.items()
                }

                # Collect responses as they complete
                doc_responses = []
                for future in as_completed(query_futures, timeout=GLOBAL_VARS["TOTAL_TIMEOUT"]):
                    file_path = query_futures[future]
                    try:
                        result = future.result()
                        result["file_path"] = file_path
                        doc_responses.append(result)
                    except Exception as e:
                        self.console.print(f"[red]Error processing {file_path}: {str(e)}[/red]")

            # Synthesize final response
            if not doc_responses:
                raise ValueError("No successful document queries")

            return self._synthesize_responses(query, doc_responses)

        except TimeoutError:
            self.console.print("[red]Total operation timeout exceeded[/red]")
            return {
                "answer": "Error: Operation timeout exceeded",
                "quotes": [],
                "context": None,
                "confidence": {
                    "answer_quality": "low",
                    "source_quality": "low",
                    "completeness": "low"
                }
            }
        except Exception as e:
            self.console.print(f"[red]Error in parallel query: {str(e)}[/red]")
            return {
                "answer": f"Error: {str(e)}",
                "quotes": [],
                "context": None,
                "confidence": {
                    "answer_quality": "low",
                    "source_quality": "low",
                    "completeness": "low"
                }
            }


def demo_functionality():
    """
    Run a demonstration of the OpenAI helper's capabilities.

    1. Initialize helper
    2. Run example queries in parallel
    3. Show parallel querying results with code examples
    v7 - Added parallel query execution and code examples
    """
    helper = OpenAIHelper(use_md_crawler=True)
    console = Console()

    console.print("\n[bold cyan]OpenAI Documentation Helper Demo[/bold cyan]")
    console.print("This demo shows how to query Vellum documentation using natural language.\n")

    # Example queries focused on CLI and common issues
    example_queries = [
        "How do I handle authentication and API keys in the Vellum CLI?",
        "What's the proper way to handle errors when executing prompts in the CLI?",
        "How can I export and analyze results from multiple prompt executions?"
    ]

    # Create results table
    table = Table(
        title="Documentation Query Results",
        show_header=True,
        header_style="bold magenta",
        show_lines=True,
        width=120
    )

    # Add columns with appropriate sizing
    table.add_column("Query", style="cyan", width=25)
    table.add_column("Answer", style="green", width=30)
    table.add_column("Supporting Evidence", style="yellow", width=35)
    table.add_column("Code Examples", style="magenta", width=30)
    table.add_column("Confidence", style="blue", width=20)

    # Run queries in parallel
    console.print("[bold cyan]Processing Queries in Parallel[/bold cyan]")

    with ThreadPoolExecutor(max_workers=len(example_queries)) as query_executor:
        # Submit all queries
        future_to_query = {
            query_executor.submit(helper.query_docs_parallel, query): query
            for query in example_queries
        }

        # Process results as they complete
        results = {}
        for future in as_completed(future_to_query):
            query = future_to_query[future]
            try:
                results[query] = future.result()
                console.print(f"[grey50]Completed query: {query}[/grey50]")
            except Exception as e:
                console.print(f"[red]Error processing query '{query}': {str(e)}[/red]")
                results[query] = {
                    "answer": f"Error: {str(e)}",
                    "quotes": [],
                    "context": None,
                    "confidence": {
                        "answer_quality": "low",
                        "source_quality": "low",
                        "completeness": "low"
                    }
                }

    # Add results to table in original order
    for query in example_queries:
        response = results[query]

        # Format quotes with sources
        quotes_text = []
        code_examples = []

        for quote in response.get("quotes", []):
            # Check if quote contains code
            text = quote.get('text', '')
            if '```' in text:
                code_examples.append(
                    f"[magenta]Example:[/magenta]\n{text}\n"
                    f"[dim]Source:[/dim] {quote.get('source', '')}"
                )
            else:
                quotes_text.append(
                    f"[yellow]Quote:[/yellow] {text}\n"
                    f"[dim]Source:[/dim] {quote.get('source', '')}\n"
                    f"[dim]Relevance:[/dim] {quote.get('relevance', '')}"
                )

        # Format confidence scores
        confidence = response.get("confidence", {})
        confidence_text = "\n".join([
            f"[blue]Answer:[/blue] {confidence.get('answer_quality', 'N/A')}",
            f"[blue]Sources:[/blue] {confidence.get('source_quality', 'N/A')}",
            f"[blue]Complete:[/blue] {confidence.get('completeness', 'N/A')}"
        ])

        # Add to table
        table.add_row(
            query,
            response.get("answer", "No answer available"),
            "\n\n".join(quotes_text) if quotes_text else "No quotes available",
            "\n\n".join(code_examples) if code_examples else "No code examples available",
            confidence_text
        )

    # Display final results
    console.print("\n[bold cyan]Final Results[/bold cyan]")
    console.print(table)

    console.print(f"\n[grey50]Total LLM Calls: {helper.llm_call_count}[/grey50]")

    console.print("\n[bold cyan]Try It Yourself[/bold cyan]")
    console.print("1. Set your OPENAI_API_KEY in .env")
    console.print("2. Import OpenAIHelper in your code")
    console.print("3. Use query_docs_parallel() for comprehensive answers")
    console.print("4. Get AI-powered documentation assistance with confidence scoring")


if __name__ == "__main__":
    demo_functionality()
