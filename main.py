########## setting up FLASK AND SQL ###############################
#importing what we need 
import os
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


#Reset the database 
try:
    os.remove("data.sqlite")
except OSError:
    pass

# creating an instance of a flask application.
app = Flask(__name__)

#find the directory we are currently in
dir_path = os.path.dirname(os.path.realpath(__file__))

# Connects our Flask App to our Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(dir_path, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'mysecretkey'
#starts our data base
db = SQLAlchemy(app)

############### DONE setting up FLASK AND SQL ############################

##############  DEFINING AND CREATING SQL TABLE####################

####### defining a Contact table: ##########

class Contact(db.Model):
  
  id = db.Column(db.Integer,primary_key=True) # Primary Key with unique id 
  name = db.Column(db.Text)  # name 
  phone = db.Column(db.Text)  # phone number

  #Contact("Shon","99999")
  # define how to make a new contact
  def __init__(self,name,phoneNumber):
    self.name = name
    self.phone = phoneNumber
    # no need to worry about id, since sql takes care of it

  # explain how to print a user
  def __repr__(self):
    return f"ID: {self.id}   Name: {self.name}   Phone: {self.phone}  "
  
####### done defining a Contact table: ##########

#back to the main code since we are not indented
# Now that we have defined our users we need to "create" the table by running:
db.create_all()

############## DONE DEFINING AND CREATING SQL TABLE####################
##############  ADD ITEMS TO THE DATABASE AS NEEDED####################

# Lets create a few names and add them to the database


# create adam,bob, and roger
adam = Contact('Adam','123-456-7890')
bob = Contact('Bob','222-222-2222')
roger = Contact('Roger','111-111-1111')
#add and commit them to the database
db.session.add(adam)
db.session.add(bob)
db.session.add(roger)
db.session.commit()

############## DONE ADDING ITEMS TO THE DATABASE AS NEEDED####################
#################### DEFINE FORMS HERE###########################3
# define a form to add a user
class AddUser(FlaskForm):
    name = StringField('Name')
    phone = StringField('Phone Number')
    # Every form needs a submit!
    submit = SubmitField('Add Contact')

# define a form to delete a user
class DeleteUser(FlaskForm):
    id = StringField('ID')
    # Every form needs a submit!
    submit = SubmitField('Delete User')
  
# define a form to update a user
class UpdateUser(FlaskForm):
    id = StringField('ID')
    name = StringField('New Name')
    phone = StringField('New Phone Number')
    # Every form needs a submit!
    submit = SubmitField('Update User')
############## MANAGE OUR ROUTES AS NEEDED #############################
# home page 
@app.route("/")                    
def index():
  contacts = Contact.query.all()           
  return render_template("index.html", contacts=contacts )

# add page 
@app.route("/add",methods=['POST','GET'])                    
def add():  
  form = AddUser()
  if form.validate_on_submit():
    # grab the data from the form 
    name = form.name.data
    phone = form.phone.data
    # create a new contact and add to the database
    user = Contact(name,phone)
    db.session.add(user)
    db.session.commit()
    # redirect
    return redirect(url_for('index'))
  
  return render_template("add.html", form=form)

# delete page 
@app.route('/delete', methods=['POST','GET'])
def delete():
  form = DeleteUser()
  if form.validate_on_submit():
    # grab the string id and convert it to a int
    id = form.id.data
    id = int(id)
    # find the user with that id 
    contact = Contact.query.get(id)
    # delete and commit these changes 
    db.session.delete(contact)
    db.session.commit()
    # redirect them back to home page 
    return redirect(url_for('index'))

    
  contacts = Contact.query.all()  
  return render_template("delete.html", contacts=contacts, form=form)
  
#Update Pages
@app.route('/update', methods = ['POST','GET'])  
def update():
  form = UpdateUser()
  if form.validate_on_submit():
    id = form.id.data
    id = int(id)
    # find the user with that id 
    contact = Contact.query.get(id)
    # grab the data from the form 
    name = form.name.data
    phone = form.phone.data
    # create a new contact and add to the database
    user = Contact(name,phone)
    db.session.add(user)
    db.session.commit()
    # redirect
    return redirect(url_for('index'))
  return render_template("update.html", form=form)

  
##################################################################

######################## Run THE APP ###################

# Makes sure this is the main process
if __name__ == "__main__": 
  # Starts the site 
	app.run( 
    # Establishes the host, required for replit to detect the site
		host='0.0.0.0',  
    # setting debug mode to true so we can see errors 
    debug=True
	)