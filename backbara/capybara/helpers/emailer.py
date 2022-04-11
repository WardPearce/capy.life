# -*- coding: utf-8 -*-

"""
GNU AFFERO GENERAL PUBLIC LICENSE
Version 3, 19 November 2007
"""

import aiosmtplib

from email.message import EmailMessage

from ..env import (
    SMTP_DOMAIN, SMTP_MAIN, SMTP_HOST,
    SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD
)


async def send_email(to: str, subject: str, content: str) -> None:
    """Send an email to the SMTP server.

    Parameters
    ----------
    to : str
    subject : str
    content : str
    """

    message = EmailMessage()
    message["From"] = f"{SMTP_MAIN}@{SMTP_DOMAIN}"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(content)

    await aiosmtplib.send(
        message, hostname=SMTP_HOST, port=SMTP_PORT,
        username=SMTP_USERNAME, password=SMTP_PASSWORD
    )
