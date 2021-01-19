import os

from flask import Flask, render_template, request, redirect, url_for, session

from model import db, Donation, Donor

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY').encode()

@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/', methods=['GET', 'POST'])
def all():
    if request.method == 'GET':
        return render_template('new_donation.jinja2')

    if request.method == 'POST':
        donor_name = str(request.form['donor'])
        value = int(request.form['value'])

        # check for new donor
        if not _find_donor(donor_name):
            Donor(name=donor_name).save()

        # get donor object
        donor = Donor.select().where(Donor.name == donor_name)[0]
        # make new donation
        Donation(donor=donor, value=value).save()

        return redirect(url_for('list'))

@app.route('/list/')
def list():
    """get donation and post"""
    return render_template('donations.jinja2', donations=Donation.select())

def _find_donor(name):
    donors = Donor.select().where(Donor.name == name)
    return any([donor.id for donor in donors])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

