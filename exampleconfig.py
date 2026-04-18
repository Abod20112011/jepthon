from sample_config import Config
class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 2
    API_HASH = ""
    # the name to display in your alive message
    ALIVE_NAME = "aBooD"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "postgresql://postgres: Abod2011@localhost:5432/aljoker"
    # After cloning the repo and installing requirements do python3 telesetup.py an fill that value with this
    STRING_SESSION = "" 
    # create a new bot in @botfather and fill the following vales with bottoken and username respectively
    TG_BOT_TOKEN = ""
    # command handler
    COMMAND_HAND_LER = "."
    # sudo enter the id of sudo users userid's in that array
    SUDO_USERS = []
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    TZ = "Asia/Baghdad"
    VCMODE = True
