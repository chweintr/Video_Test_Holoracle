#!/usr/bin/env python3
"""
Simple RAG (Retrieval-Augmented Generation) system for Indiana Oracle
Loads key Indiana documents and provides semantic search
"""

import os
import json
import pickle
from typing import List, Dict, Tuple
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class SimpleRAG:
    def __init__(self):
        """Initialize simple RAG system"""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.documents = []
        self.embeddings = []
        self.loaded = False
        
        # Load knowledge base if it exists
        self.load_knowledge_base()
    
    def add_document(self, title: str, content: str, source: str, category: str = "general"):
        """Add a document to the knowledge base"""
        doc = {
            "id": len(self.documents),
            "title": title,
            "content": content,
            "source": source,
            "category": category,
            "chunks": self.chunk_text(content)
        }
        self.documents.append(doc)
        
        # Generate embeddings for each chunk
        for chunk in doc["chunks"]:
            embedding = self.get_embedding(chunk)
            self.embeddings.append({
                "doc_id": doc["id"],
                "chunk": chunk,
                "embedding": embedding
            })
        
        logger.info(f"Added document: {title} ({len(doc['chunks'])} chunks)")
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            if len(chunk.strip()) > 0:
                chunks.append(chunk)
        
        return chunks
    
    def get_embedding(self, text: str) -> List[float]:
        """Get OpenAI embedding for text"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",  # More cost-effective
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return [0.0] * 1536  # Default embedding size
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant documents"""
        if not self.embeddings:
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, emb_data in enumerate(self.embeddings):
            similarity = self.cosine_similarity(query_embedding, emb_data["embedding"])
            similarities.append({
                "index": i,
                "similarity": similarity,
                "doc_id": emb_data["doc_id"],
                "chunk": emb_data["chunk"]
            })
        
        # Sort by similarity and return top results
        similarities.sort(key=lambda x: x["similarity"], reverse=True)
        
        results = []
        for sim in similarities[:top_k]:
            doc = self.documents[sim["doc_id"]]
            results.append({
                "title": doc["title"],
                "source": doc["source"],
                "category": doc["category"],
                "chunk": sim["chunk"],
                "similarity": sim["similarity"]
            })
        
        return results
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    def save_knowledge_base(self, filename: str = "indiana_knowledge_base.pkl"):
        """Save knowledge base to file"""
        data = {
            "documents": self.documents,
            "embeddings": self.embeddings
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        
        logger.info(f"Saved knowledge base with {len(self.documents)} documents")
    
    def load_knowledge_base(self, filename: str = "indiana_knowledge_base.pkl"):
        """Load knowledge base from file"""
        try:
            with open(filename, 'rb') as f:
                data = pickle.load(f)
            
            self.documents = data["documents"]
            self.embeddings = data["embeddings"]
            self.loaded = True
            
            logger.info(f"Loaded knowledge base with {len(self.documents)} documents")
        except FileNotFoundError:
            logger.info("No existing knowledge base found - will create new one")
        except Exception as e:
            logger.error(f"Error loading knowledge base: {e}")
    
    def initialize_indiana_knowledge(self):
        """Initialize with key Indiana documents and facts"""
        
        # Indiana Statehood
        self.add_document(
            title="Indiana Statehood History",
            content="""Indiana became the 19th state on December 11, 1816. The territory was originally part of the Northwest Territory established in 1787. The Indiana Territory was created in 1800 with William Henry Harrison as its first governor. The Enabling Act of 1816 authorized Indiana to form a state government and draft a constitution. The constitutional convention met in Corydon from June 10-29, 1816. Corydon served as the first state capital until 1825 when the capital moved to Indianapolis. The state's name means "Land of the Indians" reflecting the numerous Native American tribes that lived in the region including the Miami, Potawatomi, Delaware, and Shawnee peoples.""",
            source="Indiana Historical Bureau",
            category="history"
        )
        
        # Indiana University
        self.add_document(
            title="Indiana University History",
            content="""Indiana University was founded in 1820 as the State Seminary. It was renamed Indiana College in 1828 and became Indiana University in 1838. The Bloomington campus is known for its beautiful limestone buildings quarried locally. Herman B Wells served as president from 1938-1962 and transformed IU into a major research university. The Little 500 bicycle race began in 1951 and was featured in the movie "Breaking Away" (1979). The Kinsey Institute for Research in Sex, Gender, and Reproduction was established by Alfred Kinsey. Notable alumni include songwriter Hoagy Carmichael who composed "Stardust" while a law student.""",
            source="IU Libraries",
            category="education"
        )
        
        # Vonnegut biographical info
        self.add_document(
            title="Kurt Vonnegut Jr. Biography",
            content="""Kurt Vonnegut Jr. was born November 11, 1922, in Indianapolis, Indiana to Kurt Vonnegut Sr. and Edith Lieber. He attended Shortridge High School in Indianapolis. During World War II, he served in the 106th Infantry Division and was captured during the Battle of the Bulge in December 1944. As a prisoner of war, he survived the Allied bombing of Dresden while being held in an underground meat locker. This experience became the basis for his novel "Slaughterhouse-Five" (1969). He wrote 14 novels total including "Cat's Cradle," "The Sirens of Titan," and "Breakfast of Champions." He died April 11, 2007, in Manhattan at age 84. He was known for his anti-war views, dark humor, and humanist philosophy.""",
            source="Kurt Vonnegut Museum & Library",
            category="literature"
        )
        
        # Indianapolis 500
        self.add_document(
            title="Indianapolis Motor Speedway History",
            content="""The Indianapolis Motor Speedway was built in 1909 by Carl G. Fisher and partners as a testing ground for automobiles. The first Indianapolis 500-Mile Race was held on May 30, 1911, won by Ray Harroun driving a Marmon Wasp. The track is a 2.5-mile rectangular oval and is known as "The Brickyard" because it was originally paved with bricks. The famous phrase "Gentlemen, start your engines" (later updated to include ladies) begins each race. The Indianapolis 500 is part of the Triple Crown of Motorsport along with the Monaco Grand Prix and 24 Hours of Le Mans. The race is traditionally held on Memorial Day weekend and is called "The Greatest Spectacle in Racing.""",
            source="Indianapolis Motor Speedway",
            category="sports"
        )
        
        # Indiana Limestone
        self.add_document(
            title="Indiana Limestone Industry",
            content="""Indiana limestone, quarried primarily in Lawrence and Monroe counties around Bedford and Bloomington, has been used to build many famous structures. The Empire State Building, Pentagon, Washington National Cathedral, and numerous university buildings across America were built with Indiana limestone. The stone was formed 330 million years ago during the Mississippian period when Indiana was covered by a shallow sea. The limestone is prized for its uniform color, durability, and ease of carving. Major limestone companies included Indiana Limestone Company and Bedford Stone Company. The industry peaked in the early 20th century but continues today, earning the nickname "Indiana's gift to the world.""",
            source="Indiana Geological Survey",
            category="industry"
        )
        
        # Bloomington-specific anecdotes and stories
        self.add_document(
            title="Granfalloon Festival and Bloomington Vonnegut Legacy",
            content="""The Granfalloon Festival is an annual celebration of Kurt Vonnegut's work held in Bloomington, Indiana, founded by Professor Ed Comentale (pronounced "common-tah-lay") from Indiana University. The festival has featured major musical acts including the Flaming Lips, Father John Misty, and Khruangbin, creating a unique fusion of literature and music. Scholar Caleb Weintraub penned an influential essay titled "The Asshole and the Proto-Emoji" analyzing Vonnegut's simple drawings as early forms of visual compression, similar to modern emojis. The original Vonnegut drawings and manuscripts are housed at IU's Lilly Library, where researchers can examine his artistic process up close. The festival celebrates not just Vonnegut's novels but his entire creative output, including his artwork and philosophy of human decency.""",
            source="Granfalloon Festival Archives",
            category="culture"
        )
        
        # Upland Brewing and local hangouts
        self.add_document(
            title="Upland Brewing and Bloomington Campus Culture",
            content="""Upland Brewing Company, founded in 1998, became a beloved campus hangout near Indiana University. Located on North Walnut Street, it serves as a gathering place for students, faculty, and locals. The brewery is known for its wheat ales and seasonal offerings, creating a distinctly Bloomington social scene. Before Upland, students would frequent Nick's English Hut (established 1927) for stromboli and beer, or the Bluebird nightclub for live music. The brewery represents the evolution of Bloomington from a traditional college town to a more sophisticated cultural hub, while maintaining its Midwestern charm and affordability that makes it accessible to students.""",
            source="Bloomington Restaurant History",
            category="culture"
        )
        
        # Architectural curiosities 
        self.add_document(
            title="Mies van der Rohe Glass House and IU Architecture",
            content="""One of Indiana University's most unusual buildings was originally designed by architect Ludwig Mies van der Rohe as a glass fraternity house in the 1950s. The modernist glass box design was considered radical for a fraternity, with its transparent walls offering no privacy for typical Greek life activities. The project was eventually adapted for academic use, becoming part of IU's architectural legacy. This represents the clash between European modernism and American college traditions. Other notable IU buildings include the Gothic Revival-style Memorial Hall and the limestone buildings quarried locally from Monroe County. The campus architecture tells the story of Indiana University's evolution from a frontier seminary to a major research institution.""",
            source="IU Architecture Survey",
            category="architecture"
        )
        
        # Bloomington nightlife and hidden gems
        self.add_document(
            title="The Dunnkirk Library and Bloomington Speakeasy Culture",
            content="""The Dunnkirk Library is Bloomington's actual speakeasy, a hidden cocktail bar that captures the prohibition-era atmosphere. Unlike typical college bars, this establishment focuses on craft cocktails and intimate conversation. The speakeasy culture in Bloomington reflects the town's evolution from a simple college town to a more sophisticated cultural destination. Other notable Bloomington nightlife includes the historic Bluebird nightclub which has hosted touring acts since the 1980s, and the Buskirk-Chumley Theater which presents both films and live performances. These venues represent the artistic and cultural depth that extends beyond the university campus.""",
            source="Bloomington Entertainment Guide",
            category="nightlife"
        )

        # Save the knowledge base
        self.save_knowledge_base()
        logger.info("Initialized Indiana knowledge base with enhanced Bloomington stories")

def test_rag_system():
    """Test the RAG system"""
    rag = SimpleRAG()
    
    # Initialize if not loaded
    if not rag.loaded:
        rag.initialize_indiana_knowledge()
    
    # Test searches
    test_queries = [
        "Tell me about Kurt Vonnegut",
        "When did Indiana become a state?",
        "What is the Little 500?",
        "Indianapolis 500 history",
        "Indiana limestone buildings"
    ]
    
    for query in test_queries:
        print(f"\n[SEARCH] Query: {query}")
        results = rag.search(query, top_k=2)
        
        for i, result in enumerate(results, 1):
            print(f"  {i}. {result['title']} (similarity: {result['similarity']:.3f})")
            print(f"     {result['chunk'][:200]}...")
            print()

if __name__ == "__main__":
    test_rag_system()