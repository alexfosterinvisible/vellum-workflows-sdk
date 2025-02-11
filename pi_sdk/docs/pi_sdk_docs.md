

2 Pi R SDK home pagedark logo

Search...
⌘K
Get Started
2 Pi R SDK
Quickstart
Python API Library
Node API Library
API Reference
Introduction
Contracts
Inputs
Feedback
Inference
Prompts
Get Started
Python API Library
Installation and usage of the Python library

The Twopir Python library provides convenient access to the Twopir REST API from any Python 3.8+ application. The library includes type definitions for all request params and response fields, and offers both synchronous and asynchronous clients powered by httpx.

It is generated with Stainless.

​
Installation

# install from the production repo
pip install git+ssh://git@github.com/2pir-ai/sdk-python.git
You will need a Twopir token from us to gain access to this repository.

​
Usage

import os
from twopir import Twopir

client = Twopir(
    api_key=os.environ.get("TWOPIR_API_KEY"),  # This is the default and can be omitted
)

contracts_score_metrics = client.contracts.score(
    contract={
        "name": "My Application",
        "description": "You are a helpful assistant",
        "dimensions": [
            {
                "description": "Test whether the LLM follows instructions",
                "label": "Instruction Following",
            },
            {
                "description": "Test whether the LLM responds to the query",
                "label": "Topicality",
            },
        ],
    },
    llm_input="Help me with my problem",
    llm_output="Of course I can help with that",
)
print(contracts_score_metrics.scores)
While you can provide an api_key keyword argument, we recommend using python-dotenv to add TWOPIR_API_KEY="My API Key" to your .env file so that your API Key is not stored in source control.

​
Async usage
Simply import AsyncTwopir instead of Twopir and use await with each API call:


import os
import asyncio
from twopir import AsyncTwopir

client = AsyncTwopir(
    api_key=os.environ.get("TWOPIR_API_KEY"),  # This is the default and can be omitted
)


async def main() -> None:
    contracts_score_metrics = await client.contracts.score(
        contract={
            "name": "My Application",
            "description": "You are a helpful assistant",
            "dimensions": [
                {
                    "description": "Test whether the LLM follows instructions",
                    "label": "Instruction Following",
                },
                {
                    "description": "Test whether the LLM responds to the query",
                    "label": "Topicality",
                },
            ],
        },
        llm_input="Help me with my problem",
        llm_output="Of course I can help with that",
    )
    print(contracts_score_metrics.scores)


asyncio.run(main())
Functionality between the synchronous and asynchronous clients is otherwise identical.

​
Using types
Nested request parameters are TypedDicts. Responses are Pydantic models which also provide helper methods for things like:

Serializing back into JSON, model.to_json()
Converting to a dictionary, model.to_dict()
Typed requests and responses provide autocomplete and documentation within your editor. If you would like to see type errors in VS Code to help catch bugs earlier, set python.analysis.typeCheckingMode to basic.

​
Handling errors
When the library is unable to connect to the API (for example, due to network connection problems or a timeout), a subclass of twopir.APIConnectionError is raised.

When the API returns a non-success status code (that is, 4xx or 5xx response), a subclass of twopir.APIStatusError is raised, containing status_code and response properties.

All errors inherit from twopir.APIError.


import twopir
from twopir import Twopir

client = Twopir()

try:
    client.contracts.score(
        contract={
            "name": "My Application",
            "description": "You are a helpful assistant",
            "dimensions": [
                {
                    "description": "Test whether the LLM follows instructions",
                    "label": "Instruction Following",
                },
                {
                    "description": "Test whether the LLM responds to the query",
                    "label": "Topicality",
                },
            ],
        },
        llm_input="Help me with my problem",
        llm_output="Of course I can help with that",
    )
except twopir.APIConnectionError as e:
    print("The server could not be reached")
    print(e.__cause__)  # an underlying Exception, likely raised within httpx.
except twopir.RateLimitError as e:
    print("A 429 status code was received; we should back off a bit.")
except twopir.APIStatusError as e:
    print("Another non-200-range status code was received")
    print(e.status_code)
    print(e.response)
Error codes are as followed:

Status Code	Error Type
400	BadRequestError
401	AuthenticationError
403	PermissionDeniedError
404	NotFoundError
422	UnprocessableEntityError
429	RateLimitError
>=500	InternalServerError
N/A	APIConnectionError
​
Retries
Certain errors are automatically retried 2 times by default, with a short exponential backoff. Connection errors (for example, due to a network connectivity problem), 408 Request Timeout, 409 Conflict, 429 Rate Limit, and >=500 Internal errors are all retried by default.

You can use the max_retries option to configure or disable retry settings:


from twopir import Twopir

# Configure the default for all requests:
client = Twopir(
    # default is 2
    max_retries=0,
)

# Or, configure per-request:
client.with_options(max_retries=5).contracts.score(
    contract={
        "name": "My Application",
        "description": "You are a helpful assistant",
        "dimensions": [
            {
                "description": "Test whether the LLM follows instructions",
                "label": "Instruction Following",
            },
            {
                "description": "Test whether the LLM responds to the query",
                "label": "Topicality",
            },
        ],
    },
    llm_input="Help me with my problem",
    llm_output="Of course I can help with that",
)
​
Timeouts
By default requests time out after 1 minute. You can configure this with a timeout option, which accepts a float or an httpx.Timeout object:


