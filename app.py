from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
import secrets
import string
from urllib.parse import urlparse

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///urls.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    original_url = db.Column(
        db.String(2048),
        unique=True,
        nullable=False
    )

    short_code = db.Column(
        db.String(10),
        unique=True,
        nullable=False
    )

    click_counter = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(characters)
        for _ in range(length)
    )

def is_valid_url(url):
    try:
        result=urlparse(url)
        return result.scheme in('http','https') and bool(result.netloc)
    except Exception:
        return False

def error_response(message,code):
    return{
        'error':message
    },code

@app.errorhandler(404)
def handle_404(error):
    return error_response(
        "Resource not found",
        404
    )

@app.errorhandler(405)
def handle_405(error):
    return error_response(
        "Method not allowed",
        405
    )

@app.errorhandler(500)
def handle_500(error):
    return error_response(
        "Internal server error",
        500
    )

@app.get("/")
def home():
    return {
        "message": "URL Shortener API is running"
    }


@app.post("/api/urls")
def create_url():

    if not request.is_json:
        return error_response("Content-Type must be application/json",415)

    data = request.get_json()

    original_url = data.get("url")

    if not original_url:
        return error_response("url is required",400)

    if not is_valid_url(original_url):
        return error_response("Not a valid URL",400)

    # Check if URL already exists
    existing_url = URL.query.filter_by(
        original_url=original_url
    ).first()

    if existing_url:
        return {
            "id": existing_url.id,
            "original_url": existing_url.original_url,
            "short_code": existing_url.short_code,
            "click_counter":existing_url.click_counter
        }, 200

    # Generate new short code
    short_code = generate_short_code()

    while URL.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    new_url = URL(
        original_url=original_url,
        short_code=short_code
    )

    db.session.add(new_url)
    db.session.commit()

    return {
        "id": new_url.id,
        "original_url": new_url.original_url,
        "short_code": new_url.short_code,
        "click_counter":new_url.click_counter
    }, 201

@app.get("/ai/urls/<short_code>")
def get_url(short_code):
    url=URL.query.filter_by(short_code = short_code).first()
    if not url:
        return error_response("Short code not found",404)
    return{
        "id":url.id,
        "original_url":url.original_url,
        "short_code":url.short_code,
        "click_counter":url.click_counter
    },200

@app.get("/<short_code>")
def Shorten_url(short_code):
    url=URL.query.filter_by(short_code = short_code).first()
    if not url:
        return error_response("Short code not found",404)

    url.click_counter+=1
    db.session.commit()
    
    return redirect(url.original_url)

@app.delete("/api/urls/<short_code>")
def delete_code(short_code):
    url=URL.query.filter_by(short_code = short_code).first()
    if not url:
        return error_response("Short code not found",404)

    deleted_id = url.id
    db.session.delete(url)
    db.session.commit()
    return{
        "message":"Deleted succesfully",
        "id": deleted_id,
        "short_code": short_code
    }

@app.get("/api/urls")
def get_all_urls():
    page_value = request.args.get("page", 1)
    limit_value  = request.args.get("pagesize", 2)

    try:
        page = int(page_value)
        limit = int(limit_value)
    except ValueError:
        return error_response(
            "page and limit must be integers",
            400
        )

    if page < 1:
        return error_response("page must be >= 1", 400)

    if limit < 1 or limit > 100:
        return error_response(
            "limit must be between 1 and 100",
            400
        )

    offset = (page - 1) * limit

    urls = URL.query.offset(offset).limit(limit).all()

    total=URL.query.count()

    total_pages = ( total + limit - 1 ) // limit
    has_next = page < total_pages
    has_previous = page > 1
    return {
    "response":{
        "data":[
            {
             "id": url.id,
                "original_url": url.original_url,
                "short_code": url.short_code,
                "click_counter":url.click_counter
            }
            for url in urls
        ],
        "pagination":{
            "page":page,
            "total":total,
            "limit":limit,
            "total_pages":total_pages,
            "has_next_page":has_next,
            "has_previous_page":has_previous
        }
    }
    }

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )