'use client';

import { useState } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

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
    <div className="min-h-screen relative overflow-hidden">
      <Header />
      
      <main className="relative pt-24 pb-16">
        <div className="text-center mb-12">
          <h1 className="text-7xl font-bold text-white mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-400">MCP Inception</h1>
          <p className="text-xl text-gray-300 max-w-2xl mx-auto flex justify-center gap-2">
            <span className="inline-block animate-rise-1">Dream</span>
            <span className="inline-block animate-rise-2">it,</span>
            <span className="inline-block animate-rise-3">build</span>
            <span className="inline-block animate-rise-4">it.</span>
            <span className="inline-block animate-rise-5">Plug</span>
            <span className="inline-block animate-rise-6">and</span>
            <span className="inline-block animate-rise-7">Play.</span>
          </p>
        </div>

        <div className="w-full max-w-md mx-auto mb-16">
          <div className="backdrop-blur-lg bg-white/5 rounded-2xl p-8 relative before:absolute before:inset-0 before:rounded-2xl before:p-[2px] before:bg-gradient-to-r before:from-purple-500/50 before:via-purple-400/30 before:to-purple-500/50 before:blur-[4px] before:-z-10">
            <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-black via-gray-900 to-black -z-10"></div>
            <form onSubmit={handleSubmit}>
              <div className="mb-6">
                <label className="block text-white text-sm font-semibold mb-2" htmlFor="url">
                  Website URL
                </label>
                <input 
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
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
                  className="w-full px-4 py-3 bg-white/5 border border-white/10 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:border-purple-500/50 transition-all"
                  id="name"
                  type="text"
                  placeholder="my-mcp-server"
                  value={serverName}
                  onChange={(e) => setServerName(e.target.value)}
                />
              </div>
              
              <div className="flex justify-center">
                <button 
                  className="w-48 py-2.5 px-4 text-white font-bold rounded-lg bg-purple-900/80 hover:bg-purple-800 focus:outline-none focus:ring-2 focus:ring-purple-500/50 focus:ring-offset-2 focus:ring-offset-gray-900 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-purple-500/25 relative overflow-hidden group"
                  type="submit"
                  disabled={loading}
                  onClick={(e) => {
                    const button = e.currentTarget;
                    const ripple = document.createElement('span');
                    const rect = button.getBoundingClientRect();
                    
                    const size = Math.max(rect.width, rect.height);
                    const x = e.clientX - rect.left - size / 2;
                    const y = e.clientY - rect.top - size / 2;
                    
                    ripple.style.width = ripple.style.height = `${size}px`;
                    ripple.style.left = `${x}px`;
                    ripple.style.top = `${y}px`;
                    ripple.className = 'absolute bg-white/20 rounded-full animate-ripple';
                    
                    button.appendChild(ripple);
                    
                    ripple.addEventListener('animationend', () => {
                      ripple.remove();
                    });
                  }}
                >
                  <span className="relative z-10 flex items-center justify-center">
                    {loading ? 'Processing...' : 'Generate MCP'}
                    <span className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/50 to-purple-500/0 translate-x-[-100%] group-hover:translate-x-[100%] transition-transform duration-1000"></span>
                  </span>
                  <div className="absolute inset-0 bg-gradient-to-r from-purple-500/0 via-purple-500/30 to-purple-500/0 animate-pulse"></div>
                  <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-purple-500/0 via-purple-500/20 to-purple-500/0 animate-shimmer"></div>
                </button>
              </div>
            </form>
          </div>
        </div>

        <div className="w-full max-w-6xl mx-auto px-4">
          <h2 className="text-3xl font-bold text-white text-center mb-12">Why Choose MCP Inception?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="backdrop-blur-lg bg-white/5 rounded-2xl p-6 relative before:absolute before:inset-0 before:rounded-2xl before:p-[1px] before:bg-gradient-to-r before:from-purple-500/30 before:via-purple-400/20 before:to-purple-500/30 before:blur-[2px] before:-z-10 hover:before:from-purple-500/40 hover:before:via-purple-400/30 hover:before:to-purple-500/40 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:shadow-purple-500/20">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-black via-gray-900 to-black -z-10"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4 animate-float">
                  <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">Lightning Fast</h3>
                <p className="text-gray-300">Generate a complete MCP server in seconds, not hours. Our automated process handles everything for you.</p>
              </div>
            </div>

            <div className="backdrop-blur-lg bg-white/5 rounded-2xl p-6 relative before:absolute before:inset-0 before:rounded-2xl before:p-[1px] before:bg-gradient-to-r before:from-purple-500/30 before:via-purple-400/20 before:to-purple-500/30 before:blur-[2px] before:-z-10 hover:before:from-purple-500/40 hover:before:via-purple-400/30 hover:before:to-purple-500/40 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:shadow-purple-500/20">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-black via-gray-900 to-black -z-10"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4 animate-float">
                  <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">Zero Configuration</h3>
                <p className="text-gray-300">No need to manually configure servers or deal with complex setup processes. Just input the URL and go.</p>
              </div>
            </div>

            <div className="backdrop-blur-lg bg-white/5 rounded-2xl p-6 relative before:absolute before:inset-0 before:rounded-2xl before:p-[1px] before:bg-gradient-to-r before:from-purple-500/30 before:via-purple-400/20 before:to-purple-500/30 before:blur-[2px] before:-z-10 hover:before:from-purple-500/40 hover:before:via-purple-400/30 hover:before:to-purple-500/40 transition-all duration-300 hover:-translate-y-2 hover:shadow-xl hover:shadow-purple-500/20">
              <div className="absolute inset-0 rounded-2xl bg-gradient-to-br from-black via-gray-900 to-black -z-10"></div>
              <div className="relative">
                <div className="w-12 h-12 bg-purple-500/20 rounded-lg flex items-center justify-center mb-4 animate-float">
                  <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                  </svg>
                </div>
                <h3 className="text-xl font-semibold text-white mb-2">Production Ready</h3>
                <p className="text-gray-300">Get a fully functional, production-grade MCP server with all the necessary security and performance optimizations.</p>
              </div>
            </div>
          </div>
        </div>

        {error && (
          <div className="mt-6 p-4 border border-red-500/50 rounded-lg bg-red-500/10 backdrop-blur-sm text-red-400">
            <p className="font-semibold">Error:</p>
            <p>{error}</p>
          </div>
        )}
        
        {results && (
          <div className="mt-6">
            <p className="text-white font-semibold mb-2">Results:</p>
            <pre className="p-4 bg-white/5 border border-white/10 rounded-lg text-green-400 overflow-auto text-sm whitespace-pre-wrap max-h-80 backdrop-blur-sm">
              {results}
            </pre>
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}
