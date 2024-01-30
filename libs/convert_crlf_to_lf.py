import sys
import os

if __name__ == "__main__":
    args = sys.argv
    if len(args) < 2:
        raise RuntimeError("Required file path")
    file_path = args[1]
    if not os.path.exists(file_path):
        raise RuntimeError(f"{file_path} don't exists")
    with open(file_path, "rb") as f:
        content = f.read()
    content = content.replace(b'\r\n', b'\n')
    with open(file_path, "wb") as f:
        f.write(content)