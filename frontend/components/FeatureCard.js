export default function FeatureCard({ title, value, subtitle }) {
  return (
    <div className="feature-card">
      <h3>{title}</h3>
      <p className="value">{value}</p>
      <p className="subtitle">{subtitle}</p>
    </div>
  );
}
