# pip install vellum-ai python-dotenv rich
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from rich import print as rprint
from rich.console import Console
from rich.pretty import pprint
from rich.traceback import install
from vellum.client import Vellum
from vellum.types import PromptRequestStringInput

# Enable rich tracebacks with locals (totally bodacious debugging, man!)
install(show_locals=True)
console = Console()

# Load environment variables from a .env file
load_dotenv()

if VELLUM_API_KEY := os.environ.get("VELLUM_API_KEY"):
    client = Vellum(api_key=VELLUM_API_KEY)
else:
    raise EnvironmentError("VELLUM_API_KEY environment variable not set! Party on and set it up.")


class CONFIG:
    """Most excellent configuration for executing a Vellum prompt."""

    class PROMPT:
        # Set one of these, but not both!
        DEPLOYMENT_NAME: Optional[str] = "claim-extractor-v0-2-june24"
        PROMPT_VERSION_ID: Optional[str] = None
        PROMPT_RELEASE_TAG: str = "LATEST"  # Optional but defaults to 'LATEST'

    class INPUTS:
        # List of input dictionaries; add more if you need additional inputs, dude!
        LIST: List[Dict[str, Any]] = [
            {
                "INPUT_CONTENT": "This is a test claim. Elon musk is the richest person in the world. Or is he?"
            },
            # You can add more dictionaries here if required.
        ]

    class EXPAND_META:
        """Optional metadata to return for monitoring and analysis (totally rad for debugging)."""
        MODEL_NAME: bool = True
        USAGE: bool = True
        COST: bool = True
        FINISH_REASON: bool = True
        LATENCY: bool = True
        DEPLOYMENT_RELEASE_TAG: bool = True
        PROMPT_VERSION_ID: bool = True

    class EXPAND_RAW:
        """Optional raw info from the provider; might be useful if you wanna go low-level, man."""
        LOGPROBS: bool = True
        CHOICES: bool = True

    @staticmethod
    def _validate_config() -> None:
        """Validate that the configuration is totally excellent."""
        # Ensure at least one prompt identifier is provided
        if not CONFIG.PROMPT.DEPLOYMENT_NAME and not CONFIG.PROMPT.PROMPT_VERSION_ID:
            raise ValueError("Either DEPLOYMENT_NAME or PROMPT_VERSION_ID must be provided, dude!")

        # Ensure not both are provided (unless you're into chaos)
        if CONFIG.PROMPT.DEPLOYMENT_NAME and CONFIG.PROMPT.PROMPT_VERSION_ID:
            raise ValueError("Cannot provide both DEPLOYMENT_NAME and PROMPT_VERSION_ID. Choose your adventure!")

        # Validate that at least one input is provided
        if not CONFIG.INPUTS.LIST:
            raise ValueError("At least one input must be provided in CONFIG.INPUTS.LIST.")

        # Validate that each input is a dictionary
        for input_item in CONFIG.INPUTS.LIST:
            if not isinstance(input_item, dict):
                raise ValueError(f"Each input must be a dictionary, got {type(input_item)} instead.")

    @staticmethod
    def _create_input_objects() -> List[PromptRequestStringInput]:
        """Convert input dictionaries to PromptRequestStringInput objects."""
        input_objects: List[PromptRequestStringInput] = []
        for input_dict in CONFIG.INPUTS.LIST:
            for name, value in input_dict.items():
                try:
                    input_obj = PromptRequestStringInput(name=name, key="", value=value)  # TODO CHECK with Vellum. It's in the python output but failing mypy.
                    input_objects.append(input_obj)
                except Exception as e:
                    raise ValueError(f"Error creating input for ({name}: {value}). Error: {e}") from e
        return input_objects

    @staticmethod
    def _build_expand_meta() -> Optional[Dict[str, bool]]:
        """Build the expand_meta part of the request body."""
        meta_options = {
            "model_name": CONFIG.EXPAND_META.MODEL_NAME,
            "usage": CONFIG.EXPAND_META.USAGE,
            "cost": CONFIG.EXPAND_META.COST,
            "finish_reason": CONFIG.EXPAND_META.FINISH_REASON,
            "latency": CONFIG.EXPAND_META.LATENCY,
            "deployment_release_tag": CONFIG.EXPAND_META.DEPLOYMENT_RELEASE_TAG,
            "prompt_version_id": CONFIG.EXPAND_META.PROMPT_VERSION_ID,
        }
        expand_meta = {key: True for key, enabled in meta_options.items() if enabled}
        return expand_meta or None

    @staticmethod
    def _build_expand_raw() -> Optional[List[str]]:
        """Build the expand_raw part of the request body."""
        raw_options = {
            "logprobs": CONFIG.EXPAND_RAW.LOGPROBS,
            "choices": CONFIG.EXPAND_RAW.CHOICES,
        }
        expand_raw = [key for key, enabled in raw_options.items() if enabled]
        return expand_raw or None

    @staticmethod
    def _make_request_body() -> Dict[str, Any]:
        """Construct the complete request body for the Vellum API call."""
        CONFIG._validate_config()
        input_objects = CONFIG._create_input_objects()
        request_body: Dict[str, Any] = {
            "release_tag": CONFIG.PROMPT.PROMPT_RELEASE_TAG,
            "inputs": input_objects,
        }
        # Add the appropriate prompt identifier
        if CONFIG.PROMPT.DEPLOYMENT_NAME:
            request_body["prompt_deployment_name"] = CONFIG.PROMPT.DEPLOYMENT_NAME
        elif CONFIG.PROMPT.PROMPT_VERSION_ID:
            request_body["prompt_version_id"] = CONFIG.PROMPT.PROMPT_VERSION_ID

        if expand_meta := CONFIG._build_expand_meta():
            request_body["expand_meta"] = expand_meta

        if expand_raw := CONFIG._build_expand_raw():
            request_body["expand_raw"] = expand_raw

        return request_body


class VellumPromptRejectedError(Exception):
    """Raised when a Vellum prompt execution is rejected."""
    pass


def call_vellum_prompt(request_body: Dict[str, Any]) -> Any:
    """
    Execute the Vellum prompt using the provided request body.

    This function calls the prompt and handles any errors, ensuring a most excellent API call.
    """
    prompt_identifier = request_body.get("prompt_deployment_name") or request_body.get("prompt_version_id")
    rprint(f"[cyan]Calling Vellum prompt: {prompt_identifier} with inputs: {request_body.get('inputs')}[/cyan]")
    try:
        result = client.execute_prompt(**request_body)
    except Exception as exc:
        rprint(f"[red]An error occurred while executing the prompt: {exc}[/red]")
        raise

    if getattr(result, "state", None) == "REJECTED":
        error_message = getattr(result, "error_message", "Unknown error")
        rprint(f"[red]Prompt rejected: {error_message}[/red]")
        raise VellumPromptRejectedError(error_message)

    return result


def format_vellum_response(result: Any) -> Any:
    """
    Improve the readability of the Vellum prompt response object.
    1. convert latency from nanoseconds to seconds
    """
    result.latency = result.latency / 1_000_000_000
    return result


if __name__ == "__main__":
    try:
        # Build the request body using our totally radical CONFIG class
        rprint("[grey]Building request body:[/grey]")
        request_body = CONFIG._make_request_body()
        # Execute the Vellum prompt
        result = call_vellum_prompt(request_body)
        result = format_vellum_response(result)
        pprint(result)
        print("#--------------------------------------------------------")
        pprint(result.outputs)
    except Exception as e:
        rprint(f"[red]An exception occurred in main: {e}[/red]")
        raise
