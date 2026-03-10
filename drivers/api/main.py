from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class TriageRequest(BaseModel):
    policy_number: str


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/triage")
def run_triage(req: TriageRequest):
    return {"status": "pending_graph_implementation", "policy_number": req.policy_number}
