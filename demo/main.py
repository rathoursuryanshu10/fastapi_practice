from fastapi import FastAPI
demo = FastAPI()

@demo.get("/hello")
def hello():
    return {"message": "Hello, World!"}

@demo.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."}