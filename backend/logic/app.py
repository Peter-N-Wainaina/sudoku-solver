from fastapi import FastAPI
from solver import SudokuSolver

app = FastAPI()


@app.get("/")  # This defines the homepage route
async def root():
    return {"message": "Welcome to the Sudoku Solver API!"}
