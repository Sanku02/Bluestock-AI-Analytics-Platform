import { useEffect, useState } from "react";

import API from "../services/api";

import Loader from "../components/Loader";

function ComparePage() {

  const [companies, setCompanies] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [company1, setCompany1] =
    useState("");

  const [company2, setCompany2] =
    useState("");

  const [data1, setData1] =
    useState(null);

  const [data2, setData2] =
    useState(null);

  useEffect(() => {

    fetchCompanies();

  }, []);

  const fetchCompanies = async () => {

    try {

      const response =
        await API.get(
          "/health-scores/"
        );

      setCompanies(
        response.data || []
      );

    }

    catch (error) {

      console.error(error);

    }

    finally {

      setLoading(false);

    }

  };

  const compareCompanies =
    async () => {

      if (
        !company1 ||
        !company2
      ) {

        alert(
          "Please select both companies"
        );

        return;

      }

      try {

        const response1 =
          await API.get(
            `/company/${company1}/`
          );

        const response2 =
          await API.get(
            `/company/${company2}/`
          );

        setData1(
          response1.data
        );

        setData2(
          response2.data
        );

      }

      catch (error) {

        console.error(error);

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

  if (loading) {

    return <Loader />;

  }

  return (

    <div className="page-container">

      {/* HERO */}

      <div
        className="hero-gradient"
        style={{
          marginBottom: "32px"
        }}
      >

        <h1
          style={{
            fontSize: "48px",
            fontWeight: "800",
            marginBottom: "12px"
          }}
        >
          Compare Companies
        </h1>

        <p
          style={{
            color: "#cbd5e1",
            fontSize: "17px"
          }}
        >
          Analyze companies side-by-side using AI-powered health metrics
        </p>

      </div>

      {/* SELECTORS */}

      <div
        className="dashboard-card"
        style={{
          marginBottom: "35px",
          padding: "24px"
        }}
      >

        <div
          style={{
            display: "flex",
            gap: "16px",
            flexWrap: "wrap",
            alignItems: "center"
          }}
        >

          {/* COMPANY 1 */}

          <select
            value={company1}
            onChange={(e) =>
              setCompany1(
                e.target.value
              )
            }
            className="modern-input"
            style={{
              width: "320px"
            }}
          >

            <option value="">
              Select Company 1
            </option>

            {

              companies.map(
                (company) => (

                  <option
                    key={company.symbol}
                    value={
                      company.symbol
                    }
                  >

                    {
                      company.company_name
                    }

                    {" "}

                    (

                    {
                      company.symbol
                    }

                    )

                  </option>

                )
              )

            }

          </select>

          {/* COMPANY 2 */}

          <select
            value={company2}
            onChange={(e) =>
              setCompany2(
                e.target.value
              )
            }
            className="modern-input"
            style={{
              width: "320px"
            }}
          >

            <option value="">
              Select Company 2
            </option>

            {

              companies.map(
                (company) => (

                  <option
                    key={company.symbol}
                    value={
                      company.symbol
                    }
                  >

                    {
                      company.company_name
                    }

                    {" "}

                    (

                    {
                      company.symbol
                    }

                    )

                  </option>

                )
              )

            }

          </select>

          <button
            onClick={
              compareCompanies
            }
            className="primary-button"
            style={{
              height: "52px",
              minWidth: "130px"
            }}
          >

            Compare

          </button>

        </div>

      </div>

      {/* RESULTS */}

      {

        data1 && data2 && (

          <div
            style={{
              display: "grid",
              gridTemplateColumns:
                "repeat(auto-fit,minmax(380px,1fr))",
              gap: "28px"
            }}
          >

            {/* COMPANY 1 */}

            <CompanyCard
              data={data1}
              getRatingClass={
                getRatingClass
              }
            />

            {/* COMPANY 2 */}

            <CompanyCard
              data={data2}
              getRatingClass={
                getRatingClass
              }
            />

          </div>

        )

      }

    </div>

  );

}

/* COMPANY CARD */

function CompanyCard({

  data,
  getRatingClass

}) {

  return (

    <div
      className="dashboard-card"
      style={{
        minHeight: "500px"
      }}
    >

      <div
        style={{
          marginBottom: "26px"
        }}
      >

        <h2
          style={{
            fontSize: "32px",
            fontWeight: "800",
            lineHeight: "1.2",
            color: "#0f172a",
            marginBottom: "12px"
          }}
        >

          {
            data.company_name
          }

        </h2>

        <p
          style={{
            color: "#64748b",
            marginBottom: "18px",
            fontSize: "15px"
          }}
        >

          Symbol:
          {" "}

          <strong>

            {
              data.symbol
            }

          </strong>

        </p>

        <span
          className={
            getRatingClass(
              data.rating
            )
          }
        >

          {
            data.rating
          }

        </span>

      </div>

      <Metric
        label="Health Score"
        value={
          Number(
            data.health_score
          ).toFixed(2)
        }
        color="#2563eb"
      />

      <Metric
        label="ROE %"
        value={
          data.roe_percentage
        }
        color="#10b981"
      />

      <Metric
        label="ROCE %"
        value={
          data.roce_percentage
        }
        color="#f59e0b"
      />

      <Metric
        label="Debt To Equity"
        value={
          data.debt_to_equity || 0
        }
        color="#ef4444"
      />

    </div>

  );

}

/* METRIC */

function Metric({

  label,
  value,
  color

}) {

  return (

    <div
      style={{
        marginBottom: "28px"
      }}
    >

      <h4
        style={{
          color: "#64748b",
          marginBottom: "8px",
          fontSize: "14px",
          fontWeight: "600"
        }}
      >

        {label}

      </h4>

      <h1
        style={{
          color: color,
          fontSize: "42px",
          fontWeight: "800",
          lineHeight: "1"
        }}
      >

        {value}

      </h1>

    </div>

  );

}

export default ComparePage;