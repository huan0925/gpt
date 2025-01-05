from openai import OpenAI
import json

client = OpenAI()

# 定義計算器功能
def calculate(operation, x, y):
    if operation == "加法":
        return {"result": x + y}
    elif operation == "減法":
        return {"result": x - y}
    elif operation == "乘法":
        return {"result": x * y}
    elif operation == "除法":
        if y == 0:
            return {"error": "不能除以零"}
        return {"result": x / y}

# 定義可用的工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "進行基本的數學運算",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {
                        "type": "string",
                        "enum": ["加法", "減法", "乘法", "除法"],
                        "description": "要執行的數學運算"
                    },
                    "x": {
                        "type": "number",
                        "description": "第一個數字"
                    },
                    "y": {
                        "type": "number",
                        "description": "第二個數字"
                    }
                },
                "required": ["operation", "x", "y"]
            }
        }
    }
]

# 測試對話
messages = [
    {"role": "user", "content": "三加五等於多少？"}
]

# 調用 API
response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

# 處理回應
if response.choices[0].message.tool_calls:
    # 獲取函數調用信息
    tool_call = response.choices[0].message.tool_calls[0]
    print(tool_call)
    
    # 解析參數
    function_args = json.loads(tool_call.function.arguments)
    
    # 執行計算
    result = calculate(
        function_args["operation"],
        function_args["x"],
        function_args["y"]
    )
    
    print(f"計算結果：{result['result']}")
else:
    print("模型沒有選擇使用計算器功能")
