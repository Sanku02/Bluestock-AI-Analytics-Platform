import { useEffect, useState }
from "react";

import {
  getTopMovers
} from "../services/partnerApi";


function TopMovers() {

  const [
    movers,
    setMovers
  ] = useState(null);


  useEffect(() => {

    async function loadMovers() {

      try {

        const data =
          await getTopMovers();

        console.log(data);

        setMovers(data);

      } catch (error) {

        console.error(error);
      }
    }

    loadMovers();

  }, []);


  if (!movers) {

    return <p>Loading Top Movers...</p>;
  }


  return (

    <div
      style={{
        marginTop: "30px"
      }}
    >

      <h2>
        Top Gainers
      </h2>

      {
        movers.top_gainers.map(
          (company, index) => (

            <div
              key={index}
              style={{
                padding: "10px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                borderRadius: "10px"
              }}
            >

              <h3>
                {company.symbol}
              </h3>

              <p>
                {company.company_name}
              </p>

              <p>
                Score:
                {" "}
                {company.health_score.toFixed(2)}
              </p>

              <p>
                Rating:
                {" "}
                {company.rating}
              </p>

            </div>
          )
        )
      }


      <h2>
        Top Decliners
      </h2>

      {
        movers.top_decliners.map(
          (company, index) => (

            <div
              key={index}
              style={{
                padding: "10px",
                marginBottom: "10px",
                border: "1px solid #ccc",
                borderRadius: "10px"
              }}
            >

              <h3>
                {company.symbol}
              </h3>

              <p>
                {company.company_name}
              </p>

              <p>
                Score:
                {" "}
                {company.health_score.toFixed(2)}
              </p>

              <p>
                Rating:
                {" "}
                {company.rating}
              </p>

            </div>
          )
        )
      }

    </div>
  );
}

export default TopMovers;