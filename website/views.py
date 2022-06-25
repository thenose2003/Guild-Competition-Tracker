from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return render_template('home.html')


@views.route('/current')
def current():
    return render_template('home.html')


@views.route('/past-competitions/<int:compID>')
def past_competitions(compID):
    try:
        return render_template('comps/'+str(compID)+'.html', comp_number=compID)
    except:
        return render_template('comps/NoCompFound.html')


@views.route('/admin')
def admin():
    return render_template('base.html')