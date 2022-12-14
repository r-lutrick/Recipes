from flask import render_template, redirect, request, session
from flask_bcrypt import Bcrypt
from flask import flash
from flask_app import app
from datetime import datetime

# Import models
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


@app.route('/recipes/<int:id>/view')
def view_recipe(id):
    data = {'id': id}
    one_recipe = Recipe.get_by_id(data)
    logged_user = User.get_by_id({'id': session['user_id']})
    return render_template('view_recipe.html', one_recipe=one_recipe, logged_user=logged_user)


@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/dashboard')
    now = datetime.now()
    now = now.strftime('%Y-%m-%d')
    return render_template('new_recipe.html', now=now)


@app.route('/recipes/<int:id>/edit')
def edit_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    now = datetime.now()
    now = now.strftime('%Y-%m-%d')
    one_recipe = Recipe.get_by_id({'id': id})
    return render_template('edit_recipe.html', one_recipe=one_recipe, now=now)


@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    data = {
        'id': id,
        'name': request.form['recipe_name'],
        'description': request.form['recipe_description'],
        'instruction': request.form['recipe_instructions'],
        'created_at': request.form['recipe_created'],
        'under': request.form['recipe_under'],
        'user_id': session['user_id']
    }
    if not Recipe.validate(data):
        return redirect('/recipes/new')
    Recipe.update(data)
    return redirect('/dashboard')


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    data = {
        'name': request.form['recipe_name'],
        'description': request.form['recipe_description'],
        'instruction': request.form['recipe_instructions'],
        'created_at': request.form['recipe_created'],
        'under': request.form['recipe_under'],
        'user_id': session['user_id']
    }
    if not Recipe.validate(data):
        return redirect('/recipes/new')
    Recipe.create(data)
    return redirect('/dashboard')


@app.route('/recipes/<int:id>/remove')
def remove_recipe(id):
    if 'user_id' not in session:
        return redirect('/dashboard')
    Recipe.remove({'id': id})
    return redirect('/dashboard')
