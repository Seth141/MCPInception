'use client';

import { useState } from 'react';

export default function Home() {
  const [url, setUrl] = useState('');
  const [serverName, setServerName] = useState('');
  const [results, setResults] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    alert('Button clicked - handleSubmit triggered');
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);
    
    try {
      alert('About to fetch from local API proxy');
      const apiUrl = new URL('/api/yc', window.location.origin);

      alert(window.location.origin);
      
      // Add the URL and server name as query parameters if they're provided
      if (url) {
        apiUrl.searchParams.append('url', url);
      }
      if (serverName) {
        apiUrl.searchParams.append('serverName', serverName);
      }
      
      const response = await fetch(apiUrl.toString(), {
        method: 'GET',
        headers: {
          'Accept': 'application/json'
        }
      });
      alert('Response received');

      
      if (!response.ok) {
        alert('bad response');
        alert(`Server responded with status: ${response.status}`);
        throw new Error(`Server responded with status: ${response.status}`);
        
      }

      try {
        alert('About to parse JSON');
        const data = await response.json();
        alert('JSON parsed successfully: ' + JSON.stringify(data).substring(0, 100));
        setResults(JSON.stringify(data, null, 2));
      } catch (jsonError) {
        alert('JSON parsing error: ' + (jsonError instanceof Error ? jsonError.message : 'Unknown JSON error'));
        throw jsonError;
      }
    } catch (err) {
      console.error('Error calling scrape endpoint:', err);
      setError(err instanceof Error ? err.message : 'An unknown error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black flex flex-col items-center justify-center p-6">
      <h1 className="text-4xl font-bold text-white mb-10">Incept</h1>
      
      <div className="w-full max-w-md">
        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-white text-sm font-semibold mb-2" htmlFor="url">
              Website URL
            </label>
            <input 
              className="w-full px-3 py-2 bg-transparent border border-gray-600 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              id="url"
              type="url"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-white text-sm font-semibold mb-2" htmlFor="name">
              Server Name
            </label>
            <input 
              className="w-full px-3 py-2 bg-transparent border border-gray-600 rounded-md text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              id="name"
              type="text"
              placeholder="my-mcp-server"
              value={serverName}
              onChange={(e) => setServerName(e.target.value)}
            />
          </div>
          
          <button 
            className="w-full py-3 px-4 text-white font-bold rounded-md bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            type="submit"
            disabled={loading}
          >
            {loading ? 'Processing...' : 'Generate MCP'}
          </button>
        </form>
        
        {error && (
          <div className="mt-6 p-4 border border-red-500 rounded-md bg-transparent text-red-500">
            <p className="font-semibold">Error:</p>
            <p>{error}</p>
          </div>
        )}
        
        {results && (
          <div className="mt-6">
            <p className="text-white font-semibold mb-2">Results:</p>
            <pre className="p-4 bg-gray-900 text-green-400 rounded-md overflow-auto text-sm whitespace-pre-wrap max-h-80">
              {results}
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}
