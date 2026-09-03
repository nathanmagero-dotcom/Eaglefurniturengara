import os


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# BASE CONFIGURATION
# ============================================================

class Config:

    # --------------------------------------------------------
    # FLASK
    # --------------------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "eagle-furniture-secret-key"
    )

    WEB3FORMS_ACCESS_KEY = os.environ.get(
    "WEB3FORMS_ACCESS_KEY",
    ""
)


    # --------------------------------------------------------
    # ADMIN
    # --------------------------------------------------------

    ADMIN_USERNAME = os.environ.get(
        "ADMIN_USERNAME",
        "admin"
    )

    ADMIN_PASSWORD = os.environ.get(
        "ADMIN_PASSWORD",
        "CHANGE_THIS_PASSWORD"
    )


    # --------------------------------------------------------
    # DATABASE
    # --------------------------------------------------------

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(
            BASE_DIR,
            "instance",
            "app.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # --------------------------------------------------------
    # WEBSITE
    # --------------------------------------------------------

    SITE_NAME = "Eagle Furniture Ngara"

    SITE_URL = "https://eaglefurniture.co.ke"


    # --------------------------------------------------------
    # BUSINESS
    # --------------------------------------------------------

    BUSINESS_NAME = "Eagle Furniture Ngara"

    BUSINESS_PHONE = "+254717369779"

    BUSINESS_ADDRESS = (
        "Murang'a Road, Ngara, Nairobi, Kenya"
    )

    BUSINESS_CITY = "Nairobi"

    BUSINESS_AREA = "Ngara"

    BUSINESS_COUNTRY = "Kenya"

    BUSINESS_CURRENCY = "KES"

    BUSINESS_EMAIL = ""


    # --------------------------------------------------------
    # SOCIAL MEDIA
    # --------------------------------------------------------

    YOUTUBE_URL = (
        "https://youtube.com/@eaglefurniturer"
    )

    FACEBOOK_URL = (
        "https://www.facebook.com/eaglefurniturengara"
    )

    INSTAGRAM_URL = (
        "https://www.instagram.com/eaglefurniturengara"
    )

    LINKEDIN_URL = (
        "https://www.linkedin.com/in/eagle-ngara-"
    )

    WHATSAPP_URL = (
        "https://wa.me/254717369779"
    )

    GOOGLE_BUSINESS_URL = (
        "https://maps.app.goo.gl/MzLDzahRYtpgzEp6"
    )

    BLOG_URL = (
        "https://eaglefurniturengara.blogspot.com"
    )


# ============================================================
# DEVELOPMENT CONFIGURATION
# ============================================================

class DevelopmentConfig(Config):

    DEBUG = True


# ============================================================
# PRODUCTION CONFIGURATION
# ============================================================

class ProductionConfig(Config):

    DEBUG = False
