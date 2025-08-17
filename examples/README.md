# Aisert Examples

This directory contains comprehensive examples showing how to use Aisert in different scenarios.

## 📁 Example Files

### 🚀 [basic_usage.py](basic_usage.py)
**Getting started examples** - Perfect for beginners
- Simple validation with default config
- Custom configuration setup
- Strict vs non-strict modes
- Schema validation with Pydantic
- Content moderation basics
- Error handling patterns

### 🌍 [real_world_examples.py](real_world_examples.py)
**Production use cases** - Real-world scenarios
- Content moderation pipeline (single validator)
- API response validation (multiple validators)
- Caching performance demo (10x+ speedup)
- Different tokenization models comparison
- Single vs multiple validator trade-offs

### 🏢 [production_patterns.py](production_patterns.py)
**Enterprise patterns** - Advanced production usage
- Testing framework integration (pytest)
- CI/CD pipeline validation
- A/B testing for LLM responses
- Enterprise configuration management
- Microservices integration patterns

### ⚡ [performance_benchmarks.py](performance_benchmarks.py)
**Performance optimization** - Speed and efficiency
- Model loading benchmarks (30s → 2s)
- Batch processing optimization
- Memory usage patterns
- Provider performance comparison
- Concurrent processing (4x speedup)

## 🎯 Quick Start

```bash
# Run basic examples
python examples/basic_usage.py

# See real-world use cases
python examples/real_world_examples.py

# Check performance optimizations
python examples/performance_benchmarks.py

# Explore enterprise patterns
python examples/production_patterns.py
```

## 💡 Key Concepts Demonstrated

### Performance Optimization
- **Model Caching**: 10x+ speedup on repeated use
- **Lightweight Models**: `all-MiniLM-L6-v2` loads in 2s vs 30s
- **Batch Processing**: Optimize for high-volume scenarios
- **Concurrent Processing**: 4x speedup with threading

### Validation Patterns
- **Single Validator**: Fast, focused checks (content moderation)
- **Multiple Validators**: Comprehensive validation (API responses)
- **Strict Mode**: Fail-fast with exceptions
- **Non-Strict Mode**: Collect all errors gracefully

### Real-World Applications
- Content moderation for user-generated content
- API response quality assurance
- Educational content verification
- Customer service response validation
- CI/CD pipeline integration

### Enterprise Features
- Environment-specific configurations
- Microservices integration
- Monitoring and alerting
- A/B testing frameworks
- Custom validation rules

## 🔧 Configuration Examples

### Lightweight (Fast Loading)
```python
config = AisertConfig(
    model_provider="openai",
    token_model="gpt-3.5-turbo",
    sentence_transformer_model="all-MiniLM-L6-v2"  # 2s loading
)
```

### Production (High Quality)
```python
config = AisertConfig(
    model_provider="openai",
    token_model="gpt-4",
    sentence_transformer_model="all-MiniLM-L12-v2"  # Better accuracy
)
```

### Multi-Provider
```python
# OpenAI
config_openai = AisertConfig("openai", "gpt-3.5-turbo")

# Anthropic
config_anthropic = AisertConfig("anthropic", "claude-3-haiku")
```

## 📊 Performance Guidelines

| Use Case | Recommended Pattern | Expected Performance |
|----------|-------------------|---------------------|
| Content Moderation | Single validator | <10ms per item |
| API Validation | Multiple validators | 50-100ms per item |
| Batch Processing | Cached models | 1000+ items/second |
| Real-time | Lightweight models | <50ms response |

## 🚨 Important Notes

- **First Run**: Semantic models take 2-30s to load initially
- **Caching**: Reuse config instances for 10x+ speedup
- **Memory**: Semantic models use 100-500MB RAM
- **API Keys**: Some providers require environment variables

## 🤝 Contributing

Found a useful pattern? Add it to the examples! Make sure to:
- Include clear docstrings
- Show performance characteristics
- Demonstrate real-world value
- Keep examples focused and minimal