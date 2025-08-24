API Reference
=============

.. currentmodule:: aisert

Main Validation Class
---------------------

.. autoclass:: Aisert
   :members:

Configuration
-------------

.. autoclass:: AisertConfig
   :members:

Validation Report
-----------------

.. autoclass:: aisert.models.report.AisertReport
   :members:

Exceptions
----------

.. currentmodule:: aisert.exception

.. autoexception:: AisertError

.. autoexception:: SchemaValidationError

.. autoexception:: ContainsValidationError

.. autoexception:: TokenValidationError

.. autoexception:: SemanticValidationError

Custom Validator Base Classes
-----------------------------

Base classes for creating custom validators.

Token Validator Base
~~~~~~~~~~~~~~~~~~~~

.. autoclass:: aisert.validators.token_validator.token_validator_base.TokenValidatorBase
   :members:

Semantic Validator Base
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: aisert.validators.semantic_validator.semantic_validator_base.SemanticValidatorBase
   :members:

Validator Factories
-------------------

Factories for registering and managing custom validators.

Token Validator Factory
~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: aisert.validators.token_validator.token_validator_factory.TokenValidatorFactory
   :members:

Semantic Validator Factory
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoclass:: aisert.validators.semantic_validator.semantic_validator_factory.SemanticValidatorFactory
   :members:
