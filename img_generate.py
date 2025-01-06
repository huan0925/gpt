from io import BytesIO
from PIL import Image
from openai import OpenAI
client = OpenAI()

# generate image
# response = client.images.generate(
#     model="dall-e-3",
#     prompt="a white siamese cat",
#     size="1024x1024",
#     quality="standard",
#     n=1,
# )

# print(response.data[0].url)

# response = client.images.create_variation(
#     model="dall-e-2",
#     image=open("/Users/linzhihuan/Downloads/GAI.png", "rb"),
#     n=1,
#     size="1024x1024"
# )

# print(response.data[0].url)

# Read the image file from disk and resize it
image = Image.open("/Users/linzhihuan/Downloads/GAI.png")
width, height = 256, 256
image = image.resize((width, height))

# 將圖片轉換為二進制格式
byte_stream = BytesIO()  # 創建一個二進制流對象
image.save(byte_stream, format='PNG')  # 將圖片以 PNG 格式保存到二進制流中
byte_array = byte_stream.getvalue()  # 獲取二進制數據

# 調用 OpenAI API 生成圖片變體
response = client.images.create_variation(
    image=byte_array,    # 輸入圖片的二進制數據
    n=4,                 # 生成變體的數量 DALL-E 2 支援 1-10
    model="dall-e-2",    # 使用的模型版本
    size="1024x1024"     # 輸出圖片的尺寸
)

for i, image_data in enumerate(response.data):
    print(f"變體 {i+1} URL: {image_data.url}")