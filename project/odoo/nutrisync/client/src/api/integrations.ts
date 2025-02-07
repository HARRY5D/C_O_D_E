import api from './api';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://xyzcompany.supabase.co';
const supabaseKey = 'public-anon-key';
const supabase = createClient(supabaseUrl, supabaseKey);

// Description: Get connected health apps
// Endpoint: GET /api/integrations
// Request: {}
// Response: { integrations: Array<{ id: string, name: string, isConnected: boolean, lastSync: string }> }
export const getConnectedApps = async () => {
  try {
    const { data, error } = await supabase
      .from('integrations')
      .select('*');

    if (error) {
      throw error;
    }

    return { integrations: data };
  } catch (error) {
    console.error('Error fetching connected apps:', error);
    throw error;
  }
};

// Description: Connect health app
// Endpoint: POST /api/integrations/connect
// Request: { provider: string, token: string }
// Response: { success: boolean, message: string }
export const connectHealthApp = async (provider: string, token: string) => {
  try {
    const { data, error } = await supabase
      .from('integrations')
      .insert([{ provider, token, isConnected: true, lastSync: new Date().toISOString() }]);

    if (error) {
      throw error;
    }

    return {
      success: true,
      message: `Successfully connected to ${provider}`,
    };
  } catch (error) {
    console.error('Error connecting health app:', error);
    throw error;
  }
};

// Description: Disconnect health app
// Endpoint: POST /api/integrations/disconnect
// Request: { provider: string }
// Response: { success: boolean, message: string }
export const disconnectHealthApp = async (provider: string) => {
  try {
    const { data, error } = await supabase
      .from('integrations')
      .update({ isConnected: false })
      .eq('provider', provider);

    if (error) {
      throw error;
    }

    return {
      success: true,
      message: `Successfully disconnected from ${provider}`,
    };
  } catch (error) {
    console.error('Error disconnecting health app:', error);
    throw error;
  }
};

// Description: Sync data from health app
// Endpoint: POST /api/integrations/sync
// Request: { provider: string }
// Response: { success: boolean, message: string }
export const syncHealthApp = async (provider: string) => {
  try {
    const { data, error } = await supabase
      .from('integrations')
      .update({ lastSync: new Date().toISOString() })
      .eq('provider', provider);

    if (error) {
      throw error;
    }

    return {
      success: true,
      message: `Successfully synced data from ${provider}`,
    };
  } catch (error) {
    console.error('Error syncing health app:', error);
    throw error;
  }
};
