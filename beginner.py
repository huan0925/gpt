from openai import OpenAI
client = OpenAI()

# Streaming
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Please give me an introduction about OpenAI."
        }
    ],
    stream=True # for streaming, can only access in completion.choices[0].message.content
)


# for streaming
for chunk in completion:
    if chunk.choices[0].delta.content is not None:
        print(chunk.choices[0].delta.content, end="")


# Without streaming
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "developer",
            "content": [
                {"type": "text",
                 "text": "You are a helpful assistant that answers programming questions in the style of a southern belle from the southeast United States."
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "Are semicolons optional in JavaScript?"
        }
      ]
    }
    ]
)

print(completion.choices[0].message.content)
