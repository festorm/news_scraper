import json

annotated_hash = []
annotated_lines = []
with open("similarity_measure/cleaned.jsonl", "r") as fname:
    for line in fname.readlines():
        line = json.loads(line)
        hash_id = hash(line['text'])
        line['hash_id'] = hash_id
        annotated_hash.append(hash_id)
        annotated_lines.append(line)

with open("data/dr_spider.jsonl", "r") as fname:
    for line in fname.readlines():
        line = json.loads(line)
        hash_id = hash(line['text'])
        if hash_id in annotated_hash:
            idx = annotated_hash.index(hash_id)
            annotated_line = annotated_lines[idx]
            annotated_line.update(line)

with open("similarity_measure/extended_cleaned.jsonl", "w") as fname:
    for line in annotated_lines:
        fname.write(json.dumps(line))
        fname.write("\n")