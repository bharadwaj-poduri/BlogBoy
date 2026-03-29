import React, { useState } from 'react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';

interface CreateBlogModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

export const CreateBlogModal: React.FC<CreateBlogModalProps> = ({ isOpen, onClose, onSuccess }) => {
  const [title, setTitle] = useState('');
  const [category, setCategory] = useState('TECHNOLOGY');
  const [body, setBody] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const { token } = useAuth();

  const categories = ['TECHNOLOGY', 'LIFESTYLE', 'CREATIVE', 'BUSINESS', 'FUTURE'];

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!token) return;
    
    setLoading(true);
    setError('');

    try {
      await api.createBlog({ title, category, body }, token);
      onSuccess();
      onClose();
      setTitle('');
      setBody('');
      setCategory('TECHNOLOGY');
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-slate-950/80 backdrop-blur-sm" onClick={onClose}></div>
      <div className="glass w-full max-w-2xl p-8 rounded-3xl relative z-10 animate-in fade-in zoom-in duration-300">
        <h2 className="text-3xl font-bold mb-6">Create New Story</h2>
        
        {error && (
          <div className="p-4 rounded-xl mb-6 bg-red-500/20 text-red-400 text-sm">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="md:col-span-2">
              <label className="block text-sm font-medium text-slate-400 mb-2">Title</label>
              <input
                type="text"
                required
                placeholder="What's your story about?"
                className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 transition-colors"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-400 mb-2">Category</label>
              <select
                className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 transition-colors appearance-none"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                {categories.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-slate-400 mb-2">Story Content</label>
            <textarea
              required
              rows={8}
              placeholder="Start writing..."
              className="w-full bg-slate-900/50 border border-slate-700/50 rounded-xl px-4 py-3 text-white focus:outline-none focus:border-primary/50 transition-colors resize-none"
              value={body}
              onChange={(e) => setBody(e.target.value)}
            ></textarea>
          </div>
          <div className="flex gap-4 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="flex-1 px-6 py-3 rounded-xl border border-white/10 hover:bg-white/5 transition-colors font-bold"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="flex-[2] gradient-btn py-3 rounded-xl font-bold flex items-center justify-center gap-2"
            >
              {loading ? 'Publishing...' : 'Publish Story'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
