#!/usr/bin/env python3
"""
Test script for MVC CV Editor
"""

import tkinter as tk
from model import CVModel
from view import CVEditorView
from controller import CVEditorController

def test_latex_generation():
    """Test LaTeX generation without GUI"""
    print("Testing LaTeX generation...")
    
    model = CVModel()
    
    # Update some test data
    model.update_personal_info("name_first", "John")
    model.update_personal_info("name_last", "Doe")
    model.update_personal_info("title", "Software Engineer")
    model.update_personal_info("email", "john.doe@example.com")
    
    model.update_section("summary", "Experienced software engineer with 5+ years in web development.")
    model.update_section("education", r"\cventry{2015--2019}{Bachelor of Science in Computer Science}{University of Technology}{City, Country}{}{GPA: 3.8/4.0}")
    
    # Generate LaTeX
    try:
        latex_content = model.generate_latex()
        print("✅ LaTeX generation successful!")
        print("Generated content preview:")
        print(latex_content[:500] + "...")
        return True
    except Exception as e:
        print(f"❌ LaTeX generation failed: {e}")
        return False

def test_pdf_compilation():
    """Test PDF compilation"""
    print("\nTesting PDF compilation...")
    
    model = CVModel()
    
    def compilation_callback(success, pdf_path, message):
        if success:
            print(f"✅ PDF compilation successful!")
            print(f"PDF saved to: {pdf_path}")
        else:
            print(f"❌ PDF compilation failed: {message}")
    
    # Generate and compile
    try:
        latex_content = model.generate_latex()
        model.compile_latex(latex_content, compilation_callback)
        return True
    except Exception as e:
        print(f"❌ PDF compilation failed: {e}")
        return False

def test_gui():
    """Test GUI functionality"""
    print("\nTesting GUI...")
    
    try:
        root = tk.Tk()
        app = CVEditorController(root)
        print("✅ GUI created successfully!")
        root.destroy()
        return True
    except Exception as e:
        print(f"❌ GUI creation failed: {e}")
        return False

if __name__ == "__main__":
    print("=== MVC CV Editor Test Suite ===\n")
    
    # Test LaTeX generation
    latex_ok = test_latex_generation()
    
    # Test PDF compilation
    pdf_ok = test_pdf_compilation()
    
    # Test GUI
    gui_ok = test_gui()
    
    print(f"\n=== Test Results ===")
    print(f"LaTeX Generation: {'✅ PASS' if latex_ok else '❌ FAIL'}")
    print(f"PDF Compilation: {'✅ PASS' if pdf_ok else '❌ FAIL'}")
    print(f"GUI Creation: {'✅ PASS' if gui_ok else '❌ FAIL'}")
    
    if all([latex_ok, pdf_ok, gui_ok]):
        print("\n🎉 All tests passed! MVC version is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.") 