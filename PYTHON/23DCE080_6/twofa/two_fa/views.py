import smtplib
import os
import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Function to generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))


# Function to send an OTP via email
def send_email(receiver_email, otp):
    sender_email = os.getenv("EMAIL_HOST_USER")  # Use environment variable
    sender_password = os.getenv("EMAIL_HOST_PASSWORD")  # Use environment variable

    subject = "Your OTP Code"
    message = f"Your OTP code is: {otp}"
    email_text = f"Subject: {subject}\n\n{message}"

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, email_text)
    except Exception as e:
        print("Error sending email:", e)


# Request OTP View
def request_otp(request):
    if request.method == "POST":
        email = request.POST.get("email")
        otp = generate_otp()
        request.session["otp"] = otp
        request.session["email"] = email

        send_email(email, otp)
        messages.success(request, "OTP sent to your email.")
        return redirect("verify_otp")

    return render(request, "two_fa/request_otp.html")


# Verify OTP View
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")

        if entered_otp == stored_otp:
            messages.success(request, "OTP verified successfully!")
            return redirect("/")
        else:
            messages.error(request, "Invalid OTP. Try again.")

    return render(request, "two_fa/verify_otp.html")
