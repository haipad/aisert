Examples
========

This section provides comprehensive examples demonstrating Aisert usage patterns from basic configuration to production deployment.

Configuration Examples
----------------------

Learn different ways to configure Aisert for various providers and use cases.

:download:`Download: 01_configuration_examples.py <../examples/01_configuration_examples.py>`

.. literalinclude:: ../examples/01_configuration_examples.py
   :language: python
   :caption: Configuration Options and Patterns
   :name: configuration-examples
   :linenos:

Key topics covered:

* Default configuration usage
* Constructor-based configuration  
* Global defaults management
* Provider-specific configurations
* Lightweight vs full-featured setups

Functions in this example:

* ``default_configuration()`` - Using built-in defaults
* ``constructor_configuration()`` - Custom configuration setup
* ``global_defaults_configuration()`` - Setting application-wide defaults
* ``provider_specific_configurations()`` - Provider-specific examples

Usage Patterns
--------------

Master direct validation and fluent interface patterns.

:download:`Download: 02_usage_patterns.py <../examples/02_usage_patterns.py>`

.. literalinclude:: ../examples/02_usage_patterns.py
   :language: python
   :caption: Direct Usage and Fluent Interface
   :name: usage-patterns
   :linenos:

Key topics covered:

* Direct validation (single validators)
* Fluent interface (chained validations)
* Strict vs non-strict modes
* Error handling patterns
* Exception hierarchy usage

Functions in this example:

* ``direct_validation()`` - Single validator usage
* ``fluent_interface()`` - Chaining multiple validations
* ``strict_vs_non_strict()`` - Error handling modes
* ``error_handling()`` - Exception management

Production Use Cases
--------------------

Real-world scenarios and pipeline integration examples.

:download:`Download: 03_production_use_cases.py <../examples/03_production_use_cases.py>`

.. literalinclude:: ../examples/03_production_use_cases.py
   :language: python
   :caption: Real-World Production Scenarios
   :name: production-use-cases
   :linenos:

Key topics covered:

* Content moderation pipelines
* API response validation
* CI/CD integration
* Batch processing optimization
* Quality monitoring with metrics

Functions in this example:

* ``content_moderation_pipeline()`` - User content filtering
* ``api_response_validation()`` - LLM response validation
* ``ci_cd_integration()`` - Automated testing integration
* ``batch_processing()`` - High-volume processing
* ``quality_monitoring()`` - Production metrics

Running Examples
----------------

To run these examples locally:

.. code-block:: bash

   # Install Aisert with optional dependencies
   pip install aisert[all]
   
   # Set environment variables (for API-based validation)
   export OPENAI_API_KEY="your-openai-key"
   export ANTHROPIC_API_KEY="your-anthropic-key"
   
   # Run examples in order
   python examples/01_configuration_examples.py
   python examples/02_usage_patterns.py
   python examples/03_production_use_cases.py

Prerequisites (for running examples)
------------------------------------

**Basic Installation:**

.. code-block:: bash

   pip install aisert

**Optional Dependencies:**

.. code-block:: bash

   # For semantic validation with sentence-transformers
   pip install aisert[sentence-transformers]
   
   # For HuggingFace models
   pip install aisert[huggingface]
   
   # For all features
   pip install aisert[all]

Custom Validators
-----------------

Aisert supports bringing your own token and semantic validators by extending the base classes.

Custom Token Validator
~~~~~~~~~~~~~~~~~~~~~~

Create custom token validators by extending ``TokenValidatorBase``:

.. code-block:: python

   from aisert.validators.token_validator.token_validator_base import TokenValidatorBase
   from aisert.validators.token_validator.token_validator_factory import TokenValidatorFactory
   from aisert.exception import TokenValidationError
   import threading

   class CustomTokenValidator(TokenValidatorBase):
       """Custom token validator example."""
       _instances = {}
       _lock = threading.RLock()

       def __init__(self, model_name: str):
           super().__init__(model_provider="custom")
           self.model_name = model_name

       @classmethod
       def get_instance(cls, token_model: str = None, **kwargs):
           with cls._lock:
               if token_model not in cls._instances:
                   cls._instances[token_model] = cls(token_model)
               return cls._instances[token_model]

       def count(self, text: str) -> int:
           """Implement your custom token counting logic."""
           # Example: simple word count
           return len(text.split())

   # Register the custom validator
   TokenValidatorFactory.register_token_validator("custom", CustomTokenValidator)

   # Usage
   config = AisertConfig(token_provider="custom", token_model="my-model")
   result = Aisert("Hello world", config).assert_tokens(max_tokens=5).collect()

