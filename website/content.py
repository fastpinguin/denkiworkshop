from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, jsonify, make_response, Response
from flask_login import login_required, current_user, logout_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from FantasyNameGenerator.Pathfinder import Dhampir 
from .models import Player


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
        # insert player name into database if it does not exist
        player = Player.query.filter_by(playerid=new_name).first() # if this returns a user, then it already exists.
        if player:
            # try again
            return redirect(url_for("content.root"))
        # insert
        new_player = Player(playerid=new_name, points=0)
        db.session.add(new_player)
        db.session.commit()
        resp = make_response(redirect(url_for("content.root")))
        resp.set_cookie("player", new_name, httponly=True)
        return resp


@content.route("/api", methods=["GET"])
@login_required
def test():
    players = {}
    for player in Player.query.all():
        players[player.playerid] = player.points
    return jsonify(result=players)

@content.route("/api", methods=["POST"])
def increase_points():
    name = request.cookies.get('player')
    player = Player.query.filter_by(playerid=name).first() # if this returns a user, then it already exists.
    if player is None:
        # delete cookie and redirect to rickroll
        resp = make_response(redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))
        # Set the cookie value to an empty string
        resp.set_cookie('player', '', max_age=0)
        return resp
    player.points += 1
    db.session.commit()
    return redirect(url_for("content.root"))



@content.route("/del", methods=["POST"])
@login_required
def admin_api():
    Player.query.delete()
    db.session.commit()
    return redirect(url_for("content.adminpanel"))
    

@content.route("/admin")
@login_required
def adminpanel():
    return render_template("adminpanel.html", player="ADMIN")
