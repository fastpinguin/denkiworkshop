from flask import Blueprint, render_template, request, flash, send_file, redirect, url_for, jsonify, make_response, Response
from flask_login import login_required, current_user, logout_user
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from random import randint
from FantasyNameGenerator.Pathfinder import Dhampir 
from .models import Player
from .pagemap import PAGELIST, CONTEXT
import json


content = Blueprint("content", __name__)

def get_html_file_for_key(key: str):
    if key in PAGELIST:
        return str(PAGELIST.index(key)) + ".html"
    else: return None

@content.route("/generateName")
def generate_name():
    # generate new name if the user does not have one
    new_name = Dhampir.generate()
    # insert player name into database if it does not exist
    player = Player.query.filter_by(playerid=new_name).first() # if this returns a user, then it already exists.
    if player:
        # try again
        return redirect(url_for("content.root"))
    # insert
    new_player = Player(playerid=new_name, points=json.dumps({}))
    db.session.add(new_player)
    db.session.commit()
    try:
        resp = make_response(redirect(url_for(request.args.to_dict()["redirect"])))
    except:
        resp = make_response(redirect(url_for("content.root")))
    resp.set_cookie("player", new_name, httponly=True)
    return resp


@content.route("/", methods=["POST", "GET"])
def root():
    # has the player already got a name?
    name = request.cookies.get('player')
    if name is None:
        return redirect(url_for("content.generate_name") + "?redirect=content.root")
    else:
        player = Player.query.filter_by(playerid=name).first()
        if player is None:
            return redirect(url_for("content.generate_name") + "?redirect=content.root")
        # The player has a valid username that is in the database.
        if request.method == "GET":
            return render_template("0.html", player=name, current=CONTEXT[PAGELIST[0]][0])


        elif request.method == "POST":
            args = request.args.to_dict()
            if "current" in args.keys() and request.form.get("time") is not None:
                if args["current"] not in PAGELIST:
                    # this is an invalid code
                    flash("Hey! Don't try to cheat! This is not a valid code!")
                    return render_template("0.html", player=name)
                else:
                    # valid code, check if the user already has this current
                    current = args["current"]
                    points = json.loads(player.points)
                    if current in points.keys():
                        # serve next form field
                        return render_template(get_html_file_for_key(CONTEXT[current][1]), player=name, current=CONTEXT[current][1])
                    else:
                        # the player has unlocked a new thing:
                        points[current] = (1/(int(request.form["time"])))*10000
                        player.points = json.dumps(points)
                        db.session.commit()
                        return render_template(get_html_file_for_key(CONTEXT[current][1]), player=name, current=CONTEXT[current][1])
            elif "goback" in args.keys():
                if args["goback"] not in PAGELIST:
                    # this is an invalid code
                    flash("Hey! Don't try to cheat! This is not a valid code!")
                    return render_template("0.html", current=CONTEXT[PAGELIST[0]][0])
                else:
                    # serve previous template
                    current = args["goback"]
                    return render_template(get_html_file_for_key(CONTEXT[current][0]), player=name, current=CONTEXT[current][0])
            else:
                return render_template("error.html", error=args.keys())
        else: 
            print("Invalid method: " + request.method)
            return abort(404)


@content.route("/api", methods=["GET"])
@login_required
def test():
    players = {}
    for player in Player.query.all():
        points = 0
        for pointPoss in json.loads(player.points).values():
            points += int(pointPoss)
        players[player.playerid] = points
    return jsonify(result=players)

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
