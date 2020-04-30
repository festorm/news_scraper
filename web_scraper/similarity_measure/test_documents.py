import json 

data = []
with open("data/labled_data.json") as filename:
    for line in filename.readlines():
        data.append(json.loads(line))

print(data[0]['annotations'])
print(len(data))
cleaned_data = []

for jsonline in data:
    if len(jsonline["annotations"]) == 0:
        continue
    cleaned_data.append(jsonline)

print(len(cleaned_data))

with open("cleaned.jsonl", "w", encoding='utf8') as f:
    for line in cleaned_data:
        f.write(json.dumps(line,ensure_ascii=False))
        f.write("\n")

    