from calcconfig import app
from math import log
import time

@app.task
def raiz(a):
    return a**0.5

@app.task
def log(a):
    return log(a, 10)

@app.task
def pot(a):
    return a**a
