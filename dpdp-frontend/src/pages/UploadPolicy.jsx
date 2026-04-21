import Sidebar from "../components/Sidebar";
import { useState } from "react";
import API from "../services/api";

function UploadPolicy({ user }) {

  const [file, setFile] = useState(null);
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // File Upload Analysis
  const handleUpload = async () => {

    if (!file) {
      setError("Please upload a file");
      return;
    }

    const formData = new FormData();
    formData.append("website_url", file.name); // Use filename as URL for file upload

    try {
      setLoading(true);
      setError(null);

      // For file upload, we'll use the URL endpoint with a simulated URL
      const response = await API.post("/check-compliance/", formData);

      setResult(response.data);

    } catch (error) {
      console.error(error);
      setError("Error analyzing policy. Please try again.");
    }

    setLoading(false);
  };

  // URL Analysis
  const handleURLAnalysis = async () => {

    if (!url) {
      setError("Enter website URL");
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const formData = new FormData();
      formData.append("website_url", url);

      const response = await API.post("/check-compliance/", formData);

      setResult(response.data);

    } catch (error) {
      console.error(error);
      setError("Error analyzing URL. Please check the URL and try again.");
    }

    setLoading(false);
  };

  // Download Report
  const handleDownloadReport = () => {
    window.open("http://localhost:8000/download-report", "_blank");
  };

  return (

    <div className="flex">

      {/* Sidebar */}

      <Sidebar />

      {/* Main Content */}

      <div className="ml-64 p-10 w-full bg-gray-100 dark:bg-gray-900 dark:text-gray-100 min-h-screen">

        <h1 className="text-3xl font-bold mb-8">
          DPDP Act 2023 Compliance Checker
        </h1>

        {/* Upload Section */}

        <div className="glass p-6 rounded-xl shadow mb-6">

          <h2 className="text-lg font-semibold mb-3">
            Upload Privacy Policy File
          </h2>

          <input
            type="file"
            onChange={(e) => setFile(e.target.files[0])}
          />

          <button
            className="ml-4 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded"
            onClick={handleUpload}
          >
            Analyze File
          </button>

        </div>

        {/* URL Analysis */}

        <div className="glass p-6 rounded-xl shadow mb-6">

          <h2 className="text-lg font-semibold mb-3">
            Analyze Website Privacy Policy URL
          </h2>

          <input
            type="text"
            placeholder="Enter privacy policy URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="border p-2 w-96 rounded"
          />

          <button
            className="ml-4 bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded"
            onClick={handleURLAnalysis}
          >
            Analyze URL
          </button>

        </div>

        {/* Loading */}
          {loading && (
          <div className="bg-blue-100 dark:bg-blue-900 border-l-4 border-blue-500 dark:border-blue-300 text-blue-700 dark:text-blue-200 p-4 mb-6 rounded">
            <div className="flex items-center">
              <div className="animate-spin rounded-full h-6 w-6 border-2 border-blue-500 border-t-transparent mr-3"></div>
              AI analyzing privacy policy... Please wait
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="bg-red-100 dark:bg-red-900 border-l-4 border-red-500 dark:border-red-300 text-red-700 dark:text-red-200 p-4 mb-6 rounded">
            <p className="font-semibold">Error</p>
            <p>{error}</p>
          </div>
        )}

        {/* Results */}

        {result && (

          <div className="glass p-6 rounded-xl shadow">

            {/* Score */}

            <h2 className="text-2xl font-bold mb-4">
              Compliance Score: {result.overall_score}%
            </h2>

            {/* Risk Level */}

            <div className="mb-4">

              <p className="font-semibold mb-2">
                Risk Level
              </p>

              {result.risk_level === "Low Risk" && (
                <div className="bg-gradient-to-r from-green-100 to-emerald-100 dark:from-emerald-900 border-l-4 border-green-500 dark:border-green-300 text-green-700 dark:text-green-200 p-3 rounded w-48">
                  Low Risk
                </div>
              )}

              {result.risk_level === "Medium Risk" && (
                <div className="bg-gradient-to-r from-yellow-100 to-amber-100 dark:from-amber-900 border-l-4 border-yellow-500 dark:border-yellow-300 text-yellow-700 dark:text-yellow-200 p-3 rounded w-48">
                  Medium Risk
                </div>
              )}

              {result.risk_level === "High Risk" && (
                <div className="bg-gradient-to-r from-red-100 to-rose-100 dark:from-rose-900 border-l-4 border-red-500 dark:border-red-300 text-red-700 dark:text-red-200 p-3 rounded w-48">
                  High Risk
                </div>
              )}

            </div>

            {/* Missing Clauses */}

            <h3 className="font-semibold mt-6">
              Missing DPDP Clauses
            </h3>

            <ul className="list-disc ml-6 mt-2">

              {result.missing_clauses.map((clause, index) => (

                <li key={index} className="dark:text-gray-200">{clause}</li>

              ))}

            </ul>

            {/* Recommendations */}

            {result.recommendations && (

              <>

                <h3 className="font-semibold mt-6">
                  AI Recommendations
                </h3>

                <ul className="list-disc ml-6 mt-2">

                  {result.recommendations.map((rec, index) => (

                    <li key={index}>{rec}</li>

                  ))}

                </ul>

              </>

            )}

            {/* Chart */}

            <h3 className="text-xl font-bold mt-8">
              Compliance Chart
            </h3>

            <img
              src={`http://127.0.0.1:8000/${result.graph_path}`}
              alt="Compliance Chart"
              className="mt-4 w-full max-w-3xl border rounded"
            />

            {/* Download Report Button */}
            <div className="mt-6 text-center">
              <button
                onClick={handleDownloadReport}
                className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-semibold shadow-lg transition"
              >
                📄 Download PDF Report
              </button>
            </div>

          </div>

        )}

      </div>

    </div>

  );

}

export default UploadPolicy;