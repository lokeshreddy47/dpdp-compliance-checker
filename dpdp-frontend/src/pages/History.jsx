import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import Sidebar from '../components/layout';
import API from '../services/api';

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      setLoading(true);
      try {
        const response = await API.get('/history/');
        setHistory(response.data);
      } catch (err) {
        const stored = localStorage.getItem('complianceHistory');
        if (stored) {
          const parsed = JSON.parse(stored);
          setHistory(Array.isArray(parsed) ? parsed : [parsed]);
        }
      }
    } catch (err) {
      console.error('History fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  const exportToCSV = () => {
    if (history.length === 0) {
      alert('No history to export');
      return;
    }

    const headers = ['URL/File', 'Compliance Score', 'Risk Level', 'Date'];
    const rows = history.map(item => [
      item.url || item.file || 'N/A',
      (item.compliance_score || item.complianceScore || 0) + '%',
      item.risk_level || item.riskLevel || 'Unknown',
      item.date || new Date().toLocaleDateString()
    ]);

    const csvContent = [
      headers.join(','),
      ...rows.map(row => row.map(cell => '"' + cell + '"').join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'compliance-history-' + new Date().toISOString().split('T')[0] + '.csv';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
  };

  const filteredHistory = filter === 'all' 
    ? history 
    : history.filter(item => {
        const risk = (item.risk_level || item.riskLevel || '').toLowerCase();
        return risk === filter.toLowerCase();
      });

  return (
    <Sidebar>
      <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="p-6 md:p-8"
        >
          <div className="mb-8">
            <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
              📊 Scan History
            </h1>
            <p className="text-gray-600 dark:text-gray-400">
              View your previous compliance analysis scans
            </p>
          </div>

          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="flex gap-2">
              {['all', 'low', 'medium', 'high'].map(level => (
                <button
                  key={level}
                  onClick={() => setFilter(level)}
                  className={'px-4 py-2 rounded-lg font-semibold transition-all ' + (
                    filter === level
                      ? 'bg-blue-500 text-white shadow-lg'
                      : 'bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300'
                  )}
                >
                  {level.charAt(0).toUpperCase() + level.slice(1)}
                </button>
              ))}
            </div>
            <button
              onClick={exportToCSV}
              disabled={history.length === 0}
              className="px-4 py-2 bg-green-500 hover:bg-green-600 disabled:bg-gray-400 text-white rounded-lg font-semibold"
            >
              📥 Export CSV
            </button>
            <button
              onClick={fetchHistory}
              className="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg font-semibold"
            >
              🔄 Refresh
            </button>
          </div>

          {loading && (
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
              className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full mx-auto my-8"
            />
          )}

          {!loading && filteredHistory.length === 0 && (
            <div className="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-lg">
              <p className="text-2xl text-gray-500 dark:text-gray-400 mb-2">
                📭 No scans found
              </p>
            </div>
          )}

          {!loading && filteredHistory.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {filteredHistory.map((item, idx) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  whileHover={{ y: -5 }}
                  className="glass dark:glass-dark p-6 rounded-xl"
                >
                  <h3 className="font-semibold text-lg text-gray-900 dark:text-white mb-2 truncate">
                    {item.url || item.file || 'Unknown'}
                  </h3>
                  <div className="mb-4">
                    <div className="flex justify-between mb-2">
                      <span className="text-sm text-gray-600 dark:text-gray-400">Compliance</span>
                      <span className="font-bold text-blue-600 dark:text-blue-400">
                        {item.compliance_score || item.complianceScore || 0}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                      <div
                        className="bg-gradient-to-r from-blue-500 to-blue-600 h-full rounded-full transition-all"
                        style={{ width: (item.compliance_score || item.complianceScore || 0) + '%' }}
                      />
                    </div>
                  </div>
                  <span className="inline-block px-3 py-1 rounded-full text-sm font-semibold bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-100">
                    {item.risk_level || item.riskLevel || 'Unknown'} Risk
                  </span>
                  <p className="text-xs text-gray-600 dark:text-gray-400 mt-3">
                    {item.date || new Date().toLocaleDateString()}
                  </p>
                </motion.div>
              ))}
            </div>
          )}

          {!loading && history.length > 0 && (
            <div className="mt-8 grid grid-cols-3 gap-4 bg-gray-50 dark:bg-gray-800 rounded-lg p-6">
              <div className="text-center">
                <p className="text-2xl font-bold text-blue-600">{history.length}</p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Total Scans</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-green-600">
                  {history.filter(h => (h.risk_level || h.riskLevel || '').toLowerCase() === 'low').length}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">Low Risk</p>
              </div>
              <div className="text-center">
                <p className="text-2xl font-bold text-red-600">
                  {history.filter(h => (h.risk_level || h.riskLevel || '').toLowerCase() === 'high').length}
                </p>
                <p className="text-sm text-gray-600 dark:text-gray-400">High Risk</p>
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </Sidebar>
  );
}
