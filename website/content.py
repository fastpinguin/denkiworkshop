from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, jsonify, make_response
from flask_login import login_required, current_user, logout_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from FantasyNameGenerator.Pathfinder import Dhampir 


content = Blueprint("content", __name__)


@content.route("/", methods = ['POST', 'GET'])
def root():
    # i am aware this is a security risk. Do not have time to fix.
    name = request.cookies.get('player')
    if name:
        # return the default page
        return render_template("content.html", player=name)
    else:
        # generate new name if the user does not have one
        new_name = Dhampir.generate()
        resp = make_response(redirect(url_for("content.root")))
        resp.set_cookie("player", new_name)
        return resp


@content.route("/api")
@login_required
def test():
    to_return = [randint(0,10) for _ in range(6)]
    playerID = ["p0", "p1", "p2", "p3", "p4", "p5"]
    return jsonify(result=dict(zip(playerID,to_return)))


@content.route("/admin")
@login_required
def adminpanel():
    return render_template("adminpanel.html", player="ADMIN")
