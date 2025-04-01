export const metadata = {
    title: 'Sudoku Solver',
    description: 'A smart way to solve Sudoku puzzles',
  };
  
  export default function RootLayout({ children }: { children: React.ReactNode }) {
    return (
      <html lang="en">
        <body>{children}</body>
      </html>
    );
  }
  