import {
  useEffect,
  useState,
  useCallback
} from "react";

import { useParams } from "react-router-dom";

import API from "../services/api";

import RatingBadge from "../components/RatingBadge";

import Loader from "../components/Loader";

import {

  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer

} from "recharts";

function CompanyDetailPage() {

  const { symbol } = useParams();

  const [company, setCompany] =
    useState(null);

  const [history, setHistory] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const fetchCompany = useCallback(
    async () => {

      try {

        const response =
          await API.get(
            `/company/${symbol}/`
          );

        setCompany(
          response.data
        );

        const historyResponse =
          await API.get(
            `/score-history/${symbol}/`
          );

        setHistory(
          historyResponse.data || []
        );

      }

      catch (error) {

        console.error(error);

      }

      finally {

        setLoading(false);

      }

    },
    [symbol]
  );

  useEffect(() => {

    fetchCompany();

  }, [fetchCompany]);

  if (loading) {

    return <Loader />;

  }

  return (

    <div className="page-container">

      <div
        className="hero-gradient"
        style={{
          marginBottom: "35px"
        }}
      >

        <h1
          style={{
            fontSize: "42px",
            marginBottom: "12px",
            fontWeight: "800",
            lineHeight: "1.2"
          }}
        >

          {
            company.company_name
          }

        </h1>

        <h3
          style={{
            color: "#cbd5e1",
            fontWeight: "500",
            marginBottom: "24px",
            fontSize: "18px"
          }}
        >

          Symbol:
          {" "}

          {
            company.symbol
          }

        </h3>

        <RatingBadge
          rating={company.rating}
        />

      </div>

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
            Health Score
          </h3>

          <h1
            className="metric-value"
            style={{
              color: "#2563eb",
              fontSize: "52px"
            }}
          >

            {

              company.health_score
                ?.toFixed(2)

            }

          </h1>

        </div>

        <div className="dashboard-card hover-card">

          <h3
            style={{
              color: "#64748b",
              marginBottom: "18px"
            }}
          >
            ROE %
          </h3>

          <h1
            className="metric-value"
            style={{
              color: "#10b981",
              fontSize: "52px"
            }}
          >

            {

              company.roe_percentage
              ||
              "N/A"

            }

          </h1>

        </div>

        <div className="dashboard-card hover-card">

          <h3
            style={{
              color: "#64748b",
              marginBottom: "18px"
            }}
          >
            ROCE %
          </h3>

          <h1
            className="metric-value"
            style={{
              color: "#f59e0b",
              fontSize: "52px"
            }}
          >

            {

              company.roce_percentage
              ||
              "N/A"

            }

          </h1>

        </div>

      </div>

      <div className="dashboard-card">

        <div
          style={{
            marginBottom: "28px"
          }}
        >

          <h2
            className="section-title"
            style={{
              marginBottom: "10px"
            }}
          >
            Score History
          </h2>

          <p
            style={{
              color: "#64748b"
            }}
          >
            Historical trend of company health score
          </p>

        </div>

        <div
          style={{
            width: "100%",
            height: "420px"
          }}
        >

          <ResponsiveContainer
            width="100%"
            height="100%"
          >

            <LineChart
              data={history}
            >

              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#e2e8f0"
              />

              <XAxis
                dataKey="computed_at"
                tickFormatter={
                  (value) => {

                    return new Date(value)
                      .toLocaleDateString();

                  }
                }
              />

              <YAxis />

              <Tooltip />

              <Line
                type="monotone"
                dataKey="health_score"
                stroke="#2563eb"
                strokeWidth={4}
                dot={{
                  r: 5
                }}
                activeDot={{
                  r: 8
                }}
                animationDuration={1200}
              />

            </LineChart>

          </ResponsiveContainer>

        </div>

      </div>

      <div
        style={{
          marginTop: "35px",
          color: "#64748b",
          fontSize: "15px"
        }}
      >

        <strong>
          Computed At:
        </strong>

        {" "}

        {
          company.computed_at
        }

      </div>

    </div>

  );

}

export default CompanyDetailPage;