from typing import Annotated, List, Optional, TypedDict, Union
from pydantic import BaseModel, confloat

from api.db.schemas import User


class HealthCheck(BaseModel):
    status: str
    message: str


# -----------------

ConstrainedFloat = Annotated[float, confloat(ge=0, le=1)]


class ProbesDict(TypedDict, total=False):
    NEG: ConstrainedFloat
    NEU: ConstrainedFloat
    POS: ConstrainedFloat


class AnalyzerOutputModel(BaseModel):
    sentence: str
    context: Optional[str]
    probas: ProbesDict
    is_multilabel: bool
    output: Union[str, List[str]]


# -----------------


class UserAccessToken(BaseModel):
    user: User
    access_token: str
