from openai import OpenAI


def create_haiku():
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "developer", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Write a haiku about recursion in programming."}
        ]
    )
    print(completion.choices[0].message)


def describe_image():
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "user", "content": [
                {"type": "text", "text": "What's in this image?"},
                {"type": "image_url", "image_url": {"url": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/dd/Gfp-wisconsin-madison-the-nature-boardwalk.jpg/2560px-Gfp-wisconsin-madison-the-nature-boardwalk.jpg"}}
            ]}
        ]
    )
    print(completion.choices[0].message)


def extract_email():
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "developer", "content": "You extract email addresses into JSON data."},
            {"role": "user", "content": "Feeling stuck? Send a message to help@mycompany.com."}
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "email_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "email": {"description": "The email address that appears in the input", "type": "string"},
                        "additionalProperties": False
                    }
                }
            }
        }
    )
    print(response.choices[0].message.content)


if __name__ == "__main__":
    # Call the functions to demonstrate functionality
    create_haiku()
    describe_image()
    extract_email()
