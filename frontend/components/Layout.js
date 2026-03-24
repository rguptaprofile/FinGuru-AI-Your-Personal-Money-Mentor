import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types';

/**
 * Layout Component - Main layout wrapper for FinGuru application
 * Provides consistent header/footer and navigation across all pages
 * 
 * @param {React.ReactNode} children - Page content to be wrapped
 * @returns {JSX.Element} Complete layout structure
 */
export default function Layout({ children }) {
  const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/chat', label: 'Chat' }
  ];

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      {/* Header/Navigation */}
      <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
        <nav className="px-4 py-3">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            {/* Logo */}
            <Link href="/" className="text-2xl font-bold hover:text-blue-100 transition">
              FinGuru
            </Link>

            {/* Navigation Links */}
            <div className="flex gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.href}
                  href={link.href}
                  className="hover:text-blue-100 underline-offset-4 hover:underline transition-colors"
                  aria-label={`Navigate to ${link.label}`}
                >
                  {link.label}
                </Link>
              ))}
            </div>
          </div>
        </nav>
      </header>

      {/* Main Content */}
      <main className="flex-1">
        {children}
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-gray-300 px-4 py-6 mt-12">
        <div className="max-w-7xl mx-auto text-center text-sm">
          <p>&copy; 2024 FinGuru AI - Your Personal Money Mentor</p>
          <p className="mt-2 text-gray-400">
            Making financial planning accessible to every Indian 💰
          </p>
        </div>
      </footer>
    </div>
  );
}

// PropTypes validation
Layout.propTypes = {
  children: PropTypes.node.isRequired
};
