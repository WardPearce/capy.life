import aiosmtplib
import asyncio

from email.message import EmailMessage


async def main() -> None:
    message = EmailMessage()
    message["From"] = "noreply@mail.capy.life"
    message["To"] = "wardpearce@pm.me"
    message["Subject"] = "Greg"
    message.set_content("greg")

    await aiosmtplib.send(
        message, hostname="smtp.eu.mailgun.org", use_tls=True,
        username="postmaster@mail.capy.life",
        password="d2c2a6885dd3d3caf309d8bbcd0c9758-162d1f80-32e1735f"
    )


asyncio.run(main())
