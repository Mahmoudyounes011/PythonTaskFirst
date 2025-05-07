from flask_mail import Message

def send_welcome_email(user_email, mail):
    msg = Message(
        subject='مرحبًا بك في نظامنا!',
        recipients=[user_email],
        html='''
            <h1>مرحبًا بك!</h1>
            <p>شكرًا لتسجيلك في نظامنا.</p>
            <p>يمكنك الآن الاستفادة من جميع خدماتنا.</p>
        '''
    )
    mail.send(msg)