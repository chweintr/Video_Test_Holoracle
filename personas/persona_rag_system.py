#!/usr/bin/env python3
"""
Persona-specific RAG system for Indiana Oracle project
Each persona has its own knowledge base and system prompt
"""

import os
import json
import pickle
from typing import List, Dict, Optional
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

class PersonaRAGSystem:
    """RAG system that handles persona-specific knowledge and prompts"""
    
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.personas = {}
        self.initialize_personas()
    
    def initialize_personas(self):
        """Initialize all persona configurations"""
        
        # Vonnegut persona
        self.personas["vonnegut"] = {
            "name": "Kurt Vonnegut Jr.",
            "knowledge_file": "vonnegut_knowledge_base.pkl",
            "system_prompt_file": "personas/vonnegut_system_prompt.txt",
            "documents": [],
            "embeddings": [],
            "voice_id": "J80PasKsbR4AWMLiAQ0j",  # ElevenLabs
            "categories": ["literature", "philosophy", "indianapolis", "war", "writing"]
        }
        
        # Hoosier Oracle persona  
        self.personas["indiana"] = {
            "name": "Hoosier Oracle",
            "knowledge_file": "indiana_knowledge_base.pkl", 
            "system_prompt_file": "personas/hoosier_system_prompt.txt",
            "documents": [],
            "embeddings": [],
            "voice_id": "gpt",  # Use GPT TTS for cost savings
            "categories": ["history", "culture", "education", "sports", "industry"]
        }
        
        # Bigfoot persona (minimal - uses Simli's default)
        self.personas["bigfoot"] = {
            "name": "Brown County Bigfoot",
            "knowledge_file": "bigfoot_knowledge_base.pkl",
            "system_prompt_file": "personas/bigfoot_system_prompt.txt", 
            "documents": [],
            "embeddings": [],
            "voice_id": "simli_default",
            "categories": ["cryptids", "folklore", "indiana_legends", "forests"]
        }
        
        logger.info(f"Initialized {len(self.personas)} personas")
    
    def load_system_prompt(self, persona_id: str) -> str:
        """Load system prompt from file for specific persona"""
        if persona_id not in self.personas:
            return f"You are a helpful AI assistant representing the {persona_id} persona."
        
        prompt_file = self.personas[persona_id]["system_prompt_file"]
        try:
            with open(prompt_file, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.warning(f"System prompt file not found: {prompt_file}")
            return f"You are {self.personas[persona_id]['name']}, a knowledgeable persona about {persona_id} topics."
    
    def load_persona_knowledge(self, persona_id: str) -> bool:
        """Load knowledge base for specific persona"""
        if persona_id not in self.personas:
            logger.error(f"Unknown persona: {persona_id}")
            return False
        
        persona = self.personas[persona_id]
        knowledge_file = persona["knowledge_file"]
        
        try:
            if os.path.exists(knowledge_file):
                with open(knowledge_file, 'rb') as f:
                    data = pickle.load(f)
                persona["documents"] = data.get("documents", [])
                persona["embeddings"] = data.get("embeddings", [])
                logger.info(f"Loaded {len(persona['documents'])} documents for {persona_id}")
                return True
            else:
                logger.warning(f"Knowledge base not found for {persona_id}: {knowledge_file}")
                return False
        except Exception as e:
            logger.error(f"Error loading knowledge base for {persona_id}: {e}")
            return False
    
    def search_persona_knowledge(self, persona_id: str, query: str, top_k: int = 3) -> List[Dict]:
        """Search knowledge base for specific persona"""
        if persona_id not in self.personas:
            return []
        
        persona = self.personas[persona_id]
        
        # Load knowledge if not already loaded
        if not persona["embeddings"]:
            self.load_persona_knowledge(persona_id)
        
        if not persona["embeddings"]:
            return []
        
        # Get query embedding
        query_embedding = self.get_embedding(query)
        
        # Calculate similarities
        similarities = []
        for i, emb_data in enumerate(persona["embeddings"]):
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
            doc = persona["documents"][sim["doc_id"]]
            results.append({
                "title": doc["title"],
                "source": doc["source"],
                "category": doc["category"],
                "chunk": sim["chunk"],
                "similarity": sim["similarity"]
            })
        
        return results
    
    def get_embedding(self, text: str) -> List[float]:
        """Get OpenAI embedding for text"""
        try:
            response = self.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Embedding error: {e}")
            return [0.0] * 1536
    
    def cosine_similarity(self, a: List[float], b: List[float]) -> float:
        """Calculate cosine similarity between two vectors"""
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
    
    async def get_persona_response(self, persona_id: str, user_input: str) -> str:
        """Get AI response using persona-specific knowledge and prompt"""
        try:
            # Load system prompt
            system_prompt = self.load_system_prompt(persona_id)
            
            # Search for relevant context
            relevant_docs = self.search_persona_knowledge(persona_id, user_input, top_k=2)
            
            # Build context from relevant documents
            context = ""
            if relevant_docs:
                context_parts = []
                for doc in relevant_docs:
                    context_parts.append(f"Source: {doc['title']}\n{doc['chunk']}")
                context = "\n\n---\n\n".join(context_parts)
                context = f"Relevant knowledge from your memory:\n{context}\n\n"
            
            # Generate response using persona-specific prompt
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"{context}User: {user_input}"}
            ]
            
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                max_tokens=200,
                temperature=0.8 if persona_id == "vonnegut" else 0.7  # Vonnegut gets more creativity
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error getting {persona_id} response: {e}")
            return f"I'm having trouble accessing my thoughts right now. {e}"
    
    def get_persona_info(self, persona_id: str) -> Dict:
        """Get persona configuration info"""
        if persona_id not in self.personas:
            return {}
        
        persona = self.personas[persona_id]
        return {
            "name": persona["name"],
            "voice_id": persona["voice_id"],
            "categories": persona["categories"],
            "knowledge_loaded": len(persona["documents"]) > 0,
            "document_count": len(persona["documents"])
        }

# Backward compatibility with existing code
class SimpleRAGSystem:
    """Wrapper for backward compatibility"""
    
    def __init__(self):
        self.persona_rag = PersonaRAGSystem()
    
    async def load_knowledge_base(self, filename: str = "indiana_knowledge_base.pkl"):
        """Load knowledge base - now loads all personas"""
        try:
            # Load all persona knowledge bases
            success_count = 0
            for persona_id in self.persona_rag.personas.keys():
                if self.persona_rag.load_persona_knowledge(persona_id):
                    success_count += 1
            
            logger.info(f"Loaded knowledge for {success_count} personas")
            return success_count > 0
        except Exception as e:
            logger.error(f"Error loading knowledge bases: {e}")
            return False
    
    async def get_response(self, user_input: str, persona: str = "indiana") -> str:
        """Get AI response using persona-specific system"""
        return await self.persona_rag.get_persona_response(persona, user_input)

if __name__ == "__main__":
    # Test the persona RAG system
    import asyncio
    
    async def test_persona_rag():
        rag = PersonaRAGSystem()
        
        test_queries = [
            ("vonnegut", "What did you think about your time at Shortridge Echo?"),
            ("vonnegut", "Tell me about Dresden and the war"),
            ("indiana", "When did Indiana become a state?"),
            ("bigfoot", "What legends exist in Brown County?")
        ]
        
        for persona_id, query in test_queries:
            print(f"\n[{persona_id.upper()}] Query: {query}")
            response = await rag.get_persona_response(persona_id, query)
            print(f"Response: {response}")
            print("-" * 80)
    
    asyncio.run(test_persona_rag())