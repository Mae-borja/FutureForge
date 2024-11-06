from groq import Groq
import os

# Initialize the Groq client using the API key
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Create a chat completion request
completion = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[{
        "role": "user",
        "content": "Give me an overview of my skills based on the following text: \nPython, Data Analysis, Machine Learning, Web Development"
    }],
    temperature=1,
    max_tokens=1024,
    top_p=1,
    stream=False,  # Non-streaming response
)

# Access the response text directly
response_text = completion.choices[0].message.content  # Correct attribute access

# Print the response text
print(f"Cleaned Response Text:\n", response_text)
