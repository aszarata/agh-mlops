import torch
from transformers import AutoTokenizer, AutoModel
from fastapi import FastAPI
import onnxruntime as ort
import time
import numpy as np

from api.prediction import PredictRequest, PredictResponse

app = FastAPI()

optimized_onnx_model_path = "models/model_optimized.onnx"

tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/multi-qa-mpnet-base-cos-v1")

options_load_optimized = ort.SessionOptions()
options_load_optimized.graph_optimization_level = ort.GraphOptimizationLevel.ORT_DISABLE_ALL
ort_session_offline = ort.InferenceSession(
    optimized_onnx_model_path,
    sess_options=options_load_optimized,
    providers=["CPUExecutionProvider"]
)



@app.get("/")
def root():
    return {"message": "Torch App"}


@app.post("/inference")
def inference(request: PredictRequest):
    start_time = time.time()
    input_ids = tokenizer(request.text, truncation=True, padding="max_length", return_tensors="np")
    inputs_onnx_dict = {
        "input_ids": input_ids["input_ids"].astype(np.int64),
        "attention_mask": input_ids["attention_mask"].astype(np.int64),
    }
    
    _ = ort_session_offline.run(None, inputs_onnx_dict)
    inf_time = time.time() - start_time
    return PredictResponse(inference_time=inf_time)