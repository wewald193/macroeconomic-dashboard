import os
from openai import OpenAI

# Initialize the client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

try:
    # Make a simple test call using the new interface
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "What is the GDP of the United States?"}
        ]
    )

    # Print the response
    print("API Connection Successful!")
    print("Response:", response.choices[0].message.content)

except Exception as e:
    print("An error occurred while testing the OpenAI API connection:")
    print(e)
