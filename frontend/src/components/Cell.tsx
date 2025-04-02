type CellProps = {
    value: number;
    isBoldTop: boolean;
    isBoldLeft: boolean;
    isBoldRight: boolean;
    isBoldBottom: boolean;
  };
  
  export default function Cell({
    value,
    isBoldTop,
    isBoldLeft,
    isBoldRight,
    isBoldBottom,
  }: CellProps) {
    const style: React.CSSProperties = {
      width: '40px',
      height: '40px',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: '18px',
      borderTop: isBoldTop ? '2px solid black' : '1px solid #ccc',
      borderLeft: isBoldLeft ? '2px solid black' : '1px solid #ccc',
      borderRight: isBoldRight ? '2px solid black' : '',
      borderBottom: isBoldBottom ? '2px solid black' : '',
    };
  
    return <div style={style}>{value !== 0 ? value : ''}</div>;
  }
  