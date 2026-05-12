import fitz  # PyMuPDF
import re

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    import os
    filename = os.path.basename(pdf_path).lower()
    clean_name = filename.replace('_', ' ').replace('-', ' ').replace('.pdf', '')
    text += f"\n[FILENAME_CONTEXT: {clean_name}]"
    return text

def segment_into_chapters(text):
    # For a unified UX, we force exactly 5 chapters extracted from the PDF text.
    words = text.split()
    total_words = len(words)
    
    chapter_titles = ["Introduction", "Basics", "Core Concepts", "Advanced", "Expert"]
    chapters = []
    
    if total_words < 50:
        # Failsafe for empty or purely image-based PDFs
        for title in chapter_titles:
            chapters.append({
                "title": title,
                "content": "Content temporarily unavailable: Could not extract standard text from this document. Please ensure the PDF uses selectable text rather than images."
            })
        return chapters

    # Split evenly into 5 progressive chapters
    chunk_size = max(1, total_words // 5)
    
    for i, title in enumerate(chapter_titles):
        start = i * chunk_size
        # The last chapter absorbs the remainder
        end = (i + 1) * chunk_size if i < 4 else total_words
        
        chunk_words = words[start:end]
        
        # Break chunk into natural-looking paragraphs (roughly every 50-70 words) for beautiful reading
        paragraphs = []
        for j in range(0, len(chunk_words), 60):
            paragraph_text = " ".join(chunk_words[j:j+60])
            # Ensure it ends with a period if possible, but keep it simple for now
            if not paragraph_text.endswith('.'):
                paragraph_text += "."
            paragraphs.append(paragraph_text)
            
        formatted_content = "\n\n".join(paragraphs)
        
        chapters.append({
            "title": title,
            "content": formatted_content
        })
        
    return chapters
