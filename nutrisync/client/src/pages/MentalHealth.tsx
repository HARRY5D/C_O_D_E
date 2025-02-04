import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { getMentalHealthResources, getMeditationSessions, getCrisisSupportHotlines } from '@/api/health';
import { PlayCircle, FileText, Video, Phone } from 'lucide-react';

export function MentalHealth() {
  const [resources, setResources] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [crisisSupportHotlines, setCrisisSupportHotlines] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [resourcesData, sessionsData, hotlinesData] = await Promise.all([
          getMentalHealthResources(),
          getMeditationSessions(),
          getCrisisSupportHotlines(),
        ]);
        setResources(resourcesData.resources);
        setSessions(sessionsData.sessions);
        setCrisisSupportHotlines(hotlinesData.hotlines);
      } catch (error) {
        console.error('Error fetching mental health data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getResourceIcon = (type) => {
    switch (type) {
      case 'Video':
        return <Video className="h-5 w-5" />;
      default:
        return <FileText className="h-5 w-5" />;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Mental Health & Wellness</h1>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Meditation Sessions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {sessions.map((session) => (
                <div
                  key={session._id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <PlayCircle className="h-5 w-5 text-brand-500" />
                    <div>
                      <p className="font-medium">{session.title}</p>
                      <p className="text-sm text-muted-foreground">
                        {session.category} • {session.duration} min
                      </p>
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Start
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Wellness Resources</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {resources.map((resource) => (
                <div
                  key={resource._id}
                  className="p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4 mb-2">
                    {getResourceIcon(resource.type)}
                    <div>
                      <p className="font-medium">{resource.title}</p>
                      <p className="text-sm text-muted-foreground">
                        {resource.type}
                      </p>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {resource.description}
                  </p>
                  <Button
                    variant="link"
                    className="mt-2 p-0 h-auto font-medium text-brand-600"
                  >
                    Learn More →
                  </Button>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Crisis Support Hotlines</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {crisisSupportHotlines.map((hotline) => (
                <div
                  key={hotline._id}
                  className="p-4 border rounded-lg hover:bg-accent/50 transition-colors"
                >
                  <div className="flex items-center space-x-4 mb-2">
                    <Phone className="h-5 w-5 text-brand-500" />
                    <div>
                      <p className="font-medium">{hotline.name}</p>
                      <p className="text-sm text-muted-foreground">
                        {hotline.phone}
                      </p>
                    </div>
                  </div>
                  <p className="text-sm text-muted-foreground">
                    {hotline.description}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
