import math
from enum import Enum

from fastapi import FastAPI


class Operation(str, Enum):
    add = 'add'
    sub = 'sub'
    div = 'div'
    mul = 'mul'
    exp = 'exp'
    sqr = 'sqr'


app = FastAPI()


@app.get('/')
def home():
    return {'api_name': 'Calculator', 'page': 'home'}


@app.get('/calc/{op}')
def calc(op: Operation, a: float, b: float = 1):
    if op == op.add:
        return {'result': a + b}
    if op == op.sub:
        return {'result': a - b}
    if op == op.div:
        return {'result': a / b}
    if op == op.mul:
        return {'result': a * b}
    if op == op.exp:
        return {'result': a ** b}
    return {'result': math.sqrt(a)}


@app.get('/compute')
def compute(equation: str):
    return {'result': eval(equation)}
