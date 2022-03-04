import smtplib, ssl

port = 465  # For SSL
sender_email = "mgtbuashaloandrei@gmail.com"
message = "Subject: Data entry\n\n"
password = "1234haloMine@"

# Create a secure SSL context
def sendEmail(data):
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, sender_email, message + data)