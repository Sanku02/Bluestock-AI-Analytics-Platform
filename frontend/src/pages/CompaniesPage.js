import { useEffect, useState, useCallback } from "react";

import { Link } from "react-router-dom";

import API from "../services/api";

import Loader from "../components/Loader";

function CompaniesPage() {

  const [companies, setCompanies] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [search, setSearch] =
    useState("");

  const [sortBy, setSortBy] =
    useState("health_score");

  const [sortOrder, setSortOrder] =
    useState("desc");

  const [currentPage, setCurrentPage] =
    useState(1);

  const companiesPerPage = 10;

  const fetchCompanies = useCallback(
    async () => {

      try {

        const response =
          await API.get(
            "/health-scores/"
          );

        setCompanies(
          response.data
        );

      }

      catch (error) {

        console.error(error);

      }

      finally {

        setLoading(false);

      }

    },
    []
  );

  useEffect(() => {

    fetchCompanies();

  }, [fetchCompanies]);

  const filteredCompanies =

    companies

      .filter((company) =>

        company.symbol
          .toLowerCase()
          .includes(
            search.toLowerCase()
          )

      )

      .sort((a, b) => {

        let comparison = 0;

        if (sortBy === "symbol") {

          comparison =
            a.symbol.localeCompare(
              b.symbol
            );

        }

        else {

          comparison =
            a[sortBy] - b[sortBy];

        }

        return sortOrder === "asc"

          ? comparison

          : -comparison;

      });

  const indexOfLast =
    currentPage * companiesPerPage;

  const indexOfFirst =
    indexOfLast - companiesPerPage;

  const currentCompanies =
    filteredCompanies.slice(
      indexOfFirst,
      indexOfLast
    );

  const totalPages =
    Math.ceil(
      filteredCompanies.length
      /
      companiesPerPage
    );

  if (loading) {

    return <Loader />;

  }

  return (

    <div className="page-container">

      <div
        style={{
          background:
            "linear-gradient(135deg, #020617 0%, #001845 55%, #1e293b 100%)",
          borderRadius: "28px",
          padding: "42px",
          marginBottom: "34px",
          color: "white",
          boxShadow:
            "0 12px 40px rgba(15, 23, 42, 0.18)"
        }}
      >

        <h1
          style={{
            fontSize: "56px",
            fontWeight: "800",
            marginBottom: "12px",
            letterSpacing: "-1px"
          }}
        >
          Companies
        </h1>

        <p
          style={{
            fontSize: "20px",
            opacity: 0.9,
            marginBottom: "28px"
          }}
        >
          Browse and analyze company health scores
        </p>

      </div>

      <div
        className="dashboard-card"
        style={{
          marginBottom: "30px",
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

          <input
            type="text"
            placeholder="Search company symbol..."
            value={search}
            onChange={(e) =>
              setSearch(
                e.target.value
              )
            }
            className="modern-input"
            style={{
              width: "260px"
            }}
          />

          <select
            value={sortBy}
            onChange={(e) =>
              setSortBy(
                e.target.value
              )
            }
            className="modern-input"
          >

            <option value="health_score">
              Health Score
            </option>

            <option value="symbol">
              Alphabetical
            </option>

          </select>

          <select
            value={sortOrder}
            onChange={(e) =>
              setSortOrder(
                e.target.value
              )
            }
            className="modern-input"
          >

            <option value="desc">
              Descending
            </option>

            <option value="asc">
              Ascending
            </option>

          </select>

        </div>

      </div>

      <div
        className="dashboard-card"
        style={{
          overflowX: "auto",
          padding: "0"
        }}
      >

        <table
          style={{
            width: "100%",
            borderCollapse:
              "collapse"
          }}
        >

          <thead>

            <tr
              style={{
                background:
                  "linear-gradient(90deg,#020617,#0f172a)",
                color: "white"
              }}
            >

              <th style={tableHead}>
                Company
              </th>

              <th style={tableHead}>
                Health Score
              </th>

              <th style={tableHead}>
                Rating
              </th>

              <th style={tableHead}>
                Action
              </th>

            </tr>

          </thead>

          <tbody>

            {

              currentCompanies.map(

                (company, index) => (

                  <tr
                    key={index}
                    className="table-row-hover"
                    style={{
                      borderBottom:
                        "1px solid #e2e8f0",
                      transition:
                        "all 0.2s ease"
                    }}
                  >

                    <td style={tableCell}>

                      <div>

                        <div
                          style={{
                            fontWeight: "700",
                            fontSize: "17px",
                            color: "#0f172a",
                            marginBottom: "5px"
                          }}
                        >
                          {company.company_name}
                        </div>

                        <div
                          style={{
                            fontSize: "13px",
                            color: "#64748b",
                            fontWeight: "500",
                            letterSpacing: "0.5px"
                          }}
                        >
                          {company.symbol}
                        </div>

                      </div>

                    </td>

                    <td style={tableCell}>

                      {
                        company.health_score
                          .toFixed(2)
                      }

                    </td>

                    <td style={tableCell}>

                      <span
                        className={`company-ribbon ribbon-${company.rating.toLowerCase()}`}
                      >
                        {company.rating}
                      </span>

                    </td>

                    <td style={tableCell}>

                      <Link
                        to={`/company/${company.symbol}`}
                        style={{
                          background:
                            "#2563eb",
                          color: "white",
                          padding:
                            "10px 18px",
                          borderRadius:
                            "10px",
                          textDecoration:
                            "none",
                          fontWeight:
                            "600",
                          fontSize:
                            "14px",
                          display:
                            "inline-block"
                        }}
                      >
                        View
                      </Link>

                    </td>

                  </tr>

                )

              )

            }

          </tbody>

        </table>

      </div>

      <div
        style={{
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          gap: "20px",
          marginTop: "35px"
        }}
      >

        <button
          className="primary-button"
          disabled={
            currentPage === 1
          }
          onClick={() =>
            setCurrentPage(
              currentPage - 1
            )
          }
        >
          Previous
        </button>

        <div
          style={{
            fontWeight: "600",
            color: "#0f172a"
          }}
        >
          Page {currentPage} of {totalPages}
        </div>

        <button
          className="primary-button"
          disabled={
            currentPage === totalPages
          }
          onClick={() =>
            setCurrentPage(
              currentPage + 1
            )
          }
        >
          Next
        </button>

      </div>

    </div>

  );

}

const tableHead = {

  padding: "20px",
  textAlign: "left",
  fontSize: "15px",
  fontWeight: "700"

};

const tableCell = {

  padding: "20px",
  fontSize: "15px",
  color: "#0f172a"

};

export default CompaniesPage;