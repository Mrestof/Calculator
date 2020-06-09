import math

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def home():
    return {'api_name': 'Calculator', 'page': 'home'}


@app.get('/add')
def add(a: float, b: float):
    return {'result': a + b}


@app.get('/sub')
def sub(a: float, b: float):
    return {'result': a - b}


@app.get('/div')
def div(a: float, b: float):
    return {'result': a / b}


@app.get('/mul')
def mul(a: float, b: float):
    return {'result': a * b}


@app.get('/exp')
def exp(a: float, b: float):
    return {'result': a ** b}


@app.get('/sqr')
def sqr(a: float):
    return {'result': math.sqrt(a)}
