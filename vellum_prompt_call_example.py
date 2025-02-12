"""
To execute prompts in Vellum with both meta and raw data returned, you can utilize the expand_meta and expand_raw parameters in your API request. These parameters allow you to retrieve additional metadata and raw response fields from the model provider, respectively.

1. expand_meta Parameter:

The expand_meta parameter enables you to include additional metadata about the prompt execution in the API response. This can be useful for monitoring and analysis purposes. The available fields you can request include:
	•	model_name: The name of the model used for execution.
	•	usage: Information about token usage.
	•	cost: The cost associated with the prompt execution.
	•	finish_reason: The reason why the model stopped generating tokens.
	•	latency: The time taken for the prompt execution.
	•	deployment_release_tag: The release tag of the prompt deployment.
	•	prompt_version_id: The version ID of the prompt used.

To include these fields in your response, set the expand_meta parameter in your request body as follows:

"expand_meta": {
  "model_name": true,
  "usage": true,
  "cost": true,
  "finish_reason": true,
  "latency": true,
  "deployment_release_tag": true,
  "prompt_version_id": true
}

2. expand_raw Parameter:

The expand_raw parameter allows you to specify a list of keys whose values you’d like to directly return from the JSON response of the model provider. This is useful if you need lower-level information that Vellum would otherwise omit. The corresponding key/value pairs will be returned under the raw key of the API response.

For example, to retrieve the logprobs and choices fields from the raw response, you can set the expand_raw parameter as follows:

"expand_raw": ["logprobs", "choices"]

Example Request:

Combining both parameters, your API request body would look like this:

{
  "inputs": {
    "your_input_variable": "your_input_value"
  },
  "expand_meta": {
    "model_name": true,
    "usage": true,
    "cost": true,
    "finish_reason": true,
    "latency": true,
    "deployment_release_tag": true,
    "prompt_version_id": true
  },
  "expand_raw": ["logprobs", "choices"]
}

By configuring these parameters, you can obtain both the metadata and raw response data from your prompt executions in Vellum.

￼
"""

# pip install vellum-ai
import os
from vellum.client import Vellum
import vellum.types as types
from dotenv import load_dotenv
from pprint import pprint
from rich import print as rprint

load_dotenv()

# create your API key here: https://app.vellum.ai/api-keys#keys
client = Vellum(api_key=os.environ["VELLUM_API_KEY"])


def call_vellum_prompt(prompt_name: str, inputs: dict):
    rprint(f"[cyan]Calling Vellum prompt: {prompt_name} with inputs: {inputs}[/cyan]")
    result = client.execute_prompt(
        prompt_deployment_name=prompt_name,
        release_tag="LATEST",
    inputs=[
        types.PromptRequestStringInput(
            name="INPUT_CONTENT",
            key="",
            value="<example-string-value>",
        ),
        ],
    )

    if result.state == "REJECTED":
        raise Exception(result.error.message)

    return result


if __name__ == "__main__":
    class CONFIG:
        """prompt_deployment_name = {{}} OR prompt_version_id = {{}}, OPTIONAL: release_tag = {{}}"""
        PROMPT_DEPLOYMENT_NAME:str = "claim-extractor-v0-2-june24"  # either this or PROMPT_VERSION_ID is used as the ID
        PROMPT_VERSION_ID:str = ""  # TODO (check if string) either this or PROMPT_DEPLOYMENT_NAME is used as the ID
        INPUTS:dict = {"INPUT_CONTENT": "This is a test claim. Elon musk is the richest person in the world. Or is he?"} # dict of input variables and the values you are passing in. Key MUST match.
        class CONFIG_EXTRA:
            """These just return additional information. Keep them on. OPTIONAL:expand_meta = {{}} OPTIONAL: expand_raw = {{}}"""
            class EXPAND_META:
                MODEL_NAME:bool = True
                USAGE:bool = True
                COST:bool = True
                FINISH_REASON:bool = True
                LATENCY:bool = True
                DEPLOYMENT_RELEASE_TAG:bool = True
                PROMPT_VERSION_ID:bool = True
            class EXPAND_RAW:
                LOGPROBS:bool = True
                CHOICES:bool = True
            






  "inputs": {
    "your_input_variable": "your_input_value"
  },
  "expand_meta": {
    "model_name": true,
    "usage": true,
    "cost": true,
    "finish_reason": true,
    "latency": true,
    "deployment_release_tag": true,
    "prompt_version_id": true
  },
  "expand_raw": ["logprobs", "choices"]
}
    
    result = call_vellum_prompt(
        prompt_name=CONFIG.PROMPT_NAME,
        inputs=CONFIG.INPUTS)
    
    pprint(f"Result: {result}")
    rprint(f"[cyan]Result:[/cyan] {result!r}")
    print("\n\n")
    pprint(f"Result.outputs: {result.outputs}")
    rprint(f"[cyan]Result.outputs:[/cyan] {result.outputs!r}")
