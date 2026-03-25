export default function MoneyHealthBreakdown({ result }) {
  if (!result) {
    return null;
  }

  return (
    <div className="panel">
      <h2>Money Health Score</h2>
      <p className="big-score">{result.total_score}/100</p>
      <p className="status">Status: {result.status}</p>
      <div className="grid-2">
        {result.dimensions.map((dimension) => (
          <div key={dimension.name} className="mini-card">
            <strong>{dimension.name}</strong>
            <div>{dimension.score}/100</div>
            <small>{dimension.insight}</small>
          </div>
        ))}
      </div>
    </div>
  );
}
