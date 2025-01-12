from typing import Union
from uuid import UUID

from pydantic import BaseModel


class ExpirementResult(BaseModel):
    sample_name: str
    result: Union[float, None]
    experiment_id: UUID
    experiment_type: str
