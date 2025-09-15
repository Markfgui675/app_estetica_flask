from flask import Flask

app = Flask(__name__)
app.secret_key = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"

from app.views import homepage_massagem
