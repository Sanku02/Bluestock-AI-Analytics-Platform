function RatingBadge({ rating }) {

  let backgroundColor = "#999";

  if (rating === "EXCELLENT") {
    backgroundColor = "#16a34a";
  }

  else if (rating === "GOOD") {
    backgroundColor = "#22c55e";
  }

  else if (rating === "AVERAGE") {
    backgroundColor = "#eab308";
  }

  else if (rating === "WEAK") {
    backgroundColor = "#f97316";
  }

  else if (rating === "POOR") {
    backgroundColor = "#ef4444";
  }

  return (

    <span
      style={{
        backgroundColor,
        color: "white",
        padding: "6px 12px",
        borderRadius: "20px",
        fontWeight: "bold",
        fontSize: "14px"
      }}
    >

      {rating}

    </span>

  );

}

export default RatingBadge;