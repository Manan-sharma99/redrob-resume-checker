import json

with open("candidates.jsonl", "r", encoding="utf-8") as f:
    first = json.loads(next(f))

print("\nCAREER DESCRIPTION SAMPLE:\n")

for job in first["career_history"]:
    print("=" * 80)
    print(job["title"])
    print(job["description"])