from flask import Flask, render_template, request
from models import connect_db, db, Cocktail
import requests

API_BASE_URL = "http://www.thecocktaildb.com/api/json/v1/1/search.php?s="

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cocktaildb"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)


@app.route('/')
def home_route():
    """Show Home Page."""

    return render_template('home.html')


@app.route('/cocktail', methods=["POST"])
def get_drink():
    """Route that handles database search/store and then making a POST request as well."""

    cocktailSearch = request.form['cocktail'].title()
    result = Cocktail.query.filter_by(title=cocktailSearch).first()

    if result is not None:
        database_result = {"title": result.title, "image_url": result.image_url, "recipe": result.recipe,
                           "instructions": result.instructions, "glass": result.glass}
        return render_template('home.html', cocktail=database_result)
    else:
        cocktailResult = request_cocktail(cocktailSearch)
        db.session.add(Cocktail(**cocktailResult))
        db.session.commit()

        return render_template('home.html', cocktail=cocktailResult)


def request_cocktail(cocktail):
    """Method to make API call passed in from the POST request and then rendering it on home.html"""

    url = f"{API_BASE_URL}{cocktail}"
    response = requests.get(url)
    data = response.json()

    recipe = {}
    cocktails = data["drinks"][0]["strDrink"]
    cocktailImg = data["drinks"][0]["strDrinkThumb"]
    instructions = data["drinks"][0]["strInstructions"]
    glass = data["drinks"][0]["strGlass"]
    for i in range(1, 16, 1):
        if data["drinks"][0][f"strIngredient{i}"] is None or data["drinks"][0][f"strIngredient{i}"] == "":
            break
        else:
            if data["drinks"][0][f"strMeasure{i}"] is None:
                break
            else:
                recipe[f"recipe{i}"] = data["drinks"][0][f"strMeasure{i}"] + \
                    ": " + data["drinks"][0][f"strIngredient{i}"]

    return {"title": cocktails, "image_url": cocktailImg, "recipe": recipe, "instructions": instructions, "glass": glass}
