import sys
import os

# Add parent directory to path to import aisert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aisert import Aisert, AIsertConfig

def assert_openai_response():
    """
    Example of how to use Aisert to validate a LLM response.
    """
    
    # Mock response for demonstration (remove OpenAI dependency)
    mock_response = "Paris is the capital of France."
    
    # Configure Aisert
    config = AIsertConfig(
        token_model="gpt-3.5-turbo",
        token_encoding=None,
        model_provider="openai",
        sentence_transformer_model="all-MiniLM-L6-v2",
    )
    
    # Validate the response
    result = Aisert(content=mock_response, config=config) \
        .assert_contains(items=["Paris", "France"]) \
        .assert_tokens(40) \
        .collect()
    
    print("Validation result:", result)
    return result


def assert_openai_response_with_api():
    """
    Example of how to use Aisert to validate a LLM response.
    """
    from openai import OpenAI

    # Configure Aisert
    config = AIsertConfig(
        token_model="gpt-3.5-turbo",
        token_encoding=None,
        model_provider="openai",
        sentence_transformer_model="all-MiniLM-L6-v2",
    )

    # Get OpenAI response
    client = OpenAI() # OPENAI_API_KEY should be present in environment variables
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "What is the capital of France?"}]
    )

    # Validate the response
    result = Aisert(content=response.choices[0].message.content, config=config) \
        .assert_contains(items=["Paris", "France"]) \
        .assert_tokens(40) \
        .assert_semantic_matches("France's capital") \
        .collect()
    
    print("Validation result:", result)
    return result

if __name__ == "__main__":
    assert_openai_response_with_api()
    print("Aisert validation completed successfully.")