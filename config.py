import os


class Config(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "5824661985:AAH3DrCJ5gkFQ9NdOmYrbma0aZCF3ePFIF8")

    APP_ID = int(os.environ.get("APP_ID", 21445030))

    API_HASH = os.environ.get("API_HASH", "770ca3cb4e8d9cc50bdcb79c2556a5e9")

    UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "EzStealerLogs")
