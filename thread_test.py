from openai import OpenAI
import threading
import time

def chat_thread():
    client = OpenAI()
    
    # 创建对话
    conversation = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "你是一个有帮助的助手。"},
            {"role": "user", "content": "Please introduce Mediatek in 400 words."}
        ],
        stream=True  # 启用流式输出
    )
    
    # 实时输出回复
    for chunk in conversation:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")

# 创建并启动线程            
chat = threading.Thread(target=chat_thread)
chat.start()

# 等待线程结束
chat.join()
