from app import app
from flask import Flask, render_template, redirect, url_for, request, send_file

@app.route("/")
def index():
    return render_template("landing_page.html")