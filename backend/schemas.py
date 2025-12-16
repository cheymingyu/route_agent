from pydantic import BaseModel
from typing import Optional


class IntentSchema(BaseModel):
    origin: Optional[str] = None
    destination: Optional[str] = None
    restaurant_type: Optional[str] = None
    walk_limit_min: Optional[int] = None
    