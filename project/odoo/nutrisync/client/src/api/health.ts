import api from './api';

// Description: Get user's health metrics
// Endpoint: GET /api/health/metrics
// Request: {}
// Response: { metrics: Array<{ id: string, name: string, value: number, unit: string, trend: 'up' | 'down' | 'stable' }> }
export const getHealthMetrics = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        metrics: [
          { _id: '1', name: 'Heart Rate', value: 72, unit: 'bpm', trend: 'stable' },
          { _id: '2', name: 'Blood Pressure', value: 120, unit: 'mmHg', trend: 'up' },
          { _id: '3', name: 'Sleep', value: 7.5, unit: 'hours', trend: 'down' },
          { _id: '4', name: 'Steps', value: 8432, unit: 'steps', trend: 'up' },
        ],
      });
    }, 500);
  });
};

// Description: Get user's upcoming appointments
// Endpoint: GET /api/health/appointments
// Request: {}
// Response: { appointments: Array<{ id: string, doctor: { name: string, specialty: string, phone: string, email: string }, date: string, time: string }> }
export const getAppointments = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        appointments: [
          {
            _id: '1',
            doctor: {
              name: 'Dr. Smith',
              specialty: 'General',
              phone: '+1 (555) 123-4567',
              email: 'dr.smith@healthsync.com'
            },
            date: '2024-03-20',
            time: '10:00 AM'
          },
          {
            _id: '2',
            doctor: {
              name: 'Dr. Johnson',
              specialty: 'Cardiology',
              phone: '+1 (555) 234-5678',
              email: 'dr.johnson@healthsync.com'
            },
            date: '2024-03-25',
            time: '2:30 PM'
          },
        ],
      });
    }, 500);
  });
};

// Description: Cancel an appointment
// Endpoint: DELETE /api/health/appointments/{id}
// Request: { appointmentId: string }
// Response: { success: boolean, message: string }
export const cancelAppointment = (appointmentId: string) => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: 'Appointment cancelled successfully'
      });
    }, 500);
  });
};

// Description: Get meditation sessions
// Endpoint: GET /api/health/meditation
// Request: {}
// Response: { sessions: Array<{ id: string, title: string, duration: number, category: string }> }
export const getMeditationSessions = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        sessions: [
          { _id: '1', title: 'Morning Calm', duration: 10, category: 'Mindfulness' },
          { _id: '2', title: 'Stress Relief', duration: 15, category: 'Anxiety' },
          { _id: '3', title: 'Deep Sleep', duration: 20, category: 'Sleep' },
          { _id: '4', title: 'Focus Time', duration: 5, category: 'Productivity' },
        ],
      });
    }, 500);
  });
};

// Description: Get fitness activities
// Endpoint: GET /api/health/fitness
// Request: {}
// Response: { activities: Array<{ id: string, name: string, duration: number, calories: number, date: string }> }
export const getFitnessActivities = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        activities: [
          { _id: '1', name: 'Running', duration: 30, calories: 300, date: '2024-03-19' },
          { _id: '2', name: 'Yoga', duration: 45, calories: 150, date: '2024-03-19' },
          { _id: '3', name: 'Strength Training', duration: 60, calories: 400, date: '2024-03-18' },
        ],
      });
    }, 500);
  });
};

// Description: Get mental health resources
// Endpoint: GET /api/health/mental-health
// Request: {}
// Response: { resources: Array<{ id: string, title: string, type: string, description: string, url: string }> }
export const getMentalHealthResources = () => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        resources: [
          {
            _id: '1',
            title: 'Managing Anxiety',
            type: 'Article',
            description: 'Learn effective techniques for managing anxiety in daily life',
            url: '#',
          },
          {
            _id: '2',
            title: 'Stress Relief Techniques',
            type: 'Video',
            description: 'Quick and effective stress relief exercises',
            url: '#',
          },
          {
            _id: '3',
            title: 'Sleep Hygiene',
            type: 'Guide',
            description: 'Comprehensive guide to better sleep habits',
            url: '#',
          },
        ],
      });
    }, 500);
  });
};