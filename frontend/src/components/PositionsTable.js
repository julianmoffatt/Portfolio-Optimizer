import './PositionsTable.css';

const fmt = (val, decimals = 2) => val != null ? parseFloat(val).toFixed(decimals) : '—';
const fmtPct = (val) => val != null ? (parseFloat(val) * 100).toFixed(1) + '%' : '—';

function PositionsTable({ positions, onRemove }) {
  if (positions.length === 0) {
    return <p className="empty-msg">No positions yet. Add a ticker above.</p>;
  }

  return (
    <table className="positions-table">
      <thead>
        <tr>
          <th>TICKER</th>
          <th>NAME</th>
          <th>SECTOR</th>
          <th className="right">WEIGHT</th>
          <th className="right group-start">PE (TTM)</th>
          <th className="right">PE (FWD)</th>
          <th className="right">EV/EBITDA</th>
          <th className="right">P/S</th>
          <th className="right group-start">ROE</th>
          <th className="right">ROA</th>
          <th className="right">MARGIN</th>
          <th className="right">OP. MARGIN</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        {positions.map(pos => {
          const f = pos.fundamentals;
          return (
            <tr key={pos.id}>
              <td className="ticker">{pos.asset.ticker}</td>
              <td className="name">{pos.asset.name}</td>
              <td className="muted">{pos.asset.sector}</td>
              <td className="right">{pos.weight}%</td>
              <td className="right group-start">{fmt(f?.pe_trailing)}</td>
              <td className="right">{fmt(f?.pe_forward)}</td>
              <td className="right">{fmt(f?.ev_to_ebitda)}</td>
              <td className="right">{fmt(f?.price_to_sales)}</td>
              <td className="right group-start">{fmtPct(f?.roe)}</td>
              <td className="right">{fmtPct(f?.roa)}</td>
              <td className="right">{fmtPct(f?.profit_margin)}</td>
              <td className="right">{fmtPct(f?.operating_margin)}</td>
              <td>
                <button className="remove-btn" onClick={() => onRemove(pos.asset.id)}>✕</button>
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default PositionsTable;
