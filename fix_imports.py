"""
Script to fix import statements in the src package.
Run this once to convert absolute imports to relative imports.
"""

import os
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix imports in a single file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix imports - convert absolute to relative
    replacements = {
        'from embeddings import': 'from .embeddings import',
        'from retriever import': 'from .retriever import',
        'from llm import': 'from .llm import',
        'from ingestion import': 'from .ingestion import',
        'from chatbot import': 'from .chatbot import',
    }
    
    for old, new in replacements.items():
        content = content.replace(old, new)
    
    # Only write if changes were made
    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✓ Fixed: {file_path.name}")
        return True
    return False

def main():
    """Fix all Python files in src directory."""
    src_dir = Path('src')
    
    if not src_dir.exists():
        print("❌ Error: 'src' directory not found!")
        print("Make sure you run this script from the project root directory.")
        return
    
    print("Fixing import statements in src package...")
    print("=" * 50)
    
    files_fixed = 0
    
    # Fix all Python files in src
    for py_file in src_dir.glob('*.py'):
        if py_file.name != '__init__.py':
            if fix_imports_in_file(py_file):
                files_fixed += 1
    
    print("=" * 50)
    print(f"\n✓ Done! Fixed {files_fixed} file(s)")
    print("\nNow try running: streamlit run app/streamlit_app.py")

if __name__ == "__main__":
    main()