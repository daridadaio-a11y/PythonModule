import sys


def ft_ancient_text(file_name: str) -> None:
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")
    data = None
    try:
        data = open(file_name, "r")
        for line in data:
            print(line, end="")
        print("\n---")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening file '{file_name}': {e}")
        return
    finally:
        if data is not None:
            data.close()
            print(f"File '{file_name}' closed.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ft_ancient_text(sys.argv[1])
    else:
        print("Usage: python3 ft_ancient_text.py <file>\n")