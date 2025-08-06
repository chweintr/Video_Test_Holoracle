"""
Safe file reader for handling transcripts with various encodings.
Handles BOM, encoding issues, and malformed text files.
"""

import logging
from pathlib import Path
from typing import Optional
import chardet

logger = logging.getLogger(__name__)

def read_transcript_safely(file_path: str) -> Optional[str]:
    """
    Safely read a transcript file with automatic encoding detection.
    
    Args:
        file_path: Path to transcript file
        
    Returns:
        File content as string, or None if reading fails
    """
    try:
        file_path = Path(file_path)
        
        if not file_path.exists():
            logger.error(f"Transcript file not found: {file_path}")
            return None
        
        # Read raw bytes first
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        if len(raw_data) == 0:
            logger.warning(f"Transcript file is empty: {file_path}")
            return ""
        
        # Detect encoding
        encoding_result = chardet.detect(raw_data)
        detected_encoding = encoding_result.get('encoding', 'utf-8')
        confidence = encoding_result.get('confidence', 0)
        
        logger.info(f"Detected encoding: {detected_encoding} (confidence: {confidence:.2f})")
        
        # Try detected encoding first
        try:
            content = raw_data.decode(detected_encoding)
            
            # Remove BOM if present
            if content.startswith('\ufeff'):
                content = content[1:]
                logger.info("Removed BOM from transcript")
            
            return content.strip()
            
        except UnicodeDecodeError:
            logger.warning(f"Failed to decode with detected encoding: {detected_encoding}")
        
        # Try common encodings as fallback
        encodings_to_try = ['utf-8', 'utf-8-sig', 'latin1', 'cp1252', 'ascii']
        
        for encoding in encodings_to_try:
            try:
                content = raw_data.decode(encoding, errors='ignore')
                
                # Remove BOM if present
                if content.startswith('\ufeff'):
                    content = content[1:]
                
                logger.info(f"Successfully read transcript with {encoding} encoding")
                return content.strip()
                
            except UnicodeDecodeError:
                continue
        
        # Last resort: decode with errors='replace'
        content = raw_data.decode('utf-8', errors='replace')
        logger.warning("Read transcript with error replacement - some characters may be corrupted")
        
        # Remove BOM if present
        if content.startswith('\ufeff'):
            content = content[1:]
        
        return content.strip()
        
    except Exception as e:
        logger.error(f"Error reading transcript file {file_path}: {e}")
        return None

def validate_transcript_content(content: str) -> bool:
    """
    Validate that transcript content looks reasonable.
    
    Args:
        content: Transcript text
        
    Returns:
        True if content seems valid
    """
    if not content or len(content.strip()) < 10:
        return False
    
    # Check for reasonable text characteristics
    alpha_chars = sum(1 for c in content if c.isalpha())
    total_chars = len(content)
    
    if total_chars == 0:
        return False
    
    alpha_ratio = alpha_chars / total_chars
    
    # Should be mostly alphabetic characters
    if alpha_ratio < 0.5:
        logger.warning(f"Transcript has low alphabetic ratio: {alpha_ratio:.2f}")
        return False
    
    return True

# Test function
def test_transcript_reading():
    """Test transcript reading with the actual file."""
    transcript_path = "../sound_files/transcript_01.txt"
    
    logger.info(f"Testing transcript reading: {transcript_path}")
    
    content = read_transcript_safely(transcript_path)
    
    if content is None:
        logger.error("Failed to read transcript")
        return False
    
    if not validate_transcript_content(content):
        logger.error("Transcript content validation failed")
        return False
    
    logger.info(f"Successfully read transcript: {len(content)} characters")
    logger.info(f"First 100 characters: {content[:100]}...")
    
    return True

if __name__ == "__main__":
    # Set up logging to show output
    import sys
    
    # Configure logging to show info messages
    logging.basicConfig(
        level=logging.INFO,
        format='%(levelname)s:%(name)s:%(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )
    
    print("Starting transcript reading test...")
    
    try:
        success = test_transcript_reading()
        if success:
            print("✓ Transcript reading test passed!")
        else:
            print("✗ Transcript reading test failed!")
    except Exception as e:
        print(f"Error during test: {e}")
        import traceback
        traceback.print_exc()