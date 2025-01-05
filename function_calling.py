from openai import OpenAI
import json
client = OpenAI()

def extract_bullet_point(article):
    # 實際的函數實現
    return {"bullet_points": ["點1", "點2", "點3"]}

tools = [
  {
    "type": "function",
    "function": {
      "name": "extract_focal_points",
      "description": "Extract three focal point from input message.",
      "parameters": {
        "type": "object",
        "properties": {
          "focal_points": {
            "type": "array",
            "items":{
                "type": "string",
                "description": "Extract three focal point from input message."
            }
          },
        },
        "required": ["focal_points"],
      },
    }
  }
]
messages = [
    {"role": "developer", "content": "Just simply response in three bullet points"},
    {"role": "user", "content": "In a career of 3-point achievements, Stephen Curry had never connected on more than six triples without a miss. Until Thursday. While racking up 30 points, six rebounds and 10 assists in the Warriors’ 139-105 rout of the 76ers, Curry shot a perfect 8-for-8 from long range. To add another layer to the accomplishment, Curry played through the game with a right thumb sprain and had tape on his right hand. “Sometimes when you have a little injury or something that’s random, it kind of forces you to focus a little bit,” Curry said. “And just be free. [I was] just happy that I got to play. I was kind of unsure going into the day. “I didn’t get many attempts in the first half, but all four of them are really good in-rhythm shots and then from there you’re kind of just flowing off of the joy of things going our way and having a day where Dennis [Schroder] hit three in the first half, JK [Jonathan Kuminga] came in and hit some big shots, Moses [Moody], everybody was kind of just feeling the rhythm of the night. His performance made him the first player in NBA history to record 30-plus points, 10-plus assists and eight or more 3-pointers while shooting 100% from deep in a game. He’s also the first player to record 10-plus assists in that scenario. Curry had 24 points by halftime after going 6-for-6 from 3-point range. He made consecutive 3-pointers early in the fourth to put the Warriors up by 30 and left the game as both coaches emptied their benches minutes later. This was Curry’s sixth game this season with 30 or more points and the 296th game of his career."},
]
completion = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=messages,
  tools=tools,
  tool_choice="auto"
)

response = json.loads(completion.choices[0].message.tool_calls[0].function.arguments)

for i in range(len(response['focal_points'])):
    print(f"Point{i}: {response['focal_points'][i]}")

# 檢查是否有函數調用
# if completion.choices[0].message.tool_calls:
#     # 獲取函數調用信息
#     tool_call = completion.choices[0].message.tool_calls[0]
#     function_name = tool_call.function.name
#     function_args = json.loads(tool_call.function.arguments)
    
#     # 執行函數
#     if function_name == "extract_bullet_point":
#         function_response = extract_bullet_point(function_args["article"])
        
#         # 將函數執行結果添加到對話中
#         messages.append(completion.choices[0].message)  # 添加助手的回應
#         messages.append({
#             "role": "tool",
#             "tool_call_id": tool_call.id,
#             "name": function_name,
#             "content": json.dumps(function_response)
#         })
        
#         # 獲取最終結果
#         final_response = client.chat.completions.create(
#             model="gpt-4o-mini",
#             messages=messages
#         )
        
#         print("最終回答:", final_response.choices[0].message.content)
# else:
#     # 如果沒有函數調用，直接輸出回答
#     print("直接回答:", completion.choices[0].message.content)
