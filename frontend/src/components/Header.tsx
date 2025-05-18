'use client';

import React from 'react';
import Link from 'next/link';

const Header: React.FC = () => {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 backdrop-blur-lg bg-black/30 border-b border-white/10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2 group">
              <div className="relative w-8 h-8">
                <div className="absolute inset-0 rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 opacity-75 group-hover:opacity-100 transition-opacity"></div>
                <div className="absolute inset-0.5 rounded-lg bg-black flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                    <path 
                      className="animate-draw"
                      strokeLinecap="round" 
                      strokeLinejoin="round" 
                      strokeWidth={2} 
                      d="M4 4h16M4 12h16M4 20h16"
                    />
                  </svg>
                </div>
                <div className="absolute -inset-1 rounded-lg bg-gradient-to-r from-purple-500 to-blue-500 opacity-0 group-hover:opacity-100 blur transition-opacity"></div>
              </div>
              <span className="text-2xl font-bold text-white">MCP</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link href="/docs" className="text-gray-300 hover:text-white transition-colors">
              Documentation
            </Link>
            <Link href="/pricing" className="text-gray-300 hover:text-white transition-colors">
              Pricing
            </Link>
            <Link href="/blog" className="text-gray-300 hover:text-white transition-colors">
              Blog
            </Link>
            <Link href="/contact" className="text-gray-300 hover:text-white transition-colors">
              Contact
            </Link>
          </nav>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <button
              className="text-gray-300 hover:text-white focus:outline-none"
            >
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden">
        <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-black/95 backdrop-blur-lg">
          <Link href="/docs" className="block px-3 py-2 text-gray-300 hover:text-white transition-colors">
            Documentation
          </Link>
          <Link href="/pricing" className="block px-3 py-2 text-gray-300 hover:text-white transition-colors">
            Pricing
          </Link>
          <Link href="/blog" className="block px-3 py-2 text-gray-300 hover:text-white transition-colors">
            Blog
          </Link>
          <Link href="/contact" className="block px-3 py-2 text-gray-300 hover:text-white transition-colors">
            Contact
          </Link>
        </div>
      </div>
    </header>
  );
};

export default Header; 