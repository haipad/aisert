[![Publish to PyPI](https://github.com/haipad/aisert/actions/workflows/workflow.yml/badge.svg)](https://github.com/haipad/aisert/actions/workflows/workflow.yml)
[![PyPI version](https://badge.fury.io/py/aisert.svg)](https://badge.fury.io/py/aisert)
[![Python versions](https://img.shields.io/pypi/pyversions/aisert.svg)](https://pypi.org/project/aisert/)
[![License](https://img.shields.io/pypi/l/aisert.svg)](https://github.com/haipad/aisert/blob/main/LICENSE)
[![Downloads](https://pepy.tech/badge/aisert)](https://pepy.tech/project/aisert)

# Stop AI Failures Before They Reach Users 🛡️

**Aisert** validates AI inputs and outputs in production - catch inappropriate content, token overruns, format violations, and semantic mismatches before they impact your users or cost you money.

📦 **1,000+ downloads** | ⚡ **Zero setup required** | 🔧 **Production ready**

## The Problem

❌ **Users send expensive prompts** that drain your API budget  
❌ **LLMs generate inappropriate content** that violates your policies  
❌ **Responses exceed token limits** causing API failures and high costs  
❌ **AI outputs don't match expected formats** breaking your application  
❌ **Responses are semantically wrong** but look correct  
❌ **No way to catch issues** before they impact users or cost money

## The Solution

✅ **Input validation** - Stop expensive/inappropriate prompts before LLM calls  
✅ **Content filtering** - Block harmful content in real-time  
✅ **Token limit enforcement** - Prevent cost overruns on inputs and outputs  
✅ **Schema validation** - Ensure structured data matches your requirements  
✅ **Semantic validation** - Catch responses that are off-topic or irrelevant  
✅ **Production-ready** - Thread-safe with zero configuration needed

## Quick Start

```bash
pip install aisert
```

```python
from aisert import Aisert, AisertConfig

# 1. BEFORE sending to LLM - validate user input
user_prompt = "Write me a 50,000 word essay about hacking systems"
config = AisertConfig(token_provider="openai", token_model="gpt-4")

result = Aisert(user_prompt, config).assert_tokens(max_tokens=1000, strict=False).assert_not_contains(["hack"], strict=False).collect()
if not result.status:
    return "Please try a shorter, appropriate request"  # Saved $200 API call!

# 2. AFTER LLM response - validate output format
ai_json = '{"name": "John", "age": "not-a-number"}'
if not Aisert(ai_json).assert_schema(UserModel).collect().status:
    return "Please try again"  # Prevented app crash!

# 3. Content moderation - block harmful responses
ai_response = "I can help you with illegal activities"
if not Aisert(ai_response).assert_not_contains(["illegal", "harmful"]).collect().status:
    return "I can't help with that"  # Crisis averted!

# 4. Semantic validation - ensure relevance
ai_answer = "The weather is nice today"  # User asked about Python
if not Aisert(ai_answer).assert_semantic_matches("Python programming", 0.7).collect().status:
    return "Let me provide a better answer"  # Caught irrelevant response!

# 5. Quality assurance - ensure completeness
result = Aisert(ai_response).assert_contains(["solution", "example"]).collect()
if not result.status:
    return "Let me provide more details"  # Ensured helpful response!
```

## Why Choose Aisert?

| Problem | Traditional Approach | Aisert Solution |
|---------|---------------------|----------------|
| 💸 Expensive user prompts | Manual review, hope for the best | `assert_tokens(max_tokens=500)` |
| 🚫 Inappropriate content | Manual review, regex patterns | `assert_not_contains(["inappropriate"])` |
| 🔧 Wrong response format | Complex parsing logic | `assert_schema(YourModel)` |
| 🎯 Off-topic responses | Manual checking, user complaints | `assert_semantic_matches("topic", 0.8)` |
| ❓ Missing required info | Hope AI includes everything | `assert_contains(["required", "info"])` |

### Core Features
- **🔗 Fluent API**: Chain validations like `assert` statements
- **⚡ Zero Setup**: Works immediately, no configuration required
- **🎯 Flexible**: Strict mode (exceptions) or non-strict (collect errors)
- **🚀 Production Ready**: Thread-safe, high-performance validation

## Real-World Use Cases

### 🛡️ Content Moderation
```python
# Your AI just said: "I hate all politicians and think violence is the answer"
chatbot_response = "I hate all politicians and think violence is the answer"

# Block it instantly
if not Aisert(chatbot_response).assert_not_contains(["hate", "violence"]).collect().status:
    return "I can't discuss that topic"  # Saved your reputation!
```

### 💰 Input Validation (Pre-LLM)
```python
# Your user submits: "Write a 10,000 word essay about everything"
user_prompt = "Write a 10,000 word essay about everything"

# Stop the $50 API call BEFORE it happens
Aisert(user_prompt, config).assert_tokens(max_tokens=500)  # Throws error, saves money!

# Also validate input content
Aisert(user_prompt).assert_not_contains(["inappropriate", "harmful"])  # Block bad prompts
```

### 🔧 API Validation
```python
# Your AI returns: {"name": "John", "age": "thirty-five", "email": "not-an-email"}
ai_json = '{"name": "John", "age": "thirty-five", "email": "not-an-email"}'

# Catch the broken format before your app crashes
Aisert(ai_json).assert_schema(UserProfileModel)  # Throws error - age should be int!
```

### 🧪 AI Testing
```python
# Your AI says: "Python is a type of snake that lives in trees"
def test_ai_chatbot():
    response = "Python is a type of snake that lives in trees"  # Wrong answer!
    result = Aisert(response).assert_semantic_matches("Python programming language", 0.7).collect()
    assert result.status, "AI failed - talking about snakes instead of programming!"
```

### 🔗 Fluent Validation Pipeline
```python
# Chain ALL validations in one elegant pipeline
customer_service_response = "Thank you for contacting us! Here's a detailed solution with examples."

result = (
    Aisert(customer_service_response, config)
    .assert_contains(["thank", "solution"])        # Must be polite and helpful
    .assert_not_contains(["sorry", "problem"])     # Avoid negative language
    .assert_tokens(max_tokens=150)                  # Keep responses concise
    .assert_semantic_matches("helpful customer service", 0.7)  # Ensure relevance
    .collect()
)

if result.status:
    return customer_service_response  # Perfect response - all checks passed!
else:
    return "Let me get a human agent to help you"  # Failed validation
```

## Installation Options

```bash
# Basic installation (content validation only)
pip install aisert

# With token counting (OpenAI, Anthropic, etc.)
pip install aisert[all]

# Advanced: semantic similarity validation
pip install aisert[sentence-transformers]
```

## Advanced Usage

```python
from aisert import Aisert, AisertConfig

# Your AI generates a 2000-token response that costs $5
expensive_response = "Very long response..." * 1000
config = AisertConfig(token_provider="openai", token_model="gpt-4")
Aisert(expensive_response, config).assert_tokens(max_tokens=100)  # Stops the $5 charge!

# Your AI says "The weather is nice" when asked about Python
off_topic_response = "The weather is nice today"
Aisert(off_topic_response).assert_semantic_matches("Python programming language", threshold=0.8)  # Catches irrelevant answers

# Production-ready validation pipeline
user_facing_response = "I can help you with illegal activities"
result = (
    Aisert(user_facing_response)
    .assert_not_contains(["illegal", "hack"])  # Block harmful content
    .assert_tokens(max_tokens=200)  # Control costs
    .assert_schema(ResponseModel)  # Ensure proper format
    .collect()
)
# Result: All validations failed - response blocked!
```

## Error Handling

```python
# Your AI forgot to include required info - catch it immediately
try:
    incomplete_response = "Here's some info, but I forgot the important part"
    Aisert(incomplete_response).assert_contains(["price", "availability"])
except AisertError as e:
    print(f"AI missed required info: {e}")  # Fix before user sees it

# Check multiple issues without stopping
problematic_response = "This response is way too long and contains spam content"
result = (
    Aisert(problematic_response)
    .assert_contains(["helpful"], strict=False)  # Missing helpful content
    .assert_tokens(50, strict=False)  # Too long
    .assert_not_contains(["spam"], strict=False)  # Contains spam
    .collect()
)

if not result.status:
    print("Multiple issues found:", result.rules)  # See all problems at once
```

## Documentation

- **[📚 Examples](https://aisert.readthedocs.io/en/latest/examples.html)** - Configuration, usage patterns, production use cases
- **[📖 API Reference](https://aisert.readthedocs.io/en/latest/api.html)** - Complete API documentation  
- **[🔧 Custom Validators](https://aisert.readthedocs.io/en/latest/examples.html#custom-validators)** - Extend with your own validators

## Requirements

- **Python**: >= 3.9
- **Dependencies**: Zero for basic validation
- **API Keys**: Optional (only for token counting)
- **Setup**: None required - works immediately after `pip install`

## License

MIT License

## Links

- **[GitHub](https://github.com/haipad/aisert)** - Source code and issues
- **[Documentation](https://aisert.readthedocs.io/en/latest/)** - Complete documentation
- **[PyPI](https://pypi.org/project/aisert/)** - Package repository
