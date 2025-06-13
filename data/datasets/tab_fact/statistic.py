import json

# Đường dẫn tới file JSONL
file_path = "/Users/nhungnt/Documents/planta/data/datasets/tab_fact/small_test.jsonl"

# Tập hợp để lưu các giá trị 'name' phân biệt
unique_names = set()

# Đọc file JSONL và thu thập các giá trị 'name'
with open(file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line.strip())  # Parse dòng JSONL
        if "table" in data and "name" in data["table"]:
            unique_names.add(data["table"]["name"])

# In kết quả
print(f"Số lượng 'name' phân biệt: {len(unique_names)}")
