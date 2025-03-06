import React, { useState } from 'react';
import { supabase } from '../lib/supabase';
import { Mail, Lock, User } from 'lucide-react';
import toast from 'react-hot-toast';
import { useNavigate } from 'react-router-dom';

type AuthMode = 'signin' | 'signup' | 'forgot';

export function Auth() {
  const navigate = useNavigate();
  const [mode, setMode] = useState<AuthMode>('signin');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [username, setUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [errors, setErrors] = useState<{
    email?: string;
    password?: string;
    username?: string;
  }>({});

  const validateForm = () => {
    const newErrors: typeof errors = {};
    
    // Email validation
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation for sign up and sign in
    if (mode !== 'forgot') {
      if (!password) {
        newErrors.password = 'Password is required';
      } else if (mode === 'signup' && password.length < 6) {
        newErrors.password = 'Password must be at least 6 characters';
      }
    }

    // Username validation for sign up
    if (mode === 'signup') {
      if (!username) {
        newErrors.username = 'Username is required';
      } else if (username.length < 3) {
        newErrors.username = 'Username must be at least 3 characters';
      } else if (!/^[a-zA-Z0-9_-]+$/.test(username)) {
        newErrors.username = 'Username can only contain letters, numbers, underscores, and hyphens';
      }
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validateForm()) {
      return;
    }

    setLoading(true);
    setErrors({});

    try {
      if (mode === 'signup') {
        // Check if email exists first
        const { data: emailCheck } = await supabase.auth.signInWithPassword({
          email,
          password: 'dummy-password',
        });

        if (emailCheck) {
          setErrors({ email: 'This email is already registered. Please sign in instead.' });
          setMode('signin');
          return;
        }

        // Check if username exists
        const { data: usernameCheck } = await supabase
          .from('profiles')
          .select('username')
          .eq('username', username)
          .single();

        if (usernameCheck) {
          setErrors({ username: 'This username is already taken. Please choose another.' });
          return;
        }

        const { data: signUpData, error: signUpError } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              username,
            },
          },
        });

        if (signUpError) {
          if (signUpError.message.includes('User already registered')) {
            setErrors({ email: 'This email is already registered. Please sign in instead.' });
            setMode('signin');
            return;
          }
          throw signUpError;
        }

        if (signUpData.user) {
          const { error: profileError } = await supabase
            .from('profiles')
            .insert([{ id: signUpData.user.id, username }]);

          if (profileError) {
            if (profileError.code === '23505') {
              setErrors({ username: 'This username is already taken. Please choose another.' });
              return;
            }
            throw profileError;
          }

          toast.success('Account created successfully! You can now sign in.');
          setMode('signin');
          // Clear form
          setEmail('');
          setPassword('');
          setUsername('');
        }
      } else if (mode === 'signin') {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        });

        if (error) {
          if (error.message === 'Invalid login credentials') {
            setErrors({
              email: 'Invalid email or password',
              password: 'Invalid email or password',
            });
            return;
          }
          throw error;
        }

        toast.success('Welcome back!');
        navigate('/');
      } else if (mode === 'forgot') {
        const { error } = await supabase.auth.resetPasswordForEmail(email, {
          redirectTo: `${window.location.origin}/auth/reset-password`,
        });

        if (error) throw error;

        toast.success('Password reset instructions have been sent to your email.');
        setMode('signin');
      }
    } catch (error) {
      console.error('Auth error:', error);
      if (error instanceof Error) {
        toast.error(error.message);
      } else {
        toast.error('An unknown error occurred');
      }
    } finally {
      setLoading(false);
    }
  };

  const switchMode = (newMode: AuthMode) => {
    setMode(newMode);
    setErrors({});
  };

  return (
    <div className="max-w-md w-full mx-auto bg-white rounded-lg shadow-md p-8">
      <h2 className="text-2xl font-bold text-center mb-6">
        {mode === 'signin' ? 'Sign In' : mode === 'signup' ? 'Create Account' : 'Reset Password'}
      </h2>
      
      <form onSubmit={handleAuth} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Email</label>
          <div className="mt-1 relative">
            <Mail className="absolute left-3 top-3 text-gray-400" size={20} />
            <input
              type="email"
              value={email}
              onChange={(e) => {
                setEmail(e.target.value);
                setErrors(prev => ({ ...prev, email: undefined }));
              }}
              className={`pl-10 w-full rounded-md border ${
                errors.email ? 'border-red-500' : 'border-gray-300'
              } px-3 py-2 focus:outline-none focus:ring-2 ${
                errors.email ? 'focus:ring-red-500' : 'focus:ring-purple-500'
              }`}
              placeholder="your@email.com"
            />
          </div>
          {errors.email && (
            <p className="mt-1 text-sm text-red-600">{errors.email}</p>
          )}
        </div>

        {mode !== 'forgot' && (
          <div>
            <label className="block text-sm font-medium text-gray-700">Password</label>
            <div className="mt-1 relative">
              <Lock className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="password"
                value={password}
                onChange={(e) => {
                  setPassword(e.target.value);
                  setErrors(prev => ({ ...prev, password: undefined }));
                }}
                className={`pl-10 w-full rounded-md border ${
                  errors.password ? 'border-red-500' : 'border-gray-300'
                } px-3 py-2 focus:outline-none focus:ring-2 ${
                  errors.password ? 'focus:ring-red-500' : 'focus:ring-purple-500'
                }`}
                minLength={6}
                placeholder="••••••••"
              />
            </div>
            {errors.password && (
              <p className="mt-1 text-sm text-red-600">{errors.password}</p>
            )}
            {mode === 'signup' && !errors.password && (
              <p className="mt-1 text-sm text-gray-500">
                Password must be at least 6 characters long
              </p>
            )}
          </div>
        )}

        {mode === 'signup' && (
          <div>
            <label className="block text-sm font-medium text-gray-700">Username</label>
            <div className="mt-1 relative">
              <User className="absolute left-3 top-3 text-gray-400" size={20} />
              <input
                type="text"
                value={username}
                onChange={(e) => {
                  setUsername(e.target.value);
                  setErrors(prev => ({ ...prev, username: undefined }));
                }}
                className={`pl-10 w-full rounded-md border ${
                  errors.username ? 'border-red-500' : 'border-gray-300'
                } px-3 py-2 focus:outline-none focus:ring-2 ${
                  errors.username ? 'focus:ring-red-500' : 'focus:ring-purple-500'
                }`}
                minLength={3}
                maxLength={30}
                pattern="[a-zA-Z0-9_-]+"
                placeholder="username"
              />
            </div>
            {errors.username && (
              <p className="mt-1 text-sm text-red-600">{errors.username}</p>
            )}
            {!errors.username && (
              <p className="mt-1 text-sm text-gray-500">
                Only letters, numbers, underscores, and hyphens allowed
              </p>
            )}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {loading ? 'Loading...' : mode === 'signin' ? 'Sign In' : mode === 'signup' ? 'Sign Up' : 'Reset Password'}
        </button>
      </form>

      <div className="mt-4 text-center text-sm">
        {mode === 'signin' ? (
          <>
            <button
              onClick={() => switchMode('forgot')}
              className="text-purple-600 hover:text-purple-700"
            >
              Forgot password?
            </button>
            <div className="mt-2">
              Don't have an account?{' '}
              <button
                onClick={() => switchMode('signup')}
                className="text-purple-600 hover:text-purple-700"
              >
                Sign up
              </button>
            </div>
          </>
        ) : mode === 'signup' ? (
          <div>
            Already have an account?{' '}
            <button
              onClick={() => switchMode('signin')}
              className="text-purple-600 hover:text-purple-700"
            >
              Sign in
            </button>
          </div>
        ) : (
          <button
            onClick={() => switchMode('signin')}
            className="text-purple-600 hover:text-purple-700"
          >
            Back to sign in
          </button>
        )}
      </div>
    </div>
  );
}