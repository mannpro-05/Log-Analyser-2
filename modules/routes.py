from flask import request, render_template, send_file, redirect, url_for, flash
import sqlite3 as sl
from modules.handlers import reportHandler, filterHandler, emailHandler, handleDownloads, deleteHandler, activityHandler\
    ,magicSuggestHandler
from modules.mailDict import mailUpdate, sendMail
import time
from datetime import datetime
import inspect
import os
import json
from modules import app,db,bcrypt
from modules.forms import RegistrationForm, LoginForm, UpdateAccountForm, ResetPasswordForm, RequestResetForm
from modules.models import User
from flask_login import login_user, current_user, logout_user, login_required
from modules.savePcture import savePicture

@app.route("/")
@app.route("/home")
def home():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    return redirect(url_for('login'))


''' Code for handling log related python routes starts from here '''

@app.route('/createReport')
@login_required
def createReport():
    options = ["DATE_TIME", "STATUS", "UPLOAD", "DOWNLOAD", "CLIENT_IP", "USERNAME", "METHOD", "URL", "HTTP_REFERER", "USERAGENT", "FILTER_NAME", "FILTER_REASON", "CACHECODE", "USER_GROUP", "REQUEST_PROFILES", "APPLICATION_SIGNATURES", "CATEGORIES", "UPLOAD_CONTENT", "DOWNLOAD_CONTENT"]
    filterTable = ["Columns","Condition","Value","Action"]
    emailTable = ["Recipient","Frequency","Schedule","Actions"]
    frequency = ["Daily","Weekly","Monthly"]
    weekDays = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    return render_template('createReport.html', options=options, filterTable = filterTable, emailTable = emailTable,
                            frequency = frequency, weekDays = weekDays)

'''
input: None
processing: Gets all the reports of the user!
Output: sends a json format object to the frontend which contains all the records and information regarding it.
'''
@app.route('/viewReport')
@login_required
def viewReport():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    rows, reportsTableColumns = reportHandler.getReport()
    return render_template('viewReports.html', reportsTableColumns = reportsTableColumns, rows = rows)

@app.route('/config')
@login_required
def config():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    with open('modules/config.json') as configFile:
        config_data = json.load(configFile)
        print(config_data)
        return render_template('mailConfig.html', smtp=config_data["MAIL_SERVER"], port=config_data["MAIL_PORT"], \
                               email=config_data["MAIL_USERNAME"], password=config_data["MAIL_PASSWORD"])

@app.route('/helpForm')
@login_required
def helpForm():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    return render_template('helpForm.html')

@app.route('/activityLog')
@login_required
def activityLog():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    activity = activityHandler.getActivity()
    return render_template('activityLog.html',activity = activity)
'''
input: title, description, fields, emailDetails, Filters
processing: Stores the records into the database.
Output: sends an appropriate message to the user regarding the insertion of the record.
'''
@app.route('/insertReport', methods=["GET","POST"])
@login_required
def insertReport():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])

    if request.method == "POST":
        data = request.get_json()
        conn = sl.connect('logs.db')
        print(data)
        id = reportHandler.createReport(data["title"], data["description"], data['fields'], current_user.id)
        if type(id) is dict:
            return id
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")", "Created: " +\
                      data["title"] + " Report.", "Create Report Page."))
        conn.commit()
        filterHandler.createFIlter(id, data["filters"],data["startDate"],data["startTime"],data["endDate"], data["endTime"])
        emailHandler.createEmail(id, data["email"])
        return {'message':'The Report has been created successfully!', 'type':'success'}


'''
input: ID of the record that the user wants to download.
processing: prepares the file for the report which is asked by user.
Output: returns the file to the user.
'''
@app.route('/download/<title>/<fileType>')
@login_required
def download(title, fileType):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    start = time.time()
    fileName = handleDownloads.createDownloadFile(title=title, fileType=fileType, pythonFileName=inspect.stack()[0][3])
    end = time.time()
    conn = sl.connect('logs.db')
    conn.execute("INSERT INTO INSERT_TIME VALUES (?,?)", (title, end - start))
    conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                 (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")", "Downloaded : " +\
                  title + "." + fileType,"View Report Page."))
    conn.commit()
    print(end-start)
    return send_file(os.getcwd()+'/modules/downloadReports/'+fileName,as_attachment=True)


@app.route('/mailDownload/<token>', methods=["GET","POST"])
def mailDownload(token):
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    fileName = User.get_download_file(token)
    if fileName is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('login'))
    return send_file(os.getcwd() + '/modules/downloadReports/' + fileName, as_attachment=True)


@app.route('/deleteReport', methods=["POST"])
@login_required
def deleteReport():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    if request.method == "POST":
        data = request.get_json()
        message = deleteHandler.deleteReport(data["title"], current_user.id)
        conn = sl.connect('logs.db')
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")", "Deleted: " + data["title"] + " Report.",'View Reports Page.'))
        conn.commit()
        return message
@app.route('/mailConfig', methods=['GET','POST'])
@login_required
def mailConfig():
    now = datetime.now()
    app.logger.info(
        str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    if request.method == 'POST':
        data = request.get_json()
        message = mailUpdate.mailConfig(data)
        conn = sl.connect('logs.db')
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")"\
                          , "Made Changes in the database!", "Mail Config Page."))
        conn.commit()
        return message


