import psycopg2
from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'topreventcsrf_attacks'


class ItemForm(FlaskForm):
    name = StringField('Name', validators=[
        DataRequired(message='Name is required'),
        Length(min=1, max=100, message='Name must be between 1 and 100 characters'),
    ])
    description = TextAreaField('Description', validators=[
        DataRequired(message='Description is required'),
        Length(min=1, message='Description cannot be empty'),
    ])

    def validate_name(self, field):
        if not isinstance(field.data, str):
            print("Name validation failed: Name must be a string")
            raise ValidationError('Name must be a string')

    def validate_description(self, field):
        if not isinstance(field.data, str):
            print("Description validation failed: Description must be a string")
            raise ValidationError('Description must be a string')


DATABASE_URL = "postgresql://postgres:12345@localhost/NewDb"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()
cursor.execute('DROP TABLE IF EXISTS items')
cursor.execute('''
    CREATE TABLE items (
        id SERIAL PRIMARY KEY,
        name TEXT,
        description TEXT
    )
''')

conn.commit()


@app.route('/del')
def func():
    return "<h4>you cancelled deletion </h4>"


# Creating
@app.route('/create', methods=['GET', 'POST'])
def create_item():
    form = ItemForm()
    if form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        cursor.execute('INSERT INTO items (name, description) VALUES (%s, %s)', (name, description))
        conn.commit()
        return 'Item created', 201

    return render_template('create_item.html', form=form)


# Reading
@app.route('/read/<int:item_id>', methods=['GET'])
def read_item(item_id):
    cursor.execute('SELECT * FROM items WHERE id = %s', (item_id,))
    item = cursor.fetchone()
    if item:
        return jsonify({'id': item[0], 'name': item[1], 'description': item[2]})
    return 'Item not found', 404


# Update
@app.route('/update/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    form = ItemForm()
    if request.method == 'GET':
        cursor.execute('SELECT name, description FROM items WHERE id = %s', (item_id,))
        item_data = cursor.fetchone()
        # print("Entering update_item function")
        if item_data:
            form.name.data = item_data[0]
            form.description.data = item_data[1]
        else:
            return 'Item not found', 404

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        description = form.description.data

        try:
            cursor.execute('UPDATE items SET name = %s, description = %s WHERE id = %s', (name, description, item_id))
            conn.commit()
            print("Item updated successfully")
            return 'Item updated', 200
        except Exception as e:
            print("Error updating item:", str(e))
    else:
        print("Form validation failed:", form.errors)
    return render_template('update_item.html', form=form, item_id=item_id)


# Delete
@app.route('/delete/<int:item_id>', methods=['GET', 'POST'])
def delete_item(item_id):
    if request.method == 'GET':
        return render_template('confirm_delete.html', item_id=item_id)
    elif request.method == 'POST':
        cursor.execute('DELETE FROM items WHERE id = %s', (item_id,))
        conn.commit()
        return 'Item deleted Successfully', 200


@app.route('/')
def func1():
    return "<h4>Welcome to the flask world </h4>"


if __name__ == "__main__":
    app.run(debug=True)
