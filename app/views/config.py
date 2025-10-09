from flask import render_template, url_for, flash, request, redirect
from datetime import datetime
from app import app
from app.model.model import get_db_connection
from app.controller import config

@app.route("/config")
def config():
    return render_template('config/config.html')
