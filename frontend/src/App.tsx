import React, { useEffect, useState } from 'react';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Navbar } from './components/Navbar';
import { api, Blog } from './services/api';

function AppContent() {
  const { token, isAuthenticated, user, logout } = useAuth();
  const [blogs, setBlogs] = useState<Blog[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [selectedBlog, setSelectedBlog] = useState<Blog | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  const loadBlogs = async () => {
    try {
      setLoading(true);
      const data = await api.fetchBlogs();
      setBlogs(data);
    } catch (err: any) {
      if (err.message.includes('Token has expired') || err.message.includes('401')) {
        logout();
      } else {
        setError(err.message);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!token || !window.confirm('Are you sure you want to delete this story? This action cannot be undone.')) return;
    
    try {
      await api.deleteBlog(id, token);
      await loadBlogs();
      setSelectedBlog(null);
    } catch (err: any) {
      if (err.message.includes('Token has expired') || err.message.includes('401')) {
        alert('Your session has expired. Please log in again.');
        logout();
      } else {
        alert(err.message);
      }
    }
  };

  useEffect(() => {
    loadBlogs();
  }, []);

  const filteredBlogs = blogs.filter(blog => 
    blog.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    blog.body.toLowerCase().includes(searchQuery.toLowerCase()) ||
    blog.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="min-h-screen relative overflow-hidden bg-background">
      {/* Animated Background Orbs */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-primary/20 rounded-full blur-[120px] animate-pulse"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-secondary/20 rounded-full blur-[120px] animate-pulse delay-700"></div>

      <Navbar onBlogCreated={loadBlogs} />
      
      <main className="pt-32 px-6 pb-20 relative z-10">
        <div className="max-w-7xl mx-auto">
          <header className="mb-16 text-center">
            <h1 className="text-6xl font-extrabold mb-6 tracking-tight">
              Explore the <span className="gradient-text">Future</span> of Stories
            </h1>
            <p className="text-slate-400 text-xl max-w-2xl mx-auto font-medium mb-10">
              A premium space for visionary writers. 
              {blogs.length > 0 && ` Currently featuring ${blogs.length} stories.`}
            </p>
            
            {/* Search Bar */}
            <div className="max-w-xl mx-auto relative group">
              <input 
                type="text"
                placeholder="Search stories, categories, or authors..."
                className="w-full bg-slate-900/50 border border-white/10 rounded-2xl px-6 py-4 pl-14 text-white focus:outline-none focus:border-primary/50 transition-all backdrop-blur-md"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
              <div className="absolute left-5 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-primary transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                </svg>
              </div>
            </div>
          </header>

          {loading && blogs.length === 0 ? (
            <div className="flex justify-center items-center py-20">
              <div className="w-12 h-12 border-4 border-primary/20 border-t-primary rounded-full animate-spin"></div>
            </div>
          ) : error ? (
            <div className="glass p-12 rounded-3xl text-center max-w-xl mx-auto">
              <div className="text-red-400 mb-4 font-bold">Failed to load content</div>
              <p className="text-slate-400 mb-8">{error}</p>
              <button 
                onClick={() => loadBlogs()}
                className="px-6 py-2 rounded-xl bg-white/5 hover:bg-white/10 transition-colors border border-white/10"
              >
                Retry
              </button>
            </div>
          ) : filteredBlogs.length === 0 ? (
            <div className="glass p-12 rounded-3xl text-center max-w-xl mx-auto">
              <p className="text-slate-300 mb-4 text-lg">
                {searchQuery ? `No stories matching "${searchQuery}"` : "No stories found yet."}
              </p>
              <p className="text-slate-500 text-sm">
                {searchQuery ? "Try a different keyword or category." : "Be the first to share your vision with the world."}
              </p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {filteredBlogs.map((blog) => (
                <div 
                  key={blog.id} 
                  onClick={() => setSelectedBlog(blog)}
                  className="glass rounded-[2rem] p-7 group hover:translate-y-[-4px] transition-all duration-300 border border-white/5 cursor-pointer"
                >
                  <div className="h-52 rounded-2xl bg-slate-800 mb-6 overflow-hidden relative">
                    <div className="absolute inset-0 bg-gradient-to-br from-primary/30 to-secondary/30 opacity-0 group-hover:opacity-100 transition-opacity duration-500 z-10"></div>
                    <div className="w-full h-full bg-slate-900 group-hover:scale-110 transition-transform duration-700"></div>
                    <div className="absolute top-4 left-4 z-20">
                      <span className="px-3 py-1 rounded-full bg-background/80 backdrop-blur-md text-[10px] font-bold text-primary uppercase tracking-widest border border-white/10">
                        {blog.category}
                      </span>
                    </div>
                  </div>
                  <h3 className="text-2xl font-bold mb-4 text-white group-hover:text-primary transition-colors line-clamp-2 leading-tight">
                    {blog.title}
                  </h3>
                  <p className="text-slate-400 text-sm mb-8 line-clamp-3 font-medium leading-relaxed">
                    {blog.body}
                  </p>
                  <div className="flex justify-between items-center pt-6 border-t border-white/5">
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-primary to-secondary p-[1px]">
                        <div className="w-full h-full rounded-xl bg-slate-900 flex items-center justify-center text-xs font-bold">
                          {blog.author[0].toUpperCase()}
                        </div>
                      </div>
                      <div className="flex flex-col">
                        <span className="text-xs font-bold text-slate-100">{blog.author}</span>
                        <span className="text-[10px] text-slate-500">Author</span>
                      </div>
                    </div>
                    <div className="w-10 h-10 rounded-full flex items-center justify-center group-hover:bg-primary transition-colors">
                      <span className="text-primary group-hover:text-white transition-colors">→</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Blog Detail Modal */}
      {selectedBlog && (
        <div className="fixed inset-0 z-[60] flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-lg" onClick={() => setSelectedBlog(null)}></div>
          <div className="glass w-full max-w-3xl max-h-[80vh] overflow-y-auto p-10 rounded-[2.5rem] relative z-10 animate-in fade-in zoom-in duration-300">
            <button 
              onClick={() => setSelectedBlog(null)}
              className="absolute top-6 right-6 w-10 h-10 rounded-full flex items-center justify-center hover:bg-white/5 transition-colors text-2xl"
            >
              ×
            </button>
            <span className="inline-block px-4 py-1.5 rounded-full bg-primary/10 text-primary text-xs font-bold uppercase tracking-widest mb-6 border border-primary/20">
              {selectedBlog.category}
            </span>
            <h2 className="text-4xl md:text-5xl font-black mb-8 leading-tight">
              {selectedBlog.title}
            </h2>
            <div className="flex items-center gap-4 mb-10 pb-8 border-b border-white/5">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-primary to-secondary p-[1px]">
                <div className="w-full h-full rounded-2xl bg-slate-900 flex items-center justify-center text-lg font-bold">
                  {selectedBlog.author[0].toUpperCase()}
                </div>
              </div>
              <div className="flex flex-col">
                <span className="text-sm font-bold text-white">{selectedBlog.author}</span>
                <span className="text-xs text-slate-500 uppercase tracking-wider font-semibold">Visionary Writer</span>
              </div>
            </div>
            <div className="prose prose-invert max-w-none">
              <p className="text-slate-300 text-lg leading-relaxed whitespace-pre-wrap">
                {selectedBlog.body}
              </p>
            </div>

            <div className="mt-12 pt-8 border-t border-white/5 flex justify-between items-center">
              <button className="px-6 py-2 rounded-xl border border-white/10 hover:bg-white/5 transition-colors text-sm font-bold text-slate-300">
                Share Story
              </button>
              
              {isAuthenticated && user === selectedBlog.author && (
                <button 
                  onClick={() => handleDelete(selectedBlog.id)}
                  className="px-6 py-2 rounded-xl bg-red-500/10 text-red-500 hover:bg-red-500/20 transition-all text-sm font-bold border border-red-500/20"
                >
                  Delete Story
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
