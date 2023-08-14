from pydantic import BaseModel
from typing import Dict, List, Optional, Hashable, Any

class DataSchema(BaseModel):
    data: Dict[str, float | str]
    cached: Optional[bool]

class PredictSchema(BaseModel):
    prediction: List[Dict[Hashable, Any]]

class ErrorSchema(BaseModel):
    error_type: str
    error_msg: str
    traceback: str

class NamesSchema(BaseModel):
    names: List[str]