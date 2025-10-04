class EmailTemplate:


    # ============================================
    # TEMPLATE 1: 2FA OTP Verification
    # ============================================
    TWO_FA_OTP_TEMPLATE_SUBJECT = '🔒 Your 2FA Verification Code - Expires Soon'
    TWO_FA_OTP_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>2FA Verification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background: linear-gradient(135deg, #FF6B6B 0%, #C92A2A 100%); padding: 40px 20px; text-align: center;">
                                <div style="font-size: 36px; font-weight: bold; color: white; margin-bottom: 10px;">🔐 {{ company_name }}</div>
                                <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Two-Factor Authentication</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h1 style="font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600;">Security Verification Required</h1>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 10px;">Hi <strong style="color: #333;"></strong>,</p>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 30px;">We detected a login attempt on your account. To ensure it's really you, please use the verification code below:</p>
                                
                                <table role="presentation" style="width: 100%; margin: 30px 0;">
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #FF6B6B 0%, #C92A2A 100%); padding: 30px; text-align: center; border-radius: 12px;">
                                            <div style="font-size: 48px; font-weight: bold; color: white; letter-spacing: 8px; font-family: 'Courier New', monospace; margin-bottom: 10px;">{{ otp_code }}</div>
                                            <div style="color: white; font-size: 14px; opacity: 0.9;">Two-Factor Authentication Code</div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <table role="presentation" style="width: 100%; background-color: #fff5f5; border-left: 4px solid #FF6B6B; border-radius: 4px; margin: 20px 0;">
                                    <tr>
                                        <td style="padding: 15px 20px;">
                                            <p style="margin: 0 0 10px 0; color: #333; font-size: 14px; font-weight: 600;">⏰ This code will expire in {{ expiry_minutes }} minutes.</p>
                                </table>
                                
                                <table role="presentation" style="width: 100%; background-color: #fff3cd; border-left: 4px solid #ffc107; border-radius: 4px; margin: 20px 0;">
                                    <tr>
                                        <td style="padding: 15px 20px;">
                                            <p style="margin: 0 0 10px 0; color: #856404; font-size: 14px; font-weight: 600;">⚠️ Security Alert</p>
                                            <p style="margin: 0; color: #856404; font-size: 14px;">If you didn't attempt to log in, please secure your account immediately and contact our support team.</p>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                                <p style="color: #999; font-size: 14px; margin: 10px 0;">© {{ year }} {{ company_name }}. All rights reserved.</p>
                                <p style="margin-top: 10px;">
                                    <a href="{{ support_url }}" style="color: #FF6B6B; text-decoration: none; font-size: 14px;">Contact Support</a>
                                    <span style="color: #999; margin: 0 5px;">|</span>
                                    <a href="{{ security_url }}" style="color: #FF6B6B; text-decoration: none; font-size: 14px;">Security Settings</a>
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


    # ============================================
    # TEMPLATE 2: Sign In OTP Verification
    # ============================================


    LOGIN_OTP_TEMPLATE_SUBJECT = '[MyCompany] Sign In Code: {{ otp_code }}'
    LOGIN_OTP_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign In Verification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 40px 20px; text-align: center;">
                                <div style="font-size: 36px; font-weight: bold; color: white; margin-bottom: 10px;">🔓 {{ company_name }}</div>
                                <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Sign In Verification</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h1 style="font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600;">Verify Your Sign In</h1>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 10px;">Hello <strong style="color: #333;"></strong>,</p>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 30px;">You're attempting to sign in to your {{ company_name }} account. Please enter the verification code below to continue:</p>
                                
                                <table role="presentation" style="width: 100%; margin: 30px 0;">
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; text-align: center; border-radius: 12px;">
                                            <div style="font-size: 48px; font-weight: bold; color: white; letter-spacing: 8px; font-family: 'Courier New', monospace; margin-bottom: 10px;">{{ otp_code }}</div>
                                            <div style="color: white; font-size: 14px; opacity: 0.9;">Your Sign In Code</div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <table role="presentation" style="width: 100%; background-color: #f8f9fa; border-left: 4px solid #667eea; border-radius: 4px; margin: 20px 0;">
                                    <tr>
                                        <td style="padding: 15px 20px;">
                                            <p style="margin: 0 0 10px 0; color: #333; font-size: 14px; font-weight: 600;">⏰ Code expires in {{ expiry_minutes }} minutes</p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-top: 30px;">If you didn't request this code, please ignore this email or contact support if you have concerns about your account security.</p>
                                
                                <table role="presentation" style="margin: 30px 0;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="{{ help_url }}" style="display: inline-block; background: #667eea; color: white; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 14px;">Need Help?</a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                                <p style="color: #999; font-size: 14px; margin: 10px 0;">© {{ year }} {{ company_name }}. All rights reserved.</p>
                                <p style="margin-top: 10px;">
                                    <a href="{{ privacy_url }}" style="color: #667eea; text-decoration: none; font-size: 14px;">Privacy Policy</a>
                                    <span style="color: #999; margin: 0 5px;">|</span>
                                    <a href="{{ terms_url }}" style="color: #667eea; text-decoration: none; font-size: 14px;">Terms of Service</a>
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


    # ============================================
    # TEMPLATE 3: Sign Up OTP Verification
    # ============================================
    SIGNUP_OTP_TEMPLATE_SUBJECT = '✨ Welcome! Verify Your Email Address'
    SIGNUP_OTP_TEMPLATE = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Sign Up Verification</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f4f4;">
        <table role="presentation" style="width: 100%; border-collapse: collapse; background-color: #f4f4f4;">
            <tr>
                <td style="padding: 40px 20px;">
                    <table role="presentation" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.1);">
                        <tr>
                            <td style="background: linear-gradient(135deg, #20E2D7 0%, #0BA360 100%); padding: 40px 20px; text-align: center;">
                                <div style="font-size: 36px; font-weight: bold; color: white; margin-bottom: 10px;">✨ {{ company_name }}</div>
                                <div style="color: rgba(255,255,255,0.9); font-size: 14px;">Welcome! Let's verify your email</div>
                            </td>
                        </tr>
                        <tr>
                            <td style="padding: 40px 30px;">
                                <h1 style="font-size: 24px; color: #333; margin-bottom: 20px; font-weight: 600;">Complete Your Registration</h1>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 10px;">Hi <strong style="color: #333;"></strong>,</p>
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-bottom: 30px;">Welcome to {{ company_name }}! We're excited to have you on board. To complete your registration and verify your email address, please use the code below:</p>
                                
                                <table role="presentation" style="width: 100%; margin: 30px 0;">
                                    <tr>
                                        <td style="background: linear-gradient(135deg, #20E2D7 0%, #0BA360 100%); padding: 30px; text-align: center; border-radius: 12px;">
                                            <div style="font-size: 48px; font-weight: bold; color: white; letter-spacing: 8px; font-family: 'Courier New', monospace; margin-bottom: 10px;">{{ otp_code }}</div>
                                            <div style="color: white; font-size: 14px; opacity: 0.9;">Your Verification Code</div>
                                        </td>
                                    </tr>
                                </table>
                                
                                <table role="presentation" style="width: 100%; background-color: #e8f8f5; border-left: 4px solid #0BA360; border-radius: 4px; margin: 20px 0;">
                                    <tr>
                                        <td style="padding: 15px 20px;">
                                            <p style="margin: 0 0 10px 0; color: #0a5e3a; font-size: 14px; font-weight: 600;">⏰ Complete registration within {{ expiry_minutes }} minutes</p>
                                            <p style="margin: 0; color: #0a5e3a; font-size: 14px;">This code will expire after the time limit for security purposes.</p>
                                        </td>
                                    </tr>
                                </table>
                                
                                <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin: 25px 0;">
                                    <p style="margin: 0 0 15px 0; color: #333; font-size: 16px; font-weight: 600;">What's Next?</p>
                                    <ul style="margin: 0; padding-left: 20px; color: #666; font-size: 14px; line-height: 1.8;">
                                        <li>Enter the verification code in the sign-up form</li>
                                        <li>Complete your profile setup</li>
                                        <li>Start exploring {{ company_name }} features</li>
                                    </ul>
                                </div>
                                
                                <p style="font-size: 16px; color: #666; line-height: 1.6; margin-top: 30px;">If you didn't create an account with {{ company_name }}, you can safely ignore this email.</p>
                                
                                <table role="presentation" style="margin: 30px 0;">
                                    <tr>
                                        <td style="text-align: center;">
                                            <a href="{{ support_url }}" style="display: inline-block; background: transparent; border: 2px solid #0BA360; color: #0BA360; padding: 12px 30px; text-decoration: none; border-radius: 25px; font-weight: 600; font-size: 14px;">Questions? Contact Us</a>
                                        </td>
                                    </tr>
                                </table>
                            </td>
                        </tr>
                        <tr>
                            <td style="background-color: #f8f9fa; padding: 30px; text-align: center;">
                                <p style="color: #999; font-size: 14px; margin: 10px 0;">© {{ year }} {{ company_name }}. All rights reserved.</p>
                                <p style="margin-top: 10px;">
                                    <a href="{{ privacy_url }}" style="color: #0BA360; text-decoration: none; font-size: 14px;">Privacy Policy</a>
                                    <span style="color: #999; margin: 0 5px;">|</span>
                                    <a href="{{ terms_url }}" style="color: #0BA360; text-decoration: none; font-size: 14px;">Terms of Service</a>
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