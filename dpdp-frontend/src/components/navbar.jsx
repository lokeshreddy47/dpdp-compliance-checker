import { Link } from "react-router-dom";
import { useState, useEffect } from "react";
import { useAuth } from "../context/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    if (saved === "dark") {
      setDarkMode(true);
    } else if (saved === "light") {
      setDarkMode(false);
    } else if (window.matchMedia) {
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      setDarkMode(prefersDark);
    }
  }, []);

  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.body.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  }, [darkMode]);

  return (
    <div className="bg-gradient-to-r from-blue-700 to-indigo-800 text-white p-4 flex justify-between items-center">
      <h1 className="text-xl font-bold">
        DPDP Compliance Checker
      </h1>

      <div className="flex items-center gap-6">
        {user ? (
          <>
            <Link to="/dashboard" className="hover:text-blue-200 transition">Dashboard</Link>
            <Link to="/upload" className="hover:text-blue-200 transition">Analyze Policy</Link>
            <Link to="/reports" className="hover:text-blue-200 transition">Reports</Link>

            <span className="text-sm">
              Welcome, {user.displayName}
            </span>

            <button
              onClick={logout}
              className="bg-red-500 hover:bg-red-600 px-4 py-2 rounded transition"
            >
              Logout
            </button>
          </>
        ) : (
          <Link to="/" className="hover:text-blue-200 transition">Login</Link>
        )}

        <button
          onClick={() => setDarkMode(!darkMode)}
          aria-label="Toggle theme"
          className="text-2x bg-white/10 p-2 rounded-full hover:bg-white/20 transition"
        >
          {darkMode ? "⚒" : "🖏"}
        </button>
      </div>
    </div>
  );
}

export default Navbar;