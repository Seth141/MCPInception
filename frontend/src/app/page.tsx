export default function Home() {
  return (
    <div className="min-h-screen flex items-center justify-center px-4 font-sans">
      <div className="w-full max-w-2xl">
        <h1 className="text-6xl font-bold text-white mb-12 text-center font-sans tracking-wider">
          MCP Inception
        </h1>
        <div className="bg-black/40 backdrop-blur-sm shadow-xl rounded-lg p-8 border border-gray-800">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Enter URL here..."
              className="w-full px-4 py-3 bg-black/30 border border-gray-800 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:border-transparent font-sans input-glow"
            />
            <button className="w-full px-4 py-3 bg-gradient-to-r from-purple-900 via-purple-800 to-purple-900 hover:from-purple-800 hover:via-purple-700 hover:to-purple-800 text-white font-medium rounded-lg transition-all duration-300 font-sans button-glow border border-purple-500/30">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
