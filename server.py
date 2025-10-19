from fastapi import FastAPI, Query
from .queue.connection import queue
from .queue.worker import process_query


app = FastAPI()

@app.get("/")
def health():
    return {"status": "Server is up and running"}

@app.post("/chat")
def chat_process(
    query : str = Query(..., description="The input query for the chat process" )
):
    #query ko queue me daal dena hai
    # user ko boldo job received 
    job = queue.enqueue(process_query, query) # job is the enqueued task containing the query
    return {"message": "Job received", "job_id": job.id}
