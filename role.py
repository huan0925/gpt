from openai import OpenAI

client = OpenAI()

# Only user prompt
def user_prompt():
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user", 
                "content": "I'm five years old, please introduce what is Decorator in Python."
            }
        ],
    )

    print(completion.choices[0].message.content)

# developer and user prompt
def developer_user_prompt():

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "developer", 
                "content": "You are a Python tutor. You can only respond to Python questions. If a question is out of scope, just say 'I don't know.'"
            },
            {
                "role": "user", 
                "content": "I'm five years old, please introduce what is ChatGPT."
            }
        ],
    )

    print(completion.choices[0].message.content)

# developer, user and assistant prompt
def developer_user_assistant_prompt():

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system", 
                "content": "You are a Python tutor. You can only respond to Python questions. If a question is out of scope, just say 'You don't know.'"
            },
            {
                "role": "user", 
                "content": "I'm five years old, please introduce what is Decorator in Python."
            },
            {
                "role": "assistant", 
                "content": "Please answer in a bullet point format and provide me with the three most important concepts. \
                    Each point should be no more than 10 words. Do not include any sample code."
            }
        ],
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    # user_prompt ()
    # developer_user_prompt()
    developer_user_assistant_prompt()