import { Link, useLocation } from 'react-router-dom';
import { cn } from '@/lib/utils';
import {
  Activity,
  Calendar,
  Heart,
  Home,
  Medal,
  Moon,
  Phone,
  UserCircle,
  Link2,
} from 'lucide-react';

const navigation = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Health Metrics', href: '/metrics', icon: Activity },
  { name: 'Mental Health', href: '/mental-health', icon: Heart },
  { name: 'Appointments', href: '/appointments', icon: Calendar },
  { name: 'Meditation', href: '/meditation', icon: Moon },
  { name: 'Fitness', href: '/fitness', icon: Medal },
  { name: 'Integrations', href: '/integrations', icon: Link2 },
  { name: 'Profile', href: '/profile', icon: UserCircle },
  { name: 'Contact', href: '/contact', icon: Phone },
];

export function Sidebar() {
  const location = useLocation();

  return (
    <div className="hidden lg:fixed lg:inset-y-0 lg:flex lg:w-72 lg:flex-col">
      <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 border-r px-6 pb-4">
        <div className="flex h-16 shrink-0 items-center">
          <Link to="/" className="flex items-center space-x-2">
            <Heart className="h-6 w-6 text-brand-600" />
            <span className="text-xl font-bold">HealthSync</span>
          </Link>
        </div>
        <nav className="flex flex-1 flex-col">
          <ul role="list" className="flex flex-1 flex-col gap-y-7">
            <li>
              <ul role="list" className="-mx-2 space-y-1">
                {navigation.map((item) => {
                  const isActive = location.pathname === item.href;
                  return (
                    <li key={item.name}>
                      <Link
                        to={item.href}
                        className={cn(
                          'group flex gap-x-3 rounded-md p-2 text-sm leading-6',
                          isActive
                            ? 'bg-brand-500/10 text-brand-600 font-semibold'
                            : 'text-muted-foreground hover:bg-brand-500/10 hover:text-brand-600'
                        )}
                      >
                        <item.icon
                          className={cn(
                            'h-5 w-5 shrink-0',
                            isActive ? 'text-brand-600' : 'text-muted-foreground group-hover:text-brand-600'
                          )}
                          aria-hidden="true"
                        />
                        {item.name}
                      </Link>
                    </li>
                  );
                })}
              </ul>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
}