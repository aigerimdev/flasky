from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from app.models.cat import Cat
# from app.models.cats import cats


cats_bp = Blueprint("cats_bp", __name__, url_prefix = "/cats")

@cats_bp.post("")
def create_cat():
    request_body = request.get_json()
    name = request_body['name']
    color = request_body['color']
    personality = request_body['personality']
    
    new_cat = Cat(name=name, color=color, personality=personality)
    #adds to database
    db.session.add(new_cat)
    db.session.commit()
    
    response = {
        'id': new_cat.id,
        'name': new_cat.name,
        'color': new_cat.color,
        'personality': new_cat.personality
    }
    return response, 201

@cats_bp.get("")
def get_all_cats():
    query = db.select(Cat).order_by(Cat.id)
    cats = db.session.scalars(query)
    
    cats_response = []
    for cat in cats:
        cats_response.append(
            {
            'id': cat.id,
            'name': cat.name,
            'color': cat.color,
            'personality': cat.personality
            }
        )
    return cats_response

# get one cat

@cats_bp.get("/<id>")
def get_one_cat(id):
    cat = validate_cat(id)
    return {
        "id": cat.id,
        "name": cat.name,
        "color": cat.color,
        "personality": cat.personality
    }

@cats_bp.put("/<id>")
def update_cat(id):
    cat = validate_cat(id)
    request_body = request.get_json()
    
    cat.name = request_body['name']
    cat.color = request_body['color']
    cat.personality = request_body['personality']
    
    db.session.commit()
    return Response(status=204, mimetype="application/json")

# @cats_bp.get("")
# def get_all_cats():
#     cats_response = []
#     for cat in cats:
#         cats_response.append(dict(
#             id = cat.id,
#             name = cat.name,
#             color = cat.color,
#             personality = cat.personality
#         ))
#     return cats_response

# @cats_bp.get("/<id>")
# def get_one_cat(id):
#     cat = validate_cat(id)
#     cat_dict = dict(
#         id = cat.id,
#         name = cat.name,
#         color = cat.color,
#         personality = cat.personality
#             )
#     return cat_dict   
    
def validate_cat(id):
    try:
        id = int(id)
    except ValueError:
        invalid_response = {"message": f"Cat id ({id}) is invalid"}
        abort(make_response(invalid_response, 400))
        
    query = db.select(Cat).where(Cat.id == id)
    cat = db.session.scalars(query)
    
    if not cat:
        not_found = {"message": f"Cat id ({id}) is not found"}
        abort(make_response(not_found, 404))
    return cat
        
        
#     for cat in cats:
#         if  cat.id == id:
#             return cat
        
# not_found = {"message": f"Cat id ({id}) is not found"}
# abort(make_response(not_found, 404))