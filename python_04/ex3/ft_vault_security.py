def secure_archive(file_name: str, mode: int | str = "r", content: str | None = None) -> tuple[bool, str]:
    if mode == 1 or mode == "r":
        try:
            with open(file_name, "r") as f:
                data = f.read()
                return (True, data)
        except (FileNotFoundError, PermissionError) as e:
            return (False, f"{e}")
    elif mode == 2 or mode == "w":
        try:
            with open(file_name, "w") as f:
                if content is not None:
                    f.write(content)
                return (True, "Content successfully written to file")
        except (FileNotFoundError, PermissionError) as e:
            return (False, f"{e}")
    else:
        return (False, "Invalid mode")


if __name__ == "__main__":
    print("=== Cyber Archives Security ===\n")

    print("Using 'secure_archive' to read from a nonexistent file:")
    print(secure_archive("/not/existing/file", "r"))
    print()
    print("Using 'secure_archive' to read from an inaccessible file:")
    print(secure_archive("/etc/master.passwd", "r"))
    print()
    print("Using 'secure_archive' to read from a regular file:")
    # 前のエクササイズで使った ancient_fragment.txt を読み込みます
    read_success, read_data = secure_archive("ancient_fragment.txt", "r")
    print((read_success, read_data))

    print("Using 'secure_archive' to write previous content to a new file:")
    # 読み込んだデータを新しいファイルに書き込みます
    print(secure_archive("new_file.txt", "w", read_data))