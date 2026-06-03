import {

  BrowserRouter,

  Routes,

  Route,

  NavLink

} from "react-router-dom";

import HomePage from "./pages/HomePage";

import CompaniesPage from "./pages/CompaniesPage";

import CompanyDetailPage from "./pages/CompanyDetailPage";

import ScreenerPage from "./pages/ScreenerPage";

import ComparePage from "./pages/ComparePage";

import SectorPage from "./pages/SectorPage";

function App() {

  const navStyle = ({ isActive }) => ({

    color: isActive
      ? "#ffffff"
      : "#94a3b8",

    textDecoration: "none",

    fontWeight: "600",

    padding: "10px 18px",

    borderRadius: "10px",

    background: isActive
      ? "#2563eb"
      : "transparent",

    transition: "0.3s"

  });

  return (

    <BrowserRouter>

      <div
        style={{
          minHeight: "100vh",
          background: "#f5f7fb"
        }}
      >

        {/* NAVBAR */}

        <nav
          style={{
            position: "sticky",
            top: 0,
            zIndex: 1000,

            background:
              "linear-gradient(90deg, #020617, #0f172a)",

            padding: "18px 40px",

            display: "flex",

            justifyContent: "space-between",

            alignItems: "center",

            boxShadow:
              "0 4px 20px rgba(0,0,0,0.15)"
          }}
        >

          <div>

            <h2
              style={{
                color: "white",
                margin: 0,
                fontSize: "28px"
              }}
            >
              Bluestock AI
            </h2>

          </div>

          <div
            style={{
              display: "flex",
              gap: "14px"
            }}
          >

            <NavLink
              to="/"
              style={navStyle}
            >
              Dashboard
            </NavLink>

            <NavLink
              to="/companies"
              style={navStyle}
            >
              Companies
            </NavLink>

            <NavLink
              to="/screener"
              style={navStyle}
            >
              Screener
            </NavLink>

            <NavLink
              to="/compare"
              style={navStyle}
            >
              Compare
            </NavLink>

            <NavLink
              to="/sector"
              style={navStyle}
            >
              Sectors
            </NavLink>

          </div>

        </nav>

        {/* ROUTES */}

        <Routes>

          <Route
            path="/"
            element={<HomePage />}
          />

          <Route
            path="/companies"
            element={<CompaniesPage />}
          />

          <Route
            path="/company/:symbol"
            element={<CompanyDetailPage />}
          />

          <Route
            path="/screener"
            element={<ScreenerPage />}
          />

          <Route
            path="/compare"
            element={<ComparePage />}
          />

          <Route
            path="/sector"
            element={<SectorPage />}
          />

        </Routes>

      </div>

    </BrowserRouter>

  );

}

export default App;