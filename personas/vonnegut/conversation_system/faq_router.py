"""
FAQ Router for the Indiana Oracle system.
Routes queries to pre-existing transcript responses and generates embeddings for similarity search.
"""

import json
import logging
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import re
import asyncio
from datetime import datetime
from safe_file_reader import read_transcript_safely, validate_transcript_content

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FAQRouter:
    def __init__(self, transcript_path: str = None, faq_db_path: str = "faq_database.json"):
        self.transcript_path = transcript_path or "../sound_files/transcript_01.txt"
        self.faq_db_path = Path(faq_db_path)
        
        # FAQ database
        self.faq_entries = []
        self.embeddings = None
        
        # Configuration
        self.similarity_threshold = 0.7
        self.max_response_length = 200  # characters
        self.min_response_length = 20
        
        # Initialize (will be called async later)
        self.initialized = False
    
    async def initialize(self):
        """Initialize the FAQ system."""
        logger.info("Initializing FAQ router...")
        
        try:
            # Load existing FAQ database or create from transcript
            if self.faq_db_path.exists():
                await self.load_faq_database()
            else:
                await self.build_faq_from_transcript()
            
            # Load or generate embeddings
            await self.load_or_generate_embeddings()
            
            logger.info(f"FAQ router initialized with {len(self.faq_entries)} entries")
            
        except Exception as e:
            logger.error(f"Error initializing FAQ router: {e}")
    
    async def load_faq_database(self):
        """Load existing FAQ database."""
        try:
            with open(self.faq_db_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.faq_entries = data.get('entries', [])
            logger.info(f"Loaded {len(self.faq_entries)} FAQ entries from database")
            
        except Exception as e:
            logger.error(f"Error loading FAQ database: {e}")
            self.faq_entries = []
    
    async def build_faq_from_transcript(self):
        """Build FAQ database from the original transcript."""
        try:
            if not Path(self.transcript_path).exists():
                logger.warning(f"Transcript not found: {self.transcript_path}")
                await self.create_default_faq()
                return
            
            logger.info(f"Building FAQ from transcript: {self.transcript_path}")
            
            # Use safe file reader for transcript
            transcript = read_transcript_safely(self.transcript_path)
            
            if transcript is None:
                logger.error("Failed to read transcript file")
                await self.create_default_faq()
                return
            
            if not validate_transcript_content(transcript):
                logger.warning("Transcript content validation failed, using default FAQ")
                await self.create_default_faq()
                return
            
            # Extract interesting quotes and responses
            entries = await self.extract_faq_entries(transcript)
            
            self.faq_entries = entries
            
            # Save to database
            await self.save_faq_database()
            
            logger.info(f"Built FAQ database with {len(entries)} entries")
            
        except Exception as e:
            logger.error(f"Error building FAQ from transcript: {e}")
            await self.create_default_faq()
    
    async def extract_faq_entries(self, transcript: str) -> List[Dict]:
        """Extract FAQ entries from transcript text."""
        entries = []
        
        try:
            # Split into sentences
            sentences = self.split_into_sentences(transcript)
            
            # Extract different types of FAQ entries
            
            # 1. Direct quotes (Vonnegut's famous phrases)
            famous_phrases = [
                "So it goes",
                "Everything was beautiful and nothing hurt",
                "Listen:",
                "Human beings",
                "All this happened, more or less",
                "Billy Pilgrim",
                "unstuck in time"
            ]
            
            for phrase in famous_phrases:
                matches = self.find_phrase_contexts(sentences, phrase)
                for match in matches:
                    entries.append({
                        'id': len(entries),
                        'type': 'famous_quote',
                        'trigger_phrases': [phrase.lower()],
                        'response': match,
                        'confidence_boost': 0.2,  # Boost for famous phrases
                        'source': 'transcript',
                        'audio_file': None  # Will be generated later
                    })
            
            # 2. Question-like statements (convert to Q&A)
            question_entries = self.extract_question_responses(sentences)
            entries.extend(question_entries)
            
            # 3. Philosophical statements
            philosophical_entries = self.extract_philosophical_statements(sentences)
            entries.extend(philosophical_entries)
            
            # 4. Character references
            character_entries = self.extract_character_references(sentences)
            entries.extend(character_entries)
            
            # Remove duplicates and filter by length
            entries = self.filter_and_dedupe_entries(entries)
            
            return entries
            
        except Exception as e:
            logger.error(f"Error extracting FAQ entries: {e}")
            return []
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences."""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Filter out very short or very long sentences
        filtered = []
        for sentence in sentences:
            if self.min_response_length <= len(sentence) <= self.max_response_length:
                filtered.append(sentence)
        
        return filtered
    
    def find_phrase_contexts(self, sentences: List[str], phrase: str) -> List[str]:
        """Find sentences containing a specific phrase."""
        matches = []
        phrase_lower = phrase.lower()
        
        for sentence in sentences:
            if phrase_lower in sentence.lower():
                matches.append(sentence.strip())
        
        return matches[:3]  # Limit to 3 matches per phrase
    
    def extract_question_responses(self, sentences: List[str]) -> List[Dict]:
        """Extract question-like statements and create Q&A pairs."""
        entries = []
        
        # Look for sentences that might be responses to common questions
        question_patterns = [
            (r'what.*is', 'definition'),
            (r'how.*to', 'instruction'),
            (r'why.*', 'explanation'),
            (r'when.*', 'temporal'),
            (r'where.*', 'location'),
            (r'who.*', 'person')
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Check if sentence seems like a response
            if any(word in sentence_lower for word in ['because', 'since', 'therefore', 'thus', 'so']):
                # Create potential triggers
                triggers = self.generate_question_triggers(sentence)
                
                if triggers:
                    entries.append({
                        'id': len(entries),
                        'type': 'explanation',
                        'trigger_phrases': triggers,
                        'response': sentence,
                        'confidence_boost': 0.1,
                        'source': 'transcript',
                        'audio_file': None
                    })
        
        return entries[:10]  # Limit number of question entries
    
    def generate_question_triggers(self, response: str) -> List[str]:
        """Generate potential question triggers for a response."""
        triggers = []
        response_lower = response.lower()
        
        # Extract key nouns and concepts
        # This is a simple approach - could be improved with NLP
        words = response_lower.split()
        
        # Look for important concepts
        concepts = []
        for word in words:
            if len(word) > 4 and word.isalpha():
                concepts.append(word)
        
        # Generate question forms
        for concept in concepts[:3]:  # Limit to top 3 concepts
            triggers.extend([
                f"what is {concept}",
                f"tell me about {concept}",
                f"explain {concept}",
                concept
            ])
        
        return triggers[:5]  # Limit triggers per response
    
    def extract_philosophical_statements(self, sentences: List[str]) -> List[Dict]:
        """Extract philosophical or profound statements."""
        entries = []
        
        philosophical_keywords = [
            'life', 'death', 'time', 'existence', 'meaning', 'purpose',
            'reality', 'truth', 'human', 'nature', 'soul', 'god',
            'war', 'peace', 'love', 'hate', 'beautiful', 'ugly'
        ]
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            
            # Count philosophical keywords
            keyword_count = sum(1 for keyword in philosophical_keywords if keyword in sentence_lower)
            
            if keyword_count >= 2:  # At least 2 philosophical concepts
                # Generate triggers based on keywords found
                triggers = []
                for keyword in philosophical_keywords:
                    if keyword in sentence_lower:
                        triggers.extend([
                            keyword,
                            f"what about {keyword}",
                            f"thoughts on {keyword}"
                        ])
                
                entries.append({
                    'id': len(entries),
                    'type': 'philosophical',
                    'trigger_phrases': triggers[:5],
                    'response': sentence,
                    'confidence_boost': 0.15,
                    'source': 'transcript',
                    'audio_file': None
                })
        
        return entries[:15]  # Limit philosophical entries
    
    def extract_character_references(self, sentences: List[str]) -> List[Dict]:
        """Extract character references and descriptions."""
        entries = []
        
        # Look for character names (simplified)
        character_patterns = [
            r'Billy Pilgrim',
            r'[A-Z][a-z]+ [A-Z][a-z]+',  # Proper names
        ]
        
        for sentence in sentences:
            for pattern in character_patterns:
                matches = re.findall(pattern, sentence)
                
                if matches:
                    for character in matches:
                        triggers = [
                            character.lower(),
                            f"who is {character.lower()}",
                            f"tell me about {character.lower()}",
                            f"what about {character.lower()}"
                        ]
                        
                        entries.append({
                            'id': len(entries),
                            'type': 'character',
                            'trigger_phrases': triggers,
                            'response': sentence,
                            'confidence_boost': 0.1,
                            'source': 'transcript',
                            'audio_file': None
                        })
                        break  # One entry per sentence
        
        return entries[:10]  # Limit character entries
    
    def filter_and_dedupe_entries(self, entries: List[Dict]) -> List[Dict]:
        """Filter and remove duplicate entries."""
        # Remove duplicates based on response text
        seen_responses = set()
        filtered = []
        
        for entry in entries:
            response = entry['response'].strip()
            
            if response not in seen_responses:
                seen_responses.add(response)
                filtered.append(entry)
        
        # Sort by confidence boost (highest first)
        filtered.sort(key=lambda x: x.get('confidence_boost', 0), reverse=True)
        
        return filtered[:50]  # Limit total entries
    
    async def create_default_faq(self):
        """Create default FAQ entries when no transcript is available."""
        default_entries = [
            {
                'id': 0,
                'type': 'greeting',
                'trigger_phrases': ['hello', 'hi', 'hey', 'greetings'],
                'response': 'So it goes. What brings you to speak with me today?',
                'confidence_boost': 0.3,
                'source': 'default',
                'audio_file': None
            },
            {
                'id': 1,
                'type': 'famous_quote',
                'trigger_phrases': ['so it goes', 'death', 'mortality'],
                'response': 'So it goes. That is what I say about death and dying.',
                'confidence_boost': 0.5,
                'source': 'default',
                'audio_file': None
            },
            {
                'id': 2,
                'type': 'philosophical',
                'trigger_phrases': ['meaning', 'purpose', 'life'],
                'response': 'Everything was beautiful and nothing hurt. That is how I choose to remember it.',
                'confidence_boost': 0.4,
                'source': 'default',
                'audio_file': None
            },
            {
                'id': 3,
                'type': 'time',
                'trigger_phrases': ['time', 'past', 'future', 'unstuck'],
                'response': 'Listen: Billy Pilgrim has come unstuck in time. We all have, in our own way.',
                'confidence_boost': 0.4,
                'source': 'default',
                'audio_file': None
            }
        ]
        
        self.faq_entries = default_entries
        await self.save_faq_database()
        
        logger.info(f"Created {len(default_entries)} default FAQ entries")
    
    async def save_faq_database(self):
        """Save FAQ database to file."""
        try:
            data = {
                'created_at': datetime.now().isoformat(),
                'source_transcript': self.transcript_path,
                'total_entries': len(self.faq_entries),
                'entries': self.faq_entries
            }
            
            with open(self.faq_db_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Saved FAQ database: {self.faq_db_path}")
            
        except Exception as e:
            logger.error(f"Error saving FAQ database: {e}")
    
    async def load_or_generate_embeddings(self):
        """Load or generate embeddings for FAQ entries."""
        try:
            # For now, use simple keyword-based matching
            # In production, you'd use sentence transformers or similar
            
            # Create simple embeddings based on trigger phrases
            self.embeddings = {}
            
            for entry in self.faq_entries:
                entry_id = entry['id']
                triggers = entry['trigger_phrases']
                
                # Create a simple bag-of-words embedding
                all_words = ' '.join(triggers).lower().split()
                word_counts = {}
                
                for word in all_words:
                    word_counts[word] = word_counts.get(word, 0) + 1
                
                self.embeddings[entry_id] = word_counts
            
            logger.info(f"Generated embeddings for {len(self.embeddings)} entries")
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            self.embeddings = {}
    
    def calculate_similarity(self, query: str, entry_id: int) -> float:
        """Calculate similarity between query and FAQ entry."""
        try:
            if entry_id not in self.embeddings:
                return 0.0
            
            query_words = query.lower().split()
            entry_embedding = self.embeddings[entry_id]
            
            # Simple word overlap similarity
            matches = 0
            total_query_words = len(query_words)
            
            if total_query_words == 0:
                return 0.0
            
            for word in query_words:
                if word in entry_embedding:
                    matches += entry_embedding[word]
            
            similarity = matches / total_query_words
            
            # Apply confidence boost
            entry = self.faq_entries[entry_id]
            confidence_boost = entry.get('confidence_boost', 0)
            
            return min(1.0, similarity + confidence_boost)
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    async def check_faq(self, query: str) -> Optional[Dict]:
        """
        Check if query matches any FAQ entries.
        
        Args:
            query: User's query text
            
        Returns:
            FAQ response dict if match found, None otherwise
        """
        try:
            if not self.faq_entries:
                return None
            
            best_match = None
            best_score = 0.0
            
            # Check each FAQ entry
            for entry in self.faq_entries:
                similarity = self.calculate_similarity(query, entry['id'])
                
                if similarity > best_score:
                    best_score = similarity
                    best_match = entry
            
            # Return match if above threshold
            if best_score >= self.similarity_threshold:
                logger.info(f"FAQ match found: {best_match['type']} (score: {best_score:.3f})")
                
                return {
                    'text': best_match['response'],
                    'type': best_match['type'],
                    'confidence': best_score,
                    'entry_id': best_match['id'],
                    'audio_file': best_match.get('audio_file'),
                    'source': 'faq'
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error checking FAQ: {e}")
            return None
    
    async def add_faq_entry(self, triggers: List[str], response: str, entry_type: str = 'custom') -> int:
        """Add a new FAQ entry."""
        try:
            entry_id = len(self.faq_entries)
            
            new_entry = {
                'id': entry_id,
                'type': entry_type,
                'trigger_phrases': triggers,
                'response': response,
                'confidence_boost': 0.0,
                'source': 'manual',
                'audio_file': None,
                'created_at': datetime.now().isoformat()
            }
            
            self.faq_entries.append(new_entry)
            
            # Update embeddings
            all_words = ' '.join(triggers).lower().split()
            word_counts = {}
            
            for word in all_words:
                word_counts[word] = word_counts.get(word, 0) + 1
            
            self.embeddings[entry_id] = word_counts
            
            # Save database
            await self.save_faq_database()
            
            logger.info(f"Added new FAQ entry: {entry_id}")
            return entry_id
            
        except Exception as e:
            logger.error(f"Error adding FAQ entry: {e}")
            return -1
    
    def get_stats(self) -> Dict:
        """Get FAQ router statistics."""
        types = {}
        sources = {}
        
        for entry in self.faq_entries:
            entry_type = entry.get('type', 'unknown')
            source = entry.get('source', 'unknown')
            
            types[entry_type] = types.get(entry_type, 0) + 1
            sources[source] = sources.get(source, 0) + 1
        
        return {
            'total_entries': len(self.faq_entries),
            'types': types,
            'sources': sources,
            'similarity_threshold': self.similarity_threshold,
            'has_embeddings': self.embeddings is not None
        }

# Testing function
async def test_faq_router():
    """Test FAQ router functionality."""
    logger.info("Testing FAQ router...")
    
    router = FAQRouter()
    
    # Wait for initialization
    await asyncio.sleep(1)
    
    # Test queries
    test_queries = [
        "Hello there",
        "What is the meaning of life?",
        "So it goes",
        "Tell me about Billy Pilgrim",
        "What about time travel?",
        "Random query that shouldn't match"
    ]
    
    for query in test_queries:
        result = await router.check_faq(query)
        
        if result:
            logger.info(f"Query: '{query}'")
            logger.info(f"  -> Match: {result['type']} (confidence: {result['confidence']:.3f})")
            logger.info(f"  -> Response: {result['text'][:50]}...")
        else:
            logger.info(f"Query: '{query}' -> No match")
    
    # Print stats
    stats = router.get_stats()
    logger.info(f"FAQ Stats: {stats}")

def main():
    """Test the FAQ router."""
    asyncio.run(test_faq_router())

if __name__ == "__main__":
    main()