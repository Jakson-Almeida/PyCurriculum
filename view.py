import os
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog

class CVEditorView:
    def __init__(self, root, controller):
        self.root = root
        self.root.title("Professional CV Editor")
        self.root.geometry("1000x700")
        self.root.configure(bg="#2c3e50")
        
        self.controller = controller
        
        # Create custom styling
        self.setup_styles()
        
        # Create UI components
        self.create_header()
        self.create_notebook()
        self.create_status_bar()
        self.create_buttons()
        
        # Tooltip system
        self.tooltip = tk.Label(root, text="", bg="#ffffe0", relief=tk.SOLID, 
                               borderwidth=1, font=("Arial", 9), padx=5, pady=2)
        self.tooltip.place_forget()
    
    def setup_styles(self):
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
    
    def create_header(self):
        header = ttk.Frame(self.root, style='TFrame')
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header, text="Professional CV Editor", font=("Arial", 20, "bold"),
                        fg="white", bg="#2c3e50")
        title.pack(side=tk.LEFT)
        
        subtitle = tk.Label(header, text="Create and customize your LaTeX CV", 
                           font=("Arial", 11), fg="#bdc3c7", bg="#2c3e50")
        subtitle.pack(side=tk.LEFT, padx=10)
    
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        self.create_personal_tab()
        self.create_section_tabs()
    
    def create_personal_tab(self):
        self.personal_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.personal_tab, text="Personal Info")
        
        container = ttk.Frame(self.personal_tab)
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create two columns
        left_col = ttk.Frame(container)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        right_col = ttk.Frame(container)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)
        
        # Personal info fields
        self.personal_fields = {}
        fields = [
            ("First Name", "name_first", "Your first name only"),
            ("Last Name", "name_last", "Your last name or surname"),
            ("Professional Title", "title", "e.g., 'Senior Software Engineer'"),
            ("Address", "address", "City, Country format recommended"),
            ("Phone", "phone", "Format as you want it to appear"),
            ("Email", "email", "Professional email address"),
            ("Homepage", "homepage", "Personal website or LinkedIn URL"),
            ("LinkedIn", "linkedin", "Username part after linkedin.com/in/"),
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
            entry.bind("<KeyRelease>", lambda e, k=key: self.controller.update_personal(k, e.widget.get()))
            
            # Add tooltip to entry field
            entry.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            entry.bind("<Leave>", self.hide_tooltip)
            
            self.personal_fields[key] = entry
    
    def create_section_tabs(self):
        self.section_tabs = {}
        self.section_editors = {}
        self.section_visibility = {}
        
        sections = [
            ("Summary", "summary", "Write a 3-5 sentence professional summary"),
            ("Education", "education", "List your degrees and certifications"),
            ("Research", "research", "Describe your research experience"),
            ("Experience", "experience", "Detail your professional work history"),
            ("Projects", "projects", "Showcase your open-source projects"),
            ("Skills", "skills", "List your technical skills"),
            ("Awards", "awards", "Highlight your achievements"),
            ("Publications", "publications", "List your academic publications"),
            ("Languages", "languages", "List languages you speak")
        ]
        
        for name, key, tip in sections:
            tab = ttk.Frame(self.notebook)
            self.notebook.add(tab, text=name)
            self.section_tabs[key] = tab
            
            # Header with checkbox
            header = ttk.Frame(tab)
            header.pack(fill=tk.X, padx=10, pady=10)
            
            lbl = ttk.Label(header, text=f"{name} Section", font=("Arial", 11, "bold"))
            lbl.pack(side=tk.LEFT)
            
            # Add tooltip to header
            lbl.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            lbl.bind("<Leave>", self.hide_tooltip)
            
            # Visibility toggle
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(header, text="Include in PDF", variable=var,
                                  command=lambda k=key, v=var: self.controller.toggle_section(k, v.get()))
            chk.pack(side=tk.RIGHT, padx=10)
            self.section_visibility[key] = (var, chk)
            
            # Text area with scrollbar
            text_frame = ttk.Frame(tab)
            text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
            
            text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                font=("Consolas", 10), 
                                                bg="#f8f9fa", padx=10, pady=10)
            text_area.pack(fill=tk.BOTH, expand=True)
            text_area.bind("<KeyRelease>", lambda e, k=key: self.controller.update_section(k, e.widget.get("1.0", tk.END)))
            
            # Add tooltip to text area
            text_area.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
            text_area.bind("<Leave>", self.hide_tooltip)
            
            self.section_editors[key] = text_area
    
    def create_status_bar(self):
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                              relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X, padx=0, pady=0)
    
    def create_buttons(self):
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, text="Generate PDF", command=self.controller.generate_pdf
                  ).pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Save Project", command=self.controller.save_project
                  ).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Load Project", command=self.controller.load_project
                  ).pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(btn_frame, mode='indeterminate', length=200)
        self.progress.pack(side=tk.RIGHT, padx=10)
    
    def show_tooltip(self, event, text):
        x, y, _, _ = event.widget.bbox("insert")
        x += event.widget.winfo_rootx() + 25
        y += event.widget.winfo_rooty() + 25
        
        self.tooltip.config(text=text)
        self.tooltip.place(x=x, y=y)
        
    def hide_tooltip(self, event=None):
        self.tooltip.place_forget()
    
    def set_personal_field(self, key, value):
        if key in self.personal_fields:
            self.personal_fields[key].delete(0, tk.END)
            self.personal_fields[key].insert(0, value)
    
    def set_section_content(self, section, content):
        if section in self.section_editors:
            self.section_editors[section].delete("1.0", tk.END)
            self.section_editors[section].insert("1.0", content)
    
    def set_section_visibility(self, section, visible):
        if section in self.section_visibility:
            var, _ = self.section_visibility[section]
            var.set(visible)
    
    def show_message(self, message, is_error=False):
        self.status_var.set(message)
        if is_error:
            tk.messagebox.showerror("Error", message)
    
    def start_progress(self):
        self.progress.start(10)
    
    def stop_progress(self):
        self.progress.stop()
    
    def ask_save_path(self):
        return filedialog.asksaveasfilename(
            defaultextension=".cvproj",
            filetypes=[("CV Project", "*.cvproj"), ("All Files", "*.*")]
        )
    
    def ask_open_path(self):
        return filedialog.askopenfilename(
            filetypes=[("CV Project", "*.cvproj"), ("All Files", "*.*")]
        )
    
    def open_pdf(self, path):
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            os.subprocess.run(["open", path] if os.uname().sysname == "Darwin" else ["xdg-open", path])