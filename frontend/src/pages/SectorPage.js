import { useEffect, useState } from "react";

import API from "../services/api";

import Loader from "../components/Loader";

function SectorPage() {

  const [sectors, setSectors] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  useEffect(() => {

    fetchSectorData();

  }, []);

  const fetchSectorData = async () => {

    try {

      const response =
        await API.get(
          "/sector-analysis/"
        );

      setSectors(
        response.data
      );

      setLoading(false);

    }

    catch (error) {

      console.error(error);

      setLoading(false);

    }

  };

  const getRatingClass = (
    rating
  ) => {

    switch (rating) {

      case "EXCELLENT":
        return "rating-badge rating-excellent";

      case "GOOD":
        return "rating-badge rating-good";

      case "AVERAGE":
        return "rating-badge rating-average";

      case "WEAK":
        return "rating-badge rating-weak";

      default:
        return "rating-badge rating-poor";

    }

  };

  const topSector = sectors[0];

  if (loading) {

    return <Loader />;

  }

  return (

    <div className="page-container">

      {/* HERO SECTION */}

      {

        topSector && (

          <div
            className="hero-gradient"
            style={{
              marginBottom: "40px"
            }}
          >

            <h2
              style={{
                fontSize: "28px",
                marginBottom: "12px",
                color: "#cbd5e1"
              }}
            >
              Top Performing Sector
            </h2>

            <h1
              style={{
                fontSize: "60px",
                marginBottom: "30px"
              }}
            >
              {
                topSector.sector_name
              }
            </h1>

            <div
              style={{
                display: "flex",
                gap: "50px",
                flexWrap: "wrap"
              }}
            >

              <div>

                <p
                  style={{
                    color: "#cbd5e1",
                    marginBottom: "10px"
                  }}
                >
                  Average Score
                </p>

                <h1>
                  {
                    topSector.avg_score
                  }
                </h1>

              </div>

              <div>

                <p
                  style={{
                    color: "#cbd5e1",
                    marginBottom: "10px"
                  }}
                >
                  Companies
                </p>

                <h1>
                  {
                    topSector.company_count
                  }
                </h1>

              </div>

              <div>

                <p
                  style={{
                    color: "#cbd5e1",
                    marginBottom: "10px"
                  }}
                >
                  Rating
                </p>

                <div
                  style={{
                    marginTop: "10px"
                  }}
                >

                  <span
                    className={
                      getRatingClass(
                        topSector.rating
                      )
                    }
                  >

                    {
                      topSector.rating
                    }

                  </span>

                </div>

              </div>

            </div>

          </div>

        )

      }

      {/* SECTION TITLE */}

      <div
        style={{
          marginBottom: "30px"
        }}
      >

        <h1
          style={{
            fontSize: "44px",
            color: "#0f172a",
            marginBottom: "10px"
          }}
        >
          Sector Analytics
        </h1>

        <p
          style={{
            color: "#64748b",
            fontSize: "17px"
          }}
        >
          Analyze sector-wide financial health performance
        </p>

      </div>

      {/* SECTOR GRID */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(340px,1fr))",
          gap: "25px"
        }}
      >

        {

          sectors.map(

            (sector, index) => (

              <div
                key={index}
                className="dashboard-card"
              >

                {/* HEADER */}

                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    alignItems: "center",
                    marginBottom: "25px"
                  }}
                >

                  <h2
                    style={{
                      fontSize: "28px",
                      color: "#0f172a"
                    }}
                  >

                    {
                      sector.sector_name
                    }

                  </h2>

                  <span
                    className={
                      getRatingClass(
                        sector.rating
                      )
                    }
                  >

                    {
                      sector.rating
                    }

                  </span>

                </div>

                {/* AVG SCORE */}

                <div
                  style={{
                    marginBottom: "30px"
                  }}
                >

                  <p
                    style={{
                      color: "#64748b",
                      marginBottom: "10px"
                    }}
                  >
                    Average Health Score
                  </p>

                  <h1
                    style={{
                      fontSize: "52px",
                      color: "#2563eb"
                    }}
                  >

                    {
                      sector.avg_score
                    }

                  </h1>

                </div>

                {/* COMPANY COUNT */}

                <div>

                  <p
                    style={{
                      color: "#64748b",
                      marginBottom: "10px"
                    }}
                  >
                    Total Companies
                  </p>

                  <h2
                    style={{
                      fontSize: "34px",
                      color: "#0f172a"
                    }}
                  >

                    {
                      sector.company_count
                    }

                  </h2>

                </div>

              </div>

            )

          )

        }

      </div>

    </div>

  );

}

export default SectorPage;