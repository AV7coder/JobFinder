from flask import Flask,render_template,request,flash,redirect
from flask_login import login_user,logout_user, UserMixin, LoginManager
from flask_sqlalchemy import SQLAlchemy
#imports

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='qwertyuiopasdfghjklzxcvbnm'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
class JobReqd(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wantedjob = db.Column(db.String(120), unique=True, nullable=False)
    wantedpost = db.Column(db.String(80), nullable=False)
    wantedsalary=db.Column(db.Integer, nullable=False)
    yourdescription=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.wantedjob + self.wantedpost

class AvailableJob(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    availablejob = db.Column(db.String(120), unique=True, nullable=False)
    postreqd = db.Column(db.String(80), nullable=False)
    averagesalary=db.Column(db.Integer, nullable=False)
    jobdescription=db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return '<User %r>' % self.availablejob + self.postreqd

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    fname=db.Column(db.String(100), nullable=False)
    lname=db.Column(db.String(100), nullable=False)
    account_status=db.Column(db.String(100), nullable=False)
    db.relationship('JobReqd')
    db.relationship('AvailableJob')
    def __repr__(self):
        return '<User %r>' % self.email + self.password
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# seting up

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        email=request.form.get('email')
        password=request.form.get('password')
        user =User.query.filter_by(email=email).first()
        if user and password==user.password:
            login_user(user, remember=True)
            flash(f'Welcome to back Job Finder {email}', 'success')
            return redirect('/')
        else:
            flash(f'Invalid Credentials."', 'warning')
            return redirect('/login')
    return render_template("login.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        fname = request.form.get('first_name')
        lname = request.form.get('last_name')
        user=User(email=email,password=password,fname=fname,lname=lname,account_status="active")
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome to Job Finder {email}', 'success')
        return redirect('/login')

    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged Out of your Account', 'success')
    return redirect('/')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/vacancie', methods=['POST', 'GET'])
def vacancie():
    if request.method == 'POST':
        jobavailable = request.form.get("job_type")
        averagesalary = request.form.get("salary")
        requiredpost = request.form.get("post")
        jobdescription = request.form.get("describe")
        availablejob=AvailableJob(availablejob=jobavailable,postreqd=requiredpost,averagesalary=averagesalary,jobdescription=jobdescription)
        db.session.add(availablejob)
        db.session.commit()
        flash('Vacancie Posted', 'success')
        return redirect('/')
    return render_template('vacancie.html')

@app.route('/ApplyForJob',methods=['POST', 'GET'])
def applyforjob():
    if request.method == 'POST':
        wantedjob = request.form.get("job_type")
        wantedsalary = request.form.get("salary")
        wantedpost = request.form.get("post")
        yourdescription = request.form.get("describe")
        job=JobReqd(wantedjob=wantedjob, wantedpost=wantedpost,wantedsalary=wantedsalary,yourdescription=yourdescription)
        db.session.add(job)
        db.session.commit()
        flash("SUCCESSFULLY APPLIED!", "success")
        return redirect('/')
    return render_template('apply_for_job.html')

@app.route('/delete', methods=['POST','GET'])
def delete():
    if request.method == 'POST':
        email = request.form.get("email")
        passwordAttempt = request.form.get("password")
        user =User.query.filter_by(email=email).first()
        password = user.password
        if passwordAttempt == password:
            db.session.delete(user)
            db.session.commit()
            flash("Account Deleted.", "secondary")
            return redirect("/")
        else:
            flash("Invalid Password", "danger")
            return redirect("/")
    return render_template("delete.html")
    
@app.route("/accountstatus")
def accountstatus():
    return render_template('accountstatus.html')

@app.route("/activateaccount", methods=['GET', 'POST'])
def activateaccount():
    if request.method == 'POST':
        email = request.form.get("email")
        passwordAttempt = request.form.get("password")
        user =User.query.filter_by(email=email).first()
        password = user.password
        if passwordAttempt == password:
            user.account_status="active"
            db.session.commit()
            flash("Account Activated.", "secondary")
            return redirect("/")
        else:
            flash("Invalid Password", "danger")
            return redirect("/")
    return render_template('activate_account.html')

@app.route("/deactivateaccount", methods=['GET', 'POST'])
def deactivateaccount():
    if request.method == 'POST':
        email = request.form.get("email")
        passwordAttempt = request.form.get("password")
        user =User.query.filter_by(email=email).first()
        password = user.password
        if passwordAttempt == password:
            user.account_status="deactivate"
            db.session.commit()
            print(user.account_status)
            flash("Account Deactivated.", "secondary")
            return redirect("/")
        else:
            flash("Invalid Password", "danger")
            return redirect("/")
    return render_template('deactivateaccount.html')

@app.route("/jobforyou")
def jobforyou():
    jobs = AvailableJob.query.all()
    return render_template("jobforyou.html",variable=jobs)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)