from typing import List
from openai import OpenAI
from pydantic import BaseModel

import logging
import os
import sys

from sympy import false

# Add parent directory to path to import aisert
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
logger = logging.getLogger("SchemaValidationExample")

from aisert import Aisert, AisertConfig


# Response model containing id, name, address, age, and email
class ResponseModel(BaseModel):
    class Address(BaseModel):
        street: str
        city: str
        country: str

    id: int
    name: str
    address: Address
    age: int
    email: str


# Using Aisert to validate the schema and token_size
def assert_schema_and_token_size():
    client = OpenAI()
    response = (
        client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": "Generate 2 JSON test data with the fields id, name, address, age, email",
                },
            ],
        )
        .choices[0]
        .message.content
    )
    result = (
        Aisert(content=response)
        .assert_schema(List[ResponseModel])
        .assert_tokens(150)
        .collect()
    )
    logger.info(f"Validation result: {str(result)}")


if __name__ == "__main__":
    assert_schema_and_token_size()
