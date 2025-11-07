import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader

def send_templated_email(sender_email, sender_password, receiver_email, subject, template_name, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html_content = template.render(context)

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email) if isinstance(receiver_email, list) else receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print('✅ Email sent successfully!')
    except Exception as e:
        print('❌ Failed to send email:', e)

def technician_send_templated_email(sender_email, sender_password, receiver_email, subject, template_name, context):
    env = Environment(loader=FileSystemLoader('templates'))
    template = env.get_template(template_name)
    html_content = template.render(context)

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email) if isinstance(receiver_email, list) else receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(msg)
            print('✅ Email sent successfully!')
    except Exception as e:
        print('❌ Failed to send email:', e)
