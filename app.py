import tkinter as tk
from controller import CVEditorController

if __name__ == "__main__":
    root = tk.Tk()
    app = CVEditorController(root)
    root.mainloop()