from twopir import Twopir

# Configure the default for all requests:
client = Twopir(
    # 20 seconds (default is 1 minute)
    timeout=20.0,
)

# More granular control:
client = Twopir(
    timeout=httpx.Timeout(60.0, read=5.0, write=10.0, connect=2.0),
)

# Override per-request:
client.with_options(timeout=5.0).contracts.score(
    contract={
        "name": "My Application",
        "description": "You are a helpful assistant",
        "dimensions": [
            {
                "description": "Test whether the LLM follows instructions",
                "label": "Instruction Following",
            },
            {
                "description": "Test whether the LLM responds to the query",
                "label": "Topicality",
            },
        ],
    },
    llm_input="Help me with my problem",
    llm_output="Of course I can help with that",
)
On timeout, an APITimeoutError is thrown.

Note that requests that time out are retried twice by default.

​
Advanced
​
Logging
We use the standard library logging module.

You can enable logging by setting the environment variable TWOPIR_LOG to info.


$ export TWOPIR_LOG=info
Or to debug for more verbose logging.

​
How to tell whether None means null or missing
In an API response, a field may be explicitly null, or missing entirely; in either case, its value is None in this library. You can differentiate the two cases with .model_fields_set:


if response.my_field is None:
  if 'my_field' not in response.model_fields_set:
    print('Got json like {}, without a "my_field" key present at all.')
  else:
    print('Got json like {"my_field": null}.')
​
Accessing raw response data (e.g. headers)
The “raw” Response object can be accessed by prefixing .with_raw_response. to any HTTP method call, e.g.,


from twopir import Twopir

client = Twopir()
response = client.contracts.with_raw_response.score(
    contract={
        "name": "My Application",
        "description": "You are a helpful assistant",
        "dimensions": [{
            "description": "Test whether the LLM follows instructions",
            "label": "Instruction Following",
        }, {
            "description": "Test whether the LLM responds to the query",
            "label": "Topicality",
        }],
    },
    llm_input="Help me with my problem",
    llm_output="Of course I can help with that",
)
print(response.headers.get('X-My-Header'))

contract = response.parse()  # get the object that `contracts.score()` would have returned
print(contract.dimension_scores)
These methods return an APIResponse object.

The async client returns an AsyncAPIResponse with the same structure, the only difference being awaitable methods for reading the response content.

​
.with_streaming_response
The above interface eagerly reads the full response body when you make the request, which may not always be what you want.

To stream the response body, use .with_streaming_response instead, which requires a context manager and only reads the response body once you call .read(), .text(), .json(), .iter_bytes(), .iter_text(), .iter_lines() or .parse(). In the async client, these are async methods.


with client.contracts.with_streaming_response.score(
    contract={
        "name": "My Application",
        "description": "You are a helpful assistant",
        "dimensions": [
            {
                "description": "Test whether the LLM follows instructions",
                "label": "Instruction Following",
            },
            {
                "description": "Test whether the LLM responds to the query",
                "label": "Topicality",
            },
        ],
    },
    llm_input="Help me with my problem",
    llm_output="Of course I can help with that",
) as response:
    print(response.headers.get("X-My-Header"))

    for line in response.iter_lines():
        print(line)
The context manager is required so that the response will reliably be closed.

​
Configuring the HTTP client
You can directly override the httpx client to customize it for your use case, including:

Support for proxies
Custom transports
Additional advanced functionality

import httpx
from twopir import Twopir, DefaultHttpxClient

client = Twopir(
    # Or use the `TWOPIR_BASE_URL` env var
    base_url="http://my.test.server.example.com:8083",
    http_client=DefaultHttpxClient(
        proxy="http://my.test.proxy.example.com",
        transport=httpx.HTTPTransport(local_address="0.0.0.0"),
    ),
)
You can also customize the client on a per-request basis by using with_options():


client.with_options(http_client=DefaultHttpxClient(...))
​
Managing HTTP resources
By default the library closes underlying HTTP connections whenever the client is garbage collected. You can manually close the client using the .close() method if desired, or with a context manager that closes when exiting.

​
Versioning
This package generally follows SemVer conventions, though certain backwards-incompatible changes may be released as minor versions:

Changes that only affect static types, without breaking runtime behavior.
Changes to library internals which are technically public but not intended or documented for external use. (Please open a GitHub issue to let us know if you are relying on such internals).
Changes that we do not expect to impact the vast majority of users in practice.
We take backwards-compatibility seriously and work hard to ensure you can rely on a smooth upgrade experience.

We are keen for your feedback; please open an issue with questions, bugs, or suggestions.

​
Determining the installed version
If you’ve upgraded to the latest version but aren’t seeing any new features you were expecting then your python environment is likely still using an older version.

You can determine the version that is being used at runtime with:


import twopir
print(twopir.__version__)
​
Requirements
Python 3.8 or higher.

Quickstart
Node API Library
Powered by Mintlify
On this page
Installation
Usage
Async usage
Using types
Handling errors
Retries
Timeouts
Advanced
Logging
How to tell whether None means null or missing
Accessing raw response data (e.g. headers)
.with_streaming_response
Configuring the HTTP client
Managing HTTP resources
Versioning
Determining the installed version
Requirements
