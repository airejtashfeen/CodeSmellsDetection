import ast
import os
import radon.complexity as radon_complexity
from radon.visitors import ComplexityVisitor

# Global counter for code smells
code_smell_count = 0

class CodeSmellDetector:
    def __init__(self, directory):
        self.directory = directory

    def scan_for_smells(self):
        """Scan the directory for Python files and analyze them for code smells."""
        global code_smell_count
        code_smell_count = 0
        smells = []

        # Walk through the directory to find Python files
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    smells.extend(self.analyze_file(file_path))

        return smells

    def analyze_file(self, file_path):
        """Analyze a Python file for common code smells."""
        global code_smell_count
        smells = []

        try:
            with open(file_path, 'r', errors='ignore', encoding='utf-8') as file:
                content = file.read()
                tree = ast.parse(content)

                # Check for large functions, arguments, return statements, and loops
                smells.extend(self.check_functions(tree, file_path))

                # Check for large classes and too many methods
                smells.extend(self.check_classes(tree, file_path))

            # Check for cyclomatic complexity using Radon
            smells.extend(self.check_complexity(file_path))

            # Check for duplicated code blocks
            smells.extend(self.check_for_duplicates(content))

            # Check for magic numbers in the code
            smells.extend(self.check_for_magic_numbers(content))

            # Check for deep inheritance chains
            smells.extend(self.check_for_deep_inheritance(tree))

        except Exception as e:
            smells.append(f"Error analyzing file {file_path}: {str(e)}")
            code_smell_count += 1

        return smells

    def check_functions(self, tree, file_path):
        """Detect smells in functions like size, arguments, and structure."""
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check large functions
                if len(node.body) > 10:
                    issues.append(f"Large function: {node.name} in {file_path}")
                    code_smell_count += 1

                # Check too many arguments
                if len(node.args.args) > 5:
                    issues.append(f"Too many arguments: {node.name} in {file_path}")
                    code_smell_count += 1

                # Check too many return statements
                return_statements = sum(isinstance(n, ast.Return) for n in node.body)
                if return_statements > 2:
                    issues.append(f"Too many return statements: {node.name} in {file_path}")
                    code_smell_count += 1

                # Check deeply nested loops
                nested_loops = sum(1 for n in node.body if isinstance(n, (ast.For, ast.While)))
                if nested_loops > 3:
                    issues.append(f"Too many nested loops: {node.name} in {file_path}")
                    code_smell_count += 1

                # Check if-else chains
                if_else_count = sum(1 for n in node.body if isinstance(n, ast.If))
                if if_else_count > 5:
                    issues.append(f"Too many if-else blocks: {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_classes(self, tree, file_path):
        """Detect smells in class definitions like size and number of methods."""
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Check for large classes
                class_lines = len([n for n in node.body if isinstance(n, (ast.FunctionDef, ast.Assign))])
                if class_lines > 50:
                    issues.append(f"Large class: {node.name} in {file_path}")
                    code_smell_count += 1

                # Check too many methods in a class
                num_methods = len([n for n in node.body if isinstance(n, ast.FunctionDef)])
                if num_methods > 10:
                    issues.append(f"Too many methods in class: {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_complexity(self, file_path):
        """Check for high cyclomatic complexity using Radon."""
        global code_smell_count
        issues = []

        try:
            with open(file_path, 'r', errors='ignore', encoding='utf-8') as file:
                content = file.read()
                results = radon_complexity.cc_visit(content)
                for result in results:
                    if result.complexity > 10:
                        issues.append(f"High complexity: {result.name} in {file_path} with complexity {result.complexity}")
                        code_smell_count += 1
        except Exception as e:
            issues.append(f"Error analyzing complexity for {file_path}: {str(e)}")
            code_smell_count += 1

        return issues

    def check_for_duplicates(self, content):
        """Check for duplicated blocks of code."""
        global code_smell_count
        issues = []
        lines = content.split('\n')
        seen_blocks = set()

        for i in range(len(lines) - 5):
            block = tuple(lines[i:i+5])
            if block in seen_blocks:
                issues.append(f"Duplicated code detected: Block starting at line {i+1}")
                code_smell_count += 1
            else:
                seen_blocks.add(block)

        return issues

    def check_for_magic_numbers(self, content):
        """Check for magic numbers in the code."""
        global code_smell_count
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, start=1):
            if any(char.isdigit() for char in line):
                issues.append(f"Magic number detected at line {line_num}: {line.strip()}")
                code_smell_count += 1

        return issues

    def check_for_deep_inheritance(self, tree):
        """Check for deep inheritance chains."""
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and len(node.bases) > 3:
                issues.append(f"Deep inheritance chain in class {node.name}")
                code_smell_count += 1

        return issues
    
    def get_smells_count(self) :
        return code_smell_count


# Run the scan on a given directory
if __name__ == "__main__":
    directory = input("Enter the directory to scan for code smells: ")
    detector = CodeSmellDetector(directory)
    smells = detector.scan_for_smells()

    if smells:
        print("Code smells detected:")
        for smell in smells:
            print(smell)
    print(f"\nTotal code smells detected: {code_smell_count}")