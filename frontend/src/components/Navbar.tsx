import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { AuthModal } from './AuthModal';
import { CreateBlogModal } from './CreateBlogModal';

export const Navbar: React.FC<{ onBlogCreated?: () => void }> = ({ onBlogCreated }) => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  return (
    <>
      <nav className="fixed top-0 left-0 right-0 z-50 glass border-b border-white/10 px-6 py-4">
        <div className="max-w-7xl mx-auto flex justify-between items-center">
          <div className="text-2xl font-bold gradient-text">BlogBoy</div>
          <div className="flex gap-6 items-center">
            {isAuthenticated ? (
              <>
                <button 
                  onClick={() => setIsCreateModalOpen(true)}
                  className="flex items-center gap-2 px-4 py-2 rounded-xl bg-primary/10 text-primary hover:bg-primary/20 transition-all text-sm font-bold border border-primary/20"
                >
                  <span className="text-lg">+</span> Write
                </button>
                <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-white/5 border border-white/10">
                  <div className="w-6 h-6 rounded-full bg-gradient-to-r from-primary to-secondary"></div>
                  <span className="text-slate-200 font-medium">{user}</span>
                </div>
                <button 
                  onClick={logout}
                  className="px-4 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-white/5 transition-all text-sm font-semibold"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <button 
                  onClick={() => setIsAuthModalOpen(true)}
                  className="text-slate-300 hover:text-white transition-colors font-medium"
                >
                  Login
                </button>
                <button 
                  onClick={() => setIsAuthModalOpen(true)}
                  className="px-5 py-2 rounded-xl bg-gradient-to-r from-primary to-secondary hover:opacity-90 transition-all shadow-lg shadow-primary/20 font-bold text-white text-sm"
                >
                  Get Started
                </button>
              </>
            )}
          </div>
        </div>
      </nav>
      <AuthModal isOpen={isAuthModalOpen} onClose={() => setIsAuthModalOpen(false)} />
      <CreateBlogModal 
        isOpen={isCreateModalOpen} 
        onClose={() => setIsCreateModalOpen(false)} 
        onSuccess={() => {
          setIsCreateModalOpen(false);
          onBlogCreated?.();
        }}
      />
    </>
  );
};
