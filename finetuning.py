from openai import OpenAI

client = OpenAI()

# 1. 首先上傳文件
file_response = client.files.create(
    file=open("/Users/linzhihuan/Desktop/gpt/test_fintuning.jsonl", "rb"),
    purpose="fine-tune"
)

# 2. 獲取文件 ID
file_id = file_response.id

job = client.fine_tuning.jobs.create(
    training_file=file_id,
    model="gpt-4o-2024-08-06",
    method={
        "type": "supervised",
        "supervised": {
            "hyperparameters": {"n_epochs": 2},
        },
    },
)