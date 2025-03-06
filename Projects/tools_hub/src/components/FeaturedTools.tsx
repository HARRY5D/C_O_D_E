import React from 'react';
import { Star, ExternalLink } from 'lucide-react';
import { categoryDescriptions } from '../lib/constants';

interface Tool {
  id: string;
  name: string;
  category: string;
  rating: number;
  votes: number;
  image_url?: string;
  description: string;
  link: string;
  username?: string;
}

interface FeaturedToolsProps {
  tools: Tool[];
  category: string;
  user: any;
  onVote: (id: string, rating: number) => void;
}

export function FeaturedTools({ tools, category, user, onVote }: FeaturedToolsProps) {
  const topTools = tools
    .filter(tool => category === 'All' || tool.category === category)
    .sort((a, b) => b.rating - a.rating || b.votes - a.votes)
    .slice(0, 3);

  if (topTools.length === 0) return null;

  return (
    <div className="mb-12">
      <div className="mb-6">
        <h2 className="text-2xl font-bold mb-2">
          {category === 'All' ? 'Top Rated Tools' : `Top Tools for ${category}`}
        </h2>
        <p className="text-gray-600">
          {category === 'All' 
            ? 'The most highly rated tools across all categories'
            : categoryDescriptions[category as keyof typeof categoryDescriptions]}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {topTools.map((tool, index) => (
          <div 
            key={tool.id}
            className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-200 relative"
          >
            {index === 0 && (
              <div className="absolute top-4 right-4 bg-yellow-400 text-white px-3 py-1 rounded-full text-sm font-semibold">
                #1 in {tool.category}
              </div>
            )}
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
                          onClick={() => onVote(tool.id, rating)}
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
    </div>
  );
}