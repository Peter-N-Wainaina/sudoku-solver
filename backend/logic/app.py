from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from http import HTTPStatus

from solver import SudokuSolver
from exceptions import UnsolvableBoard, InvalidBoard

app = FastAPI()
# CORS config to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #TODO: Update restriction for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BoardInput(BaseModel):
    board: List[List[int]]

@app.get("/")  # This defines the homepage route
async def root():
    return {"message": "Welcome to the Sudoku Solver API!"}


@app.post("/solve")
async def solve_board(input:BoardInput):
    board = input.board
    board = [[None if cell == 0 else cell for cell in row] for row in board]
    try:
        solver = SudokuSolver(board,(3,3))
        solution = solver.get_solution()
        solution= [[0 if cell == None else cell for cell in row] for row in solution]
        return {"solved_board": solution}
        
    except InvalidBoard as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except UnsolvableBoard as e:
        raise HTTPException(status_code=HTTPStatus.CONTINUEUNPROCESSABLE_ENTITY, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Internal server error")

