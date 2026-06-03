import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";

import API from "../services/api";
import Loader from "../components/Loader";

function ScreenerPage() {

  const [companies, setCompanies] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  /* URL PARAM */

  const params =
    new URLSearchParams(
      window.location.search
    );

  const initialRating =
    params
      .get("rating")
      ?.trim()
      ?.toUpperCase() || "";

  /* FILTER STATES */

  const [ratingFilter, setRatingFilter] =
    useState(initialRating);

  const [minScore, setMinScore] =
    useState("");

  const [maxScore, setMaxScore] =
    useState("");

  /* FETCH DATA */

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

        Array.isArray(response.data)

          ? response.data

          : []

      );

    }

    catch (error) {

      console.error(
        "Screener fetch error:",
        error
      );

    }

    finally {

      setLoading(false);

    }

  };

  /* FILTERED DATA */

  const filteredCompanies =
    useMemo(() => {

      return companies.filter(
        (company) => {

          const rating =
            company.rating
              ?.trim()
              ?.toUpperCase();

          const score =
            Number(
              company.health_score || 0
            );

          const matchesRating =

            ratingFilter === ""

            ||

            rating ===
            ratingFilter;

          const matchesMin =

            minScore === ""

            ||

            score >=
            Number(minScore);

          const matchesMax =

            maxScore === ""

            ||

            score <=
            Number(maxScore);

          return (

            matchesRating

            &&

            matchesMin

            &&

            matchesMax

          );

        }
      );

    }, [

      companies,
      ratingFilter,
      minScore,
      maxScore

    ]);

  /* KPI */

  const companyCount =
    filteredCompanies.length;

  const topScore =

    filteredCompanies.length > 0

      ?

      Math.max(

        ...filteredCompanies.map(
          company =>
            Number(
              company.health_score || 0
            )
        )

      ).toFixed(2)

      :

      "0";

  const formatLabel = (text) => {

    return text
      ?.charAt(0)
      ?.toUpperCase()

      +

      text
        ?.slice(1)
        ?.toLowerCase();

  };

  const dynamicLabel =

    ratingFilter

      ?

      `${formatLabel(ratingFilter)} Companies`

      :

      "Strong Companies";

  const dynamicCount =

    ratingFilter

      ?

      filteredCompanies.length

      :

      filteredCompanies.filter(

        company =>

          company.rating
            ?.toUpperCase() ===
            "GOOD"

          ||

          company.rating
            ?.toUpperCase() ===
            "EXCELLENT"

      ).length;

  /* COLORS */

  const getMetricColor = () => {

    if (
      ratingFilter === "GOOD"
      ||
      ratingFilter === "EXCELLENT"
    ) {
      return "#10b981";
    }

    if (
      ratingFilter === "AVERAGE"
    ) {
      return "#f59e0b";
    }

    if (
      ratingFilter === "WEAK"
      ||
      ratingFilter === "POOR"
    ) {
      return "#ef4444";
    }

    return "#10b981";

  };

  const getRatingClass =
    (rating) => {

      switch (
        rating
          ?.toUpperCase()
      ) {

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

  /* LOADER */

  if (loading) {

    return <Loader />;

  }

  return (

    <div className="page-container">

      {/* HERO */}

      <div
        className="hero-gradient"
        style={{
          marginBottom: "35px"
        }}
      >

        <h1
          style={{
            fontSize: "48px",
            marginBottom: "14px",
            fontWeight: "800"
          }}
        >
          Stock Screener
        </h1>

        <p
          style={{
            color: "#cbd5e1",
            fontSize: "18px"
          }}
        >
          Discover fundamentally strong companies
        </p>

        {

          ratingFilter && (

            <div
              style={{
                marginTop: "20px"
              }}
            >

              <span
                style={{

                  background:
                    getMetricColor(),

                  color: "white",

                  padding:
                    "8px 18px",

                  borderRadius:
                    "999px",

                  fontSize: "13px",

                  fontWeight: "700",

                  letterSpacing:
                    "0.5px"

                }}
              >

                {formatLabel(ratingFilter)}
                {" "}
                FILTER ACTIVE

              </span>

            </div>

          )

        }

      </div>

      {/* FILTERS */}

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
            gap: "18px",
            flexWrap: "wrap"
          }}
        >

          <select
            value={ratingFilter}
            onChange={(e) =>
              setRatingFilter(
                e.target.value
              )
            }
            className="modern-input"
          >

            <option value="">
              All Ratings
            </option>

            <option value="EXCELLENT">
              Excellent
            </option>

            <option value="GOOD">
              Good
            </option>

            <option value="AVERAGE">
              Average
            </option>

            <option value="WEAK">
              Weak
            </option>

            <option value="POOR">
              Poor
            </option>

          </select>

          <input
            type="number"
            placeholder="Minimum Score"
            value={minScore}
            onChange={(e) =>
              setMinScore(
                e.target.value
              )
            }
            className="modern-input"
          />

          <input
            type="number"
            placeholder="Maximum Score"
            value={maxScore}
            onChange={(e) =>
              setMaxScore(
                e.target.value
              )
            }
            className="modern-input"
          />

        </div>

      </div>

      {/* KPI SECTION */}

      <div
        className="analytics-grid"
        style={{
          marginBottom: "40px"
        }}
      >

        <div className="dashboard-card hover-card">

          <h3
            style={{
              color: "#64748b",
              marginBottom: "18px"
            }}
          >
            Results
          </h3>

          <h1
            className="metric-value"
            style={{
              fontSize: "52px"
            }}
          >
            {companyCount}
          </h1>

        </div>

        <div className="dashboard-card hover-card">

          <h3
            style={{
              color: "#64748b",
              marginBottom: "18px"
            }}
          >
            Top Score
          </h3>

          <h1
            className="metric-value"
            style={{
              color: "#2563eb",
              fontSize: "52px"
            }}
          >
            {topScore}
          </h1>

        </div>

        <div className="dashboard-card hover-card">

          <h3
            style={{
              color: "#64748b",
              marginBottom: "18px"
            }}
          >
            {dynamicLabel}
          </h3>

          <h1
            className="metric-value"
            style={{
              color:
                getMetricColor(),
              fontSize: "52px"
            }}
          >
            {dynamicCount}
          </h1>

        </div>

      </div>

      {/* COMPANIES */}

      <div
        style={{

          display: "grid",

          gridTemplateColumns:
            "repeat(auto-fit,minmax(280px,1fr))",

          gap: "24px"

        }}
      >

        {

          filteredCompanies.map(
            (company, index) => (

              <div
                key={index}
                className="dashboard-card hover-card"
              >

                <div
                  style={{
                    display: "flex",
                    justifyContent:
                      "space-between",
                    alignItems:
                      "center",
                    marginBottom:
                      "18px"
                  }}
                >

                  <h2
                    style={{
                      color: "#0f172a",
                      fontSize: "18px",
                      fontWeight: "700"
                    }}
                  >
                    {company.symbol}
                  </h2>

                  <span
                    className={
                      getRatingClass(
                        company.rating
                      )
                    }
                  >

                    {company.rating}

                  </span>

                </div>

                <h1
                  style={{
                    fontSize: "42px",
                    fontWeight: "800",
                    color: "#0f172a",
                    marginBottom: "10px"
                  }}
                >

                  {

                    Number(
                      company.health_score || 0
                    ).toFixed(2)

                  }

                </h1>

                <p
                  style={{
                    color: "#64748b",
                    marginBottom: "24px"
                  }}
                >
                  Financial Health Score
                </p>

                <Link
                  to={`/company/${company.symbol}`}
                  className="primary-button"
                  style={{
                    display: "inline-block"
                  }}
                >
                  View Details →
                </Link>

              </div>

            )
          )

        }

      </div>

      {

        filteredCompanies.length === 0 && (

          <div
            className="dashboard-card"
            style={{
              marginTop: "40px",
              textAlign: "center",
              padding: "60px"
            }}
          >

            <h2
              style={{
                marginBottom: "10px"
              }}
            >
              No companies found
            </h2>

            <p
              style={{
                color: "#64748b"
              }}
            >
              Try changing the filters
            </p>

          </div>

        )

      }

    </div>

  );

}

export default ScreenerPage;