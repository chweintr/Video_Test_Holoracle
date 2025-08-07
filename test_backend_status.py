#!/usr/bin/env python3
"""
Test script to verify Simli Voice Backend status and initialization
"""

import asyncio
import json
import os
from simli_voice_backend import backend, app

async def test_backend_status():
    """Test the backend status and initialization"""
    print("=== Simli Voice Backend Status Test ===\n")
    
    # Test 1: Check initial status
    print("1. Initial Status Check:")
    print(f"   Voice System: {backend.voice_system is not None}")
    print(f"   RAG System: {backend.rag_system is not None}")
    print(f"   Systems Initialized: {backend.voice_system is not None or backend.rag_system is not None}")
    
    # Test 2: Check environment variables
    print("\n2. Environment Variables:")
    print(f"   OPENAI_API_KEY: {'✓' if os.getenv('OPENAI_API_KEY') else '✗'}")
    print(f"   ELEVENLABS_API_KEY: {'✓' if os.getenv('ELEVENLABS_API_KEY') else '✗'}")
    print(f"   Knowledge Base: {'✓' if os.path.exists('indiana_knowledge_base.pkl') else '✗'}")
    
    # Test 3: Manual initialization
    print("\n3. Manual Initialization:")
    success = await backend.initialize_systems()
    print(f"   Initialization Result: {'✓' if success else '✗'}")
    
    # Test 4: Check status after initialization
    print("\n4. Status After Initialization:")
    print(f"   Voice System: {backend.voice_system is not None}")
    print(f"   RAG System: {backend.rag_system is not None}")
    print(f"   Systems Initialized: {backend.voice_system is not None or backend.rag_system is not None}")
    
    # Test 5: Simulate root endpoint response
    print("\n5. Root Endpoint Response:")
    voice_ready = backend.voice_system is not None
    rag_ready = backend.rag_system is not None
    systems_initialized = voice_ready or rag_ready
    
    response = {
        "message": "Simli Voice Backend",
        "status": "running",
        "systems_initialized": systems_initialized,
        "voice_system_ready": voice_ready,
        "rag_system_ready": rag_ready,
        "environment": {
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "elevenlabs_key": bool(os.getenv("ELEVENLABS_API_KEY")),
            "knowledge_base_exists": os.path.exists("indiana_knowledge_base.pkl")
        }
    }
    
    print(json.dumps(response, indent=2))
    
    print("\n=== Test Complete ===")

if __name__ == "__main__":
    asyncio.run(test_backend_status())
