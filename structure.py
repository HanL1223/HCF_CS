import os

structure = {
    'data': ['raw', 'processed'],
    'notebooks': [],
    'src': [],
    'models': [],
    'reports': ['figures'],
    'config': [],
}

print("Creating folder structure...")
for folder, subfolders in structure.items():
    os.makedirs(folder, exist_ok=True)
    print(f"Created: {folder}/")
    for subfolder in subfolders:
        path = os.path.join(folder, subfolder)
        os.makedirs(path, exist_ok=True)
        print(f"Created: {path}/")

print("Folder structure created successfully!")