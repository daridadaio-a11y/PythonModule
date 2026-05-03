import sys


def ft_archive_creation(file_name: str) -> None:
    new_file_list = []
    data = None
    print("=== Cyber Archives Recovery & Preservation ===")
    print(f"Accessing file '{file_name}'")
    try:
        data = open(file_name, "r")
        print("---\n")
        for line in data:
            print(line, end="")
            if len(line) > 0 and line[-1] == "\n":
                clean_line = line[:-1]
            else:
                clean_line = line
            new_file = (clean_line + "#")
            new_file_list.append(new_file + "\n")
        print("---")
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return
    finally:
        if data is not None:
            data.close()
            print(f"File '{file_name}' closed.\n")
    print("Transform data:")
    print("---\n")
    for new_line in new_file_list:
        print(new_line, end="")
    print("---")
    save_name = input("Enter new file name (or empty): ")
    if save_name:
        print(f"Saving data to '{save_name}'")
        out = None
        try:
            out = open(save_name, "w")
            for append_file in new_file_list:
                out.write(append_file)
            print(f"Data saved in file '{save_name}'.")
        except (FileNotFoundError, PermissionError) as e:
            print(f"Error: {e}")
            print("Data not saved.")
        finally:
            if out is not None:
                out.close()
    else:
        print("Not saving data.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        ft_archive_creation(sys.argv[1])
    else:
        print("Usage: python3 ft_archive_creation.py <filename>")
