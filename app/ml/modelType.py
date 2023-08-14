from pydantic import BaseModel
from typing import Dict

class ModelType(BaseModel):
    data: Dict[str, float | str]
