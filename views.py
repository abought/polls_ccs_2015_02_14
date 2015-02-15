import uuid

from flask import (flash,
                   jsonify,
                   render_template,
                   redirect,
                   request,
                   url_for)

from app import app
from models import poll_data  # KNOWN_POLLS, VOTE_COUNTS

import forms

@app.route("/", methods=["GET"])
def list_polls():
    """
    Display a list of all currently known polls: title and link
    Key on UID since there are no guarantees titles will be unique
    """

    print "pt", poll_data, dir(poll_data)
    # Template expects {url:title} dict
    polls = {url_for("poll_display", poll_id=uid): title
             for uid, title in poll_data.get_all_poll_titles()}

    return render_template('polls_list.html', polls=polls)


@app.route("/polls/create", methods=['GET', 'POST'])
def create_poll():
    """Allows creation of a new poll"""
    form = forms.CreatePollForm()

    if form.validate_on_submit():
        uid = uuid.uuid4().hex  # Generate unique identifier for poll

        # Get the choices. # TODO: This is ugly
        choices = []
        for f in ["choice1", "choice2", "choice3", "choice4", "choice5"]:
            # Only store counts for choices with values
            field_val = getattr(form, f).data
            if field_val:
                choices.append(field_val)

        poll_data.make_poll(uid, form.title.data, choices)

        return redirect(url_for("poll_display", poll_id=uid))
    else:
        print "Creating a new poll"
        return render_template('poll_create.html', form=form)


@app.route("/polls/view/<poll_id>", methods=["GET"])
def poll_display(poll_id):
    """Display the poll information in a single HTML page"""
    data = poll_data.get_poll_data(poll_id)
    if data is None:
        flash("No poll matching the given id was found")
        return redirect(url_for("list_polls"))

    # Ensure dictionary is always displayed in same order (alphabetical)
    counts = sorted(data["votes"].items(), key=lambda x: x[0])

    return render_template("poll_display.html",
                           title=data["title"], counts=counts)


@app.route("/polls/vote/<poll_id>", methods=["GET", "POST"])
def poll_vote(poll_id):
    """Vote in a specific poll"""
    data = poll_data.get_poll_counts()
    if data is None:
        flash("No poll matching the given id was found")
        return redirect(url_for("list_polls"))

    if request.method == "POST":
        choice = request.form["choice"]
        if choice is None or choice not in data["votes"]:
            flash("You must choose a valid option")
        else:
            poll_data.vote(poll_id, choice)
            return redirect(url_for("poll_display", poll_id=poll_id))

    # If this is an invalid form or a GET request...
    return render_template("poll_vote.html",
                           title=data["title"],
                           choices=data["votes"].keys(),
                           poll_id=poll_id)

@app.route("/polls/data/<poll_id>")
def poll_data(poll_id):
    """Return poll data as JSON"""
    data = poll_data.get_poll_counts()
    if data is None:
        err = jsonify({"message": "No poll matching the given id was found"})
        return err, 404

    return jsonify(data)
