from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, Blueprint
from app.models import db, category
from app.views.forms import CategoryForm, SubcategoryForm
from app.models.category import Category, Subcategory
from app import db



categoriesbp = Blueprint('categoriesbp', __name__)
subcategoriesbp = Blueprint('subcategoriesbp', __name__)

from app.models.category import Category

@categoriesbp.route('/', methods=['GET', 'POST'])
def manage_categories():
    form = CategoryForm()
    if form.validate_on_submit():
        new_category = Category(name=form.name.data)
        db.session.add(new_category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('categoriesbp.manage_categories'))

    # Fetch all categories from the database
    categories = Category.query.all()

    return render_template('categories.html', form=form, categories=categories)


@categoriesbp.route('/categories/delete/<int:category_id>', methods=['POST'])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('categoriesbp.manage_categories'))



# @subcategoriesbp.route('/subcategories', methods=['GET', 'POST'])
# def manage_subcategories():
#     form = SubcategoryForm()
#     form.category_id.choices = [(cat.id, cat.name) for cat in Category.query.all()]
#     if form.validate_on_submit():
#         subcategory = Subcategory(name=form.name.data, category_id=form.category_id.data)
#         db.session.add(subcategory)
#         db.session.commit()
#         flash('Subcategory added successfully!', 'success')
#         return redirect(url_for('manage_subcategories'))
#     subcategories = subcategory.query.all()
#     return render_template('subcategories.html', form=form, subcategories=subcategories)


@subcategoriesbp.route('/subcategories', methods=['GET', 'POST'])
def manage_subcategories():
    form = SubcategoryForm()
    form.category_id.choices = [(cat.id, cat.name) for cat in Category.query.all()]
    if form.validate_on_submit():
        subcategory = Subcategory(name=form.name.data, category_id=form.category_id.data)
        db.session.add(subcategory)
        db.session.commit()
        flash('Subcategory added successfully!', 'success')
        return redirect(url_for('subcategoriesbp.manage_subcategories'))  # Correct the redirect here

    subcategories = Subcategory.query.all()
    return render_template('subcategories.html', form=form, subcategories=subcategories)



@subcategoriesbp.route('/subcategories/delete/<int:subcategory_id>', methods=['POST'])
def delete_subcategory(subcategory_id):
    subcategory = Subcategory.query.get_or_404(subcategory_id)
    db.session.delete(subcategory)
    db.session.commit()
    flash('Subcategory deleted successfully!', 'success')
    return redirect(url_for('subcategoriesbp.manage_subcategories'))

@subcategoriesbp.route('/get_subcategories/<int:category_id>', methods=['GET'])
def get_subcategories(category_id):
    subcategories = Subcategory.query.filter_by(category_id=category_id).all()
    return jsonify([(sub.id, sub.name) for sub in subcategories])