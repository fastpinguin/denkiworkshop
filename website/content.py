from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, jsonify
from flask_login import login_required, current_user, logout_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint



content = Blueprint("main", __name__)


@content.route("/")
def root():
    return render_template("content.html")


@content.route("/api")
@login_required
def test():
    to_return = [randint(0,10) for _ in range(6)]
    playerID = ["p0", "p1", "p2", "p3", "p4", "p5"]
    return jsonify(result=dict(zip(playerID,to_return)))


@content.route("/admin")
@login_required
def adminpanel():
    return render_template("adminpanel.html")
