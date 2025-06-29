import os
import json
import tempfile
import subprocess
from pathlib import Path
from jinja2 import Template

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
            "education": [
                {
                    "degree": "Degree Name",
                    "institution": "University Name",
                    "start": "2017",
                    "end": "Present",
                    "details": "Additional details"
                }
            ],
            "experience": [
                {
                    "job_title": "Job Title",
                    "company": "Company",
                    "start": "2017",
                    "end": "2022",
                    "details": "Describe your responsibilities..."
                }
            ],
            "research": [
                {
                    "project_title": "Project Title",
                    "institution": "Institution",
                    "start": "2025",
                    "end": "Present",
                    "details": "Describe your role and contributions"
                }
            ],
            "projects": [
                {
                    "project_name": "Project Name",
                    "years": "2023--Present",
                    "description": "Description of the project including purpose, technologies, and key features"
                }
            ],
            "skills": [
                {"category": "Languages", "items": "Python, C++, Java"},
                {"category": "Frameworks", "items": "Django, React"},
                {"category": "Tools", "items": "Git, Docker"}
            ],
            "awards": [
                {"year": "2024", "award_name": "Award Name", "organization": "Organization"}
            ],
            "publications": [
                {"year": "2024", "title": "Publication Title", "authors": "Authors", "venue": "Conference/Journal"}
            ],
            "languages": [
                {"language": "Portuguese", "proficiency": "Native"},
                {"language": "English", "proficiency": "Proficiency level"}
            ]
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
\end{{document}}"""
    
    def generate_latex(self):
        """
        Generate LaTeX content from template and user data
        Returns formatted LaTeX document as string
        """
        # Load the raw template (with escaped braces)
        template = self.load_template()
        
        # Build content from visible sections
        content = self.build_content_sections()
        
        # Format with named parameters for safety
        try:
            return template.format(content=content, **self.personal_info)
        except KeyError as e:
            raise ValueError(f"Missing required personal info field: {e}") from e

    def build_content_sections(self):
        """Construct the LaTeX content for all visible sections"""
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
            if self.section_visibility.get(section_key, True):
                content += self.build_section(section_key, section_title)
        
        return content

    def build_section(self, section_key, section_title):
        """Build individual section with header and content"""
        if section_key == "education":
            entries = self.sections["education"]
            latex = ""
            for edu in entries:
                latex += (
                    rf"\cventry{{{edu['start']}--{edu['end']}}}"
                    rf"{{{edu['degree']}}}"
                    rf"{{{edu['institution']}}}"
                    rf"{{}}"  # Location (optional, left blank)
                    rf"{{}}"  # Empty field
                    rf"{{{edu['details']}}}\n"
                )
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "experience":
            entries = self.sections["experience"]
            latex = ""
            for exp in entries:
                latex += (
                    rf"\cventry{{{exp['start']}--{exp['end']}}}"
                    rf"{{{exp['job_title']}}}"
                    rf"{{{exp['company']}}}"
                    rf"{{}}"  # Location (optional, left blank)
                    rf"{{}}"  # Empty field
                    rf"{{{exp['details']}}}\n"
                )
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "research":
            entries = self.sections["research"]
            latex = ""
            for res in entries:
                latex += (
                    rf"\cventry{{{res['start']}--{res['end']}}}"
                    rf"{{{res['project_title']}}}"
                    rf"{{{res['institution']}}}"
                    rf"{{}}"  # Location (optional, left blank)
                    rf"{{}}"  # Empty field
                    rf"{{{res['details']}}}\n"
                )
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "projects":
            entries = self.sections["projects"]
            latex = ""
            for proj in entries:
                latex += (
                    rf"\cvitem{{{proj['years']}}}{{\textbf{{{proj['project_name']}}} {proj['description']}}}\n"
                )
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "skills":
            entries = self.sections["skills"]
            latex = ""
            for skill in entries:
                latex += rf"\cvitem{{{skill['category']}}}{{{skill['items']}}}\n"
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "awards":
            entries = self.sections["awards"]
            latex = ""
            for award in entries:
                latex += rf"\cvitem{{{award['year']}}}{{{award['award_name']} - {award['organization']}}}\n"
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "publications":
            entries = self.sections["publications"]
            latex = ""
            for pub in entries:
                latex += rf"\cvitem{{{pub['year']}}}{{{pub['authors']}. \"{pub['title']}\". {pub['venue']}, {pub['year']}.}}\n"
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        elif section_key == "languages":
            entries = self.sections["languages"]
            latex = ""
            for lang in entries:
                latex += rf"\cvitem{{{lang['language']}}}{{{lang['proficiency']}}}\n"
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{latex}
"""
        else:
            return rf"""
% ======================
% {section_title.upper()}
% ======================
\section{{{section_title}}}
{self.sections[section_key]}
"""

    def compile_latex(self, latex_content, callback):
        """Compile LaTeX content to PDF and call callback with result"""
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
        """Save project data to JSON file"""
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
        """Load project data from JSON file"""
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