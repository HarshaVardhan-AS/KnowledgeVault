from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class DocumentBase(BaseModel):
    title : str = Field(max_length = 50)
    raw_text : str = Field(min_length=1)

class DocumentCreate(DocumentBase):
    pass

class DocumentResponse(DocumentBase):
    model_config = ConfigDict(
        from_attributes=True
    )
    id : int
    created_at : datetime
    source_type : str

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    query : str
    chunks : list[str]
    answer : str
