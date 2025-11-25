import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI
import time

from api.prediction import PredictRequest, PredictResponse

app = FastAPI()

tokenizer = AutoTokenizer.from_pretrained("models/torch_app/tokenizer", local_files_only=True)
model = AutoModel.from_pretrained("models/torch_app/model", local_files_only=True)
model = torch.compile(model)

device = 'cpu'
model.to(device).eval()


@app.get("/")
def root():
    return {"message": "Torch App"}


@app.post("/inference")
def inference(request: PredictRequest):
    start_time = time.time()
    input_ids = tokenizer(request.text, truncation=True, padding="max_length", return_tensors="pt")
    with torch.inference_mode():
        _ = model(**input_ids)

    inf_time = time.time() - start_time
    return PredictResponse(inference_time=inf_time)