Custom Semantic Validator
~~~~~~~~~~~~~~~~~~~~~~~~~

Create custom semantic validators by extending ``SemanticValidatorBase``:

.. code-block:: python

   from aisert.validators.semantic_validator.semantic_validator_base import SemanticValidatorBase
   from aisert.validators.semantic_validator.semantic_validator_factory import SemanticValidatorFactory
   from aisert.exception import SemanticValidationError
   from aisert.models.result import Result
   import threading

   class CustomSemanticValidator(SemanticValidatorBase):
       """Custom semantic validator example."""
       _instances = {}
       _lock = threading.RLock()

       def __init__(self, model_name: str = None):
           super().__init__()
           self.model_name = model_name or "custom-model"

       @classmethod
       def get_instance(cls, model_name: str = None, **kwargs):
           key = model_name or "default"
           with cls._lock:
               if key not in cls._instances:
                   cls._instances[key] = cls(model_name)
               return cls._instances[key]

       def validate(self, text1: str, text2: str, threshold: float = 0.8) -> Result:
           """Implement your custom semantic similarity logic."""
           if not (0 <= threshold <= 1):
               raise SemanticValidationError("Threshold must be between 0 and 1")

           # Example: simple keyword overlap similarity
           words1 = set(text1.lower().split())
           words2 = set(text2.lower().split())
           similarity = len(words1 & words2) / len(words1 | words2) if words1 | words2 else 0

           if similarity < threshold:
               raise SemanticValidationError(
                   f"Custom similarity score: {similarity:.3f} is less than threshold: {threshold}"
               )

           return Result(self.validator_name, True,
                        f"Custom similarity score: {similarity:.3f}, Threshold: {threshold}")

   # Register the custom validator
   SemanticValidatorFactory.register_semantic_validator("custom", CustomSemanticValidator)

   # Usage
   config = AisertConfig(semantic_provider="custom", semantic_model="my-model")
   result = Aisert("Hello world", config).assert_semantic_matches("Hi world", 0.5).collect()

Key Implementation Points
~~~~~~~~~~~~~~~~~~~~~~~~~

**Token Validators:**

* Extend ``TokenValidatorBase``
* Implement ``count(text: str) -> int`` method
* Use singleton pattern with thread-safe ``get_instance()``
* Register with ``TokenValidatorFactory.register_token_validator()``

**Semantic Validators:**

* Extend ``SemanticValidatorBase``
* Implement ``validate(text1: str, text2: str, threshold: float) -> Result`` method
* Use singleton pattern with thread-safe ``get_instance()``
* Register with ``SemanticValidatorFactory.register_semantic_validator()``

**Best Practices:**

* Use thread-safe singleton pattern for performance
* Handle errors gracefully with appropriate exceptions
* Validate input parameters (e.g., threshold range)
* Return descriptive error messages
* Cache expensive operations (models, connections)

Complete Custom Validator Example
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:download:`Download: custom_validators_example.py <../examples/custom_validators_example.py>`

.. code-block:: python

   # Complete working example
   from aisert import Aisert, AisertConfig
   from aisert.validators.token_validator.token_validator_base import TokenValidatorBase
   from aisert.validators.token_validator.token_validator_factory import TokenValidatorFactory
   from aisert.validators.semantic_validator.semantic_validator_base import SemanticValidatorBase
   from aisert.validators.semantic_validator.semantic_validator_factory import SemanticValidatorFactory
   from aisert.models.result import Result
   import threading

   # Custom implementations here...
   # (See full example in downloadable file)

   if __name__ == "__main__":
       # Test custom validators
       config = AisertConfig(
           token_provider="custom",
           token_model="word-counter",
           semantic_provider="custom",
           semantic_model="keyword-overlap"
       )
       
       result = (
           Aisert("Hello world from custom validators", config)
           .assert_tokens(max_tokens=10)
           .assert_semantic_matches("Hi world custom", threshold=0.3)
           .collect()
       )
       
       print(f"Custom validation result: {result.status}")
