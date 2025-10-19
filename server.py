from fastapi import FastAPI, Query
from .queue.connection import queue
from .queue.worker import process_query


app = FastAPI()


@app.get("/")
def health():
    return {"status": "Server is up and running"}


@app.post("/chat")
def chat_process(
    query: str = Query(..., description="The input query for the chat process")
):
    # job is the enqueued task containing the query
    job = queue.enqueue(process_query, query)
    return {"message": "Job received", "job_id": job.id}
