const BASE_URL = 'http://localhost:8000/api';

export async function getPortfolio(id) {
  const res = await fetch(`${BASE_URL}/portfolios/${id}/`);
  if (!res.ok) throw new Error('Failed to fetch portfolio');
  return res.json();
}

export async function addPosition(portfolioId, ticker, weight) {
  const res = await fetch(`${BASE_URL}/portfolios/${portfolioId}/positions/add/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ticker, weight }),
  });
  if (!res.ok) throw new Error('Failed to add position');
  return res.json();
}

export async function removePosition(portfolioId, assetId) {
  const res = await fetch(`${BASE_URL}/portfolios/${portfolioId}/positions/${assetId}/remove/`, {
    method: 'DELETE',
  });
  if (!res.ok) throw new Error('Failed to remove position');
}

export async function getPerformance(portfolioId, period = '3Y') {
  const res = await fetch(`${BASE_URL}/portfolios/${portfolioId}/performance/?period=${period}`);
  if (!res.ok) throw new Error('Failed to fetch performance');
  return res.json();
}
