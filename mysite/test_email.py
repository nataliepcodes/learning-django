
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()

from django.core.mail import send_mail

send_mail(
    "Test Subject",
    "This is a test email.",
    "from@example.com",
    ["to@example.com"],
)

"""
CONSOLE OUTPUT

Content-Type: text/plain; charset="utf-8"
Content-Transfer-Encoding: 7bit
MIME-Version: 1.0
Subject: Test Subject
From: from@example.com
To: to@example.com
Date: Sat, 27 Jun 2026 04:49:55 +0000
Message-ID: <178253579589.6515.5481663268816444114@1.0.0.127.in-addr.arpa>

This is a test email.

-------------------------------------------------------------------------------
"""