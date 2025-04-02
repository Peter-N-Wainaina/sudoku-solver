"use client";

import { useState } from "react";
import Board from "../components/board";

const SAMPLE_BOARD = [
  [5, 3, 3, 0, 7, 0, 0, 0, 0],
  [6, 0, 0, 1, 9, 5, 0, 0, 0],
  [0, 9, 8, 0, 0, 0, 0, 6, 0],
  [8, 0, 0, 0, 6, 0, 0, 0, 3],
  [4, 0, 0, 8, 0, 3, 0, 0, 1],
  [7, 0, 0, 0, 2, 0, 0, 0, 6],
  [0, 6, 0, 0, 0, 0, 2, 8, 0],
  [0, 0, 0, 4, 1, 9, 0, 0, 5],
  [0, 0, 0, 0, 8, 0, 0, 7, 9],
];

const EMPTY_BOARD = Array.from({length:9},  () => Array(9).fill(0))

export default function Home() {
  const [board, setBoard] = useState(SAMPLE_BOARD);

  async function handleSolve(){
    try{

      const response = await fetch("http://localhost:8000/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ board }),
      });
      
      if (!response.ok){
        const errorData = await response.json(); // get the error message
        let message = errorData.detail || "Unknown error";
        if (response.status === 400) {
          throw new Error("Invalid board: " + message);
        } else if (response.status === 422) {
          throw new Error("Unsolvable board: " + message);
        } else if (response.status === 500) {
          throw new Error("Server error: " + message);
        } else {
          throw new Error("Unexpected error: " + message);
        }
      }

      const data =  await response.json();
      const solvedBoard = data.solved_board
      setBoard(solvedBoard)

    }
    catch(err: any){
      console.log("Solve error: ",err)
      alert(err.message)
    }

    };
    
  return (
      <main>
        <h1>Welcome to Sudoku Solver</h1>
        <Board board={board}/>
        <button onClick={handleSolve}>Solve</button>
        <button onClick={() => setBoard(EMPTY_BOARD)}>Reset</button>
      </main>
  );
}
