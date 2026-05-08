from functions.get_files_content import get_file_content


def test():
    result = get_file_content("calculator", "lorem.txt")
    print("Result from Lorem.txt:")
    print(result)
    print("")

    result = get_file_content("calculator", "main.py")
    print("Result from main.py:")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/calculator.py")
    print("Result from pkg/calculator.py:")
    print(result)
    print("")

    result = get_file_content("calculator", "/bin/cat")
    print("Result from /bin/cat.py:")
    print(result)
    print("")

    result = get_file_content("calculator", "pkg/does_not_exist.py")
    print("Result from /pkg/does_not_exist.py:")
    print(result)
    print("")


if __name__ == "__main__":
    test()
