import { useEffect, useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { getHealthMetrics, getAppointments } from '@/api/health';
import { Activity, Calendar, Heart, TrendingUp, TrendingDown, Minus } from 'lucide-react';

export function Dashboard() {
  const [metrics, setMetrics] = useState([]);
  const [appointments, setAppointments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [metricsData, appointmentsData] = await Promise.all([
          getHealthMetrics(),
          getAppointments(),
        ]);
        setMetrics(metricsData.metrics);
        setAppointments(appointmentsData.appointments);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
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
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">Dashboard</h1>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {metrics.map((metric) => (
          <Card key={metric._id}>
            <CardHeader className="flex flex-row items-center justify-between pb-2 space-y-0">
              <CardTitle className="text-sm font-medium">{metric.name}</CardTitle>
              {getTrendIcon(metric.trend)}
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">
                {metric.value}
                <span className="ml-1 text-sm font-normal text-muted-foreground">
                  {metric.unit}
                </span>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upcoming Appointments</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {appointments.map((appointment) => (
              <div
                key={appointment._id}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center space-x-4">
                  <Calendar className="h-5 w-5 text-brand-500" />
                  <div>
                    <p className="font-medium">{appointment.doctor.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {appointment.doctor.specialty}
                    </p>
                  </div>
                </div>
                <div className="text-right">
                  <p className="font-medium">{appointment.date}</p>
                  <p className="text-sm text-muted-foreground">{appointment.time}</p>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
