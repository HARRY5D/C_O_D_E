import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  getConnectedApps,
  connectHealthApp,
  disconnectHealthApp,
  syncHealthApp,
} from '@/api/integrations';
import { Link2, Link2Off, RefreshCw, Loader2 } from 'lucide-react';
import { useToast } from '@/hooks/useToast';
import { useGoogleLogin } from '@react-oauth/google';

export function Integrations() {
  const [apps, setApps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [syncingApp, setSyncingApp] = useState(null);
  const { toast } = useToast();

  useEffect(() => {
    fetchApps();
  }, []);

  const fetchApps = async () => {
    try {
      const data = await getConnectedApps();
      setApps(data.integrations);
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to fetch connected apps",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleFitLogin = useGoogleLogin({
    scope: 'https://www.googleapis.com/auth/fitness.activity.read https://www.googleapis.com/auth/fitness.body.read',
    onSuccess: async (response) => {
      try {
        await connectHealthApp('Google Fit', response.access_token);
        toast({
          title: "Success",
          description: "Successfully connected to Google Fit",
        });
        fetchApps();
      } catch (error) {
        toast({
          variant: "destructive",
          title: "Error",
          description: "Failed to connect to Google Fit",
        });
      }
    },
    onError: () => {
      toast({
        variant: "destructive",
        title: "Error",
        description: "Failed to connect to Google Fit",
      });
    }
  });

  const handleDisconnect = async (provider: string) => {
    try {
      await disconnectHealthApp(provider);
      toast({
        title: "Success",
        description: `Successfully disconnected from ${provider}`,
      });
      fetchApps();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: `Failed to disconnect from ${provider}`,
      });
    }
  };

  const handleSync = async (appId: string, provider: string) => {
    try {
      setSyncingApp(appId);
      await syncHealthApp(provider);
      toast({
        title: "Success",
        description: `Successfully synced data from ${provider}`,
      });
      fetchApps();
    } catch (error) {
      toast({
        variant: "destructive",
        title: "Error",
        description: `Failed to sync data from ${provider}`,
      });
    } finally {
      setSyncingApp(null);
    }
  };

  const getConnectHandler = (app) => {
    switch (app.name) {
      case 'Google Fit':
        return handleGoogleFitLogin;
      default:
        return () => null;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Health App Integrations</h1>

      <div className="grid gap-6 md:grid-cols-2">
        {apps.map((app) => (
          <Card key={app._id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>{app.name}</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">
                    Status: {app.isConnected ? 'Connected' : 'Not Connected'}
                  </p>
                  {app.lastSync && (
                    <p className="text-sm text-muted-foreground">
                      Last synced: {app.lastSync}
                    </p>
                  )}
                </div>
                <div className="space-x-2">
                  {app.isConnected ? (
                    <>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleSync(app._id, app.name)}
                        disabled={syncingApp === app._id}
                      >
                        {syncingApp === app._id ? (
                          <>
                            <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                            Syncing...
                          </>
                        ) : (
                          <>
                            <RefreshCw className="mr-2 h-4 w-4" />
                            Sync
                          </>
                        )}
                      </Button>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => handleDisconnect(app.name)}
                      >
                        <Link2Off className="mr-2 h-4 w-4" />
                        Disconnect
                      </Button>
                    </>
                  ) : (
                    <Button
                      onClick={getConnectHandler(app)}
                      disabled={!getConnectHandler(app)}
                    >
                      <Link2 className="mr-2 h-4 w-4" />
                      Connect
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}