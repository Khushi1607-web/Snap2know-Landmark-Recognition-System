# check_dataset.py
import os

root = "dataset"
classes = sorted(os.listdir(root))
print("Total classes:", len(classes))
for c in classes:
    path = os.path.join(root, c)
    if os.path.isdir(path):
        count = len([f for f in os.listdir(path) if f.lower().endswith(('.jpg','.jpeg','.png'))])
        print(f"{c}: {count} images")