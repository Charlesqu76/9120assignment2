# Importing the frameworks
from flask import *
from datetime import datetime
import database

user_details = {}
session = {}
page = {}

# Initialise the application
app = Flask(__name__)
app.secret_key = 'aab12124d346928d14710610f'


#####################################################
##  INDEX
#####################################################

@app.route('/')
def index():
    # Check if the user is logged in
    if('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))
    page['title'] = 'The Central Sydney Hospital'
    
    return redirect(url_for('list_admission'))

    #return render_template('index.html', session=session, page=page, user=user_details)

#####################################################
##  LOGIN
#####################################################

@app.route('/login', methods=['POST', 'GET'])
def login():
    # Check if they are submitting details, or they are just logging in
    if (request.method == 'POST'):
        # submitting details
        login_return_data = check_login(request.form['id'], request.form['password'])

        # If they have incorrect details
        if login_return_data is None:
            page['bar'] = False
            flash("Incorrect login info, please try again.")
            return redirect(url_for('login'))

        # Log them in
        page['bar'] = True
        welcomestr = 'Welcome back, ' + login_return_data['firstName'] + ' ' + login_return_data['lastName']
        flash(welcomestr)
        session['logged_in'] = True

        # Store the user details
        global user_details
        user_details = login_return_data
        return redirect(url_for('index'))

    elif (request.method == 'GET'):
        return(render_template('login.html', page=page))

#####################################################
##  LOGOUT
#####################################################

@app.route('/logout')
def logout():
    session['logged_in'] = False
    page['bar'] = True
    flash('You have been logged out. See you soon!')
    return redirect(url_for('index'))

#####################################################
##  List Admission
#####################################################

@app.route('/list_admission', methods=['POST', 'GET'])
def list_admission():
    # Check if user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # User is just viewing the page
    if (request.method == 'GET'):
        # First check if specific admission
        admission_list = database.findAdmissionsByAdmin(user_details['login'])
        if (admission_list is None):
            admission_list = []
            flash("There are no admissions in the system for " + user_details['firstName'] + " " + user_details['lastName'])
            page['bar'] = False
        return render_template('admission_list.html', admissionlist=admission_list, session=session, page=page)

    # Otherwise try to get from the database
    elif (request.method == 'POST'):
        search_term = request.form['search']
        if (search_term == ''):
            admission_list_find = database.findAdmissionsByAdmin(user_details['login'])
        else:    
            admission_list_find = database.findAdmissionsByCriteria(search_term)
        if (admission_list_find is None):
            admission_list_find = []
            flash("Searching \'{}\' does not return any result".format(request.form['search']))
            page['bar'] = False
        return render_template('admission_list.html', admissionlist=admission_list_find, session=session, page=page)

#####################################################
##  Add Admissioin
#####################################################

@app.route('/new_admission' , methods=['GET', 'POST'])
def new_admission():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # If we're just looking at the 'new admission' page
    if(request.method == 'GET'):
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('new_admission.html', user=user_details, times=times, session=session, page=page)

	# If we're adding a new admission
    success = database.addAdmission(request.form['type'],
                                    request.form['department'],
                                    request.form['patient'],
                                    request.form['condition'],
                                    user_details['login'])
    if(success == True):
        page['bar'] = True
        flash("Admission added!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error adding a new admission")
        return(redirect(url_for('new_admission')))

#####################################################
## Update Admission
#####################################################
@app.route('/update_admission', methods=['GET', 'POST'])
def update_admission():
    # Check if the user is logged in
    if ('logged_in' not in session or not session['logged_in']):
        return redirect(url_for('login'))

    # If we're just looking at the 'update admission' page
    if (request.method == 'GET'):

        datelen = len(request.args.get('discharge_date'))
        if (datelen > 0):
            discharge_date = datetime.strptime(request.args.get('discharge_date'), '%d-%m-%Y').date()
        else:
            discharge_date = ''

        # Get the admission
        admission = {
            'admission_id': request.args.get('admission_id'),
            'type': request.args.get('type'),
			'department': request.args.get('department'),
            'discharge_date': discharge_date,
            'fee': request.args.get('fee'),
            'patient': request.args.get('patient'),
            'condition':request.args.get('condition')
        }

        # If there is no admission
        if admission['admission_id'] is None:
            admission = []
		    # Do not allow viewing if there is no admission to update
            page['bar'] = False
            flash("You do not have access to update that record!")
            return(redirect(url_for('index')))

	    # Otherwise, if admission details can be retrieved
        times = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]
        return render_template('update_admission.html', admissionInfo=admission, user=user_details, times=times, session=session, page=page)

    # If we're updating admission
    discharge_date = request.form['discharge_date']
    if (discharge_date == ''):
        discharge_date = None

    success = database.updateAdmission(request.form['admission_id'],
                                        request.form['type'],
                                        request.form['department'],
                                        discharge_date,
                                        request.form['fee'],
                                        request.form['patient'],
                                        request.form['condition'])
    if (success == True):
        page['bar'] = True
        flash("Admission record updated!")
        return(redirect(url_for('index')))
    else:
        page['bar'] = False
        flash("There was an error updating the admission")
        return(redirect(url_for('index')))


def get_admission(admission_id, patientID):
    for admisison_item in database.findAdmissionByAdmin(patientID):
        if admisison_item['admission_id'] == admission_id:
            return admisison_item
    return None

def check_login(login, password):
    userInfo = database.checkLogin(login, password)

    if userInfo is None:
        return None
    else:
        tuples = {
            'login': userInfo[0],
            'firstName': userInfo[1],
            'lastName': userInfo[2],
            'email': userInfo[3],
        }
        return tuples
