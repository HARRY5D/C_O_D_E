import React, { useState } from 'react';
import { supabase } from '../lib/supabase';
import toast from 'react-hot-toast';
import { categories, toolDescriptionGuide, popularTools } from '../lib/constants';
import { Info } from 'lucide-react';

export function AddTool() {
  const [loading, setLoading] = useState(false);
  const [showGuide, setShowGuide] = useState(false);
  const [tool, setTool] = useState({
    name: '',
    description: '',
    category: '',
    imageUrl: '',
    link: '',
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const user = (await supabase.auth.getUser()).data.user;
      if (!user) throw new Error('Please sign in to submit a tool');

      const { error } = await supabase.from('tools').insert([
        {
          name: tool.name,
          description: tool.description,
          category: tool.category,
          image_url: tool.imageUrl,
          link: tool.link,
          user_id: user.id,
        },
      ]);

      if (error) throw error;

      toast.success('Tool submitted successfully!');
      setTool({ name: '', description: '', category: '', imageUrl: '', link: '' });
    } catch (error) {
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow-md p-8">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Submit a Tool</h2>
          <button
            onClick={() => setShowGuide(!showGuide)}
            className="text-purple-600 hover:text-purple-700 flex items-center"
          >
            <Info size={20} className="mr-1" />
            Writing Guidelines
          </button>
        </div>

        {showGuide && (
          <div className="mb-8 bg-purple-50 p-4 rounded-lg">
            <h3 className="font-semibold text-lg mb-2">{toolDescriptionGuide.title}</h3>
            <ul className="list-disc pl-5 space-y-1">
              {toolDescriptionGuide.guidelines.map((guideline, index) => (
                <li key={index} className="text-gray-700">{guideline}</li>
              ))}
            </ul>
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-gray-700">Tool Name</label>
            <input
              type="text"
              value={tool.name}
              onChange={(e) => setTool({ ...tool, name: e.target.value })}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
              placeholder="e.g., Figma, VS Code, Trello"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <div className="mt-1 relative">
              <textarea
                value={tool.description}
                onChange={(e) => setTool({ ...tool, description: e.target.value })}
                className="w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
                rows={5}
                required
                placeholder="Describe the tool's main features, benefits, pricing model, and best use cases..."
              />
              <div className="absolute bottom-2 right-2 text-sm text-gray-500">
                {tool.description.length}/500
              </div>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Category</label>
            <select
              value={tool.category}
              onChange={(e) => setTool({ ...tool, category: e.target.value })}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              required
            >
              <option value="">Select a category</option>
              {categories.map((category) => (
                <option key={category} value={category}>
                  {category}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Image URL</label>
            <input
              type="url"
              value={tool.imageUrl}
              onChange={(e) => setTool({ ...tool, imageUrl: e.target.value })}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="https://example.com/image.jpg"
              required
            />
            <p className="mt-1 text-sm text-gray-500">
              Provide a URL to an image that represents the tool (logo, screenshot, etc.)
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700">Tool URL</label>
            <input
              type="url"
              value={tool.link}
              onChange={(e) => setTool({ ...tool, link: e.target.value })}
              className="mt-1 w-full rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-purple-500"
              placeholder="https://example.com"
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50"
          >
            {loading ? 'Submitting...' : 'Submit Tool'}
          </button>
        </form>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-semibold mb-4">Popular Tools for Inspiration</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {popularTools.map((popularTool) => (
            <div key={popularTool.name} className="bg-white rounded-lg shadow-md p-4">
              <h4 className="font-semibold text-lg">{popularTool.name}</h4>
              <span className="inline-block bg-purple-100 text-purple-800 text-sm px-2 py-1 rounded-full mt-1">
                {popularTool.category}
              </span>
              <p className="text-gray-600 mt-2 text-sm">{popularTool.description}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}