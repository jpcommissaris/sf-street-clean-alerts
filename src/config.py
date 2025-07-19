import os


class Config:
    DEBUG = os.environ.get("FLASK_DEBUG", True)
    SFMTA_API_URL = os.environ.get(
        "SFMTA_API_URL", "https://data.sfgov.org/resource/yhqp-riqs.json"
    )

    # -- TODO --
    SECRET_KEY = os.environ.get("SECRET_KEY", "")
    SFMTA_API_TOKEN = os.environ.get("SFMTA_API_TOKEN", "")
