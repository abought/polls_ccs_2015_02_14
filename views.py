import uuid

from flask import (flash,
                   jsonify,
                   render_template,
                   redirect,
                   request,
                   url_for)

from app import app
from models import KNOWN_POLLS, VOTE_COUNTS

import forms

@app.route("/", methods=["GET"])
def list_polls():
    """
    Display a list of all currently known polls: title and link
    Key on UID since there are no guarantees titles will be unique
    """
    # Template expects {url:title} dict
    polls = {url_for("poll_display", poll_id=uid): title
             for uid, title in KNOWN_POLLS.items()}

    return render_template('polls_list.html', polls=polls)


@app.route("/polls/create", methods=['GET', 'POST'])
def create_poll():
    """Allows creation of a new poll"""
    form = forms.CreatePollForm()

    if form.validate_on_submit():
        uid = uuid.uuid4().hex  # Generate unique identifier for poll
        KNOWN_POLLS[uid] = form.title.data

        # Get the choices. # TODO: This is ugly
        choices = {}
        for f in ["choice1", "choice2", "choice3", "choice4", "choice5"]:
            # Only store counts for choices with values
            field_val = getattr(form, f).data
            if field_val:
                choices[field_val] = 0

        VOTE_COUNTS[uid] = choices

        return redirect(url_for("poll_display", poll_id=uid))
    else:
        print "Creating a new poll"
        return render_template('poll_create.html', form=form)


@app.route("/polls/view/<poll_id>", methods=["GET"])
def poll_display(poll_id):
    """Display the poll information in a single HTML page"""
    try:
        counts = VOTE_COUNTS[poll_id]
        title = KNOWN_POLLS[poll_id]
    except KeyError:
        flash("No poll matching the given id was found")
        return redirect(url_for("list_polls"))

    # Ensure dictionary is always displayed in same order (alphabetical)
    counts = sorted(counts.items(), key=lambda x: x[0])

    return render_template("poll_display.html", title=title, counts=counts)


@app.route("/polls/vote/<poll_id>", methods=["GET", "POST"])
def poll_vote(poll_id):
    """Vote in a specific poll"""
    try:
        counts = VOTE_COUNTS[poll_id]
        title = KNOWN_POLLS[poll_id]
    except KeyError:
        flash("No poll matching the given id was found")
        return redirect(url_for("list_polls"))

    if request.method == "POST":
        choice = request.form["choice"]
        if choice is None or choice not in counts:
            flash("You must choose a valid option")
        else:
            VOTE_COUNTS[poll_id][choice] += 1
            return redirect(url_for("poll_display", poll_id=poll_id))

    # If this is an invalid form or a GET request...
    return render_template("poll_vote.html", title=title,
                           choices=counts.keys(),
                           poll_id=poll_id)

@app.route("/polls/data/<poll_id>")
def poll_data(poll_id):
    """Return poll data as JSON"""
    try:
        counts = VOTE_COUNTS[poll_id]
        title = KNOWN_POLLS[poll_id]
    except KeyError:
        err = jsonify({"message": "No poll matching the given id was found"})
        return err, 404

    return jsonify(counts)
