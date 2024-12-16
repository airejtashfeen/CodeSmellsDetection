from tkinter import *
from tkinter import filedialog
from code_smells_detection import CodeSmellDetector


class Frontend:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Python Code Smells Detection Software")
        self.file_path = None  # Initialize file_path to None

        # Title Label
        self.title = Label(
            self.root,
            text="Code Smells Detection",
            font=("Poppins", 45, "bold"),
            bg="#4C7766",
            fg="white",
        )
        self.title.place(x=0, y=0, width=1530, height=100)

        self.root.configure(bg="#EBE6E0")

        # Upload File Button
        self.upload_btn = Button(
            self.root,
            text="Upload File",
            width=15,
            height=2,
            fg="black",
            bd=0,
            command=self.upload_folder,
        )
        self.upload_btn.place(x=650, y=200)

        # Detect Smells Button
        self.detect_btn = Button(
            self.root,
            text="Detect Smells",
            width=15,
            height=2,
            fg="black",
            bd=0,
            command=self.detect_smells,
        )
        self.detect_btn.place(x=650, y=300)

        # Text Widget to Display Results
        self.result_text = Text(
            self.root,
            width=100,
            height=20,
            font=("Poppins", 12),
            bg="#F5F5F5",
            fg="black",
        )
        self.result_text.place(x=350, y=400)

    def upload_folder(self):
        """Open file dialog to select a folder."""
        folder_path = filedialog.askdirectory()  # Open a dialog to select a folder
        if folder_path:
            self.file_path = folder_path  # Save the selected folder path
            self.result_text.delete(1.0, END)
            self.result_text.insert(
            END, "Folder selected. Please press the detect smells button to proceed.\n"
            )
        else:
            self.result_text.delete(1.0, END)
            self.result_text.insert(
            END, "No folder selected. Please select a folder to proceed.\n"
            )
           

    def detect_smells(self):
        """Detect code smells in the uploaded file."""
        if self.file_path:
            # Initialize the CodeSmellDetector with the selected file
            detector = CodeSmellDetector(self.file_path)
            smells = detector.scan_for_smells()
            code_smell_count= detector.get_smells_count()
            

            # Display the results in the text widget
            self.result_text.delete(1.0, END)  # Clear previous results
            if smells :
                self.result_text.insert(END, "Code smells detected:\n")
                for smell in smells:
                    self.result_text.insert(END, f"- {smell}\n")
                # Display the total count of code smells
                self.result_text.insert(END, f"\nTotal code smells detected: {code_smell_count}\n")
            else:
                self.result_text.insert(END, "No code smells detected.\n")
        else:
            self.result_text.delete(1.0, END)
            self.result_text.insert(END, "Please upload a file first!\n")

if __name__ == "__main__":
    root = Tk()
    obj = Frontend(root)
    root.mainloop()