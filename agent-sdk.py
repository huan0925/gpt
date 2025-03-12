# 載入 Agent SDK 所需的模組
from agents import Agent, Runner, WebSearchTool, function_tool

# 定義一個工具函數，用來模擬處理退款請求的邏輯
@function_tool
def submit_refund_request(item_id: str, reason: str) -> str:
    # 模擬退款邏輯（實際情況下可以連接數據庫或第三方支付系統）
    return f"已提交退款申請，商品編號 {item_id}，原因：{reason}"

# 定義一個客服代理，專門處理退款相關的問題
support_agent = Agent(
    name="Support & Returns",
    instructions="你是一個客服代理，專門負責退款事宜。當收到退款相關的指令時，請使用 submit_refund_request 工具來處理退款申請。",
    tools=[submit_refund_request]
)

# 定義一個購物助手代理，利用內建的 WebSearchTool 來幫助用戶查詢產品資訊
shopping_agent = Agent(
    name="Shopping Assistant",
    instructions="你是一個購物助手，能夠進行網路搜索以查詢產品資訊。當用戶詢問關於產品的問題時，請使用 WebSearchTool 來獲取資訊。",
    tools=[WebSearchTool()]
)

# 定義一個調度代理，負責判斷用戶的需求並轉接到合適的子代理
triage_agent = Agent(
    name="Triage Agent",
    instructions=(
        "你負責判斷用戶的需求：\n"
        "- 如果用戶提到退款、退貨等，則請將請求轉接給 Support & Returns 代理；\n"
        "- 如果用戶詢問產品資訊、推薦等，則請轉接給 Shopping Assistant 代理。"
    ),
    handoffs=[shopping_agent, support_agent]  # 手動指定轉接的子代理
)

# 使用 Runner.run_sync 以同步方式啟動代理流程，並傳入用戶的原始輸入
output = Runner.run_sync(
    starting_agent=triage_agent,
    input="我剛剛購買的鞋子有問題，我想申請退款。"
)

print("最終輸出：", output)