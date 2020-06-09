import math
import unittest
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


# test zone
class TestApp(unittest.TestCase):

    def test_calc(self):
        self.assertEqual(calc(Operation.add, 8, 2)['result'], 10, 'Should equal to 10')
        self.assertEqual(calc(Operation.sub, 8, 2)['result'], 6, 'Should equal to 6')
        self.assertEqual(calc(Operation.div, 8, 2)['result'], 4, 'Should equal to 4')
        self.assertEqual(calc(Operation.mul, 8, 2)['result'], 16, 'Should equal to 16')
        self.assertEqual(calc(Operation.exp, 8, 2)['result'], 64, 'Should equal to 64')
        self.assertEqual(calc(Operation.sqr, 9)['result'], 3, 'Should equal to 3')

    def test_compute(self):
        self.assertEqual(compute(' 3 *5+ 40 /2-5** 2')['result'], 10, 'Should equal to 10')
