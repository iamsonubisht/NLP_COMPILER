from parser import extract_info
from code_generator import generate_python_code
from compiler import compile_and_run

def main():
    user_input = input("Enter a math operation (e.g., 'Add 5 and 3'): ")
    print(f"[DEBUG] User Input: {user_input}")

    numbers, operation = extract_info(user_input)
    print(f"[DEBUG] Extracted Numbers: {numbers}, Operation: {operation}")

    if not numbers or not operation:
        print("Invalid input. Please try again with a valid operation like 'Add 4 and 5'.")
        return

    code = generate_python_code(numbers, operation)
    print(f"[DEBUG] Generated Code:\n{code}")

    result = compile_and_run(code)
    print(f"[DEBUG] Execution Result: {result}")

    print(result)

if __name__ == "__main__":
    main()
