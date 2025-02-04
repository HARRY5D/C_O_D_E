import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getMeditationSessions } from '@/api/health';
import { Play, Pause, Clock, Tag } from 'lucide-react';

export function Meditation() {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeSession, setActiveSession] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getMeditationSessions();
        setSessions(data.sessions);
      } catch (error) {
        console.error('Error fetching meditation sessions:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const toggleSession = (sessionId) => {
    if (activeSession === sessionId) {
      setActiveSession(null);
    } else {
      setActiveSession(sessionId);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Meditation</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {sessions.map((session) => (
          <Card key={session._id} className="hover:shadow-lg transition-shadow">
            <CardHeader>
              <CardTitle>{session.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <Clock className="h-4 w-4" />
                  <span>{session.duration} minutes</span>
                </div>
                <div className="flex items-center space-x-2 text-sm text-muted-foreground">
                  <Tag className="h-4 w-4" />
                  <span>{session.category}</span>
                </div>
                <Button
                  className="w-full"
                  variant={activeSession === session._id ? "secondary" : "default"}
                  onClick={() => toggleSession(session._id)}
                >
                  {activeSession === session._id ? (
                    <>
                      <Pause className="mr-2 h-4 w-4" /> Pause
                    </>
                  ) : (
                    <>
                      <Play className="mr-2 h-4 w-4" /> Start Session
                    </>
                  )}
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}