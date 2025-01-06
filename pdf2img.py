import fitz  # PyMuPDF
from PIL import Image
import io
from openai import OpenAI
import base64

def pdf_to_images(pdf_path):
    """将PDF转换为图片列表"""
    pdf_document = fitz.open(pdf_path)
    images = []
    
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        images.append(img)
    
    pdf_document.close()
    return images

def image_to_base64(image):
    """将PIL Image转换为base64字符串"""
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def get_pages_with_tables(pdf_path):
    """检测PDF中包含表格的页面"""
    doc = fitz.open(pdf_path)
    pages_with_tables = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        # 检测页面中的表格
        tables = page.find_tables()
        if tables.tables:  # 如果找到表格
            pages_with_tables.append(page_num)
    
    doc.close()
    return pages_with_tables

# Put single page into model
def analyze_specific_page_with_gpt(pdf_path, page_num, prompt, preview=True):
    """分析PDF中特定页面的内容"""
    client = OpenAI()
    
    # 只处理指定页面
    pdf_document = fitz.open(pdf_path)
    if page_num >= len(pdf_document):
        print(f"错误：PDF只有 {len(pdf_document)} 页")
        pdf_document.close()
        return
        
    # 预览页面内容
    if preview:
        page = pdf_document[page_num]
        print(f"\n=== 第 {page_num + 1} 页内容预览 ===")
        print(page.get_text().strip()[:500] + "...")  # 只显示前500个字符
        print("=" * 50)
        user_input = input("是否继续分析这个页面？(y/n): ")
        if user_input.lower() != 'y':
            print("已取消分析")
            pdf_document.close()
            return
    
    # 转换指定页面为图片
    page = pdf_document[page_num]
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    pdf_document.close()
    
    # 將 PIL Image 保存為 JPEG 格式，並進行壓縮
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG", quality=85, optimize=True)  # quality 可以調整，範圍 1-100
    buffered.seek(0)
    base64_image = base64.b64encode(buffered.getvalue()).decode()
    
    # 创建GPT请求
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Just give me the shortest response or I need to pay a lot of money. And just give me the information in the file."},
            {
                "role": "user",
                "content": [
                    
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=1000
    )
    
    print(f"第 {page_num + 1} 页分析结果:")
    print(response.choices[0].message.content)
    print("-" * 50)



# Put all page into model
def analyze_pdf_with_gpt(pdf_path, prompt):
    """使用GPT分析PDF中包含表格的页面"""
    client = OpenAI()
    
    # 获取包含表格的页面编号
    table_pages = get_pages_with_tables(pdf_path)
    
    if not table_pages:
        print("未检测到任何表格！")
        return
    
    # 只将包含表格的页面转换为图片
    pdf_document = fitz.open(pdf_path)
    images = []
    for page_num in table_pages:
        page = pdf_document[page_num]
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # 將 PIL Image 保存為 JPEG 格式
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG", quality=85, optimize=True)
        buffered.seek(0)
        images.append((page_num + 1, buffered))
    pdf_document.close()
    
    # 准备内容
    content = [{"type": "text", "text": f"{prompt}\n以下是PDF中包含表格的页面（第 {', '.join(str(p+1) for p in table_pages)} 页）："}]
    
    # 将所有表格页面的图片添加到内容中
    for page_num, image_buffer in images:
        base64_image = base64.b64encode(image_buffer.getvalue()).decode()
        content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
            }
        })
    
    # 创建GPT请求
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Just give me the shortest ressponse or I need to pay a lot of money."},
            {
                "role": "user",
                "content": content
            }
        ],
        max_tokens=1000
    )
    
    print("表格分析结果:")
    print(response.choices[0].message.content)
    print("-" * 50)

# 使用示例
# pdf_path = "/Users/linzhihuan/Downloads/林芝歡考生資料.pdf"
# prompt = "How old is she now?"
# analyze_pdf_with_gpt(pdf_path, prompt)

pdf_path = '/Users/linzhihuan/Desktop/gpt/Test Document.pdf'
page_num = 0  # 第一页从0开始
prompt = "Gama 系列的 XC1234 的防護等級是什麼？"
analyze_specific_page_with_gpt(pdf_path, page_num, prompt)