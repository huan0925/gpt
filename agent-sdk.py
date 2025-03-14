# # 載入 Agent SDK 所需的模組
import asyncio
from agents import Agent, Runner, WebSearchTool, function_tool, trace

@function_tool
def atom_habit(habit: str) -> str:
    return f"你想要利用原子習慣一書說明的方法養成 {habit} 的習慣"

@function_tool
def rich_poor_daddy() -> str:
    return f"你想要知道更多富爸爸與窮爸爸的內容"

atom_habbit_agent = Agent(
    name="Atom Habbit Reader",
    instructions="你是一個精通原子習慣這本書的 Agent，可以替使用者利用原子習慣書中的原理一步步引導使用者該如何做增加養成好習慣或戒掉壞習慣的方法。",
    tools=[atom_habit]
)

rich_poor_daddy_agent = Agent(
    name="Rich & Poor Daddy Reader",
    instructions="你是一個精通富爸爸與窮爸爸這本書的 Agent，可以更多地透過書中富爸爸為何致富，窮爸爸為何窮的內容，教導使用者該如何理財。",
    tools=[rich_poor_daddy]
)

finding_books_agent = Agent(
    name="Buying Books Agent",
    instructions="你是一個買書的助手，能夠進行網路搜索以查詢產品資訊。當用戶詢問關於產品的問題時，請使用 WebSearchTool 來獲取資訊。。",
    tools=[WebSearchTool()]
)

triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "你負責判斷用戶的需求：\n"
        "- 如果用戶提到原子習慣相關問題，請轉交給 Atom Habbit Reader 代理；\n"
        "- 如果用戶提到與財務有關的問題，則請轉接給 Rich & Poor Daddy Reader 代理; \n"
        "- 如果用戶詢問購買書籍相關的問題，則轉接給 Buying Books Agent 代理。"
    ),
    handoffs=[atom_habbit_agent, rich_poor_daddy_agent, finding_books_agent]  # 手動指定轉接的子代理
)

async def chat():
    print("Start chating, input 'exit' to finish chat...")
    
    # 生成一個唯一的 thread_id
    thread_id = "thread_" + str(hash(str(asyncio.current_task())))
    
    conversation_history = False
    
    with trace(workflow_name="Customer Service Conversation", group_id=thread_id):
        status = True
        while status:
            prompt = input("Prompt: ")
            
            # 檢查是否輸入退出指令
            if prompt.lower() in ['exit', 'quit', 'q']:
                print("\nSee you next time...")
                status = False
                break
            
            # 將新的輸入加入對話歷史
            if conversation_history:
                new_input = result.to_input_list() + [{"role": "user", "content": prompt}]
            else:
                new_input = prompt
                conversation_history = True
            
            # 使用 Runner.run 進行對話
            result = await Runner.run(
                starting_agent=triage_agent,
                input=new_input
            )
            
            print(result.final_output)

if __name__ == '__main__':
    # 運行異步主函數
    asyncio.run(chat())