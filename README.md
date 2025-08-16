# Aisert 🚀

Validate AI responses with confidence! ✨  
Aisert provides a fluent, chainable API for comprehensive AI output validation.  
From token counts to semantic similarity - ensure your AI behaves exactly as expected! 🎯

## Who Is This For? 👥

**AI/ML Engineers** - Just like you use `assert` statements in unit tests, use Aisert to validate LLM outputs in production  
**QA Engineers** - Automated testing for AI responses, similar to how Selenium tests web UIs  
**DevOps Teams** - Monitor AI model performance and catch regressions, like APM tools for traditional apps  
**Product Teams** - Ensure AI features meet quality standards before reaching users

## Features

- **Fluent Interface**: Chain multiple validations with a beautiful, readable API
- **Multiple Validators**: Schema, content, token count, and semantic similarity validation
- **Flexible Modes**: Strict mode (raises exceptions) or non-strict mode (collects results)
- **Thread-Safe**: Production-ready with proper concurrency handling and model caching
- **Multi-Provider Support**: OpenAI, Anthropic, HuggingFace, and Google token counting
- **Extensible**: Custom token validators via TokenValidatorBase inheritance

## Installation

```bash
pip install aisert
```

## Quick Start

```python
from aisert import Aisert, AisertConfig

# Configure for your AI model
config = AisertConfig(
    token_model="gpt-3.5-turbo",
    model_provider="openai"
)

# Validate AI response with fluent interface
result = (
    Aisert(content="Paris is the capital of France.", config=config)
    .assert_contains(["Paris", "France"])
    .assert_tokens(max_tokens=50)
    .assert_semantic_matches("France's capital", threshold=0.8)
    .collect()
)

print(f"Validation passed: {result.status}")
print(f"Details: {result.rules}")
```

## Validation Types

### Content Validation
```python
# Check if response contains specific items
Aisert(content).assert_contains(["keyword1", "keyword2"])

# Check if response doesn't contain items
Aisert(content).assert_not_contains(["spam", "inappropriate"])
```

### Token Count Validation
```python
# Ensure response is within token limits
Aisert(content, config).assert_tokens(max_tokens=100)
```

### Schema Validation
```python
# Validate with Pydantic model
from pydantic import BaseModel

class UserModel(BaseModel):
    name: str
    age: int

Aisert(json_content).assert_schema(UserModel)
```

### Semantic Similarity
```python
# Check semantic similarity to expected content
Aisert(content).assert_semantic_matches(
    expected="Information about artificial intelligence",
    threshold=0.75
)
```

## Validation Modes

### Strict Mode (Default)
Raises exceptions immediately when validation fails:

```python
try:
    Aisert(content).assert_contains(["required_term"])
except AisertError as e:
    print(f"Validation failed: {e}")
```

### Non-Strict Mode
Collects all validation results without raising exceptions:

```python
result = (
    Aisert(content)
    .assert_contains(["term1"], strict=False)
    .assert_tokens(100, strict=False)
    .collect()
)

if not result.status:
    print("Some validations failed:", result.rules)
```

## Configuration

```python
from aisert import AisertConfig

config = AisertConfig(
    token_model="gpt-4",           # Model for token counting
    model_provider="openai",       # Provider: "openai", "anthropic", "huggingface", "google"
    token_encoding=None,           # Custom encoding (OpenAI only)
    sentence_transformer_model="all-MiniLM-L6-v2"  # Semantic similarity model
)
```

## Real-World Examples

### API Response Validation
```python
def validate_chatbot_response(response_text):
    return (
        Aisert(response_text, config)
        .assert_not_contains(["inappropriate", "harmful"])
        .assert_tokens(max_tokens=500)
        .assert_semantic_matches("helpful customer service", 0.7)
        .collect()
    )
```

### Content Moderation
```python
def moderate_content(user_content):
    moderation_result = (
        Aisert(user_content)
        .assert_not_contains(["spam", "offensive"], strict=False)
        .assert_tokens(max_tokens=1000, strict=False)
        .collect()
    )
    
    return moderation_result.status
```

### Batch Processing
```python
def validate_multiple_responses(responses):
    results = []
    for response in responses:
        result = (
            Aisert(response, config)
            .assert_contains(["required_info"], strict=False)
            .assert_tokens(200, strict=False)
            .collect()
        )
        results.append(result)
    return results
```

## Exception Handling

Aisert provides specific exceptions for different validation types:

```python
from aisert import AisertError
from aisert.exception import (
    SchemaValidationError,    # Schema validation failures
    ContainsValidationError,  # Content validation failures
    TokenValidationError,     # Token count validation failures
    SemanticValidationError   # Semantic similarity failures
)

try:
    Aisert(content).assert_schema(UserModel)
except SchemaValidationError as e:
    print(f"Schema validation failed: {e}")
except AisertError as e:
    print(f"General validation error: {e}")
```

## Important Notes 📝

- **First Model Load**: Initial semantic model loading takes ~30 seconds ⏳
- **Custom Token Validators**: Extend `TokenValidatorBase` for custom providers 🔧
- **Performance**: Models are cached after first load for faster subsequent validations ⚡
- **Thread Safety**: All validators use singleton pattern with proper locking 🔒
- **Default Config**: Uses OpenAI gpt-3.5-turbo and all-MiniLM-L6-v2 by default ⚙️

## Current Limitations ⚠️

- **Schema Validation**: Only supports Pydantic models and TypeAdapter, not raw JSON schemas
- **Semantic Models**: Limited to sentence-transformers compatible models

## Supported Providers 🌐

- **OpenAI**: tiktoken-based encoding with model-specific tokenizers
- **Anthropic**: Native anthropic client token counting
- **HuggingFace**: AutoTokenizer from transformers library
- **Google**: genai client integration (experimental)
- **Custom**: Extend TokenValidatorBase for additional providers

## Requirements

- Python >= 3.9
- Dependencies: jsonschema, sentence-transformers, tiktoken, transformers, anthropic, pydantic, torch

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Links

- [Homepage](https://github.com/haipad/aisert)
- [Issues](https://github.com/haipad/aisert/issues)