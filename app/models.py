"""Define the data clients/users must send when creating or (editing) a car"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field
# A category must match one of these strings exactly

Category = Literal[
    "Hatchback"
    "Sedan",
    "SUV",
    "Coupe",
]

class CarInput(BaseModel):
    """The content of a car, without an ID"""

    model_config = ConfigDict(
        #Remove surroundign whtitespace before checking string lengths
        str_strip_whitespace=True,
        #Reject unexpected fields   
        extra="forbid",
    )

    #POST and PUT validate the same six editable fields
    name: str = Field(min_length=2, max_length=50)
    category: Category
    manufacturer: str = Field(min_length=2, max_length=50)
    variant: str = Field(min_length=3, max_length=60)
    description: str = Field(min_length=20, max_length=500)
    tip: str = Field(min_length=5, max_length=200)
