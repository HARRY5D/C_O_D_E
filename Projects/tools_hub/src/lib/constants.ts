export const categories = [
  'Web Design',
  'Web Development',
  'AI Tools',
  'Project Management',
  'Graphics & Design',
  'Productivity',
  'Communication',
  'Finance',
] as const;

export const toolDescriptionGuide = {
  title: 'How to Write a Great Tool Description',
  guidelines: [
    'Be specific about what the tool does',
    'Mention key features and benefits',
    'Include pricing model (Free, Freemium, Paid)',
    'Add relevant use cases',
    'Mention integration capabilities if applicable'
  ]
};

export const popularTools = [
  {
    name: 'Figma',
    description: 'Professional design tool for UI/UX designers. Create, prototype, and collaborate on interface designs. Features real-time collaboration, design systems, and developer handoff. Free plan available with premium features for teams.',
    category: 'Web Design',
    image_url: 'https://images.unsplash.com/photo-1542744094-24638eff58bb?auto=format&fit=crop&q=80',
    link: 'https://figma.com'
  },
  {
    name: 'VS Code',
    description: 'Powerful, extensible code editor with built-in Git integration, debugging support, and thousands of extensions. Perfect for web development, with features like IntelliSense and Live Share. Free and open-source.',
    category: 'Web Development',
    image_url: 'https://images.unsplash.com/photo-1618477247222-acbdb0e159b3?auto=format&fit=crop&q=80',
    link: 'https://code.visualstudio.com'
  },
  {
    name: 'ChatGPT',
    description: 'Advanced AI language model for content creation, coding assistance, and problem-solving. Helps with writing, analysis, and creative tasks. Available in free and premium versions with GPT-4 access.',
    category: 'AI Tools',
    image_url: 'https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&q=80',
    link: 'https://chat.openai.com'
  },
  {
    name: 'Trello',
    description: 'Visual project management tool using Kanban boards. Organize tasks, collaborate with teams, and track progress. Features automation, custom workflows, and integrations. Free plan with premium features available.',
    category: 'Project Management',
    image_url: 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?auto=format&fit=crop&q=80',
    link: 'https://trello.com'
  },
  {
    name: 'Canva',
    description: 'User-friendly graphic design platform with templates for social media, presentations, and marketing materials. Includes stock photos, fonts, and collaboration tools. Generous free tier with premium features.',
    category: 'Graphics & Design',
    image_url: 'https://images.unsplash.com/photo-1611162617474-5b21e879e113?auto=format&fit=crop&q=80',
    link: 'https://canva.com'
  }
] as const;

export const categoryDescriptions = {
  'Web Design': 'Tools for creating beautiful and functional websites',
  'Web Development': 'Development environments, frameworks, and coding tools',
  'AI Tools': 'Artificial intelligence and machine learning powered solutions',
  'Project Management': 'Task tracking, team collaboration, and project organization',
  'Graphics & Design': 'Design software, asset creation, and visual tools',
  'Productivity': 'Time management and workflow optimization tools',
  'Communication': 'Team chat, video conferencing, and collaboration platforms',
  'Finance': 'Invoicing, accounting, and financial management tools'
} as const;