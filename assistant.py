from openai import OpenAI

def chat_with_assistant():
    client = OpenAI()
    
    # 创建助手
    assistant = client.beta.assistants.create(
        name="Coding assistant",
        instructions="你是一个专业的编程助手，可以帮助用户解决各种编程问题。",
        model="gpt-4o-mini",
        tools=[{"type": "code_interpreter"}]
    )
    
    # 创建会话
    thread = client.beta.threads.create()
    
    # 添加用户消息
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="用 50 字解释一下Python中的装饰器是什么？"
    )
    
    # 运行助手
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    
    # 等待运行完成
    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "completed":
            break

    
    # 获取助手回复
    messages = client.beta.threads.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            print(msg.content[0].text.value)

# 直接调用，没有使用 Python 的线程
chat_with_assistant()

