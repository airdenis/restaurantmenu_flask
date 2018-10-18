from flask import (
        Flask, render_template, redirect, request, url_for, flash, jsonify
    )
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from database_setup import Base, Restaurant, MenuItem
app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

session_factory = sessionmaker(bind=engine)
DBSession = scoped_session(session_factory)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def restaurantsMenu():
    items = session.query(Restaurant).all()
    session.close()
    return render_template(
            'restaurants.html',
            items=items
            )


@app.route('/restaurants/new/', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        newRestaurant = Restaurant(name=request.form['name'])
        session.add(newRestaurant)
        session.commit()
        session.close()
        flash("New restaurant has been created!")
        return redirect(url_for('restaurantsMenu'))
    else:
        return render_template('newrestaurant.html')


@app.route(
        '/restaurants/<int:restaurant_id>/edit/',
        methods=['GET', 'POST']
        )
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(Restaurant).filter_by(
            id=restaurant_id
            ).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
        session.add(editedRestaurant)
        session.commit()
        session.close()
        flash("Restaurant has been edited!")
        return redirect(url_for('restaurantsMenu'))
    else:
        return render_template(
                'editrestaurant.html',
                restaurant_id=restaurant_id,
                item=editedRestaurant)


@app.route(
        '/restaurants/<int:restaurant_id>/delete/',
        methods=['GET', 'POST']
        )
def deleteRestaurant(restaurant_id):
    deleteRestaurant = session.query(Restaurant).filter_by(
            id=restaurant_id
            ).one()
    if request.method == 'POST':
        session.delete(deleteRestaurant)
        session.commit()
        session.close()
        flash("Restaurant has been deleted!")
        return redirect(url_for('restaurantsMenu'))
    else:
        return render_template(
                'deleterestaurant.html',
                item=deleteRestaurant
                )


@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template(
            'menu.html',
            restaurant=restaurant,
            items=items
            )


@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
                name=request.form['name'],
                description=request.form['description'],
                price=request.form['price'],
                course=request.form['course'],
                restaurant_id=restaurant_id
                )
        session.add(newItem)
        session.commit()
        session.close()
        flash("new menu item created!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route(
        '/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
        methods=['GET', 'POST']
        )
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        session.close()
        flash("menu item edited!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
                'editmenuitem.html',
                restaurant_id=restaurant_id,
                menu_id=menu_id,
                item=editedItem)


@app.route(
        '/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
        methods=['GET', 'POST']
        )
def deleteMenuItem(restaurant_id, menu_id):
    deleteItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleteItem)
        session.commit()
        session.close()
        flash("menu item deleted!")
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
                'deletemenuitem.html',
                item=deleteItem
                )


@app.route('/restaurants/JSON/')
def restaurantsJSON():
    items = session.query(Restaurant).all()
    session.close()
    return jsonify(Restaurants=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/JSON/')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
            restaurant_id=restaurant.id
            ).all()
    session.close()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id=menu_id).one()
    session.close()
    return jsonify(MenuItem=item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
