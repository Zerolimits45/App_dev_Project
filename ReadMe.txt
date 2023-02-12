Admin id: admin@mail.com
Admin password: password

Instructions to run app:
1. Please ensure all packages are downloaded from the requirements.txt

2. Please sign up as a user before you use the website

3. To be able to get a coupon you first have to purchase an item, so you can get points to redeem a coupon

4. You may use 4242 4242 4242 4242 as a dummy card number in the stripe api

Team Members:
 Aloysius (Orders)
 Kenneth (Users)
 Xie Hong (Rewards)
 Riyaz (Feedback)
 Jia Hui (Products)

Additional features

Kenneth:
- Forget Password
    - Using Flask-Mail to email the user the link to change password
    - Used Mailtrap to capture the test emails
    - For example, changing john@example.com password.
    - The link To Change Password will be http://127.0.0.1:5000/changepassword/john%40example.com

- Search User by Email
- Sort Users By Points Using Lambda
- Created Sales Data Graph Using plotly

Riyaz:
- Filter Feedbacks By Reason Function

Aloysius:
- Strip Api Payment
