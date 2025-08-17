# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Alpha Release]

## [0.1.1] - 2024-12-19

### Added
- Initial alpha release of Aisert
- Fluent API for chaining AI response validations
- Content validation (contains/not_contains)
- Token count validation with multi-provider support (OpenAI, Anthropic, HuggingFace, Google)
- Schema validation using Pydantic models
- Semantic similarity validation using sentence transformers
- Strict and non-strict validation modes
- Thread-safe model caching for performance
- Comprehensive examples and documentation
- Performance benchmarks and optimization guides
- Support for Python 3.9+

### Supported Providers
- OpenAI (tiktoken-based encoding)
- Anthropic (native client)
- HuggingFace (AutoTokenizer)
- Google (genai client - experimental)

### Performance Features
- Model caching with 10x+ speedup on repeated use
- Lightweight model options for faster loading
- Selective validation patterns for optimal performance
- Concurrent processing support

[Unreleased]: https://github.com/haipad/aisert/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/haipad/aisert/releases/tag/v0.1.0
