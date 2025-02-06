import api from './api';

// Description: Login user
// Endpoint: POST /api/auth/login
// Request: { email: string, password: string }
// Response: { accessToken: string, refreshToken: string }
export const login = (email: string, password: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        accessToken: 'mock-access-token',
        refreshToken: 'mock-refresh-token',
      });
    }, 500);
  });
};

// Description: Google login
// Endpoint: POST /api/auth/google
// Request: { token: string }
// Response: { accessToken: string, refreshToken: string }
export const googleLogin = (token: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        accessToken: 'mock-access-token',
        refreshToken: 'mock-refresh-token',
      });
    }, 500);
  });
};

// Description: Phone number login
// Endpoint: POST /api/auth/phone/verify
// Request: { phoneNumber: string, code: string }
// Response: { accessToken: string, refreshToken: string }
export const phoneLogin = (phoneNumber: string, code: string) => {
  // Mocking the response for Indian phone number
  if (phoneNumber === '+919537554466' && code === '123456') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          accessToken: 'mock-access-token',
          refreshToken: 'mock-refresh-token',
        });
      }, 500);
    });
  }
  return Promise.reject(new Error('Invalid phone number or code'));
};

// Description: Send phone verification code
// Endpoint: POST /api/auth/phone/send-code
// Request: { phoneNumber: string }
// Response: { success: boolean, message: string }
export const sendPhoneCode = (phoneNumber: string) => {
  // Mocking the response for Indian phone number
  if (phoneNumber === '+919537554466') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          message: 'Verification code sent successfully to your Indian mobile number',
        });
      }, 500);
    });
  }
  return Promise.reject(new Error('Invalid phone number format. Please use +91XXXXXXXXXX format.'));
};

// Description: Register user
// Endpoint: POST /api/auth/register
// Request: { email: string, password: string }
// Response: { success: boolean, message: string }
export const register = (email: string, password: string) => {
  // Mocking the response for specific email
  if (email === 'harnishbackup@gmail.com') {
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve({
          success: true,
          message: 'Registration successful',
        });
      }, 500);
    });
  }
  return Promise.reject(new Error('Registration failed. Please try again.'));
};

// Description: Request password reset
// Endpoint: POST /api/auth/forgot-password
// Request: { email: string }
// Response: { success: boolean, message: string }
export const forgotPassword = (email: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: 'Password reset instructions sent to your email',
      });
    }, 500);
  });
};

// Description: Reset password
// Endpoint: POST /api/auth/reset-password
// Request: { token: string, newPassword: string }
// Response: { success: boolean, message: string }
export const resetPassword = (token: string, newPassword: string) => {
  // Mocking the response
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        success: true,
        message: 'Password reset successful',
      });
    }, 500);
  });
};

// Description: Validate Indian phone number
// Endpoint: POST /api/auth/validate-phone
// Request: { phoneNumber: string }
// Response: { isValid: boolean, message: string }
export const validateIndianPhoneNumber = (phoneNumber: string) => {
  const indianPhoneRegex = /^\+91[1-9]\d{9}$/;
  return {
    isValid: indianPhoneRegex.test(phoneNumber),
    message: indianPhoneRegex.test(phoneNumber) 
      ? 'Valid Indian phone number' 
      : 'Please enter a valid Indian phone number starting with +91'
  };
};