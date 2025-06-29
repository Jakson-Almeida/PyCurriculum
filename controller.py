import threading
import shutil
from model import CVModel
from view import CVEditorView

class CVEditorController:
    def __init__(self, root):
        self.root = root
        self.model = CVModel()
        self.view = CVEditorView(root, self)
        
        # Initialize view with model data
        self.load_data_to_view()
    
    def load_data_to_view(self):
        # Personal info
        for key, value in self.model.personal_info.items():
            self.view.set_personal_field(key, value)
        
        # Sections content
        for section, content in self.model.sections.items():
            self.view.set_section_content(section, content)
        
        # Section visibility
        for section, visible in self.model.section_visibility.items():
            self.view.set_section_visibility(section, visible)
    
    def update_personal(self, key, value):
        self.model.update_personal_info(key, value)
    
    def update_section(self, section, content):
        self.model.update_section(section, content)
    
    def toggle_section(self, section, visible):
        self.model.toggle_section(section, visible)
    
    def generate_pdf(self):
        self.view.start_progress()
        self.view.show_message("Generating PDF...")
        
        def generate_thread():
            latex_content = self.model.generate_latex()
            self.model.compile_latex(latex_content, self.handle_compilation_result)
        
        threading.Thread(target=generate_thread, daemon=True).start()
    
    def handle_compilation_result(self, success, pdf_path, message):
        self.view.stop_progress()
        self.view.show_message(message)
        
        if success:
            try:
                # Get user info for filename
                first_name = self.model.personal_info.get("name_first", "")
                last_name = self.model.personal_info.get("name_last", "")
                # Prompt user for save location with suggested filename
                save_path = self.view.ask_pdf_save_path(first_name, last_name)
                if save_path:
                    shutil.copyfile(pdf_path, save_path)
                    self.view.open_pdf(save_path)
                else:
                    self.view.show_message("PDF was generated but not saved.")
            except Exception as e:
                self.view.show_message(f"Error saving/opening PDF: {str(e)}", True)
        else:
            self.view.show_message(message, True)
    
    def save_project(self):
        file_path = self.view.ask_save_path()
        if file_path:
            success, message = self.model.save_project(file_path)
            self.view.show_message(message)
            if not success:
                self.view.show_message(message, True)
    
    def load_project(self):
        file_path = self.view.ask_open_path()
        if file_path:
            success, message = self.model.load_project(file_path)
            if success:
                self.load_data_to_view()
            self.view.show_message(message, not success)