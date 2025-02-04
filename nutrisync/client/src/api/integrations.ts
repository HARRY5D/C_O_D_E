import api from './api';

// Description: Get connected health apps
// Endpoint: GET /api/integrations
// Request: {}
// Response: { integrations: Array<{ id: string, name: string, isConnected: boolean, lastSync: string }> }
export const getConnectedApps = () => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        integrations: [
          { _id: '1', name: 'Google Fit', isConnected: false, lastSync: '' },
          { _id: '2', name: 'Apple Health', isConnected: false, lastSync: '' },
          { _id: '3', name: 'Fitbit', isConnected: false, lastSync: '' },
          { _id: '4', name: 'Garmin Connect', isConnected: false, lastSync: '' },
        ],
      });
    }, 500);
  });
};

// Description: Connect health app
// Endpoint: POST /api/integrations/connect
// Request: { provider: string, token: string }
// Response: { success: boolean, message: string }
export const connectHealthApp = (provider: string, token: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: `Successfully connected to ${provider}`,
      });
    }, 500);
  });
};

// Description: Disconnect health app
// Endpoint: POST /api/integrations/disconnect
// Request: { provider: string }
// Response: { success: boolean, message: string }
export const disconnectHealthApp = (provider: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: `Successfully disconnected from ${provider}`,
      });
    }, 500);
  });
};

// Description: Sync data from health app
// Endpoint: POST /api/integrations/sync
// Request: { provider: string }
// Response: { success: boolean, message: string }
export const syncHealthApp = (provider: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: `Successfully synced data from ${provider}`,
      });
    }, 500);
  });
};
