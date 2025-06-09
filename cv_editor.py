import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import subprocess
import os
import tempfile
import threading
import time
from tkinter.font import Font
import platform

# Base LaTeX template with instructional comments
LATEX_TEMPLATE = r"""\documentclass[11pt,a4paper,sans]{{moderncv}}
\moderncvstyle{{classic}}
\moderncvcolor{{blue}}
\usepackage[scale=0.75]{{geometry}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[brazil]{{babel}}
\usepackage{{fontspec}}
\setmainfont{{Arial}}

% ======================
% GENERAL INFORMATION
% ======================

% Fill your full name (First and Last names separated)
\name{{{name_first}}}{{{name_last}}}
% Your professional title (e.g., "Senior Software Engineer")
\title{{{title}}}
% Your current address (City, Country format recommended)
\address{{{address}}}
% Phone number with country code (format as you want it to appear)
\phone{{{phone}}}
% Professional email address
\email{{{email}}}
% Personal website or LinkedIn profile URL
\homepage{{{homepage}}}
% LinkedIn username (only the username part after linkedin.com/in/)
\social[linkedin]{{{linkedin}}}
% GitHub username
\social[github]{{{github}}}

\begin{{document}}
\makecvtitle
{content}
\end{{document}}
"""

class CVEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional CV Editor")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        # Custom styling
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TFrame', background='#2c3e50')
        self.style.configure('TNotebook', background='#2c3e50', borderwidth=0)
        self.style.configure('TNotebook.Tab', background='#34495e', 
                             foreground='white', padding=[10, 5])
        self.style.map('TNotebook.Tab', background=[('selected', '#3498db')])
        self.style.configure('TButton', background='#3498db', foreground='white', 
                            font=('Arial', 10, 'bold'))
        self.style.map('TButton', background=[('active', '#2980b9')])
        self.style.configure('TCheckbutton', background='#2c3e50', 
                            foreground='white', font=('Arial', 9))
        
        # Initialize data structure
        self.data = {
            "personal": {
                "name_first": "John",
                "name_last": "Doe",
                "title": "Electrical Engineering Student",
                "address": "City, Country",
                "phone": "(+55) 00~0000-0000",
                "email": "your.email@example.com",
                "homepage": "www.yourwebsite.com",
                "linkedin": "your-linkedin-username",
                "github": "your-github-username"
            },
            "sections": {
                "summary": "Write a 3-5 sentence professional summary highlighting:\n- Your professional identity\n- Key skills/expertise\n- Career objectives\n- Unique value proposition",
                "education": r"\cventry{2017--Present}{Degree Name}{University Name}{Location}{}{Additional details}",
                "research": r"\cventry{2025--Present}{Project Title}{Institution}{Location}{}{\begin{itemize}\item Describe your role and contributions\item Mention specific technologies/methods used\end{itemize}}",
                "experience": r"\cventry{2017--2022}{Job Title}{Company}{Location}{}{\begin{itemize}\item Describe your responsibilities\item Highlight key achievements\end{itemize}}",
                "projects": r"\cvitem{2023--Present}{\textbf{Project Name} Description of the project including purpose, technologies, and key features}",
                "skills": r"\cvitem{Languages}{List programming languages}\n\cvitem{Frameworks}{List relevant frameworks}\n\cvitem{Tools}{List development tools}",
                "awards": r"\cvitem{2024}{Award Name - Organization}",
                "publications": r"\cvitem{2024}{Authors. \"Publication Title\". Conference/Journal, Year.}",
                "languages": r"\cvitem{Portuguese}{Native}\n\cvitem{English}{Proficiency level}"
            }
        }
        
        # Section visibility (all enabled by default)
        self.section_visibility = {
            "summary": True,
            "education": True,
            "research": True,
            "experience": True,
            "projects": True,
            "skills": True,
            "awards": True,
            "publications": True,
            "languages": True
        }
        
        # Create header
        self.create_header()
        
        # Create notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Create tabs
        self.create_personal_tab()
        self.create_section_tabs()
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
        
        # Generate button
        btn_frame = ttk.Frame(root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Generate PDF", command=self.start_pdf_generation
                  ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Save Project", command=self.save_project
                  ).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Project", command=self.load_project
                  ).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(btn_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT, padx=10)
        
        # Tooltips
        self.tooltip = tk.Label(root, text="", bg="#ffffe0", relief=tk.SOLID, borderwidth=1,
                               font=("Arial", 9), padx=5, pady=2)
        self.tooltip.place_forget()
        
    def create_header(self):
        header = ttk.Frame(self.root, style='TFrame')
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header, text="Professional CV Editor", font=("Arial", 20, "bold"),
                        fg="white", bg="#2c3e50")
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(header, text="Create and customize your LaTeX CV", 
                           font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50")
        subtitle.pack(side=tk.LEFT, padx=10)
        
    def create_personal_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Personal Info")
        
        container = ttk.Frame(tab)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create two columns
        left_col = ttk.Frame(container)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_col = ttk.Frame(container)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        fields = [
            ("First Name", "name_first", "Your first name only"),
            ("Last Name", "name_last", "Your last name or surname"),
            ("Professional Title", "title", "e.g., 'Senior Software Engineer' or 'Electrical Engineering Student'"),
            ("Address", "address", "City, Country format recommended"),
            ("Phone", "phone", "Format as you want it to appear. Include country code"),
            ("Email", "email", "Professional email address"),
            ("Homepage", "homepage", "Personal website or LinkedIn profile URL"),
            ("LinkedIn", "linkedin", "Only the username part after linkedin.com/in/"),
            ("GitHub", "github", "Your GitHub username")
        ]
        
        for i, (label, key, tip) in enumerate(fields):
            col = left_col if i < 5 else right_col
            frame = ttk.Frame(col)
            frame.pack(fill=tk.X, padx=5, pady=8)
            
            lbl = ttk.Label(frame, text=label, width=15, anchor=tk.W)
            lbl.pack(side=tk.LEFT)
            
            # Add tooltip binding
            lbl.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            lbl.bind("<Leave>", self.hide_tooltip)
            
            entry = ttk.Entry(frame, width=30)
            entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
            entry.insert(0, self.data["personal"][key])
            entry.bind("<KeyRelease>", lambda e, k=key: self.update_personal(k, e.widget.get()))
            
            # Add tooltip to entry field
            entry.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            entry.bind("<Leave>", self.hide_tooltip)
    
    def update_personal(self, key, value):
        self.data["personal"][key] = value

    def create_section_tabs(self):
        sections = [
            ("Summary", "summary", "Write a 3-5 sentence professional summary"),
            ("Education", "education", "List your degrees and certifications"),
            ("Research Projects", "research", "Describe your research experience"),
            ("Experience", "experience", "Detail your professional work history"),
            ("Projects", "projects", "Showcase your open-source or personal projects"),
            ("Skills", "skills", "List your technical skills and proficiencies"),
            ("Awards", "awards", "Highlight your achievements and recognitions"),
            ("Publications", "publications", "List your academic publications"),
            ("Languages", "languages", "List languages you speak with proficiency")
        ]
        
        for name, key, tip in sections:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            
            # Header with checkbox
            header = ttk.Frame(tab)
            header.pack(fill=tk.X, padx=10, pady=10)
            
            lbl = ttk.Label(header, text=f"{name} Section", font=("Arial", 11, "bold"))
            lbl.pack(side=tk.LEFT)
            
            # Add tooltip to header
            lbl.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            lbl.bind("<Leave>", self.hide_tooltip)
            
            # Visibility toggle
            var = tk.BooleanVar(value=self.section_visibility[key])
            chk = ttk.Checkbutton(header, text="Include in PDF", variable=var,
                                  command=lambda k=key, v=var: self.toggle_section(k, v))
            chk.pack(side=tk.RIGHT, padx=10)
            
            # Text area with scrollbar
            text_frame = ttk.Frame(tab)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                font=("Consolas", 10), 
                                                bg="#f8f9fa", padx=10, pady=10)
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.insert("1.0", self.data["sections"][key])
            text_area.bind("<KeyRelease>", lambda e, k=key: self.update_section(k, e.widget.get("1.0", tk.END)))
            
            # Add tooltip to text area
            text_area.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            text_area.bind("<Leave>", self.hide_tooltip)
    
    def toggle_section(self, section, var):
        self.section_visibility[section] = var.get()
    
    def update_section(self, key, value):
        self.data["sections"][key] = value.strip()

    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 25
        
        self.tooltip.config(text=text)
        self.tooltip.place(x=x, y=y)
        
    def hide_tooltip(self, event=None):
        self.tooltip.place_forget()
    
    def start_pdf_generation(self):
        self.progress.start(10)
        self.status_var.set("Generating PDF...")
        self.root.update()
        
        # Run in a separate thread to prevent UI freeze
        threading.Thread(target=self.generate_pdf, daemon=True).start()
    
    def find_xelatex(self):
        if platform.system()!="Windows":
            return "xelatex"
        """Find XeLaTeX executable on Windows"""
        # Common MikTeX installation paths
        possible_paths = [
            r"C:\Program Files\MiKTeX\miktex\bin\x64\xelatex.exe",
            r"C:\Program Files (x86)\MiKTeX\miktex\bin\xelatex.exe",
            r"C:\Users\{}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\xelatex.exe".format(os.getenv("USERNAME")),
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        
        # Try PATH environment variable as last resort
        try:
            subprocess.run(["xelatex", "--version"], capture_output=True, check=True)
            return "xelatex"
        except:
            return None
    
    def generate_pdf(self):
        try:
            # Build the content string with only visible sections
            content = ""
            section_order = [
                ("summary", "Summary"),
                ("education", "Education"),
                ("research", "Research Projects"),
                ("experience", "Professional Experience"),
                ("projects", "Personal Open Source Projects"),
                ("skills", "Technical Skills"),
                ("awards", "Awards"),
                ("publications", "Publications"),
                ("languages", "Languages")
            ]
            
            for section_key, section_title in section_order:
                if self.section_visibility[section_key]:
                    content += f"\n% ======================\n% {section_title.upper()}\n% ======================\n"
                    content += f"\\section{{{section_title}}}\n"
                    content += self.data["sections"][section_key] + "\n"
            
            # Merge personal info into template
            merged = LATEX_TEMPLATE.format(
                content=content,
                **self.data["personal"]
            )
            
            # Create temporary directory
            with tempfile.TemporaryDirectory() as tmpdir:
                tex_path = os.path.join(tmpdir, "cv.tex")
                pdf_path = os.path.join(tmpdir, "cv.pdf")
                
                # Write LaTeX file
                with open(tex_path, "w", encoding="utf-8") as f:
                    f.write(merged)
                
                xelatex_path = self.find_xelatex()
                if not xelatex_path:
                    raise FileNotFoundError("XeLaTeX not found. Please ensure MikTeX is installed.")
                
                # Compile with XeLaTeX
                result = subprocess.run(
                    [xelatex_path, "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                    capture_output=True,
                    text=True
                )
                
                # Check if PDF was generated
                if os.path.exists(pdf_path):
                    # Open PDF
                    if os.name == 'nt':  # Windows
                        os.startfile(pdf_path)
                    elif os.name == 'posix':  # macOS, Linux
                        subprocess.run(["open", pdf_path] if os.uname().sysname == "Darwin" else ["xdg-open", pdf_path])
                    
                    self.status_var.set(f"PDF generated successfully")
                    messagebox.showinfo("Success", "PDF generated successfully!")
                else:
                    # Show error details
                    error_msg = "PDF generation failed.\n\nLaTeX Output:\n"
                    error_msg += result.stdout[:1000] + "\n\nErrors:\n" + result.stderr[:1000]
                    self.status_var.set("PDF generation failed")
                    messagebox.showerror("LaTeX Error", error_msg)
        
        except Exception as e:
            self.status_var.set("Error generating PDF")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        finally:
            self.progress.stop()
            self.root.after(100, self.progress.stop)
    
    def save_project(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".cvproj",
            filetypes=[("CV Project", "*.cvproj"), ("All Files", "*.*")]
        )
        if not file_path:
            return
        
        try:
            import json
            save_data = {
                "personal": self.data["personal"],
                "sections": self.data["sections"],
                "visibility": self.section_visibility
            }
            with open(file_path, "w") as f:
                json.dump(save_data, f, indent=2)
            self.status_var.set(f"Project saved: {os.path.basename(file_path)}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save project:\n{str(e)}")
    
    def load_project(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("CV Project", "*.cvproj"), ("All Files", "*.*")]
        )
        if not file_path or not os.path.exists(file_path):
            return
        
        try:
            import json
            with open(file_path, "r") as f:
                load_data = json.load(f)
            
            # Update personal info
            for key, value in load_data["personal"].items():
                if key in self.data["personal"]:
                    self.data["personal"][key] = value
            
            # Update sections
            for key, value in load_data["sections"].items():
                if key in self.data["sections"]:
                    self.data["sections"][key] = value
            
            # Update visibility
            for key, value in load_data["visibility"].items():
                if key in self.section_visibility:
                    self.section_visibility[key] = value
            
            self.status_var.set(f"Project loaded: {os.path.basename(file_path)}")
            messagebox.showinfo("Success", "Project loaded successfully!\nPlease navigate through tabs to see updated content.")
        except Exception as e:
            messagebox.showerror("Load Error", f"Failed to load project:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CVEditor(root)
    root.mainloop()