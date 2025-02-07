import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getHealthMetrics } from '@/api/health';
import { Activity, Heart, TrendingUp, TrendingDown, Minus } from 'lucide-react';
import { GoogleFit, HealthKit } from 'react-native-health';

export function Metrics() {
  const [metrics, setMetrics] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getHealthMetrics();
        setMetrics(data.metrics);
      } catch (error) {
        console.error('Error fetching health metrics:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getTrendIcon = (trend) => {
    switch (trend) {
      case 'up':
        return <TrendingUp className="h-4 w-4 text-green-500" />;
      case 'down':
        return <TrendingDown className="h-4 w-4 text-red-500" />;
      default:
        return <Minus className="h-4 w-4 text-gray-500" />;
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold text-blue-500">Health Metrics</h1>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {metrics.map((metric) => (
          <Card key={metric._id} className="hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium text-blue-500">{metric.name}</CardTitle>
              {getTrendIcon(metric.trend)}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-500">
                {metric.value}
                <span className="ml-1 text-sm font-normal text-muted-foreground">
                  {metric.unit}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
