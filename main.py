"""
Web app main
"""
import os

from flask import Flask, render_template, request, redirect, url_for

from model import Donation, Donor

app = Flask(__name__)


@app.route('/')
def home():
    """home redirect"""
    return redirect(url_for('donations'))


@app.route('/donations/', methods=['GET', 'POST'])
def donations():
    """
    GET: new donation form
    POST: Make donation entry in db (make donor if not exist)
    :return: webpage
    """
    if request.method == 'GET':
        return render_template('new_donation.jinja2')

    if request.method == 'POST':
        donor_name = str(request.form['donor'])
        value = int(request.form['value'])

        # create new donor if not exist in db
        if not _find_donor(donor_name):
            Donor(name=donor_name).save()

        # get donor object
        donor = Donor.select().where(Donor.name == donor_name)[0]
        # make new donation
        Donation(donor=donor, value=value).save()

        return redirect(url_for('list_donations'))


@app.route('/list/')
def list_donations():
    """get Donation table and post it"""
    return render_template('donations.jinja2', donations=Donation.select())


def _find_donor(name):
    """
    Check to see if donor.name in Donor table
    :param name: donor's name (unique value)
    :type name: str
    :return: bool
    """
    donors = Donor.select().where(Donor.name == name)
    return any([donor.id for donor in donors])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
