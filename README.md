# Custom SQL-Like Query Parser and Evaluator

This project implements a **custom SQL-like query parser** using PLY (Python Lex-Yacc), enabling parsing and execution of simplified SQL queries on Pandas DataFrames. It also supports basic plotting commands like bar, line, and pie charts.

---

## Features

- Lexical analysis and parsing of SQL-like statements (`SELECT`, `INSERT`, `DELETE`).
- Supports `WHERE`, `GROUP BY`, `ORDER BY`, and `LIMIT` clauses.
- Basic aggregate functions (`AVG`).
- Custom metrics and simple function calls.
- Data manipulation on in-memory Pandas DataFrames.
- Support for plotting data with `PLOT BAR GRAPH`, `PLOT LINE GRAPH`, `PLOT PIE CHART`.
- Easy to extend with additional SQL-like features.

---

## Getting Started

### Prerequisites

- Python 3.7+
- Packages:
  - `ply`
  - `pandas`
  - `matplotlib`

You can install dependencies via:

```bash
pip install ply pandas matplotlib# NLP Compiler

## 📌 Project Description
This project is an **NLP-based Compiler** that converts natural language math expressions into executable Python code. It extracts numbers and operations from user input, generates valid Python code, and executes it dynamically.

## 🚀 Features
- Converts English math expressions into Python code
- Supports **addition, subtraction, multiplication, and division**
- Handles **errors like division by zero**
- Uses **spaCy** for NLP processing
- Modular structure for easy expansion

## 🛠 Installation
### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### 2️⃣ Run the Compiler
```bash
python main.py
```

## 📂 Project Directory Structure
```
📂 NLP_Compiler_Project
│── 📄 main.py              # Main script to integrate all components
│── 📄 parser.py            # Extracts numbers & operations from text
│── 📄 code_generator.py     # Generates Python code dynamically
│── 📄 compiler.py          # Compiles and executes Python code
│── 📄 temp.py              # Temporary file for execution
│── 📄 requirements.txt     # Dependencies
│── 📄 README.md            # Project documentation
```

## 🔥 Usage Examples
| User Input | Output |
|------------|--------|
| Add 5 and 3 | Output: 8 |
| Multiply 4 by 6 | Output: 24 |
| Divide 10 by 0 | Error: Division by zero! |

## 📜 How It Works
1️⃣ **NLP Processing (parser.py)**
   - Extracts numbers and operations from the input sentence.

2️⃣ **Code Generation (code_generator.py)**
   - Converts the extracted data into valid Python code.

3️⃣ **Compilation & Execution (compiler.py)**
   - Writes the generated code to a temporary file and executes it.

## 🎯 Future Enhancements
- ✅ Support for **modulus, exponentiation, and square roots**
- ✅ Implement **question-based queries** (e.g., "What is the sum of 4 and 6?")
- ✅ Build a **GUI or web-based interface**

## 👨‍💻 Contributors
- **Sonu Bisht** – NLP Processing
- **Sourav Singh** – Code Generation
- **Siddhi Kandpal** – Compilation & Execution
- **Pardeep Singh Bisht** – Integration & Testing

---
📢 **Feel free to expand or modify this project!** 🚀

