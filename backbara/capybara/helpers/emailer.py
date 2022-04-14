# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiosmtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from ..env import (
    SMTP_DOMAIN, SMTP_MAIN, SMTP_HOST,
    SMTP_USERNAME, SMTP_PASSWORD
)


async def send_email(to: str, subject: str, content: str) -> None:
    """Send an email to the SMTP server.

    Parameters
    ----------
    to : str
    subject : str
    content : str
    """

    message = MIMEMultipart("alternative")
    message["From"] = f"{SMTP_MAIN}@{SMTP_DOMAIN}"
    message["To"] = to
    message["Subject"] = subject
    message.attach(MIMEText(
        content, "plain", "utf-8"
    ))

    await aiosmtplib.send(
        message, hostname=SMTP_HOST,
        username=SMTP_USERNAME, password=SMTP_PASSWORD,
        use_tls=True
    )
