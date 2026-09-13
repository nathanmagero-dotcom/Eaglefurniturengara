import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "eagle-furniture-secret-key"
    )

    WEB3FORMS_ACCESS_KEY = os.environ.get(
        "WEB3FORMS_ACCESS_KEY",
        ""
    )

    ADMIN_USERNAME = os.environ.get(
        "ADMIN_USERNAME",
        "admin"
    )

    ADMIN_PASSWORD = os.environ.get(
        "ADMIN_PASSWORD",
        "CHANGE_THIS_PASSWORD"
    )

    # ---------------------------------------------------------
    # DATABASE
    # ---------------------------------------------------------
    # Local development:
    #     SQLite -> instance/app.db
    #
    # Railway production:
    #     PostgreSQL -> DATABASE_URL
    # ---------------------------------------------------------

    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(BASE_DIR, "instance", "app.db")
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ---------------------------------------------------------
    # BUSINESS INFORMATION
    # ---------------------------------------------------------

    SITE_NAME = "Eagle Furniture Ngara"
    SITE_URL = "https://eaglefurniture.co.ke"

    BUSINESS_NAME = "Eagle Furniture Ngara"
    BUSINESS_PHONE = "+254717369779"
    BUSINESS_ADDRESS = "Murang'a Road, Ngara, Nairobi, Kenya"
    BUSINESS_CITY = "Nairobi"
    BUSINESS_AREA = "Ngara"
    BUSINESS_COUNTRY = "Kenya"
    BUSINESS_CURRENCY = "KES"
    BUSINESS_EMAIL = ""

    # ---------------------------------------------------------
    # SOCIAL MEDIA
    # ---------------------------------------------------------

    YOUTUBE_URL = "https://youtube.com/@eaglefurniturer"
    FACEBOOK_URL = "https://www.facebook.com/eaglefurniturengara"
    INSTAGRAM_URL = "https://www.instagram.com/eaglefurniturengara"
    LINKEDIN_URL = "https://www.linkedin.com/in/eagle-ngara-"

    WHATSAPP_URL = "https://wa.me/254717369779"

    GOOGLE_BUSINESS_URL = (
        "https://maps.app.goo.gl/MzLDzahRYtpgzEp6"
    )

    BLOG_URL = "https://eaglefurniturengara.blogspot.com"


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False