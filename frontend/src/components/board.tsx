import Cell from './Cell';

type BoardProps = {
  board: number[][];
};

export default function Board({ board }: BoardProps) {
  const boardStyle: React.CSSProperties = {
    display: 'grid',
    gridTemplateColumns: 'repeat(9, 40px)',
    gridTemplateRows: 'repeat(9, 40px)',
    gap: '0',
    border: '2px solid black',
    marginTop: '1rem',
    width: 'fit-content',
  };

  return (
    <div style={boardStyle}>
      {board.map((row, rowIndex) =>
        row.map((value, colIndex) => {
          const isBoldTop = rowIndex % 3 === 0;
          const isBoldLeft = colIndex % 3 === 0;
          const isBoldBottom = rowIndex === 8;
          const isBoldRight = colIndex === 8;

          return (
            <Cell
              key={`${rowIndex}-${colIndex}`}
              value={value}
              isBoldTop={isBoldTop}
              isBoldLeft={isBoldLeft}
              isBoldRight={isBoldRight}
              isBoldBottom={isBoldBottom}
            />
          );
        })
      )}
    </div>
  );
}
