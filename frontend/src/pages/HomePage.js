import { useEffect, useState } from "react";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from "recharts";

import API from "../services/api";

import {
  getDashboard,
  getSectorRankings,
  getTopCompanies
} from "../services/partnerApi";

import Loader from "../components/Loader";

function HomePage() {

  const [summary, setSummary] =
    useState(null);

  const [sectorData, setSectorData] =
    useState([]);

  const [topCompanies, setTopCompanies] =
    useState([]);

  const [aiData, setAiData] =
    useState({
      top_picks: [],
      risky_companies: [],
      high_roe: []
    });

  useEffect(() => {

    fetchDashboard();

  }, []);

  const fetchDashboard = async () => {

    try {

      const summaryResponse =
        await getDashboard();

      const sectorResponse =
        await getSectorRankings();

      const companiesResponse =
        await getTopCompanies();

      const aiResponse =
        await API.get(
          "/ai-recommendations/"
        );

      setSummary(summaryResponse);

      setSectorData(

        Array.isArray(sectorResponse)

          ?

          sectorResponse.slice(0, 6)

          :

        Array.isArray(
          sectorResponse.data
        )

          ?

          sectorResponse.data.slice(0, 6)

          :

          []

      );

      setTopCompanies(

        Array.isArray(companiesResponse)

          ?

          companiesResponse.slice(0, 5)

          :

        Array.isArray(
          companiesResponse.data
        )

          ?

          companiesResponse.data.slice(0, 5)

          :

          []

      );

      setAiData({

        top_picks:
          aiResponse?.data?.top_picks || [],

        risky_companies:
          aiResponse?.data?.risky_companies || [],

        high_roe:
          aiResponse?.data?.high_roe || []

      });

    }

    catch (error) {

      console.error(error);

    }

  };

  if (!summary) {

    return <Loader />;

  }

  const pieData = [

    {
      name: "Excellent",
      value:
        summary.excellent_count ||
        summary.excellent ||
        0
    },

    {
      name: "Good",
      value:
        summary.good_count ||
        summary.good ||
        0
    },

    {
      name: "Average",
      value:
        summary.average_count ||
        summary.average ||
        0
    },

    {
      name: "Weak",
      value:
        summary.weak_count ||
        summary.weak ||
        0
    },

    {
      name: "Poor",
      value:
        summary.poor_count ||
        summary.poor ||
        0
    }

  ];

  const COLORS = [

    "#10b981",
    "#22c55e",
    "#f59e0b",
    "#ef4444",
    "#7f1d1d"

  ];

  return (

    <div className="page-container">

      {/* HERO SECTION */}

      <div
        className="hero-gradient"
        style={{
          marginBottom: "40px",
          padding: "45px",
          borderRadius: "28px",
          background:
            "linear-gradient(135deg,#020617,#001845,#0f172a)",
          boxShadow:
            "0 15px 40px rgba(0,0,0,0.18)"
        }}
      >

        <h1
          style={{
            fontSize: "52px",
            marginBottom: "15px",
            color: "white",
            fontWeight: "800",
            letterSpacing: "-2px"
          }}
        >
          Bluestock Analytics Platform
        </h1>

        <p
          style={{
            fontSize: "22px",
            color: "#cbd5e1",
            marginBottom: "40px"
          }}
        >
          AI-powered stock intelligence dashboard
        </p>

        <div
          style={{
            display: "flex",
            gap: "60px",
            flexWrap: "wrap"
          }}
        >

          <div>

            <p
              style={{
                color: "#cbd5e1",
                marginBottom: "8px"
              }}
            >
              Total Companies
            </p>

            <h2
              style={{
                color: "white",
                fontSize: "34px"
              }}
            >
              {summary.total_companies}
            </h2>

          </div>

          <div>

            <p
              style={{
                color: "#cbd5e1",
                marginBottom: "8px"
              }}
            >
              Top Company
            </p>

            <h2
              style={{
                color: "white",
                fontSize: "34px"
              }}
            >
              {summary.top_company}
            </h2>

          </div>

          <div>

            <p
              style={{
                color: "#cbd5e1",
                marginBottom: "8px"
              }}
            >
              Top Sector
            </p>

            <h2
              style={{
                color: "white",
                fontSize: "34px"
              }}
            >
              {summary.top_sector}
            </h2>

          </div>

        </div>

      </div>

      {/* KPI CARDS */}

      <div
        className="analytics-grid"
        style={{
          marginBottom: "40px",
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(220px,1fr))",
          gap: "25px"
        }}
      >

        {

          pieData.map((item, index) => (

            <div
              key={index}

              className="dashboard-card"

              onClick={() => {

                window.location.href =
                  `/screener?rating=${item.name.toUpperCase()}`;

              }}

              onMouseEnter={(e) => {

                e.currentTarget.style.transform =
                  "translateY(-10px)";

                e.currentTarget.style.boxShadow =
                  "0 18px 35px rgba(0,0,0,0.14)";

              }}

              onMouseLeave={(e) => {

                e.currentTarget.style.transform =
                  "translateY(0px)";

                e.currentTarget.style.boxShadow =
                  "0 10px 25px rgba(0,0,0,0.08)";

              }}

              style={{
                cursor: "pointer",
                transition: "all 0.35s ease",
                borderRadius: "24px",
                padding: "28px",
                background: "white",
                boxShadow:
                  "0 10px 25px rgba(0,0,0,0.08)"
              }}
            >

              <h3
                style={{
                  color: "#64748b",
                  marginBottom: "18px",
                  fontSize: "20px"
                }}
              >
                {item.name}
              </h3>

              <h1
                className="metric-value"
                style={{
                  color: COLORS[index],
                  fontSize: "46px",
                  fontWeight: "800",
                  marginBottom: "18px"
                }}
              >
                {item.value}
              </h1>

              <p
                style={{
                  color: "#94a3b8",
                  fontSize: "15px"
                }}
              >
                Click to explore →
              </p>

            </div>

          ))

        }

      </div>

      {/* CHARTS */}

      <div
        style={{
          display: "grid",
          gridTemplateColumns:
            "repeat(auto-fit,minmax(520px,1fr))",
          gap: "30px",
          marginBottom: "40px"
        }}
      >

        {/* PIE CHART */}

          <div
            className="dashboard-card"
            style={{
              borderRadius: "26px",
              padding: "28px",
              background: "white",
              boxShadow:
                "0 10px 25px rgba(0,0,0,0.08)"
            }}
          >

            <h2
              style={{
                marginBottom: "25px",
                fontSize: "28px",
                fontWeight: "800"
              }}
            >
              Rating Distribution
            </h2>

            <div
              style={{
                width: "100%",
                height: "420px"
              }}
            >

          <ResponsiveContainer
            width="100%"
            height={420}
          >
            <PieChart>

              <defs>

                <linearGradient
                  id="grad1"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#00C853"
                  />
                  <stop
                    offset="100%"
                    stopColor="#00E676"
                  />
                </linearGradient>

                <linearGradient
                  id="grad2"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#1E88E5"
                  />
                  <stop
                    offset="100%"
                    stopColor="#42A5F5"
                  />
                </linearGradient>

                <linearGradient
                  id="grad3"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#FB8C00"
                  />
                  <stop
                    offset="100%"
                    stopColor="#FFA726"
                  />
                </linearGradient>

                <linearGradient
                  id="grad4"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#FF1744"
                  />
                  <stop
                    offset="100%"
                    stopColor="#FF5252"
                  />
                </linearGradient>

                <linearGradient
                  id="grad5"
                  x1="0"
                  y1="0"
                  x2="1"
                  y2="1"
                >
                  <stop
                    offset="0%"
                    stopColor="#8E0000"
                  />
                  <stop
                    offset="100%"
                    stopColor="#B71C1C"
                  />
                </linearGradient>

              </defs>

              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={85}
                outerRadius={145}
                paddingAngle={5}
                dataKey="value"
                animationDuration={1200}
                animationEasing="ease-out"
              >

                {pieData.map((entry, index) => {

                  const fills = [
                    "url(#grad1)",
                    "url(#grad2)",
                    "url(#grad3)",
                    "url(#grad4)",
                    "url(#grad5)"
                  ]

                  return (
                    <Cell
                      key={index}
                      fill={fills[index]}
                      stroke="#ffffff"
                      strokeWidth={3}
                    />
                  )

                })}

              </Pie>

              <Tooltip />

              <Legend />

            </PieChart>

          </ResponsiveContainer>
            </div>

          </div>

        {/* BAR CHART */}

        <div
          className="dashboard-card"
          style={{
            borderRadius: "26px",
            padding: "28px",
            background: "white",
            boxShadow:
              "0 10px 25px rgba(0,0,0,0.08)"
          }}
        >

          <h2
            style={{
              marginBottom: "25px",
              fontSize: "28px",
              fontWeight: "800"
            }}
          >
            Sector Performance
          </h2>

          <div
            style={{
              width: "100%",
              height: "360px"
            }}
          >

            <ResponsiveContainer
              width="100%"
              height="100%"
            >

              <BarChart
                data={sectorData}
              >

                <CartesianGrid
                  strokeDasharray="3 3"
                />

                <XAxis
                  dataKey="sector_name"
                />

                <YAxis />

                <Tooltip />

                <Bar
                  dataKey="average_health_score"
                  fill="#2563eb"
                  radius={[8, 8, 0, 0]}
                />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

      {/* AI RECOMMENDATIONS */}

      <div
        style={{
          marginBottom: "45px"
        }}
      >

        <h1
          style={{
            marginBottom: "30px",
            fontSize: "46px",
            fontWeight: "800"
          }}
        >
          AI Recommendations
        </h1>

        <div
          style={{
            display: "grid",
            gridTemplateColumns:
              "repeat(auto-fit,minmax(360px,1fr))",
            gap: "25px"
          }}
        >

          {/* TOP PICKS */}

          <div
            className="dashboard-card"
            style={{
              padding: "28px",
              borderRadius: "24px",
              background: "white",
              boxShadow:
                "0 10px 25px rgba(0,0,0,0.08)"
            }}
          >

            <h2
              style={{
                marginBottom: "25px",
                color: "#10b981",
                fontSize: "28px",
                fontWeight: "800"
              }}
            >
              Top Picks
            </h2>

            {

              aiData.top_picks.map(
                (company, index) => (

                  <div
                    key={index}
                    style={{
                      marginBottom: "25px",
                      paddingBottom: "20px",
                      borderBottom:
                        "1px solid #e2e8f0"
                    }}
                  >

                    <h3
                      style={{
                        fontSize: "18px",
                        marginBottom: "10px"
                      }}
                    >
                      {company.company_name}
                    </h3>

                    <p
                      style={{
                        marginBottom: "12px"
                      }}
                    >
                      Score:
                      {" "}
                      {
                        Number(
                          company.health_score || 0
                        ).toFixed(2)
                      }
                    </p>

                    <span
                      className="rating-badge rating-good"
                    >
                      GOOD
                    </span>

                  </div>

                )
              )

            }

          </div>

          {/* RISK */}

          <div
            className="dashboard-card"
            style={{
              padding: "28px",
              borderRadius: "24px",
              background: "white",
              boxShadow:
                "0 10px 25px rgba(0,0,0,0.08)"
            }}
          >

            <h2
              style={{
                marginBottom: "25px",
                color: "#ef4444",
                fontSize: "28px",
                fontWeight: "800"
              }}
            >
              Risk Alerts
            </h2>

            {

              aiData.risky_companies.map(
                (company, index) => (

                  <div
                    key={index}
                    style={{
                      marginBottom: "25px",
                      paddingBottom: "20px",
                      borderBottom:
                        "1px solid #e2e8f0"
                    }}
                  >

                    <h3
                      style={{
                        fontSize: "18px",
                        marginBottom: "10px"
                      }}
                    >
                      {company.company_name}
                    </h3>

                    <p
                      style={{
                        marginBottom: "12px"
                      }}
                    >
                      Score:
                      {" "}
                      {
                        Number(
                          company.health_score || 0
                        ).toFixed(2)
                      }
                    </p>

                    <span
                      className="rating-badge rating-poor"
                    >
                      POOR
                    </span>

                  </div>

                )
              )

            }

          </div>

          {/* HIGH ROE */}

          <div
            className="dashboard-card"
            style={{
              padding: "28px",
              borderRadius: "24px",
              background: "white",
              boxShadow:
                "0 10px 25px rgba(0,0,0,0.08)"
            }}
          >

            <h2
              style={{
                marginBottom: "25px",
                color: "#2563eb",
                fontSize: "28px",
                fontWeight: "800"
              }}
            >
              High ROE Companies
            </h2>

            {

              aiData.high_roe.map(
                (company, index) => (

                  <div
                    key={index}
                    style={{
                      marginBottom: "25px",
                      paddingBottom: "20px",
                      borderBottom:
                        "1px solid #e2e8f0"
                    }}
                  >

                    <h3
                      style={{
                        fontSize: "18px",
                        marginBottom: "10px"
                      }}
                    >
                      {company.company_name}
                    </h3>

                    <p>
                      ROE:
                      {" "}
                      {company.roe || "N/A"}
                    </p>

                  </div>

                )
              )

            }

          </div>

        </div>

      </div>

      {/* TOP COMPANIES */}

      <div
        className="dashboard-card"
        style={{
          padding: "30px",
          borderRadius: "26px",
          background: "white",
          boxShadow:
            "0 10px 25px rgba(0,0,0,0.08)"
        }}
      >

        <h2
          style={{
            marginBottom: "25px",
            fontSize: "32px",
            fontWeight: "800"
          }}
        >
          Top Companies
        </h2>

        <table
          className="modern-table"
          style={{
            width: "100%",
            borderCollapse: "collapse",
            overflow: "hidden",
            borderRadius: "18px"
          }}
        >

          <thead>

            <tr
              style={{
                background:
                  "#020b24",
                color: "white"
              }}
            >

              <th
                style={{
                  padding: "20px",
                  textAlign: "left"
                }}
              >
                Symbol
              </th>

              <th
                style={{
                  padding: "20px",
                  textAlign: "left"
                }}
              >
                Health Score
              </th>

              <th
                style={{
                  padding: "20px",
                  textAlign: "left"
                }}
              >
                Rating
              </th>

            </tr>

          </thead>

          <tbody>

            {

              topCompanies.map(
                (company, index) => (

                  <tr
                    key={index}
                    style={{
                      borderBottom:
                        "1px solid #e2e8f0"
                    }}
                  >

                    <td
                      style={{
                        padding: "20px"
                      }}
                    >
                      {company.symbol}
                    </td>

                    <td
                      style={{
                        padding: "20px"
                      }}
                    >

                      {
                        Number(
                          company.health_score || 0
                        ).toFixed(2)
                      }

                    </td>

                    <td
                      style={{
                        padding: "20px"
                      }}
                    >

                      <span
                        className={

                          company.rating ===
                          "EXCELLENT"

                            ?

                            "rating-badge rating-excellent"

                            :

                          company.rating ===
                          "GOOD"

                            ?

                            "rating-badge rating-good"

                            :

                          company.rating ===
                          "AVERAGE"

                            ?

                            "rating-badge rating-average"

                            :

                          company.rating ===
                          "WEAK"

                            ?

                            "rating-badge rating-weak"

                            :

                            "rating-badge rating-poor"

                        }
                      >

                        {
                          company.rating
                        }

                      </span>

                    </td>

                  </tr>

                )
              )

            }

          </tbody>

        </table>

      </div>

    </div>

  );

}

export default HomePage;