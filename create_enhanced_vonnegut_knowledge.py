#!/usr/bin/env python3
"""
Create enhanced Vonnegut knowledge base with comprehensive biographical and literary content
"""

import pickle
import logging
from personas.persona_rag_system import PersonaRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_enhanced_vonnegut_knowledge():
    """Create comprehensive Vonnegut knowledge base with the provided content"""
    
    # Enhanced Vonnegut documents with the provided biographical content
    vonnegut_documents = [
        {
            "id": 0,
            "title": "Kurt Vonnegut Complete Biography",
            "content": """Kurt Vonnegut (1922–2007) was an American writer known for blending dark humor, satire and science fiction. He was born in Indianapolis on 11 Nov 1922; his father, Kurt Sr., was a prominent architect, and his mother Edith was the daughter of a brewer. The Great Depression devastated the family's finances, forcing them to sell their home and removing young Kurt from private school. Vonnegut began writing as a teenager for The Shortridge Echo and later became an editor and columnist for The Cornell Sun. His journalism experience taught him to value clarity and brevity. During World War II he served in the U.S. Army, was captured in the Battle of the Bulge and survived the Allied fire‑bombing of Dresden as a prisoner of war. He and other prisoners sheltered in the meat locker of slaughterhouse number 5 and afterwards were forced to help burn corpses. This traumatic experience provided the basis for his famous novel Slaughterhouse‑Five. After the war he married Jane Marie Cox, worked in public relations at General Electric in Schenectady, New York and wrote short fiction on the side. He and Jane adopted his sister's three sons after she and her husband died in 1958; supporting a large family pushed him toward writing full‑length novels.""",
            "source": "Kurt Vonnegut Museum and Library",
            "category": "biography",
            "chunks": []
        },
        {
            "id": 1,
            "title": "Vonnegut's Writing Career and Major Works",
            "content": """Vonnegut's early novels include Player Piano (1952), The Sirens of Titan (1959), Mother Night (1961), Cat's Cradle (1963), God Bless You, Mr. Rosewater (1965) and Slaughterhouse‑Five (1969). Later he published Breakfast of Champions (1973) and continued writing through the 1980s and 1990s. Personal turmoil in the 1970s—his divorce from Jane, subsequent marriage to photographer Jill Krementz and writer's block—affected his tone. He remained politically active, defending constitutional liberties and attacking war and corporate power. His late works include the semi‑autobiographical Timequake (1997) and the essay collection A Man Without a Country (2005). Vonnegut died on 11 Apr 2007 after a fall. He wrote 14 novels total, numerous short stories, essays, speeches, plays and screenplays. His fiction often mixes science fiction and satire while exploring free will, humanism and the absurdity of war.""",
            "source": "Vonnegut Literary Compendium",
            "category": "literature",
            "chunks": []
        },
        {
            "id": 2,
            "title": "The Shortridge Echo and Early Writing Experience",
            "content": """Vonnegut began writing as a teenager for The Shortridge Echo and later became an editor and columnist for The Cornell Sun. His journalism experience taught him to value clarity and brevity. At Shortridge High School in Indianapolis, he first discovered his love for writing and journalism. The high school was considered progressive for its time, with a diverse student body that included many children of immigrants. This early exposure to different cultures and perspectives would later influence his humanist worldview. He wrote about his Shortridge experience throughout his life, crediting it as foundational to his development as a writer. His work on the school newspaper gave him practical experience in clear, direct communication that became a hallmark of his literary style.""",
            "source": "Shortridge High School Archives",
            "category": "education",
            "chunks": []
        },
        {
            "id": 3,
            "title": "Dresden Experience and War Trauma",
            "content": """During World War II he served in the U.S. Army, was captured in the Battle of the Bulge and survived the Allied fire‑bombing of Dresden as a prisoner of war. He and other prisoners sheltered in the meat locker of slaughterhouse number 5 and afterwards were forced to help burn corpses. This traumatic experience provided the basis for his famous novel Slaughterhouse‑Five. As a prisoner of war, Vonnegut survived the Allied firebombing of Dresden on February 13-14, 1945. He was held in an underground meat locker (Schlachthof-fünf, or Slaughterhouse-Five) which protected him from the firestorm that killed an estimated 25,000 civilians. The next morning, he and other POWs were forced to collect and burn corpses. This traumatic experience became the central event of his most famous novel. He rarely spoke about Dresden immediately after the war, taking 24 years to process the experience into literature.""",
            "source": "War Records and Slaughterhouse-Five",
            "category": "war",
            "chunks": []
        },
        {
            "id": 4,
            "title": "Major Novels and Literary Works",
            "content": """Player Piano (1952) - Satire of automation and corporate control, Vonnegut's debut novel emerged from his work at General Electric. The Sirens of Titan (1959) - Science‑fiction epic exploring free will and the purpose of humanity. Mother Night (1961) - Novel of a playwright turned Nazi propagandist who claims he was an American spy. Cat's Cradle (1963) - A darkly comic tale about scientists, religion (the invented Bokononism) and the apocalyptic ice‑nine. God Bless You, Mr. Rosewater (1965) - Satire about wealth, philanthropy and mental health. Slaughterhouse‑Five (1969) - Semi‑autobiographical novel about Billy Pilgrim, the Dresden bombing, time travel and trauma. Breakfast of Champions (1973) - Meta‑fictional novel in which Vonnegut appears as a character; critiques American consumer culture. Later works include Slapstick, Jailbird, Deadeye Dick, Galápagos, Bluebeard, Hocus Pocus and Timequake (1997).""",
            "source": "Complete Vonnegut Bibliography",
            "category": "literature",
            "chunks": []
        },
        {
            "id": 5,
            "title": "Vonnegut's Speeches and Public Presence",
            "content": """Vonnegut delivered many witty and critical speeches. Most accessible transcripts are compiled in If This Isn't Nice, What Is?. Notable speeches include his 'Harrison Bergeron' reading at the Moratorium Day rally in New York City (1969), where he denounced the Vietnam War. His commencement address at Bennington College (1970) emphasised imagination and kindness. At Hobart and William Smith Colleges (1974) he urged graduates to treat the world with compassion. He also spoke to the Indiana Civil Liberties Union and accepted the Carl Sandburg Award. Additionally, Palm Sunday and Fates Worse Than Death reproduce speeches including his Address to the American Physical Society (1969), a satirical talk about the reliability of nuclear power. He remained politically active throughout his life, defending constitutional liberties and attacking war and corporate power.""",
            "source": "If This Isn't Nice, What Is?",
            "category": "speeches",
            "chunks": []
        },
        {
            "id": 6,
            "title": "Indianapolis Roots and Midwestern Identity",
            "content": """Kurt Vonnegut was born in Indianapolis on November 11, 1922. His father, Kurt Sr., was a prominent architect, and his mother Edith was the daughter of a brewer. Indianapolis shaped Vonnegut's identity as a Midwestern writer. The city's practical, unpretentious culture influenced his writing style. He often referenced Indianapolis in his works and remained connected to the city throughout his life. The Kurt Vonnegut Museum and Library opened in Indianapolis in 2010. He appreciated the city's honest, working-class values and frequently contrasted Midwestern sensibilities with East Coast pretensions. Indianapolis represented for him authentic American values. The Great Depression devastated the family's finances, forcing them to sell their home and removing young Kurt from private school, an experience that shaped his understanding of economic inequality and social justice.""",
            "source": "Indianapolis Cultural History",
            "category": "indianapolis",
            "chunks": []
        },
        {
            "id": 7,
            "title": "Philosophy and Recurring Themes",
            "content": """Vonnegut's fiction often mixes science fiction and satire while exploring free will, humanism and the absurdity of war. His writing philosophy emphasized that writers should serve as society's canaries in coal mines, warning of danger. His writing style deliberately used simple language to discuss complex philosophical ideas. He often said 'I want to be preposterous' and used dark humor to make serious points about human nature. His recurring themes included the meaninglessness of war, the destructiveness of technology, and the need for human compassion. He invented the planet Tralfamadore and the phrase 'So it goes' as literary devices to cope with death and trauma. His drawings and sketches, including asterisks and simple faces, were integral to his artistic expression. He remained an advocate for simple human kindness above all, skeptical of technology and progress while supporting socialist ideals and criticizing capitalism.""",
            "source": "Vonnegut Literary Analysis",
            "category": "philosophy",
            "chunks": []
        }
    ]
    
    # Create embeddings and chunks (simplified for demo)
    embeddings = []
    
    # For each document, create simple chunks and fake embeddings
    for doc in vonnegut_documents:
        # Simple chunking - split by sentences, group by 2-3 sentences
        sentences = doc["content"].split('. ')
        chunks = []
        for i in range(0, len(sentences), 3):  # Group 3 sentences per chunk
            chunk = '. '.join(sentences[i:i+3])
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
    
    logger.info(f"Created enhanced Vonnegut knowledge base with {len(vonnegut_documents)} documents and {len(embeddings)} chunks")
    print("✅ Enhanced Vonnegut knowledge base created successfully!")
    print(f"📚 {len(vonnegut_documents)} documents covering:")
    print("   - Complete biography and family background")
    print("   - All 14 novels and major works")
    print("   - Shortridge Echo and journalism experience")
    print("   - Dresden POW experience and war trauma")
    print("   - Indianapolis roots and Midwestern identity")
    print("   - Speeches and public appearances")
    print("   - Writing philosophy and recurring themes")
    print("\n🎯 Ready to update with scraped corpus when available!")
    
    # Also update the voice configuration
    print(f"🔊 ElevenLabs Voice ID: J80PasKsbR4AWMLiAQ0j")

if __name__ == "__main__":
    create_enhanced_vonnegut_knowledge()