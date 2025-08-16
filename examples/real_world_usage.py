"""
Real-world usage examples demonstrating Aisert's potential
"""
import logging

from pydantic import BaseModel

import os
import sys

# Add parent directory to path to import aisert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aisert import Aisert, AisertConfig, AisertError

logging.basicConfig(
    level=logging.DEBUG
)

# Example 1: API Response Validation
class UserProfile(BaseModel):
    name: str
    email: str
    age: int

def validate_api_response():
    """Validate LLM-generated API responses match expected schema"""
    llm_response = '{"name": "John Doe", "email": "john@example.com", "age": 30}'
    
    result = (
        Aisert(llm_response)
        .assert_schema(UserProfile, strict=False)
        .assert_contains(["name", "email"], strict=False)
        .assert_tokens(100, strict=False)
        .collect()
    )
    print(f"API Response Valid: {result.status}")

# Example 2: Content Moderation
def content_moderation():
    """Ensure LLM responses don't contain inappropriate content"""
    llm_response = "This is a helpful and appropriate response about cooking."
    
    try:
        Aisert(llm_response).assert_not_contains([
            "violence", "hate", "inappropriate"
        ], strict=True)
        print("✅ Content is appropriate")
    except AisertError as e:
        print(f"❌ Content contains inappropriate material: {e}")

# Example 3: Educational Content Validation
def validate_educational_content():
    """Ensure educational LLM responses meet quality standards"""
    llm_response = "Python is a programming language. It was created by Guido van Rossum."
    
    result = (
        Aisert(llm_response)
        .assert_contains(["Python", "programming"], strict=False)
        .assert_tokens(200, strict=False)  # Not too long
        .assert_semantic_matches("Python programming language explanation", 0.7, strict=False)
        .collect()
    )
    print(f"Educational content quality: {result.status}")

# Example 4: Chatbot Response Validation
def validate_chatbot_response():
    """Ensure chatbot responses are helpful and on-topic"""
    user_question = "How do I bake a cake?"
    llm_response = "To bake a cake, you need flour, eggs, sugar, and butter. Mix ingredients and bake at 350°F."
    
    result = (
        Aisert(llm_response)
        .assert_contains(["flour", "bake"], strict=False)
        .assert_tokens(150, strict=False)
        .assert_semantic_matches("cake baking instructions", 0.6, strict=False)
        .collect()
    )
    print(f"Chatbot response relevance: {result.status}")

# Example 5: Code Generation Validation
def validate_generated_code():
    """Validate LLM-generated code meets requirements"""
    generated_code = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""
    
    result = (
        Aisert(generated_code)
        .assert_contains(["def", "fibonacci", "return"], strict=False)
        .assert_tokens(500, strict=False)
        .collect()
    )
    print(f"Generated code validity: {result.status}")

# Example 6: Multi-Language Support Validation
def validate_translation():
    """Ensure translations contain expected elements"""
    translation = "Bonjour, comment allez-vous? Je suis très bien, merci."
    
    result = (
        Aisert(translation)
        .assert_contains(["Bonjour", "merci"], strict=False)
        .assert_semantic_matches("Hello, how are you? I am very well, thank you.", 0.7, strict=False)
        .collect()
    )
    print(f"Translation quality: {result.status}")

# Example 7: Batch Processing with Error Handling
def batch_validation():
    """Process multiple LLM responses with graceful error handling"""
    responses = [
        "Paris is the capital of France.",
        "Invalid response with no content",
        "London is the capital of England."
    ]
    
    config = AisertConfig(
        token_model="gpt-3.5-turbo",
        model_provider="openai"
    )
    
    for i, response in enumerate(responses):
        try:
            result = (
                Aisert(response, config)
                .assert_contains(["capital"], strict=False)
                .assert_tokens(50, strict=False)
                .collect()
            )
            print(f"Response {i+1}: {'✅ Valid' if result.status else '❌ Invalid'}")
        except Exception as e:
            print(f"Response {i+1}: ❌ Error - {e}")

if __name__ == "__main__":
    print("=== Real-World Aisert Usage Examples ===\n")
    
    print("1. API Response Validation:")
    validate_api_response()
    
    print("\n2. Content Moderation:")
    content_moderation()
    
    print("\n3. Educational Content:")
    validate_educational_content()
    
    print("\n4. Chatbot Response:")
    validate_chatbot_response()
    
    print("\n5. Code Generation:")
    validate_generated_code()
    
    print("\n6. Translation Validation:")
    validate_translation()
    
    print("\n7. Batch Processing:")
    batch_validation()