import os
import json
import tempfile
import subprocess
from pathlib import Path

# Default template path
TEMPLATE_PATH = Path(__file__).parent / "templates" / "cv_template.tex"

class CVModel:
    def __init__(self):
        self.personal_info = {
            "name_first": "John",
            "name_last": "Doe",
            "title": "Electrical Engineering Student",
            "address": "City, Country",
            "phone": "(+55) 00~0000-0000",
            "email": "your.email@example.com",
            "homepage": "www.yourwebsite.com",
            "linkedin": "your-linkedin-username",
            "github": "your-github-username"
        }
        
        self.sections = {
            "summary": "Write a 3-5 sentence professional summary...",
            "education": r"\cventry{2017--Present}{Degree Name}{University Name}{Location}{}{Additional details}",
            "research": r"\cventry{2025--Present}{Project Title}{Institution}{Location}{}{\begin{itemize}\item Describe your role...\end{itemize}}",
            "experience": r"\cventry{2017--2022}{Job Title}{Company}{Location}{}{\begin{itemize}\item Describe your responsibilities...\end{itemize}}",
            "projects": r"\cvitem{2023--Present}{\textbf{Project Name} Description...}",
            "skills": r"\cvitem{Languages}{List programming languages}\n\cvitem{Frameworks}{List relevant frameworks}",
            "awards": r"\cvitem{2024}{Award Name - Organization}",
            "publications": r"\cvitem{2024}{Authors. \"Publication Title\". Conference/Journal, Year.}",
            "languages": r"\cvitem{Portuguese}{Native}\n\cvitem{English}{Proficiency level}"
        }
        
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
    
    def update_personal_info(self, key, value):
        if key in self.personal_info:
            self.personal_info[key] = value
    
    def update_section(self, section, content):
        if section in self.sections:
            self.sections[section] = content.strip()
    
    def toggle_section(self, section, visible):
        if section in self.section_visibility:
            self.section_visibility[section] = visible
    
    def load_template(self):
        try:
            with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return self.get_fallback_template()
    
    def get_fallback_template(self):
        return r"""\documentclass[11pt,a4paper,sans]{{moderncv}}
\moderncvstyle{{classic}}
\moderncvcolor{{blue}}
\usepackage[scale=0.75]{{geometry}}
\usepackage[utf8]{{inputenc}}
\usepackage[T1]{{fontenc}}
\usepackage[brazil]{{babel}}
\usepackage{{fontspec}}
\setmainfont{{Arial}}

\name{{{name_first}}}{{{name_last}}}
\title{{{title}}}
\address{{{address}}}
\phone{{{phone}}}
\email{{{email}}}
\homepage{{{homepage}}}
\social[linkedin]{{{linkedin}}}
\social[github]{{{github}}}

\begin{{document}}
\makecvtitle
{content}
\end{{document}}
"""
    
    def generate_latex(self):
        template = self.load_template()
        
        # Build content from visible sections
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
                content += self.sections[section_key] + "\n"
        
        return template.format(content=content, **self.personal_info)
    
    def compile_latex(self, latex_content, callback):
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                tex_path = os.path.join(tmpdir, "cv.tex")
                pdf_path = os.path.join(tmpdir, "cv.pdf")
                
                # Write LaTeX file
                with open(tex_path, "w", encoding="utf-8") as f:
                    f.write(latex_content)
                
                # Compile with XeLaTeX
                result = subprocess.run(
                    ["xelatex", "-interaction=nonstopmode", "-output-directory", tmpdir, tex_path],
                    capture_output=True,
                    text=True
                )
                
                # Check result
                if os.path.exists(pdf_path):
                    callback(True, pdf_path, "PDF generated successfully")
                else:
                    error_msg = "PDF generation failed.\n\nLaTeX Output:\n"
                    error_msg += result.stdout[:1000] + "\n\nErrors:\n" + result.stderr[:1000]
                    callback(False, None, error_msg)
        except Exception as e:
            callback(False, None, f"Compilation error: {str(e)}")
    
    def save_project(self, file_path):
        try:
            data = {
                "personal": self.personal_info,
                "sections": self.sections,
                "visibility": self.section_visibility
            }
            with open(file_path, "w") as f:
                json.dump(data, f, indent=2)
            return True, f"Project saved: {os.path.basename(file_path)}"
        except Exception as e:
            return False, f"Save failed: {str(e)}"
    
    def load_project(self, file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
            
            # Update personal info
            for key, value in data.get("personal", {}).items():
                if key in self.personal_info:
                    self.personal_info[key] = value
            
            # Update sections
            for key, value in data.get("sections", {}).items():
                if key in self.sections:
                    self.sections[key] = value
            
            # Update visibility
            for key, value in data.get("visibility", {}).items():
                if key in self.section_visibility:
                    self.section_visibility[key] = value
            
            return True, "Project loaded successfully"
        except Exception as e:
            return False, f"Load failed: {str(e)}"