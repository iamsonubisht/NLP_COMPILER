def generate_python_code(numbers, operation):
    """Generates Python code for the extracted operation."""
    if operation == "/" and numbers[1] == 0:
        return "print(\"Error: Division by zero!\")"
    
    return f"""
result = {numbers[0]} {operation} {numbers[1]}
print(f'Output: {{result}}')
"""
