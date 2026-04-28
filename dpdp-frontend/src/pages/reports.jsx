import { useEffect, useState } from "react";
import API from "../services/api";

function Reports() {

  const [reports, setReports] = useState([]);

  useEffect(() => {

    const fetchReports = async () => {

      try {

        const response = await API.get("/reports-history");

        setReports(response.data);

      } catch (error) {

        console.error(error);

      }

    };

    fetchReports();

  }, []);

  return (

    <div className="p-10">

      <h1 className="text-2xl font-bold mb-6">
        Compliance Reports
      </h1>

      {reports.length === 0 && (
        <p>No reports generated yet.</p>
      )}

      {reports.map((report, index) => (

        <div
          key={index}
          className="border rounded p-4 mb-4 bg-gray-50"
        >

          <p>
            <b>Policy File:</b> {report.filename}
          </p>

          <p>
            <b>Compliance Score:</b> {report.score}%
          </p>

          <p>
            <b>Risk Level:</b> {report.risk}
          </p>

          <p>
            <b>Date:</b> {report.date}
          </p>

        </div>

      ))}

    </div>

  );

}

export default Reports;