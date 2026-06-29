import ast
import os
import glob
from pathlib import Path

def get_imports(filepath):
    imports = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        tree = ast.parse(content, filename=filepath)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")
    return imports

def main():
    all_py_files = [f for f in glob.glob("*.py")]
    # Strip .py to get module names
    modules = {f[:-3]: f for f in all_py_files}
    
    # Files known to be entry points
    entry_points = [
        "extract_candidate_features.py",
        "rank_candidates_v3.py",
        "validate_ranking_system.py",
        "validate_submission.py"
    ]
    
    referenced = set(entry_points)
    to_visit = list(entry_points)
    
    while to_visit:
        curr = to_visit.pop()
        if not os.path.exists(curr):
            continue
        imps = get_imports(curr)
        for imp in imps:
            if imp in modules:
                fname = modules[imp]
                if fname not in referenced:
                    referenced.add(fname)
                    to_visit.append(fname)
                    
    print("=== Referenced Python Files ===")
    for f in sorted(referenced):
        print(f)
        
    print("\n=== Unreferenced Python Files ===")
    for f in sorted(all_py_files):
        if f not in referenced:
            print(f)

if __name__ == "__main__":
    main()
