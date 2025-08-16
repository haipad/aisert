import json
from typing import List
from openai import OpenAI
from pydantic import BaseModel

import logging
import os
import sys

logging.basicConfig(
    level=logging.DEBUG
)
logger = logging.getLogger("SchemaValidationExample")

from aisert import Aisert


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
                    "content": "Generate 2 JSON test data with the fields id, name, address(with street, city, country), age, email",
                },
            ],
            response_format={"type": "json_object"}
        )
        .choices[0]
        .message.content
    )
    result = (
        Aisert(content=json.loads(response).get("data"))
        .assert_schema(List[ResponseModel])
        .assert_tokens(150)
        .collect()
    )
    logger.info(f"Validation result: {str(result)}")


if __name__ == "__main__":
    assert_schema_and_token_size()
