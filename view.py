import os
import subprocess
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
            ("Experience", "experience", "Detail your professional work history"),
            ("Research", "research", "Describe your research experience"),
            ("Projects", "projects", "Showcase your open-source projects"),
            ("Skills", "skills", "List your technical skills"),
            ("Awards", "awards", "Highlight your achievements"),
            ("Publications", "publications", "List your academic publications"),
            ("Languages", "languages", "List languages you speak")
        ]
        multi_entry_sections = {
            "education": [
                ("Degree", "degree"),
                ("Institution", "institution"),
                ("Start Year", "start"),
                ("End Year", "end"),
                ("Details", "details")
            ],
            "experience": [
                ("Job Title", "job_title"),
                ("Company", "company"),
                ("Start Year", "start"),
                ("End Year", "end"),
                ("Details", "details")
            ],
            "research": [
                ("Project Title", "project_title"),
                ("Institution", "institution"),
                ("Start Year", "start"),
                ("End Year", "end"),
                ("Details", "details")
            ],
            "projects": [
                ("Project Name", "project_name"),
                ("Years", "years"),
                ("Description", "description")
            ],
            "skills": [
                ("Category", "category"),
                ("Items", "items")
            ],
            "awards": [
                ("Year", "year"),
                ("Award Name", "award_name"),
                ("Organization", "organization")
            ],
            "publications": [
                ("Year", "year"),
                ("Title", "title"),
                ("Authors", "authors"),
                ("Venue", "venue")
            ],
            "languages": [
                ("Language", "language"),
                ("Proficiency", "proficiency")
            ]
        }
        
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
            
            if key in multi_entry_sections:
                # Pretty UI for multi-entry sections
                frame = ttk.Frame(tab)
                frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
                setattr(self, f"{key}_list_frame", frame)
                self._make_refresh_list(key, multi_entry_sections[key])()
                btn_frame = ttk.Frame(tab)
                btn_frame.pack(fill=tk.X, padx=10, pady=5)
                ttk.Button(btn_frame, text=f"Add {name}", command=lambda k=key: self._entry_dialog(k, multi_entry_sections[k])).pack(side=tk.LEFT)
            else:
                # Text area with scrollbar for summary
                text_frame = ttk.Frame(tab)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
                text_area = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                    font=("Consolas", 10), 
                                                    bg="#f8f9fa", padx=10, pady=10)
                text_area.pack(fill=tk.BOTH, expand=True)
                text_area.bind("<KeyRelease>", lambda e, k=key: self.controller.update_section(k, e.widget.get("1.0", tk.END)))
                text_area.bind("<Enter>", lambda e, t=tip: self.show_tooltip(e, t))
                text_area.bind("<Leave>", self.hide_tooltip)
                self.section_editors[key] = text_area

    def _make_refresh_list(self, key, fields):
        def refresh():
            frame = getattr(self, f"{key}_list_frame")
            for widget in frame.winfo_children():
                widget.destroy()
            # Table header
            header = ttk.Frame(frame)
            header.pack(fill=tk.X)
            for i, (col, _) in enumerate(fields + [("Actions", None)]):
                ttk.Label(header, text=col, font=("Arial", 10, "bold")).grid(row=0, column=i, padx=5, pady=2)
            # List entries
            for idx, entry in enumerate(self.controller.model.sections[key]):
                row = ttk.Frame(frame)
                row.pack(fill=tk.X, pady=2)
                for i, (_, field) in enumerate(fields):
                    ttk.Label(row, text=entry.get(field, "")).grid(row=0, column=i, padx=5)
                ttk.Button(row, text="Edit", command=lambda i=idx, k=key, f=fields: self._entry_dialog(k, f, i)).grid(row=0, column=len(fields), padx=2)
                ttk.Button(row, text="Delete", command=lambda i=idx, k=key: self._delete_entry(k, i)).grid(row=0, column=len(fields)+1, padx=2)
        return refresh

    def _entry_dialog(self, key, fields, idx=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(f"{key.capitalize()} Entry")
        dialog.geometry("400x400")
        dialog.grab_set()
        entries = {}
        entry_data = self.controller.model.sections[key][idx] if idx is not None else None
        for i, (label, field) in enumerate(fields):
            ttk.Label(dialog, text=label).pack(anchor=tk.W, padx=10, pady=(10 if i==0 else 2, 2))
            entry = ttk.Entry(dialog, width=40)
            entry.pack(padx=10, pady=2)
            if entry_data:
                entry.insert(0, entry_data.get(field, ""))
            entries[field] = entry
        def save():
            new_entry = {k: e.get() for k, e in entries.items()}
            if idx is not None:
                self.controller.model.sections[key][idx] = new_entry
            else:
                self.controller.model.sections[key].append(new_entry)
            dialog.destroy()
            getattr(self, f"refresh_{key}_list")()
        ttk.Button(dialog, text="Save", command=save).pack(pady=10)
        ttk.Button(dialog, text="Cancel", command=dialog.destroy).pack()

    def _delete_entry(self, key, idx):
        del self.controller.model.sections[key][idx]
        getattr(self, f"refresh_{key}_list")()

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
    
    def ask_pdf_save_path(self, first_name=None, last_name=None):
        if first_name and last_name:
            initialfile = f"{last_name}_{first_name}_Resume.pdf"
        else:
            initialfile = "Resume.pdf"
        return filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF Document", "*.pdf"), ("All Files", "*.*")],
            initialfile=initialfile
        )
    
    def open_pdf(self, path):
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.run(["open", path] if os.uname().sysname == "Darwin" else ["xdg-open", path])