@app.route('/sendQuery', methods=["GET","POST"])
@login_required
def sendQuery():
    if request.method == "POST":
        now = datetime.now()
        app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
        data = request.get_json()
        sendMail.sendQuery(data["subject"],data["body"])
        conn = sl.connect('logs.db')
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.email + " ("+current_user.email+")",\
                      "Sent a query to support@safesquid.net", "Help Form Page."))
        conn.commit()
        return {"message":"done!"}

@app.route('/getMagicSuggestData', methods=["POST"])
@login_required
def getMagicSuggestData():
    if request.method == "POST":
        data = request.get_json()
        return magicSuggestHandler.getData(data["filter"])


''' Code for handling log related python routes Ends here '''




'''  Code for login module starts from here!!  '''

@app.route("/register", methods=['GET', 'POST'])
@login_required
def register():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    if current_user.is_authenticated and current_user.admin:
        form = RegistrationForm()
        if form.validate_on_submit():
            hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(email=form.email.data).first()
            conn = sl.connect('logs.db')
            conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                         (now.strftime("%H:%M %Y-%m-%d"), current_user.username,
                          "Created: " + user.username+ " ("+current_user.email+")" + " User in the system."\
                          , "Register Page."))
            conn.commit()
            flash('Your account has been created!', 'success')
            sendMail.user_register(user)
            return redirect(url_for('login'))
        return render_template(r'register.html', title='Register', form=form)
    else:
        flash('you do not have permission to register new users!','danger')
        return redirect(url_for('account'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    conn = sl.connect('logs.db')
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form = LoginForm()
    if form.validate_on_submit():
        user_email = User.query.filter_by(email=form.email.data).first()
        user_username = User.query.filter_by(username=form.email.data).first()
        if (user_email and bcrypt.check_password_hash(user_email.password, form.password.data)):
            login_user(user_email, remember=True)

            conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                         (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")",
                          "Logged into the system.", "Login Page"))
            conn.commit()
            return redirect(url_for('account'))


        elif (user_username and bcrypt.check_password_hash(user_username.password, form.password.data)):
            login_user(user_username, remember=True)
            conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                         (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")",
                          "Logged into the system.","Login Page"))
            conn.commit()
            return redirect(url_for('account'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template(r'login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    if current_user.is_authenticated:
        conn = sl.connect('logs.db')

        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.username + " ("+current_user.email+")",
                      "Logged out from the system.", "Account Page"))
        conn.commit()
        logout_user()
    return redirect(url_for('login'))



@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    form = UpdateAccountForm()
    if form.validate_on_submit():
        conn = sl.connect('logs.db')
        if form.picture.data:
            picture_file= savePicture.save_picture(form.picture.data)
            current_user.image_file = picture_file
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), current_user.username+ " ("+current_user.email+")",
                      "Made changes to their account details.","Account Page"))
        conn.commit()
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file= url_for('static', filename='profiles/' + current_user.image_file)
    return render_template(r'account.html', title='Account', image_file=image_file, form=form)


@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    now = datetime.now()
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        conn = sl.connect('logs.db')
        user = User.query.filter_by(email=form.email.data).first()
        sendMail.send_reset_email(user)
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), form.email.data,
                      "Requested for reset password","Reset Password Page"))
        conn.commit()
        flash('An email has been send to the administrator with instructions to reset your password!','success')
        return redirect(url_for('login'))
    return render_template(r'reset_request.html', title='Reset password', form=form, legend='Reset Password')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        now = datetime.now()
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        conn = sl.connect('logs.db')
        conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                     (now.strftime("%H:%M %Y-%m-%d"), user.username + " ("+user.email+")" ,
                      "Admin Re-set the password password","Update Password Page"))
        conn.commit()
        flash('Your password has been Updated!', 'success')
        return redirect(url_for('home'))
    return render_template(r'reset_token.html', title='Reset Password', form=form)

@app.route('/remove_pic', methods=['GET','post'])
def remove_pic():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    form=UpdateAccountForm()
    current_user.image_file = 'default.jpg'
    db.session.commit()
    if request.method=='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file= url_for('static', filename='profiles/default.jpg')
    return redirect(url_for('account', image_file=image_file))

@app.route('/delete_profile')
def delete_account():
    now = datetime.now()
    app.logger.info(str(now.strftime("%H:%M %Y-%m-%d")) + ' ' + __file__ + ' ' + inspect.stack()[0][3])
    user=User.query.filter_by(email=current_user.email).first()
    now = datetime.now()
    conn = sl.connect('logs.db')
    conn.execute("INSERT INTO ACTIVITY VALUES (?,?,?,?)",
                 (now.strftime("%H:%M %Y-%m-%d"), current_user.username,
                  "Deleted their account","Account's Page"))
    conn.commit()
    User.query.filter_by(email=user.email).delete()
    flash('Your password has been Updated!', 'success')
    db.session.commit()
    flash('Profile has been removed successfully','success')
    return redirect(url_for('logout'))

'''  Code for login module ends from here!!  '''
