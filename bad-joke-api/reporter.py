import smtplib


def send_report(text, app):
    text = f'Subject: BJA error report\n\n{text}'
    config = app['config']['error-reporter']

    with smtplib.SMTP_SSL(config['smtp']['host']) as smtp:
        smtp.login(config['smtp']['login'], config['smtp']['password'])
        smtp.sendmail(config['smtp']['login'], config['targets'], text.encode("utf8"))
