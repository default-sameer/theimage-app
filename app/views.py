import os
from flask import render_template, url_for, request, redirect, abort, send_from_directory, flash, send_file
from flask.wrappers import Response
from app import app, db, view_counter
from app.forms import User, LoginForm, RegistrationForm, EditProfileForm, ImageForm
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from app.utils import validate_image
from flask_login import login_required, current_user, logout_user, login_user
from app.models import User, Image, Category
from io import BytesIO
import base64
from base64 import b64encode


@app.route('/view_counter')
@view_counter.count
def view_counter():
	return "Hello World"

@app.cli.command('refresh')
def refresh():
    db.drop_all()
    db.create_all()
    u = User(username='Test@123', email='sameer@theimage-app.com', password_hash='pbkdf2:sha256:260000$rgzKhVsEpwmgFiPo$9948467113a6a459558d1c23df8e5f4f086cf0b4eb636addef1f06606905e4fa')
    db.session.add(u)
    db.session.commit()
    print('Data Added')

@app.get('/')
def index():
    users = User.query.all()
    return render_template('index.html', title='Home', users=users)


@app.get('/explore')
def explore():
    # images = os.listdir(app.config['UPLOAD_FOLDER'])
    images = Image.query.order_by(Image.pic_date.desc())
    return render_template('explore.html', title='Explore', images=images)


@app.get('/categories')
def categories():
    images = Image.query.all()
    return render_template('categories.html', title='Categories', images=images)

@app.get('/categories/<name>')
def categories_name(name):
    image = Image.query.filter_by(category_name=name)
    return render_template('categories_name.html', title=name, image=image)


@app.get('/login')
@app.post('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(request.referrer)


@app.get('/register')
@app.post('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/user/<username>")
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    images = Image.query.filter_by(author=user)
    return render_template('profile.html', user=user, images=images, title=username)

@app.get('/edit_profile')
@app.post('/edit_profile')
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('profile', username=current_user.username))
    elif request.method == 'GET':
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii')
    return render_pic

@app.get('/upload')
@app.post('/upload')
@login_required
def upload():
    form = ImageForm()
    if request.method == 'POST':
        file = form.file.data
        filename = secure_filename(file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(file.stream):
                flash('Invalid Image')
                return redirect(request.referrer)
        data = file.read()
        render_file = render_picture(data)
        text = form.text.data
        category = form.categories.data
        new_image = Image(name=file.filename, data=data, rendered_data=render_file, text=text, user_id=current_user.id, category_name=category)
        # category = Category(name=category, image_id=current_user.id)
        db.session.add(new_image)
        # db.session.add(category)
        db.session.commit()
        flash('Image Uploaded Sucessfully')
        return redirect(url_for('upload'))
    return render_template('upload.html', title='Upload', form=form)


# @app.post('/file-upload')
# @login_required
# def upload_file():
#     form = ImageForm()
#     file = form.file.data
#     filename = secure_filename(file.filename)
#     if filename != '':
#         file_ext = os.path.splitext(filename)[1]
#         if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
#                 file_ext != validate_image(file.stream):
#             return "Invalid image", 400
#     data = file.read()
#     render_file = render_picture(data)
#     text = request.form['text']
#     location = request.form['location']
    
#     newFile = Image(name=file.filename, data=data, rendered_data=render_file, text=text, location=location, user_id=current_user.id) 
#     db.session.add(newFile)
#     db.session.commit()
#     flash('Image Uploaded Sucessfully')
#     return redirect(url_for('index'))

@app.route('/download/<int:pic_id>')
def download(pic_id):
    file_data=Image.query.filter_by(id=pic_id).first()
    file_name=file_data.name
    return send_file(BytesIO(file_data.data), attachment_filename=file_name, as_attachment=True)


@app.route('/image/<int:pic_id>')
def image(pic_id):
    get_img = Image.query.filter_by(id=pic_id).first()
    return render_template('image.html', pic=get_img)


@app.post("/delete/<int:pic_id>")
@login_required
def delete(pic_id):
    del_pic = Image.query.get(pic_id)
    if request.method == 'POST':
        form = request.form['delete']
        db.session.delete(del_pic)
        db.session.commit()
        return redirect(url_for('index'))
    

@app.errorhandler(413)
def too_large(e):
    flash('File Too Large')
    return redirect(request.referrer)



