from app import app
from flask import render_template, flash, redirect, url_for
from app.forms import AddContactForm, LoginForm, SignupForm
from app.models import Address, User
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/') # no colon here...
@app.route('/index') # you can combine multiple routes and define the render template in def part
def index():
    return render_template('index.html')


@app.route('/signup', methods=["GET", "POST"]) # to be able to retrieve from server as well
def signup():
    # need to create user db/class if: user does not exist w same email; set user_id auto; 
    form = SignupForm()
    if form.validate_on_submit():
        print('form has been validated!')
        email = form.email.data
        password = form.password.data # i think here is where i should create password hash? so i'm checking to see if form data matches so that the user can get logged in...
        # before creating a new user need to check if user already exists before adding them
        existing_user = User.query.filter(email == User.email).first() # this filters out the first instance with the same email as the one trying to be created
        if existing_user:
            # tell user that email already exists, re-render template for signup
            flash("Sorry, a user with that email already exists.", 'danger')
            return redirect(url_for('signup'))
        new_user = User(email=email, password=password) # generate a password hash...this us done entirely in User class
        print(new_user) # print to test out
        # flash msg signup success
        flash("Thanks for signing up! Please sign in to continue", 'success')
        return redirect(url_for('login'))
    print('form was not validated.')
    return render_template('signup.html', form=form) # this form=form indicates to create a new SignupForm if form not validated


@app.route('/login', methods=["GET", "POST"]) # to be able to retrieve from server as well
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # store user's input from form
        email = form.email.data
        password = form.password.data
        # check db for both a matching email and matching password
        user = User.query.filter_by(email=email).first() # COME BACK TO TRY TO UNDERSTAND THIS
        # if user email does exist, check their password to see if it matches with db
        if user and user.check_password(password):
            # if True, log the user in
            login_user(user)
            flash(f'Welcome back!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Sorry, your email/password is incorrect. Please try again.', 'danger')
            return redirect(url_for('login')) # WHY DO WE NEED THIS? IF NO ELSE, THEN WOULDNT THE LAST RETURN RENDER_TEMPLATE WORK?
    return render_template('login.html', form=form) # insert in () the variables that need to be displayed in html from login form


@app.route('/phonebook', methods=["GET", "POST"]) # to be able to retrieve from server as well
def phonebook():
    addresses = Address.query.all()
    print(addresses)
    # ...maybe need to add code to only get the phonebook for the user that is logged in...or maybe done in html
    return render_template('phonebook.html', addresses=addresses) # insert in () the variables that need to be displayed in html from phonebook form


@app.route('/logout', methods=["GET", "POST"]) # to be able to retrieve from server as well
def logout():
    logout_user()
    flash("You have logged out successfully", "success") 
    return redirect(url_for('index')) # insert in () the variables that need to be displayed in html from login form


@app.route('/phone', methods=['GET', 'POST']) # method error in browser if methods NOT input here
@login_required
def phone():
    form = AddContactForm()
    if form.validate_on_submit(): # validate_on_submit is a module/fn inside FlaskForm
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        new_address = Address(name=name, phone=phone, address=address, user_id=current_user.id) # create instance Address from models.py
        print(new_address)
        flash(f"You've added {new_address.name} to your phonebook!", 'success')
        return redirect(url_for('phonebook'))
    return render_template('phone.html', form=form)


@app.route('/addresses/<address_id>') # COME BACL LATER TO UNDERSTAND THIS
@login_required
def view_address(address_id): # the address_id in () refers to the <address_id> in the app.route
    ###################### A USER SHOULD ONLY BE ABLE TO VIEW THEIR OWN CONTACTS/PHONEBOOK, NOT OTHER USERS'
    address_to_view = Address.query.get_or_404(address_id)
    print(current_user.id, address_to_view.user_id)
    if current_user.id != address_to_view.user_id:
        flash('''Sorry, the contact address you are looking for does not belong to you. 
                Please choose a contact from your list.''', 'danger')
        return redirect(url_for('phonebook'))
    return render_template('address.html', address_to_view=address_to_view)


# CREATE ROUTES FOR EDITING CONTACT ADDRESS, AND DELETING...

@app.route('/addresses/<address_id>/edit_address', methods=["POST", "GET"])
@login_required
def edit_address(address_id):
    # need to render new html page? to edit the content? or can edit in same page?
    # in any case, will need to show phone form again so that they can edit it.
    address_to_edit = Address.query.get_or_404(address_id) # this gets the desired contact info
    # make sure the address to edit is owned by its owner
    if address_to_edit.owner != current_user:
        flash('Sorry, this contact does not belong to you. Please edit one of your contacts.', 'danger')
        return redirect(url_for('view_address', address_id=address_id)) # COME BACK LATER TO UNDERSTAND THIS
    form = AddContactForm()
    if form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        address = form.address.data
        address_to_edit.update(name=name, phone=phone, address=address)
        flash(f'You have successfully updated {address_to_edit.name}\'s info to your phonebook.', 'success')
        return redirect(url_for('view_address', address_id=address_id))
    return render_template('edit_address.html', address=address_to_edit, form=form)


@app.route('/addresses/<address_id>/delete_address')
@login_required
def delete_address(address_id):
    # need to delete the indicated address..so user has already selected an address to delete..
    address_to_delete = Address.query.get_or_404(address_id)
    if address_to_delete.owner != current_user:
        flash(f'Sorry, this post does not belong to you. Please choose one of your own contacts.', 'danger')
        return redirect(url_for('view_address', address_id=address_id))
    address_to_delete.delete()
    flash(f'Contact info successfully deleted for {address_to_delete.name}.', 'info')
    return redirect(url_for('phonebook'))