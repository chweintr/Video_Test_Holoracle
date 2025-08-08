#!/usr/bin/env python3
"""
Create Vonnegut-specific knowledge base
This will be a sample - ideally you'd import from your vonnegut-ai-oracle repo
"""

import pickle
import logging
from personas.persona_rag_system import PersonaRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_vonnegut_knowledge():
    """Create a sample Vonnegut knowledge base"""
    
    # This is sample content - you should replace with actual Vonnegut corpus
    vonnegut_documents = [
        {
            "id": 0,
            "title": "Shortridge High School Experience", 
            "content": """Kurt Vonnegut attended Shortridge High School in Indianapolis from 1936 to 1940. He worked on the school newspaper "The Shortridge Echo" where he first discovered his love for writing and journalism. At Shortridge, he was influenced by his English teachers who encouraged his literary interests. The high school was considered progressive for its time, with a diverse student body that included many children of immigrants. This early exposure to different cultures and perspectives would later influence his humanist worldview. He wrote about his Shortridge experience throughout his life, crediting it as foundational to his development as a writer.""",
            "source": "Vonnegut Biographical Research",
            "category": "education",
            "chunks": []
        },
        {
            "id": 1,
            "title": "Dresden Bombing Experience",
            "content": """As a prisoner of war, Vonnegut survived the Allied firebombing of Dresden on February 13-14, 1945. He was held in an underground meat locker (Schlachthof-fünf, or Slaughterhouse-Five) which protected him from the firestorm that killed an estimated 25,000 civilians. The next morning, he and other POWs were forced to collect and burn corpses. This traumatic experience became the central event of his most famous novel. He rarely spoke about Dresden immediately after the war, taking 24 years to process the experience into literature. The bombing represented for him the ultimate absurdity and horror of war, shaping his lifelong anti-war stance.""",
            "source": "Slaughterhouse-Five Historical Context",
            "category": "war",
            "chunks": []
        },
        {
            "id": 2,
            "title": "Writing Philosophy and Style",
            "content": """Vonnegut believed that writers should serve as society's canaries in coal mines, warning of danger. His writing style deliberately used simple language to discuss complex philosophical ideas. He often said 'I want to be preposterous' and used dark humor to make serious points about human nature. His recurring themes included the meaninglessness of war, the destructiveness of technology, and the need for human compassion. He invented the planet Tralfamadore and the phrase 'So it goes' as literary devices to cope with death and trauma. His drawings and sketches, including asterisks and simple faces, were integral to his artistic expression.""",
            "source": "Vonnegut Literary Analysis",
            "category": "philosophy",
            "chunks": []
        },
        {
            "id": 3,
            "title": "Indianapolis Roots and Influence",
            "content": """Indianapolis shaped Vonnegut's identity as a Midwestern writer. He was born at 2007 North Delaware Street in Indianapolis. His father was an architect, his mother from a wealthy Indianapolis brewery family (Lieber). The city's practical, unpretentious culture influenced his writing style. He often referenced Indianapolis in his works and remained connected to the city throughout his life. The Kurt Vonnegut Museum and Library opened in Indianapolis in 2010. He appreciated the city's honest, working-class values and frequently contrasted Midwestern sensibilities with East Coast pretensions. Indianapolis represented for him authentic American values.""",
            "source": "Indianapolis Cultural History",
            "category": "indianapolis",
            "chunks": []
        }
    ]
    
    # Create embeddings and chunks (simplified for demo)
    embeddings = []
    
    # For each document, create simple chunks and fake embeddings
    for doc in vonnegut_documents:
        # Simple chunking - split by sentences
        sentences = doc["content"].split('. ')
        chunks = []
        for i in range(0, len(sentences), 2):  # Group 2 sentences per chunk
            chunk = '. '.join(sentences[i:i+2])
            if chunk.strip():
                chunks.append(chunk + '.')
        
        doc["chunks"] = chunks
        
        # Create fake embeddings for demo (normally you'd use OpenAI)
        for chunk in chunks:
            embeddings.append({
                "doc_id": doc["id"],
                "chunk": chunk,
                "embedding": [0.0] * 1536  # Placeholder - real system would generate these
            })
    
    # Save to file
    data = {
        "documents": vonnegut_documents,
        "embeddings": embeddings
    }
    
    with open("vonnegut_knowledge_base.pkl", 'wb') as f:
        pickle.dump(data, f)
    
    logger.info(f"Created Vonnegut knowledge base with {len(vonnegut_documents)} documents and {len(embeddings)} chunks")
    print("Vonnegut knowledge base created successfully!")
    print("Note: This is a demo version. For production, import your actual Vonnegut corpus")
    print("and generate real embeddings using OpenAI's embedding API.")

if __name__ == "__main__":
    create_vonnegut_knowledge()