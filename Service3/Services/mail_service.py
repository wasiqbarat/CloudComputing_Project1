from mailersend import emails
import os
from dotenv import load_dotenv

load_dotenv()

mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

# define an empty dict to populate with mail values
mail_body = {}

mail_from = {
    "name": "Cloud Computing, HW1",
    "email": "MS_GaPcAx@trial-jy7zpl96rk0l5vx6.mlsender.net",
}

reply_to = {
    "name": "Wasiqbarat",
    "email": "MS_GaPcAx@trial-jy7zpl96rk0l5vx6.mlsender.net",
}

def sendMail(id, email, image_url):
    recipients = [
    {
        "name": "Customer",
        "email": f"{email}",
    }]
    
    mailer.set_mail_from(mail_from, mail_body)
    mailer.set_mail_to(recipients, mail_body)
    
    mailer.set_subject("AUT Image Service", mail_body)
    mailer.set_html_content(f"""Dear Customer, Your request for the AUT AI image generator has been completed.<br>
                            Your ID: {id}<br>
                            To download the image click on this link:<br>
                            {image_url['message']}
                            """, mail_body)
    
    mailer.set_plaintext_content("This is the text content", mail_body)
    mailer.set_reply_to(reply_to, mail_body)

    # using print() will also return status code and data
    print(mailer.send(mail_body))

