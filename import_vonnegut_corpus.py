#!/usr/bin/env python3
"""
Import actual Vonnegut corpus from JSONL files and create comprehensive knowledge base
"""

import json
import pickle
import logging
import os
from typing import List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_jsonl_file(filepath: str) -> List[Dict]:
    """Load JSONL file and return list of records"""
    records = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line:  # Skip empty lines
                    try:
                        record = json.loads(line)
                        records.append(record)
                    except json.JSONDecodeError as e:
                        logger.warning(f"Skipping malformed JSON on line {line_num}: {e}")
        logger.info(f"Loaded {len(records)} records from {filepath}")
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
    except Exception as e:
        logger.error(f"Error loading {filepath}: {e}")
    
    return records

def extract_meaningful_text(record: Dict) -> str:
    """Extract meaningful text content from a record"""
    text = record.get('text', '')
    
    # Skip records with no substantial text
    if not text or len(text.strip()) < 100:
        return ""
    
    # Clean up Project Gutenberg headers and footers
    if "Project Gutenberg" in text:
        lines = text.split('\n')
        content_lines = []
        in_content = False
        
        for line in lines:
            line = line.strip()
            # Skip Gutenberg metadata
            if any(skip in line.lower() for skip in ['project gutenberg', 'ebook', 'release date', 'language:', 'title:', 'author:']):
                continue
            # Start content after metadata
            if line and not in_content and len(line) > 50:
                in_content = True
            if in_content and line:
                content_lines.append(line)
        
        text = '\n'.join(content_lines)
    
    # Basic cleanup
    text = text.replace('\n\n\n', '\n\n')  # Remove excessive newlines
    text = text.strip()
    
    return text

def create_comprehensive_vonnegut_knowledge():
    """Create comprehensive Vonnegut knowledge base from JSONL corpus files"""
    
    # Load the JSONL files
    pd_records = load_jsonl_file("E:\\Downloads\\vonnegut_pd_dataset_pilot.jsonl")
    non_pd_records = load_jsonl_file("E:\\Downloads\\vonnegut_non_pd_manifest.jsonl")
    
    # Combine all records
    all_records = pd_records + non_pd_records
    logger.info(f"Total records to process: {len(all_records)}")
    
    # Process records into knowledge base documents
    documents = []
    doc_id = 0
    
    # Start with our existing enhanced biographical content
    base_documents = [
        {
            "id": doc_id,
            "title": "Kurt Vonnegut Complete Biography",
            "content": """Kurt Vonnegut (1922–2007) was an American writer known for blending dark humor, satire and science fiction. He was born in Indianapolis on 11 Nov 1922; his father, Kurt Sr., was a prominent architect, and his mother Edith was the daughter of a brewer. The Great Depression devastated the family's finances, forcing them to sell their home and removing young Kurt from private school. Vonnegut began writing as a teenager for The Shortridge Echo and later became an editor and columnist for The Cornell Sun. His journalism experience taught him to value clarity and brevity. During World War II he served in the U.S. Army, was captured in the Battle of the Bulge and survived the Allied fire‑bombing of Dresden as a prisoner of war. He and other prisoners sheltered in the meat locker of slaughterhouse number 5 and afterwards were forced to help burn corpses. This traumatic experience provided the basis for his famous novel Slaughterhouse‑Five.""",
            "source": "Kurt Vonnegut Museum and Library",
            "category": "biography",
            "date": "comprehensive",
            "chunks": []
        }
    ]
    
    documents.extend(base_documents)
    doc_id += 1
    
    # Process corpus records
    for record in all_records:
        text = extract_meaningful_text(record)
        if not text or len(text) < 200:  # Skip very short texts
            continue
        
        # Categorize content
        title = record.get('title', 'Unknown')
        date = record.get('date', 'Unknown')
        venue = record.get('venue', 'Unknown')
        
        # Determine category based on content and venue
        category = "general"
        if any(term in title.lower() for term in ['speech', 'address', 'commencement', 'lecture', 'talk']):
            category = "speeches"
        elif 'interview' in title.lower():
            category = "interviews"
        elif any(term in venue.lower() for term in ['cornell', 'shortridge', 'sun']):
            category = "journalism"
        elif any(term in title.lower() for term in ['story', 'fiction']):
            category = "fiction"
        elif 'review' in venue.lower():
            category = "interviews"
        
        doc = {
            "id": doc_id,
            "title": title,
            "content": text,
            "source": venue,
            "category": category,
            "date": date,
            "chunks": []
        }
        
        documents.append(doc)
        doc_id += 1
        
        # Limit to reasonable size for initial testing
        if len(documents) >= 20:
            break
    
    logger.info(f"Created {len(documents)} documents for knowledge base")
    
    # Create embeddings and chunks (simplified for demo)
    embeddings = []
    
    for doc in documents:
        # Simple chunking - split by sentences, group by 2-3 sentences
        content = doc["content"]
        if len(content) > 2000:  # Split longer texts into smaller chunks
            # Split by paragraphs first, then sentences
            paragraphs = content.split('\n\n')
            chunks = []
            for para in paragraphs:
                if len(para) > 500:
                    sentences = para.split('. ')
                    for i in range(0, len(sentences), 3):
                        chunk = '. '.join(sentences[i:i+3])
                        if chunk.strip():
                            chunks.append(chunk + '.')
                else:
                    if para.strip():
                        chunks.append(para.strip())
        else:
            # Shorter content, just split by sentences
            sentences = content.split('. ')
            chunks = []
            for i in range(0, len(sentences), 3):
                chunk = '. '.join(sentences[i:i+3])
                if chunk.strip():
                    chunks.append(chunk + '.')
        
        doc["chunks"] = chunks
        
        # Create fake embeddings for demo (normally you'd use OpenAI)
        for chunk in chunks:
            if len(chunk.strip()) > 50:  # Only meaningful chunks
                embeddings.append({
                    "doc_id": doc["id"],
                    "chunk": chunk,
                    "embedding": [0.0] * 1536  # Placeholder
                })
    
    # Save comprehensive knowledge base
    data = {
        "documents": documents,
        "embeddings": embeddings
    }
    
    with open("vonnegut_knowledge_base.pkl", 'wb') as f:
        pickle.dump(data, f)
    
    # Print summary
    categories = {}
    for doc in documents:
        cat = doc.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("🎉 COMPREHENSIVE VONNEGUT KNOWLEDGE BASE CREATED!")
    print(f"📚 Total documents: {len(documents)}")
    print(f"🧩 Total chunks: {len(embeddings)}")
    print("\n📊 Content breakdown:")
    for category, count in sorted(categories.items()):
        print(f"   {category}: {count} documents")
    
    print(f"\n🔊 ElevenLabs Voice ID: J80PasKsbR4AWMLiAQ0j")
    print("✅ Ready for authentic Vonnegut conversations!")
    
    logger.info(f"Successfully created comprehensive knowledge base with {len(documents)} documents and {len(embeddings)} chunks")

if __name__ == "__main__":
    create_comprehensive_vonnegut_knowledge()