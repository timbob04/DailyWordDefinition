import ast
import os

def get_imports_recursive(file_path, visited=None):
    if visited is None:
        visited = set()
    if file_path in visited:
        return []
    visited.add(file_path)

    with open(file_path, "r") as file:
        tree = ast.parse(file.read())

    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            module = node.module
            for alias in node.names:  # Fix: Loop through `node.names` here
                imports.append(f"{module}.{alias.name}" if module else alias.name)
                # Check if module refers to a local file
                if module and os.path.exists(f"{module.replace('.', '/')}.py"):
                    imports += get_imports_recursive(f"{module.replace('.', '/')}.py", visited)

    return imports

if __name__ == "__main__":
    file_path = "wordDef.py"  # Replace with your file
    imports = get_imports_recursive(file_path)
    print("Specific Imports:")
    for imp in set(imports):  # Use `set` to avoid duplicates
        print(imp)
