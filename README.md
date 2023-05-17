# Django_eCommerce
eCommerce webapp using Stripe API

For stripe API you need to create account on https://stripe.com/
Also for changing password you will need to generate google password. 

Create & use app passwords
Important: To create an app password, you need 2-Step Verification on your Google Account.

If you use 2-Step-Verification and get a "password incorrect" error when you sign in, you can try to use an app password.

Go to your Google Account.
Select Security
Under "Signing in to Google," select 2-Step Verification.
At the bottom of the page, select App passwords.
Enter a name that helps you remember where you’ll use the app password.
Select Generate.
To enter the app password, follow the instructions on your screen. The app password is the 16-character code that generates on your device.
Select Done.

And then add it in setting.py for EMAIL_HOST_PASSWORD
