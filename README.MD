# Code Smells Detection

Code Smells Detection is a project designed to identify and analyze code smells in software projects. Code smells are surface indicators of deeper problems in the codebase that may hinder maintainability, readability, or scalability.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)


## Features
- Detects common code smells such as Long Methods, Large Classes, Duplicated Code etc.
- Outputs detailed reports highlighting the affected code areas.
- Supports multiple programming languages.
- Easy-to-use GUI and CLI-based interface.

## Installation

### Prerequisites
- Python 3.8 or later
- Tkinter
- Git
- Virtual Environment (Optional but recommended)

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/abasit834/Code-Smells-Detection.git
   cd Code-Smells-Detection
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python3 -m venv myvenv
   source myvenv/bin/activate  # On Windows, use `myvenv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure the repository is set up and dependencies are installed.
2. Run the main script to analyze a project for code smells:

**GUI MODE**
   ```bash
   python frontend.py
   ```

**CLI MODE**
   ```bash
   python code_smells_detection.py
   /path/to/your/codebase
   ```
3. Review the generated report for identified code smells.

## Technologies Used
- **Python**: Core programming language for the project.
- **Tkinter**: For building the GUI.
- **Git**: Version control system.

## Contributing
We welcome contributions! To contribute:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Commit your changes and submit a pull request.

---

### Contact
For questions or feedback, please open an issue or contact the repository owner directly through GitHub.
