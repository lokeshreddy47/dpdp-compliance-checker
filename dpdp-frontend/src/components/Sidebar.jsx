import { NavLink } from "react-router-dom";

function Sidebar() {

  return (

    <div className="w-64 h-screen bg-gradient-to-b from-indigo-900 to-black text-white p-6 fixed">

      <h1 className="text-2xl font-bold mb-10">
        DPDP Checker
      </h1>

      <nav className="space-y-4">

        <NavLink
          to="/dashboard"
          className="block p-2 rounded hover:bg-white/10"
        >
          Dashboard
        </NavLink>

        <NavLink
          to="/upload"
          className="block p-2 rounded hover:bg-white/10"
        >
          Analyze Policy
        </NavLink>

        <NavLink
          to="/reports"
          className="block p-2 rounded hover:bg-white/10"
        >
          Reports
        </NavLink>

      </nav>

    </div>

  );
}

export default Sidebar;
