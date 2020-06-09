import math
import unittest
from enum import Enum

from fastapi import FastAPI
from pymongo import MongoClient


class Operation(str, Enum):
    add = 'add'
    sub = 'sub'
    div = 'div'
    mul = 'mul'
    exp = 'exp'
    sqr = 'sqr'


app = FastAPI()

client = MongoClient(
    'mongodb+srv://calco:calco@calculatoroperations-7lpdk.mongodb.net/CalculatorOperations?retryWrites=true&w=majority'
)
db = client.CalculatorOperations
atomic_ops = db.atomic_operations
long_ops = db.long_operations


@app.get('/')
def home():
    return {'api_name': 'Calculator', 'page': 'home'}


@app.get('/calc/{op}')
def calc(op: Operation, a: float, b: float = 1, send_to_db: bool = True):
    """
    Calculate the result of equation that consists of two (or one in case of sqr) operands and the operation sign
    between them (a op b). Example: a=1, b=2, op=add -> 1 + 2

    :param op: Operation to do with two operands
    :param a: First (left) operand
    :param b: Second (right) operand
    :param send_to_db: If True - result of calculation will be sent to the MongoDB
    :return: Dict with operands, op-sign and solution or with error message
    """
    output = {'operation': op.value, 'operands': [a, b]}

    if op == op.add:
        output['result'] = a + b
    if op == op.sub:
        output['result'] = a - b
    if op == op.div:
        output['result'] = a / b
    if op == op.mul:
        output['result'] = a * b
    if op == op.exp:
        output['result'] = a ** b
    if op == op.sqr:
        output['result'] = math.sqrt(a)

    if send_to_db:
        atomic_ops.insert_one(output)
        output.pop('_id')

    return output


@app.get('/compute')
def compute(equation: str, send_to_db: bool = True):
    """
    Compute the result of a given equation as a string like any other calculator.

    :param equation: String with math equation.
    :param send_to_db: If True - result of calculation will be sent to the MongoDB
    :return: Dict with equation and solution or with error message
    """
    try:
        output = {'equation': equation.replace(' ', ''), 'result': eval(equation)}
    except SyntaxError:
        return {'SyntaxError': 'Check the equation for some typos'}

    if send_to_db:
        long_ops.insert_one(output)
        output.pop('_id')

    return output


# test zone
class TestApp(unittest.TestCase):

    def test_calc(self):
        self.assertEqual(calc(Operation.add, 8, 2, False)['result'], 10, 'Should equal to 10')
        self.assertEqual(calc(Operation.sub, 8, 2, False)['result'], 6, 'Should equal to 6')
        self.assertEqual(calc(Operation.div, 8, 2, False)['result'], 4, 'Should equal to 4')
        self.assertEqual(calc(Operation.mul, 8, 2, False)['result'], 16, 'Should equal to 16')
        self.assertEqual(calc(Operation.exp, 8, 2, False)['result'], 64, 'Should equal to 64')
        self.assertEqual(calc(Operation.sqr, 9, 1, False)['result'], 3, 'Should equal to 3')

    def test_compute(self):
        self.assertEqual(compute(' 3 *5+ 40 /2-5** 2', False)['result'], 10, 'Should equal to 10')
