function SummaryCard({ title, value }) {

  return (

    <div
      style={{
        border: "1px solid #ddd",
        borderRadius: "10px",
        padding: "20px",
        minWidth: "180px",
        backgroundColor: "#ffffff",
        boxShadow: "0 2px 6px rgba(0,0,0,0.1)"
      }}
    >

      <h3>{title}</h3>

      <h2>{value}</h2>

    </div>

  );

}

export default SummaryCard;