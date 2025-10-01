class EmailTemplate:

    OTP_SEND = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OTP Verification</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
    <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">

                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                            <div style="font-size: 36px; font-weight: bold; color: white; margin-bottom: 10px;">🔐 YourApp</div>
                            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Secure Verification</div>
                        </td>
                    </tr>

                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h1 style="font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600;">Verify Your Account</h1>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 10px;">Hello there!</p>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 30px;">We received a request to verify your account. Use the code below to complete your verification:</p>

                            <!-- OTP Box -->
                            <table role="presentation" style="width: 100%; margin: 30px 0;">
                                <tr>
                                    <td style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 30px; text-align: center; border-radius: 12px;">
                                        <div style="font-size: 48px; font-weight: bold; color: white; letter-spacing: 8px; font-family: 'Courier New', monospace; margin-bottom: 10px;">
                                            {{otp}}</div>
                                        <div style="color: white; font-size: 14px; opacity: 0.9;">Your One-Time Password</div>
                                    </td>
                                </tr>
                            </table>

                            <!-- Info Box -->
                            <table role="presentation" style="width: 100%; background-color: #f8f9fa; border-left: 4px solid #667eea; border-radius: 4px; margin: 20px 0;">
                                <tr>
                                    <td style="padding: 15px 20px;">
                                        <p style="margin: 0 0 10px 0; color: #333; font-size: 14px; font-weight: 600;">⏰ This code will expire in 2 minutes.</p>
                                        <p style="margin: 0; color: #666; font-size: 14px;">For security reasons, please do not share this code with anyone.</p>
                                    </td>
                                </tr>
                            </table>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-top: 30px;">If you didn't request this code, please ignore this email or contact our support team if you have concerns.</p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                            <!-- Social Links -->
                            <div style="margin: 20px 0;">
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">f</a>
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">t</a>
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">in</a>
                            </div>

                            <p style="color: #999; font-size: 14px; margin: 10px 0;">© 2025 YourApp. All rights reserved.</p>

                            <p style="margin-top: 10px;">
                                <a href="#" style="color: #667eea; text-decoration: none; font-size: 14px;">Privacy Policy</a>
                                <span style="color: #999; margin: 0 5px;">|</span>
                                <a href="#" style="color: #667eea; text-decoration: none; font-size: 14px;">Terms of Service</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """

    WELCOME_ONBOARD = """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to YourApp</title>
</head>
<body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
    <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
        <tr>
            <td style="padding: 40px 20px;">
                <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">

                    <!-- Header -->
                    <tr>
                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                            <div style="font-size: 36px; font-weight: bold; color: white; margin-bottom: 10px;">🎉 YourApp</div>
                            <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Welcome to Our Community</div>
                        </td>
                    </tr>

                    <!-- Body -->
                    <tr>
                        <td style="padding: 40px 30px;">
                            <h1 style="font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600;">Welcome Aboard!</h1>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 10px;">Hi <strong style="color: #333;">John Doe</strong>,</p>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 30px;">We're thrilled to have you join our community! Your account has been successfully created and you're all set to get started.</p>

                            <!-- CTA Button -->
                            <table role="presentation" style="margin: 30px 0;">
                                <tr>
                                    <td style="text-align: center;">
                                        <a href="#" style="display: inline-block; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 16px 40px; text-decoration: none; border-radius: 30px; font-weight: 600; font-size: 16px; box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);">Get Started Now</a>
                                    </td>
                                </tr>
                            </table>

                            <p style="font-size: 16px; color: #333; font-weight: 600; margin-top: 30px; margin-bottom: 15px;">Here's what you can do next:</p>

                            <ul style="color: #666; line-height: 1.8; font-size: 16px; padding-left: 20px;">
                                <li style="margin-bottom: 10px;">Complete your profile to personalize your experience</li>
                                <li style="margin-bottom: 10px;">Explore our features and discover what we offer</li>
                                <li style="margin-bottom: 10px;">Connect with other members of our community</li>
                                <li style="margin-bottom: 10px;">Check out our getting started guide</li>
                            </ul>

                            <!-- Info Box -->
                            <table role="presentation" style="width: 100%; background-color: #f8f9fa; border-left: 4px solid #667eea; border-radius: 4px; margin: 30px 0;">
                                <tr>
                                    <td style="padding: 15px 20px;">
                                        <p style="margin: 0 0 10px 0; color: #333; font-size: 14px; font-weight: 600;">💡 Need Help?</p>
                                        <p style="margin: 0; color: #666; font-size: 14px;">Our support team is here for you 24/7. Feel free to reach out anytime at <a href="mailto:support@yourapp.com" style="color: #667eea; text-decoration: none;">support@yourapp.com</a></p>
                                    </td>
                                </tr>
                            </table>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-top: 30px;">Thank you for choosing YourApp. We can't wait to see what you'll accomplish!</p>

                            <p style="font-size: 16px; color: #666; line-height: 1.6; margin-top: 20px;">
                                Best regards,<br>
                                <strong style="color: #333;">The YourApp Team</strong>
                            </p>
                        </td>
                    </tr>

                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                            <!-- Social Links -->
                            <div style="margin: 20px 0;">
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">f</a>
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">t</a>
                                <a href="#" style="display: inline-block; width: 40px; height: 40px; background-color: #667eea; color: white; border-radius: 50%; line-height: 40px; margin: 0 5px; text-decoration: none;">in</a>
                            </div>

                            <p style="color: #999; font-size: 14px; margin: 10px 0;">© 2025 YourApp. All rights reserved.</p>

                            <p style="margin-top: 10px;">
                                <a href="#" style="color: #667eea; text-decoration: none; font-size: 14px;">Privacy Policy</a>
                                <span style="color: #999; margin: 0 5px;">|</span>
                                <a href="#" style="color: #667eea; text-decoration: none; font-size: 14px;">Terms of Service</a>
                                <span style="color: #999; margin: 0 5px;">|</span>
                                <a href="#" style="color: #667eea; text-decoration: none; font-size: 14px;">Unsubscribe</a>
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
    """