# Aisert Examples

This directory contains organized examples demonstrating Aisert usage patterns from basic configuration to production deployment.

## 📁 Example Organization

### 01_configuration_examples.py
**Configuration Options and Patterns**
- Default configuration usage
- Constructor-based configuration
- Global defaults management
- Provider-specific configurations
- Lightweight vs full-featured setups

### 02_usage_patterns.py
**Direct Usage and Fluent Interface**
- Direct validation (single validators)
- Fluent interface (chained validations)
- Strict vs non-strict modes
- Error handling patterns
- Exception hierarchy usage

### 03_production_use_cases.py
**Real-World Production Scenarios**
- Content moderation pipelines
- API response validation
- CI/CD integration
- Batch processing optimization
- Quality monitoring with metrics

## 🚀 Quick Start

```bash
# Run examples in order
python examples/01_configuration_examples.py
python examples/02_usage_patterns.py
python examples/03_production_use_cases.py
```

## 📋 Prerequisites

**Basic Installation:**
```bash
pip install aisert
```

**Optional Dependencies:**
```bash
# For semantic validation with sentence-transformers
pip install aisert[sentence-transformers]

# For HuggingFace models
pip install aisert[huggingface]

# For all features
pip install aisert[all]
```

**Environment Variables (for API-based validation):**
```bash
export OPENAI_API_KEY="your-openai-key"
export ANTHROPIC_API_KEY="your-anthropic-key"
```

## 🎯 Learning Path

1. **Start Here:** `01_configuration_examples.py`
   - Learn different ways to configure Aisert
   - Understand provider options
   - See expected results for each configuration

2. **Usage Patterns:** `02_usage_patterns.py`
   - Master direct validation and fluent interface
   - Learn error handling strategies
   - Understand strict vs non-strict modes

3. **Production Ready:** `03_production_use_cases.py`
   - Implement real-world scenarios
   - Integrate with existing systems
   - Monitor and optimize performance

## 💡 Key Features Demonstrated

- **Simple Configuration:** Constructor-based setup
- **Flexible Validation:** Chain multiple validators
- **Error Handling:** Graceful failure modes
- **Performance:** Optimized for production use
- **Integration:** CI/CD and monitoring patterns

## 📊 Expected Results

Each example includes expected results as comments:
```python
result = Aisert(content).assert_contains(["test"]).collect()
print(f"Status: {result.status}")  # Expected: True
```

This helps you verify that examples work correctly in your environment.