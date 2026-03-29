const BASE_URL = '/api';

export interface Blog {
  id: number;
  title: string;
  category: string;
  author: string;
  body: string;
}

export const api = {
  async fetchBlogs(): Promise<Blog[]> {
    const res = await fetch(`${BASE_URL}/blogresource`);
    if (!res.ok) throw new Error('Failed to fetch blogs');
    const result = await res.json();
    return result.data || [];
  },

  async register(username: string, password: string) {
    const res = await fetch(`${BASE_URL}/registration`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.message || 'Registration failed');
    }
    return res.json();
  },

  async login(username: string, password: string) {
    const res = await fetch(`${BASE_URL}/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (!res.ok) {
        const err = await res.json();
        throw new Error(err.message || 'Login failed');
    }
    return res.json();
  },

  async logout(token: string) {
    await fetch(`${BASE_URL}/logout/access`, {
      method: 'POST',
      headers: { 'Authorization': `Bearer ${token}` },
    });
  },

  async createBlog(data: { title: string; category: string; body: string }, token: string) {
    const res = await fetch(`${BASE_URL}/blogresource`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.msg || err.message || 'Failed to create blog');
    }
    return res.json();
  },

  async deleteBlog(id: number, token: string) {
    const res = await fetch(`${BASE_URL}/blogresource?id=${id}`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.msg || err.message || 'Failed to delete blog');
    }
    return res.json();
  }
};
