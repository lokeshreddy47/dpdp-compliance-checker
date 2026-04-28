import { useEffect, useState } from "react";
import API from "../services/api";

import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend
} from "chart.js";

import { Pie } from "react-chartjs-2";

ChartJS.register(ArcElement, Tooltip, Legend);

function Analytics() {

  const [reports, setReports] = useState([]);

  useEffect(() => {

    const fetchReports = async () => {

      const response = await API.get("/reports-history");

      setReports(response.data);

    };

    fetchReports();

  }, []);

  const totalPolicies = reports.length;

  const averageScore =
    reports.length > 0
      ? (
          reports.reduce((sum, r) => sum + r.score, 0) /
          reports.length
        ).toFixed(2)
      : 0;

  const lowRisk = reports.filter(r => r.risk === "Low Risk").length;
  const mediumRisk = reports.filter(r => r.risk === "Medium Risk").length;
  const highRisk = reports.filter(r => r.risk === "High Risk").length;

  const chartData = {
    labels: ["Low Risk", "Medium Risk", "High Risk"],
    datasets: [
      {
        label: "Risk Distribution",
        data: [lowRisk, mediumRisk, highRisk],
        backgroundColor: [
          "#22c55e",
          "#f59e0b",
          "#ef4444"
        ]
      }
    ]
  };

  return (

    <div className="p-10">

      <h1 className="text-2xl font-bold mb-6">
        Compliance Analytics
      </h1>

      <div className="grid grid-cols-2 gap-6 mb-10">

        <div className="border rounded p-6 bg-gray-50">
          <h2 className="text-lg font-semibold">
            Total Policies Analyzed
          </h2>
          <p className="text-3xl mt-2">{totalPolicies}</p>
        </div>

        <div className="border rounded p-6 bg-gray-50">
          <h2 className="text-lg font-semibold">
            Average Compliance Score
          </h2>
          <p className="text-3xl mt-2">{averageScore}%</p>
        </div>

      </div>

      <div className="max-w-md">

        <h2 className="text-xl font-semibold mb-4">
          Risk Distribution
        </h2>

        <Pie data={chartData} />

      </div>

    </div>

  );

}

export default Analytics;