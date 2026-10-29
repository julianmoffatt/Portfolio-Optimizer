import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { getPerformance } from '../services/api';
import './EquityChart.css';

const PERIODS = ['1M', '6M', '1Y', '3Y', '5Y'];

const COLORS = [
  '#c9a84c', '#4caf8c', '#4c8fcb', '#cb4c7a',
  '#cb8f4c', '#7a4ccb', '#4ccb8f', '#cb4c4c',
];

function EquityChart({ portfolioId }) {
  const [curves, setCurves] = useState(null);
  const [period, setPeriod] = useState('3Y');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getPerformance(portfolioId, period)
      .then(data => { setCurves(data.curves); setLoading(false); })
      .catch(() => setLoading(false));
  }, [portfolioId, period]);

  const tickers = curves ? Object.keys(curves) : [];

  // Construye array de puntos para Recharts: [{date, AAPL: 5.2, MSFT: 3.1, ...}]
  const chartData = (() => {
    if (!curves || tickers.length === 0) return [];
    const first = curves[tickers[0]];
    return first.dates.map((date, i) => {
      const point = { date };
      tickers.forEach(t => {
        point[t] = curves[t].returns[i] ?? null;
      });
      return point;
    });
  })();

  return (
    <div className="equity-chart">
      <div className="chart-header">
        <span className="chart-title">ASSET PERFORMANCE</span>
        <div className="period-selector">
          {PERIODS.map(p => (
            <button
              key={p}
              className={`period-btn ${period === p ? 'active' : ''}`}
              onClick={() => setPeriod(p)}
            >
              {p}
            </button>
          ))}
        </div>
      </div>

      {loading && <div className="chart-loading">Loading...</div>}

      {!loading && chartData.length > 0 && (
        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={chartData} margin={{ top: 10, right: 55, left: 0, bottom: 0 }}>
            <XAxis
              dataKey="date"
              tick={{ fill: '#444', fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={d => d.slice(0, 7)}
              ticks={chartData
                .filter(d => ['01', '07'].includes(d.date.slice(5, 7)))
                .map(d => d.date)}
            />
            <YAxis
              tick={{ fill: '#444', fontSize: 11 }}
              tickLine={false}
              axisLine={false}
              tickFormatter={v => `${v > 0 ? '+' : ''}${v.toFixed(0)}%`}
              width={52}
            />
            <Tooltip
              contentStyle={{ background: '#141414', border: '1px solid #2a2a2a', borderRadius: 4 }}
              labelStyle={{ color: '#666', fontSize: 11 }}
              itemStyle={{ fontSize: 12 }}
              formatter={(value, name) => [`${value > 0 ? '+' : ''}${value?.toFixed(2)}%`, name]}
            />
            <ReferenceLine y={0} stroke="#2a2a2a" strokeDasharray="3 3" />
            {tickers.map((ticker, i) => {
              const color = COLORS[i % COLORS.length];
              const EndLabel = (props) => {
                if (props.index !== chartData.length - 1) return null;
                return (
                  <text x={props.x + 6} y={props.y + 4} fill={color} fontSize={11} fontFamily="monospace">
                    {ticker}
                  </text>
                );
              };
              return (
                <Line
                  key={ticker}
                  type="monotone"
                  dataKey={ticker}
                  stroke={color}
                  dot={false}
                  strokeWidth={1.5}
                  connectNulls
                  label={<EndLabel />}
                />
              );
            })}
          </LineChart>
        </ResponsiveContainer>
      )}

      {!loading && chartData.length === 0 && (
        <div className="chart-loading">No data for this period.</div>
      )}
    </div>
  );
}

export default EquityChart;
