import logging
import sys
import time
import os

# Add parent directory to path to import aisert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aisert import Aisert, AIsertConfig

logger=logging.getLogger("BasicUsageExample")

def assert_openai_mcok_response():
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
    )
    
    # Validate the response
    result = Aisert(content=mock_response, config=config) \
        .assert_contains(items=["Paris", "France"], strict=False) \
        .assert_tokens(40, strict=False) \
        .assert_semantic_matches("France's capital", 0.75, strict=False) \
        .collect()
    
    print("Validation result:", str(result))
    return result


def assert_openai_response():
    """
    Example of how to use Aisert to validate a LLM response.
    """
    from openai import OpenAI

    logger.info("Start of LLM request")
    # Get OpenAI response
    client = OpenAI() # OPENAI_API_KEY should be present as environment variable
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "About France in 50 words"}]
    )
    logger.info("End of LLM request")

    # AIsert validation
    logger.info("Start of Aisert validation")
    # Configure Aisert
    config = AIsertConfig(
        token_model="gpt-3.5-turbo",
        token_encoding=None,
        model_provider="openai",
        sentence_transformer_model="paraphrase-MiniLM-L3-v2",
    )
    result = Aisert(content=response.choices[0].message.content, config=config) \
        .assert_contains(items=["Paris", "France"], strict=False) \
        .assert_tokens(40, strict=False) \
        .assert_semantic_matches("France's capital", 0.75, strict=False) \
        .collect()
    
    logger.info("Validation result:", str(result))
    return result

if __name__ == "__main__":
    start_time = time.time()
    assert_openai_mcok_response()
    end_time = time.time()
    print(f"Execution time: {end_time - start_time} seconds")