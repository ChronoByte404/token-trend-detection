def open_file(file_path):
    with open(file_path, "r") as f:
        file_data = f.read()
    return file_data
