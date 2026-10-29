import { useState } from 'react';
import './AddTickerBar.css';

function AddTickerBar({ onAdd }) {
  const [ticker, setTicker] = useState('');
  const [weight, setWeight] = useState('');
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    if (!ticker || !weight) return;
    setLoading(true);
    await onAdd(ticker.toUpperCase(), parseFloat(weight));
    setTicker('');
    setWeight('');
    setLoading(false);
  }

  return (
    <form className="add-ticker-bar" onSubmit={handleSubmit}>
      <input
        className="ticker-input"
        placeholder="Ticker (e.g. AAPL)"
        value={ticker}
        onChange={e => setTicker(e.target.value)}
        disabled={loading}
      />
      <input
        className="weight-input"
        type="number"
        placeholder="Weight %"
        value={weight}
        onChange={e => setWeight(e.target.value)}
        min="0"
        max="100"
        disabled={loading}
      />
      <button className="add-btn" type="submit" disabled={loading}>
        {loading ? 'Adding...' : 'Add'}
      </button>
    </form>
  );
}

export default AddTickerBar;
