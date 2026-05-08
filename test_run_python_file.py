from functions.run_python_file import run_python_file


def test():
    result = run_python_file("calculator", "main.py")
    print("Result from calculator, main:")
    print(result)
    print("")

    result = run_python_file("calculator", "main.py", ["3 + 5"])
    print("Result from calculator, main, 3 + 5:")
    print(result)
    print("")

    result = run_python_file("calculator", "tests.py")
    print("Result from calculator, tests:")
    print(result)
    print("")

    result = run_python_file("calculator", "../main.py")
    print("Result from calculator, ../main:")
    print(result)
    print("")

    result = run_python_file("calculator", "nonexistent.py")
    print("Result from calculator, nonexistent:")
    print(result)
    print("")

    result = run_python_file("calculator", "lorem.txt")
    print("Result from calculator, lorem.txt:")
    print(result)
    print("")


if __name__ == "__main__":
    test()

