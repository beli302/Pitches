from flask import render_template, request, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . forms import PitchForm, CommentForm, CategoryForm, UpdateProfile
from .import main
from .. import db
from ..models import User, Pitch, Comments, PitchCategory, Votes

# @main.route("/")
# def welcome():
#     return render_template('welcome.html', title = 'Welcome')


#display categories on the landing page
@main.route('/')
def index():
    """
    View root page function that returns index page
    """

    all_pitches = Pitch.query.all()
    print(all_pitches)

    title = 'Home- Welcome'
    return render_template('index.html', title=title, all_pitches=all_pitches)


# Route for adding a new pitch
@main.route('/pitch', methods=['GET', 'POST'])
@login_required
def new_pitch():
    """
    Function to check Pitches form and fetch data from the fields
    """

    form = PitchForm()

    if form.validate_on_submit():

        content = form.content.data
        new_pitch = Pitch(content=content, user=current_user)
        new_pitch.save_pitch()

        return redirect(url_for('main.index'))

    return render_template('new_pitch.html', pitch_form=form)



@main.route('/categories/<int:id>')
def category(id):
    category=PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches=Pitch.get_pitches(id)

    return render_template('category.html', pitches=pitches, category=category)


@main.route('/add/category', methods=['GET', 'POST'])
@login_required
def new_category():
    """
    View new group route function that returns a page with a form to create a category
    """

    form=CategoryForm()

    if form.validate_on_submit():
        name=form.name.data
        new_category=PitchCategory(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title='New category'
    return render_template('new_category.html', category_form=form, title=title)


# view single pitch alongside its comments
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    """
    Function the returns a single pitch for a comment to be added
    """
    pitches=Pitch.query.get(id)
    # pitches = Pitch.query.filter_by(id=id).all()

    if pitches is None:
        abort(404)
    #
    comment=Comments.get_comments(id)
    count_likes=Votes.query.filter_by(pitches_id=id, vote=1).all()
    count_dislikes=Votes.query.filter_by(pitches_id=id, vote=2).all()
    return render_template('view_pitch.html', pitches=pitches, comment=comment, count_likes=len(count_likes), count_dislikes=len(count_dislikes), category_id=id)

# adding a comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """
    Function to post comments
    """

    form=CommentForm()
    title='post comment'
    pitches=Pitch.query.filter_by(id=id).first()

    if pitches is None:
         abort(404)

    if form.validate_on_submit():
        opinion=form.opinion.data
        new_comment=Comments(
            opinion=opinion, user_id=current_user.id, pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)


# Routes upvoting/downvoting pitches
@main.route('/pitch/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id, vote_type):
    """
    View function that adds one to the vote_number column in the votes table
    """
    # Query for user
    votes=Votes.query.filter_by(user_id=current_user.id).all()
    print(f'The new vote is {votes}')
    to_str=f'{vote_type}:{current_user.id}:{id}'
    print(f'The current vote is {to_str}')

    if not votes:
        new_vote=Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
        new_vote.save_vote()
        # print(len(count_likes))
        print('YOU HAVE new VOTED')

    for vote in votes:
        if f'{vote}' == to_str:
            print('Y')
            break
        else:
            new_vote=Votes(
                vote=vote_type, user_id=current_user.id, pitches_id=id)
            new_vote.save_vote()
            print('YOU HAVE VOTED')
            break

    return redirect(url_for('.view_pitch', id=id))



@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)


@main.route('/user/<uname>/update', methods=['GET', 'POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        flash('Your account has been updated!', 'success')

        return redirect(url_for('.profile', uname=user.username))

    return render_template('profile/update.html', form=form)