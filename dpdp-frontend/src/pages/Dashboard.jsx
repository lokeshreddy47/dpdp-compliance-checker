import Sidebar from "../components/Sidebar";
import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

function Dashboard() {
  const { user } = useAuth();

  return (
    <div className="flex">
      <Sidebar />

      <div className="ml-64 p-10 w-full bg-gray-100 dark:bg-gray-900 dark:text-gray-100 min-h-screen">

        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">
            Compliance Dashboard
          </h1>
          {user && (
            <p className="text-gray-600 dark:text-gray-300">
              Welcome back, {user.displayName}! Ready to check DDPD compliance?
            </p>
          )}
        </div>

        <div className="grid grid-cols-3 gap-8">

          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="glass glass-hover p-6 rounded-xl shadow-lg"
          >
            <h2 className="text-lg font-semibold">
              Compliance Score
            </h2>
            <p className="text-gray-600 dark:text-gray-300 mt-2">
              AI calculated DPDP compliance score
            </p>
          </motion.div>

          <Link to="/upload">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="glass glass-hover p-6 rounded-xl shadow-lg cursor-pointer"
            >
              <h2 className="text-lg font-semibold">
                Policy Upload
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mt-2">
                Upload privacy policy for analysis
              </p>
            </motion.div>
          </Link>

          <Link to="/reports">
            <motion.div
              whileHover={{ scale: 1.05 }}
              className="glass glass-hover p-6 rounded-xl shadow-lg cursor-pointer"
            >
              <h2 className="text-lg font-semibold">
                Reports
              </h2>
              <p className="text-gray-600 dark:text-gray-300 mt-2">
                View compliance reports
              </p>
            </motion.div>
          </Link>

        </div>

      </div>
    </div>
  );
}

export default Dashboard;