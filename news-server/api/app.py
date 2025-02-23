import celery.states as states
from fastapi import FastAPI,Query
from fastapi.responses import HTMLResponse
from worker import celery
from pymongo import MongoClient
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os

client = MongoClient(os.environ.get('MONGO_URI',"mongodb://mongo:27017/news_db"))
db = client["news_db"]
news_collection=db["news"]
app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173", 
    "*"  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"], 
)

@app.get("/add/{param1}/{param2}", response_class=JSONResponse)
async def add(param1: int, param2: int) -> dict:
    task = celery.send_task('tasks.add', args=[param1, param2], kwargs={})
    response = {
        "task_id": task.id,
        "status_url": app.url_path_for("check_task", task_id=task.id),
        "collections": db.list_collection_names(),
    }
    print(response)
    return response  


@app.get("/check/{task_id}", response_class=HTMLResponse)
async def check_task(task_id: str) -> str:
    res = celery.AsyncResult(task_id)
    if res.state == states.PENDING:
        return res.state
    else:
        return str(res.result)
    
@app.get("/fetch_news", response_class=HTMLResponse)
async def fetch()->str:
    task=celery.send_task('tasks.fetch_news')
    response = f"<a href='{app.url_path_for('check_task', task_id=task.id)}'>check status of {task.id} </a>"
    return response


@app.get("/news", response_class=JSONResponse)
async def get_news(limit: int = Query(10, ge=1, le=100)):
    
    latest_news = list(news_collection.find({}, {"_id": 0})
                       .sort("published_at", -1)
                       .limit(limit))
    
    return {"news": latest_news}


@app.get("/health_check")
async def health_check():
    return {"Status": "Ok"}
