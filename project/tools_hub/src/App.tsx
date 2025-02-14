import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom';
import { Search, Star, ThumbsUp, Filter, ExternalLink, LogOut, Plus } from 'lucide-react';
import { Toaster } from 'react-hot-toast';
import { supabase } from './lib/supabase';
import { Auth } from './components/Auth';
import { ResetPassword } from './components/ResetPassword';
import { AddTool } from './components/AddTool';
import { FeaturedTools } from './components/FeaturedTools';
import { categories } from './lib/constants';
import { User } from '@supabase/supabase-js';

interface Tool {
  id: string;
  name: string;
  description: string;
  category: string;
  image_url: string;
  link: string;
  profiles: { username: string } | null;
  votes: { rating: number }[];
}

interface ToolWithStats extends Tool {
  username: string | null;
  rating: number;
  votesCount: number;
}

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [tools, setTools] = useState<ToolWithStats[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check current auth status
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // Listen for auth changes
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });

    return () => subscription.unsubscribe();
  }, []);

  useEffect(() => {
    fetchTools();
  }, [selectedCategory, searchQuery]);

  const fetchTools = async () => {
    try {
      setLoading(true);
      let query = supabase
        .from('tools')
        .select(`
          *,
          profiles:user_id(username),
          votes(rating)
        `)
        .order('created_at', { ascending: false });

      if (selectedCategory !== 'All') {
        query = query.eq('category', selectedCategory);
      }

      if (searchQuery) {
        query = query.or(`name.ilike.%${searchQuery}%,description.ilike.%${searchQuery}%`);
      }

      const { data, error } = await query;
      
      if (error) throw error;

      interface Tool {
        id: string;
        name: string;
        description: string;
        category: string;
        image_url: string;
        link: string;
        profiles: { username: string } | null;
        votes: { rating: number }[];
      }

      interface ToolWithStats extends Tool {
        username: string | null;
        rating: number;
        votesCount: number;
      }

      const toolsWithStats: ToolWithStats[] = data.map((tool: Tool) => ({
        ...tool,
        username: tool.profiles?.username || null,
        rating: tool.votes.length > 0 
          ? tool.votes.reduce((acc, vote) => acc + vote.rating, 0) / tool.votes.length 
          : 0,
        votesCount: tool.votes.length
      }));

      setTools(toolsWithStats);
    } catch (error) {
      console.error('Error fetching tools:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleVote = async (toolId: string, rating: number) => {
    try {
      if (!user) throw new Error('Please sign in to vote');

      const { error } = await supabase
        .from('votes')
        .upsert({
          tool_id: toolId,
          user_id: user.id,
          rating
        });

      if (error) throw error;

      fetchTools();
    } catch (error) {
      console.error('Error voting:', error);
    }
  };

  const handleSignOut = async () => {
    await supabase.auth.signOut();
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-purple-600"></div>
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Toaster position="top-right" />
        
        {/* Header */}
        <header className="bg-gradient-to-r from-purple-600 to-indigo-600 text-white">
          <div className="container mx-auto px-4 py-4">
            <div className="flex justify-between items-center">
              <Link to="/" className="text-2xl font-bold">Freelancer Tools Directory</Link>
              <div className="flex items-center space-x-4">
                {user ? (
                  <>
                    <Link
                      to="/submit"
                      className="flex items-center px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-gray-100"
                    >
                      <Plus size={20} className="mr-2" />
                      Submit Tool
                    </Link>
                    <button
                      onClick={handleSignOut}
                      className="flex items-center px-4 py-2 bg-purple-700 text-white rounded-lg hover:bg-purple-800"
                    >
                      <LogOut size={20} className="mr-2" />
                      Sign Out
                    </button>
                  </>
                ) : (
                  <Link
                    to="/auth"
                    className="px-4 py-2 bg-white text-purple-600 rounded-lg hover:bg-gray-100"
                  >
                    Sign In
                  </Link>
                )}
              </div>
            </div>
          </div>
        </header>

        <Routes>
          <Route path="/auth" element={
            <div className="container mx-auto px-4 py-12">
              <Auth />
            </div>
          } />
          
          <Route path="/auth/reset-password" element={
            <div className="container mx-auto px-4 py-12">
              <ResetPassword />
            </div>
          } />
          
          <Route path="/submit" element={
            <div className="container mx-auto px-4 py-12">
              {user ? <AddTool onToolAdded={fetchTools} /> : <Auth />}
            </div>
          } />
          
          <Route path="/" element={
            <main className="container mx-auto px-4 py-12">
              {/* Featured Tools Section */}
              <FeaturedTools 
                tools={tools}
                category={selectedCategory}
                user={user}
                onVote={handleVote}
              />

              {/* Search Bar */}
              <div className="max-w-2xl mx-auto relative mb-8">
                <Search className="absolute left-4 top-3.5 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Search for tools..."
                  className="w-full pl-12 pr-4 py-3 rounded-lg bg-white text-gray-800 focus:outline-none focus:ring-2 focus:ring-purple-300 shadow-md"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>

              {/* Categories */}
              <div className="flex flex-wrap gap-2 mb-8">
                <button
                  onClick={() => setSelectedCategory('All')}
                  className={`px-4 py-2 rounded-full ${
                    selectedCategory === 'All'
                      ? 'bg-purple-600 text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  } transition-colors duration-200 shadow-sm`}
                >
                  All
                </button>
                {categories.map(category => (
                  <button
                    key={category}
                    onClick={() => setSelectedCategory(category)}
                    className={`px-4 py-2 rounded-full ${
                      selectedCategory === category
                        ? 'bg-purple-600 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-100'
                    } transition-colors duration-200 shadow-sm`}
                  >
                    {category}
                  </button>
                ))}
              </div>

              {/* Tools Grid */}
              {tools.length === 0 ? (
                <div className="text-center py-12">
                  <p className="text-gray-600 text-lg">
                    {loading ? 'Loading tools...' : 'No tools found. Try adjusting your search or category filter.'}
                  </p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {tools.map(tool => (
                    <div key={tool.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-200">
                      <img 
                        src={tool.image_url || 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&q=80'} 
                        alt={tool.name} 
                        className="w-full h-48 object-cover"
                        onError={(e) => {
                          e.currentTarget.src = 'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&q=80';
                        }}
                      />
                      <div className="p-6">
                        <div className="flex justify-between items-start mb-4">
                          <h3 className="text-xl font-semibold">{tool.name}</h3>
                          <span className="inline-flex items-center bg-purple-100 text-purple-800 px-2.5 py-0.5 rounded-full text-sm">
                            {tool.category}
                          </span>
                        </div>
                        <p className="text-gray-600 mb-4">{tool.description}</p>
                        <div className="flex items-center justify-between">
                          <div className="flex items-center">
                            <Star className="text-yellow-400 fill-current" size={20} />
                            <span className="ml-1 font-semibold">{tool.rating.toFixed(1)}</span>
                            <span className="text-gray-500 text-sm ml-2">({tool.votes} votes)</span>
                          </div>
                          <div className="flex items-center space-x-2">
                            {user && (
                              <div className="flex space-x-1">
                                {[1, 2, 3, 4, 5].map((rating) => (
                                  <button
                                    key={rating}
                                    onClick={() => handleVote(tool.id, rating)}
                                    className="text-yellow-400 hover:text-yellow-500"
                                  >
                                    <Star size={16} className="fill-current" />
                                  </button>
                                ))}
                              </div>
                            )}
                            <a
                              href={tool.link}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex items-center text-purple-600 hover:text-purple-700"
                            >
                              Visit <ExternalLink size={16} className="ml-1" />
                            </a>
                          </div>
                        </div>
                        <div className="mt-2 text-sm text-gray-500">
                          Submitted by {tool.username || 'Anonymous'}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </main>
          } />
        </Routes>

        {/* Footer */}
        <footer className="bg-gray-800 text-white py-8">
          <div className="container mx-auto px-4 text-center">
            <p>© 2024 Freelancer Tools Directory. All tools are rated by the community.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}