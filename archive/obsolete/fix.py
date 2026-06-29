with open('run_audits.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('open("REGEX_SHADOWING_REPORT.md", "w")', 'open("REGEX_SHADOWING_REPORT.md", "w", encoding="utf-8")')
c = c.replace('open("FAMILY_DIVERSITY_AUDIT.md", "w")', 'open("FAMILY_DIVERSITY_AUDIT.md", "w", encoding="utf-8")')
c = c.replace('open("CONCEPT_REGISTRY_SCHEMA.md", "w")', 'open("CONCEPT_REGISTRY_SCHEMA.md", "w", encoding="utf-8")')
c = c.replace('open("CONCEPT_REGISTRY_UPDATE.md", "w")', 'open("CONCEPT_REGISTRY_UPDATE.md", "w", encoding="utf-8")')
c = c.replace("open('candidates.jsonl', 'r')", "open('candidates.jsonl', 'r', encoding='utf-8')")

with open('run_audits.py', 'w', encoding='utf-8') as f:
    f.write(c)
