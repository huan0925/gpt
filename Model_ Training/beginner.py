# 匯入必要的庫
import torch
from torch.utils.data import DataLoader
from transformers import AutoTokenizer, AutoModel
from sentence_transformers import SentenceTransformer, losses, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from datasets import load_dataset

# 檢查 MPS 是否可用
if torch.backends.mps.is_available():
    print("MPS is available. Using Apple GPU for acceleration!")
else:
    print("MPS is not available. Running on CPU.")


# ===============================
# 1. 確定設備
# ===============================
print("Step 1: 確定設備開始...")
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")
print("Step 1: 確定設備完成！")

# ===============================
# 2. 加載預訓練模型和分詞器
# ===============================
print("Step 2: 加載預訓練模型和分詞器開始...")
model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name).to(device)
print(f"Model {model_name} 已加載到設備 {device} 上")
print("Step 2: 加載預訓練模型和分詞器完成！")

# ===============================
# 3. 准備數據集
# ===============================
print("Step 3: 准備數據集開始...")
dataset = load_dataset("glue", "stsb")
train_examples = [
    InputExample(texts=[example["sentence1"], example["sentence2"]], label=float(example["label"]) / 5.0)
    for example in dataset["train"]
]
val_examples = [
    InputExample(texts=[example["sentence1"], example["sentence2"]], label=float(example["label"]) / 5.0)
    for example in dataset["validation"]
]
print(f"Train examples: {len(train_examples)}, Validation examples: {len(val_examples)}")
print("Step 3: 准備數據集完成！")

# ===============================
# 4. 創建數據加載器
# ===============================
print("Step 4: 創建數據加載器開始...")
train_dataloader = DataLoader(train_examples, batch_size=16, shuffle=True)
val_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(val_examples, name="sts-dev")
print("Train DataLoader 和 Validation Evaluator 已創建！")
print("Step 4: 創建數據加載器完成！")

# ===============================
# 5. 設置損失函數和優化器
# ===============================
print("Step 5: 設置損失函數和優化器開始...")
train_loss = losses.CosineSimilarityLoss(model=SentenceTransformer(model_name))
print("損失函數已設置！")
print("Step 5: 設置損失函數和優化器完成！")

# ===============================
# 6. 訓練模型
# ===============================
print("Step 6: 訓練模型開始...")
model = SentenceTransformer(model_name)
num_epochs = 4
warmup_steps = int(len(train_dataloader) * num_epochs * 0.1)  # 10% 的 Warm-up
print(f"模型將進行 {num_epochs} 輪訓練，每輪 Warm-up 步驟為 {warmup_steps}")

model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    evaluator=val_evaluator,
    epochs=num_epochs,
    evaluation_steps=1000,
    warmup_steps=warmup_steps,
    output_path="./trained_embedding_model",
)
print("Step 6: 訓練模型完成！")

# ===============================
# 7. 保存和測試模型
# ===============================
print("Step 7: 保存和測試模型開始...")
model.save("./trained_embedding_model")
print("模型已保存到 './trained_embedding_model'")

# 測試模型
test_sentences = ["I love programming", "Coding is amazing"]
embeddings = model.encode(test_sentences)
print("測試句子的嵌入向量：")
for i, emb in enumerate(embeddings):
    print(f"Sentence {i+1}: {test_sentences[i]}, Embedding: {emb[:5]}... (truncated)")
print("Step 7: 保存和測試模型完成！")