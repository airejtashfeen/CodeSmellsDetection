import ast
import os
import radon.complexity as radon_complexity
from radon.visitors import ComplexityVisitor

# A counter for code smells
code_smell_count = 0

class CodeSmellDetector:
    def __init__(self, directory):
        self.directory = directory

    def scan_for_smells(self):
        global code_smell_count
        code_smell_count = 0
        smells = []

        # Walk through the directory and find any Python files
        for root, dirs, files in os.walk(self.directory):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    smells.extend(self.analyze_file(file_path))

        return smells

    def analyze_file(self, file_path):
        global code_smell_count
        smells = []

        try:
            # Open the file in read mode with UTF-8 encoding, ignoring errors
            with open(file_path, 'r', errors='ignore', encoding='utf-8') as file:
                content = file.read()
                tree = ast.parse(content)

                smells.extend(self.check_functions(tree, file_path))
                smells.extend(self.check_classes(tree, file_path))
                smells.extend(self.check_complexity(file_path))
                smells.extend(self.check_for_duplicates(content))
                smells.extend(self.check_for_magic_numbers(content))
                smells.extend(self.check_for_deep_inheritance(tree))
                smells.extend(self.check_excessive_comments(content, file_path))
                smells.extend(self.check_unnecessary_imports(content, file_path))
                smells.extend(self.check_long_lines(content, file_path))
                smells.extend(self.check_unreachable_code(tree, file_path))
                smells.extend(self.check_naming_conventions(tree, file_path))  # Added
                smells.extend(self.check_useless_exception_handling(tree, file_path))  # Added
                smells.extend(self.check_list_comprehension_complexity(tree, file_path))  # Added
                smells.extend(self.check_functional_decomposition(tree, file_path))  # Added
                smells.extend(self.check_spaghetti_code(tree, file_path))  # Added
                smells.extend(self.check_feature_envy(tree, file_path))  # Added
                smells.extend(self.check_god_class(tree, file_path))  # Added

        except Exception as e:
            smells.append(f"Error analyzing file {file_path}: {str(e)}")
            code_smell_count += 1

        return smells

    def check_functions(self, tree, file_path):
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Research paper metric: "Many Parameters" threshold = 5
                if len(node.args.args) > 5:
                    issues.append(f"Too many arguments: {node.name} in {file_path}")
                    code_smell_count += 1

                # Research paper metric: "Long Method" threshold = 100 lines
                if len(node.body) > 100:
                    issues.append(f"Long method: {node.name} in {file_path}")
                    code_smell_count += 1

                # Nested loops threshold = 3 (general threshold)
                nested_loops = sum(1 for n in node.body if isinstance(n, (ast.For, ast.While)))
                if nested_loops > 3:
                    issues.append(f"Too many nested loops: {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_classes(self, tree, file_path):
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                # Research paper metric: "Large Class" threshold = 200 lines or NOA+NOM > 40
                class_loc = sum(1 for n in node.body if isinstance(n, (ast.FunctionDef, ast.Assign)))
                num_attributes = sum(1 for n in node.body if isinstance(n, ast.Assign))
                num_methods = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                if class_loc > 200 or (num_attributes + num_methods) > 40:
                    issues.append(f"Large class: {node.name} in {file_path} (LOC: {class_loc}, NOA+NOM: {num_attributes + num_methods})")
                    code_smell_count += 1

                # Research paper metric: "Long Base Class List" threshold = 3
                if len(node.bases) > 3:
                    issues.append(f"Long base class list: {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_complexity(self, file_path):
        global code_smell_count
        issues = []

        try:
            with open(file_path, 'r', errors='ignore', encoding='utf-8') as file:
                content = file.read()
                # Research paper metric: "Cognitive Complexity" threshold = 8
                results = radon_complexity.cc_visit(content)
                for result in results:
                    if result.complexity > 8:
                        issues.append(f"High complexity: {result.name} in {file_path} with complexity {result.complexity}")
                        code_smell_count += 1

        except Exception as e:
            issues.append(f"Error analyzing complexity for {file_path}: {str(e)}")
            code_smell_count += 1

        return issues

# General metric
    def check_for_duplicates(self, content):
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
        global code_smell_count
        issues = []
        lines = content.split('\n')

        for line_num, line in enumerate(lines, start=1):
            if any(char.isdigit() for char in line):
                issues.append(f"Potential magic number detected at line {line_num}")
                code_smell_count += 1

        return issues

    def check_for_deep_inheritance(self, tree):
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and len(node.bases) > 3:
                issues.append(f"Deep inheritance chain in class {node.name}")
                code_smell_count += 1

        return issues

    def check_excessive_comments(self, content, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: Excessive comments threshold = 20
        comment_count = content.count("#")
        if comment_count > 20:
            issues.append(f"Excessive comments in {file_path} (more than 20 comments)")
            code_smell_count += 1

        return issues

# General metric
    def check_unnecessary_imports(self, content, file_path):
        global code_smell_count
        issues = []

        lines = content.split('\n')
        imported_modules = set()

        for line in lines:
            if line.startswith("import ") or line.startswith("from "):
                imported_modules.add(line.strip())

        if len(imported_modules) > 15:
            issues.append(f"Unnecessary number of imports in {file_path}")
            code_smell_count += 1

        return issues

    def check_long_lines(self, content, file_path):
        global code_smell_count
        issues = []

        lines = content.split('\n')
        for i, line in enumerate(lines, start=1):
            # Research paper metric: Long line threshold = 80 characters
            if len(line) > 80:
                issues.append(f"Long line detected in {file_path} at line {i}")
                code_smell_count += 1

        return issues

  # Did not need research paper for this one 
    def check_unreachable_code(self, tree, file_path):
        global code_smell_count
        issues = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                has_return = False
                for stmt in node.body:
                    if isinstance(stmt, ast.Return):
                        has_return = True
                    elif has_return:
                        issues.append(f"Unreachable code after return in function {node.name} in {file_path}")
                        code_smell_count += 1
                        break

        return issues

    def check_naming_conventions(self, tree, file_path):
        global code_smell_count
        issues = []

        # Check for PEP8 non-compliance in variable/function names
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not node.name.islower() or '_' not in node.name:
                    issues.append(f"Non-PEP8 compliant function name: {node.name} in {file_path}")
                    code_smell_count += 1
            elif isinstance(node, ast.Name):
                if not node.id.islower() or '_' not in node.id:
                    issues.append(f"Non-PEP8 compliant variable name: {node.id} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_useless_exception_handling(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: "Useless Exception Handling" NEC = 1 and NGEC = 1 or NEEC = NEEC
        for node in ast.walk(tree):
            if isinstance(node, ast.Try):
                except_count = len(node.handlers)
                general_except_count = sum(1 for handler in node.handlers if handler.type is None)
                if except_count == 1 and general_except_count == 1:
                    issues.append(f"Useless exception handling in {file_path}")
                    code_smell_count += 1

        return issues

    def check_list_comprehension_complexity(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: "Complex List Comprehension" NOL + NOCC >= 4
        for node in ast.walk(tree):
            if isinstance(node, ast.ListComp):
                num_loops = sum(1 for gen in node.generators if isinstance(gen, ast.comprehension))
                num_conditions = sum(1 for gen in node.generators if gen.ifs)
                if num_loops + num_conditions >= 4:
                    issues.append(f"Complex list comprehension in {file_path} at line {node.lineno}")
                    code_smell_count += 1

        return issues

    def check_functional_decomposition(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: Functional Decomposition LOCMETHOD >= 151
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                loc_method = len(node.body)
                if loc_method >= 151:
                    issues.append(f"Functional decomposition detected in method {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_spaghetti_code(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: Spaghetti Code NPRIVFIELD >= 7 and NMD = 16
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                private_fields = sum(1 for n in node.body if isinstance(n, ast.Assign) and any(t.id.startswith('_') for t in n.targets if isinstance(t, ast.Name)))
                num_methods = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))
                if private_fields >= 7 and num_methods == 16:
                    issues.append(f"Spaghetti code detected in class {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_feature_envy(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: Feature Envy FDP <= 5 and ATFD > 5 and LAA < 1/3
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                foreign_data_accesses = 0
                local_data_accesses = 0
                foreign_classes = set()

                for n in ast.walk(node):
                    if isinstance(n, ast.Attribute):
                        if isinstance(n.value, ast.Name) and n.value.id != 'self':
                            foreign_data_accesses += 1
                            foreign_classes.add(n.value.id)
                        elif isinstance(n.value, ast.Name) and n.value.id == 'self':
                            local_data_accesses += 1

                fdp = len(foreign_classes)
                atfd = foreign_data_accesses
                laa = local_data_accesses / (local_data_accesses + foreign_data_accesses) if (local_data_accesses + foreign_data_accesses) > 0 else 0

                if fdp <= 5 and atfd > 5 and laa < 1/3:
                    issues.append(f"Feature Envy detected in method {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def check_god_class(self, tree, file_path):
        global code_smell_count
        issues = []

        # Research paper metric: God Class WMC >= 47, ATFD > 5, TCC < 1/3
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                wmc = 0
                atfd = 0
                total_methods = 0
                connected_methods = 0

                methods = [n for n in node.body if isinstance(n, ast.FunctionDef)]
                total_methods = len(methods)
                shared_attributes = set()

                for method in methods:
                    method_complexity = len(method.body)
                    wmc += method_complexity

                    for n in ast.walk(method):
                        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id != 'self':
                            atfd += 1
                        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == 'self':
                            shared_attributes.add(n.attr)

                for method in methods:
                    for n in ast.walk(method):
                        if isinstance(n, ast.Attribute) and n.attr in shared_attributes:
                            connected_methods += 1
                            break

                tcc = connected_methods / total_methods if total_methods > 0 else 0

                if wmc >= 47 and atfd > 5 and tcc < 1/3:
                    issues.append(f"God Class detected: {node.name} in {file_path}")
                    code_smell_count += 1

        return issues

    def get_smells_count(self):
        return code_smell_count

# Main function representation
if __name__ == "__main__":
    directory = input("Enter the directory to scan for code smells: ")
    detector = CodeSmellDetector(directory)
    smells = detector.scan_for_smells()

    if smells:
        print("\nCode smells detected:")
        for smell in smells:
            print(smell)

    print(f"\nTotal code smells detected: {code_smell_count}")
