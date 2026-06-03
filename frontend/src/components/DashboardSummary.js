import { useEffect, useState } from "react";

import {
  getDashboard
} from "../services/partnerApi";


function DashboardSummary() {

  const [
    summary,
    setSummary
  ] = useState(null);


  useEffect(() => {

    async function loadDashboard() {

      try {

        const data =
          await getDashboard();

        console.log(data);

        setSummary(data);

      } catch (error) {

        console.error(error);
      }
    }

    loadDashboard();

  }, []);


  if (!summary) {

    return <p>Loading...</p>;
  }


  return (

    <div
      style={{
        marginTop: "30px",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "10px"
      }}
    >

      <h2>
        Dashboard Summary
      </h2>

      <p>
        Total Companies:
        {" "}
        {summary.total_companies}
      </p>

      <p>
        Average Health Score:
        {" "}
        {summary.average_health_score}
      </p>

      <p>
        Top Sector:
        {" "}
        {summary.top_sector}
      </p>

      <p>
        Top Company:
        {" "}
        {summary.top_company}
      </p>

    </div>
  );
}

export default DashboardSummary;