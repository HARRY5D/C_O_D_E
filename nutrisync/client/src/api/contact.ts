import api from './api';

// Description: Send contact message
// Endpoint: POST /api/contact
// Request: { name: string, email: string, message: string }
// Response: { success: boolean, message: string }
export const sendContactMessage = (data: { name: string; email: string; message: string }) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: 'Message sent successfully',
      });
    }, 500);
  });
};