import { useState, useEffect } from 'react';
import { getPortfolio, addPosition, removePosition } from '../services/api';
import PositionsTable from '../components/PositionsTable';
import AddTickerBar from '../components/AddTickerBar';
import EquityChart from '../components/EquityChart';
import './PortfolioScreen.css';

function PortfolioScreen({ portfolioId }) {
  const [portfolio, setPortfolio] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    getPortfolio(portfolioId)
      .then(data => { setPortfolio(data); setLoading(false); })
      .catch(err => { setError(err.message); setLoading(false); });
  }, [portfolioId]);

  async function applyWeights(updatedPositions) {
    for (const pos of updatedPositions) {
      await addPosition(portfolioId, pos.asset.ticker, pos.weight);
    }
    const updated = await getPortfolio(portfolioId);
    setPortfolio(updated);
  }

  async function handleAddTicker(ticker, weight) {
    try {
      const existingPositions = portfolio.positions.filter(
        p => p.asset.ticker !== ticker
      );
      const totalExisting = existingPositions.reduce(
        (sum, p) => sum + parseFloat(p.weight), 0
      );
      const newTotal = totalExisting + weight;

      if (newTotal > 100) {
        // Normaliza todo proporcionalmente para sumar exactamente 100
        const allPositions = [
          ...existingPositions.map(p => ({ ...p, weight: parseFloat(p.weight) })),
          { asset: { ticker }, weight },
        ];
        const scale = 100 / newTotal;
        const normalized = allPositions.map(p => ({
          ...p,
          weight: Math.round(p.weight * scale * 100) / 100,
        }));
        await applyWeights(normalized);
      } else {
        await addPosition(portfolioId, ticker, weight);
        const updated = await getPortfolio(portfolioId);
        setPortfolio(updated);
      }
    } catch (err) {
      alert(`Error añadiendo ${ticker}: ${err.message}`);
    }
  }

  async function handleRebalance() {
    const positions = portfolio.positions;
    if (positions.length === 0) return;
    const total = positions.reduce((sum, p) => sum + parseFloat(p.weight), 0);
    if (total === 0) return;
    const normalized = positions.map(p => ({
      ...p,
      weight: Math.round((parseFloat(p.weight) / total) * 100 * 100) / 100,
    }));
    try {
      await applyWeights(normalized);
    } catch (err) {
      alert(`Error rebalanceando: ${err.message}`);
    }
  }

  async function handleRemove(assetId) {
    try {
      await removePosition(portfolioId, assetId);
      const updated = await getPortfolio(portfolioId);
      setPortfolio(updated);
    } catch (err) {
      alert(`Error eliminando posición: ${err.message}`);
    }
  }

  if (loading) return <div className="screen-message">Loading portfolio...</div>;
  if (error)   return <div className="screen-message error">{error}</div>;

  const totalWeight = portfolio.positions.reduce(
    (sum, p) => sum + parseFloat(p.weight), 0
  );
  const totalColor = totalWeight > 100 ? '#e05c5c' : totalWeight === 100 ? '#4caf8c' : '#aaa';

  return (
    <div className="portfolio-screen">
      <header className="portfolio-header">
        <div className="flex gap-2 items-center">
          <span className="title-main">PORTFOLIO</span>
          <span className="title-sub">OPTIMIZER</span>
        </div>
      </header>

      <AddTickerBar onAdd={handleAddTicker} />

      <section className="positions-section">
        <div className="section-header">
          <span>POSITIONS &nbsp; <span className="count">{portfolio.positions.length} ASSETS</span></span>
          <div className="section-header-right">
            <span className="total-weight" style={{ color: totalColor }}>
              TOTAL {totalWeight.toFixed(1)}%
            </span>
            {portfolio.positions.length > 0 && (
              <button className="rebalance-btn" onClick={handleRebalance}>
                Rebalance
              </button>
            )}
          </div>
        </div>
        <PositionsTable positions={portfolio.positions} onRemove={handleRemove} />
      </section>

      {portfolio.positions.length > 0 && (
        <EquityChart portfolioId={portfolioId} />
      )}
    </div>
  );
}

export default PortfolioScreen;
