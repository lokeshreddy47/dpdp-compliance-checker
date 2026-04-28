import { Link, useNavigate } from "react-router-dom";

function Layout({ children }) {

  const navigate = useNavigate();

  const handleLogout = () => {
    navigate("/");
  };

  return (

    <div className="flex min-h-screen">

      {/* Sidebar */}
      <div className="w-64 bg-white text-gray-900 dark:bg-gray-900 dark:text-white p-6">

        <h1 className="text-xl font-bold mb-8">
          DPDP Checker
        </h1>

        <nav className="space-y-4">

          <Link to="/dashboard" className="block hover:text-gray-300">
            Dashboard
          </Link>

          <Link to="/upload" className="block hover:text-gray-300">
            Upload Policy
          </Link>

          <Link to="/reports" className="block hover:text-gray-300">
            Reports
          </Link>

          <Link to="/analytics" className="block hover:text-gray-300">
            Analytics
          </Link>

        </nav>

        <button
          onClick={handleLogout}
          className="mt-10 bg-red-500 px-4 py-2 rounded w-full"
        >
          Logout
        </button>

      </div>

      {/* Page Content */}
      <div className="flex-1 p-10 bg-gray-100">
        {children}
      </div>

    </div>

  );

}

export default Layout;