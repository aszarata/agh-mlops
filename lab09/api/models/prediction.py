from pydantic import BaseModel, field_validator


class PredictRequest(BaseModel):
    text: str

    @field_validator("text")
    def text_cannot_be_empty(cls, v):
        if isinstance(v, str) and v.strip() == "":
            raise ValueError('Empty string is not valid')
        return v


class PredictResponse(BaseModel):
    prediction: str
