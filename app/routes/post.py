from flask import Blueprint, render_template, request, redirect, abort
from ..extensions import db
from ..models.post import Post
from ..models.user import User
from sqlalchemy import desc
from flask_login import login_required, current_user
from ..forms import StudentForm

post = Blueprint('post', __name__)


@post.route('/', methods=['POST','GET'])
def all():
    posts = Post.query.order_by(desc(Post.date)).all()
    return render_template('post/all.html', posts = posts, user=User)


@post.route('/post/create', methods=['POST', 'GET'])
@login_required
def create():
    form = StudentForm()
    if current_user.status == 'teacher':

        form.student.choices = [s.name for s in User.query.filter_by(status='user')]
        if request.method == 'POST':
            subject = request.form.get('subject')
            student = request.form.get('student')
            student_id = User.query.filter_by(name=student).first().id

            post = Post(teacher=current_user.id, subject=subject, student=student_id)

            try:
                db.session.add(post)
                db.session.commit()
                return redirect('/')
            except Exception as e:
                print(str(e))
        else:
            return render_template('post/create.html', form=form)
    else:
        abort(403)


@post.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    post = Post.query.get(id)

    if post.teacher == current_user.id:

        if request.method == 'POST':
            student = request.form.get('student')
            subject = request.form.get('subject')

            try:
                db.session.commit()
                return redirect('/')

            except Exception as e:
                print(str(e))


        else:
            return render_template('post/update.html', post_id=post.id, post=post, user=User)

    else:
        abort(403)



@post.route('/post/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def delete(id):
    post = Post.query.get(id)

    if post.teacher == current_user.id and current_user.status == 'teacher':

        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        abort(403)