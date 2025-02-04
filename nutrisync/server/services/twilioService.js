const twilio = require('twilio');

const client = twilio(
  process.env.TWILIO_ACCOUNT_SID,
  process.env.TWILIO_AUTH_TOKEN
);

const sendOTP = async (phoneNumber) => {
  try {
    const verification = await client.verify.v2
      .services(process.env.TWILIO_SERVICE_SID)
      .verifications.create({
        to: phoneNumber,
        channel: 'sms'
      });
    return verification;
  } catch (error) {
    console.error('Twilio OTP Error:', error);
    throw new Error('Failed to send OTP');
  }
};

const verifyOTP = async (phoneNumber, code) => {
  try {
    const verification = await client.verify.v2
      .services(process.env.TWILIO_SERVICE_SID)
      .verificationChecks.create({
        to: phoneNumber,
        code: code
      });
    return verification;
  } catch (error) {
    console.error('Twilio Verification Error:', error);
    throw new Error('Failed to verify OTP');
  }
};

module.exports = {
  sendOTP,
  verifyOTP
};