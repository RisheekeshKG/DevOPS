import React from 'react';
import Header from './Header';
import Navbar from './Navbar';
import Footer from './Footer';

const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex flex-col min-h-screen bg-surface selection:bg-primary-fixed selection:text-on-primary-fixed-variant">
      <Header />
      <Navbar />
      <main className="flex-1 w-full max-w-screen-2xl mx-auto px-6 md:px-12 py-8 md:py-12">
        {children}
      </main>
      <Footer />
    </div>
  );
};

export default Layout;
