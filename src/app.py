import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Personas, Vehiculos, Planetas, Favoritos 

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/usuarios', methods=['GET']) 
def get_all_users():
    usuarios = User.query.all()
    all_usuarios = [
        {
            "id": user.id,
            "nombre": user.nombre,
            "correo": user.correo,
            "url": url_for('get_single_user', user_id=user.id, _external=True)
        } for user in usuarios
    ]
    return jsonify({"results": all_usuarios}), 200

@app.route('/usuario/<int:user_id>', methods=['GET']) 
def get_single_user(user_id): 
    usuario = User.query.get(user_id) 
    if usuario is None:
        raise APIException("Usuario no encontrado", status_code=404)
    return jsonify(usuario.serialize()), 200

@app.route('/usuario', methods=['POST'])
def create_user():
    body = request.get_json()
    if not body or not 'correo' in body or not 'contraseña' in body:
        raise APIException("Correo y contraseña son requeridos", status_code=400)

    existing_user = User.query.filter_by(correo=body['correo']).first() 
    if existing_user:
        raise APIException("El usuario con este correo ya existe", status_code=409)

    user = User(nombre=body.get('nombre', 'Nuevo Usuario'), correo=body['correo'], contraseña=body['contraseña'], is_active=True)
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "Usuario creado exitosamente", "usuario": user.serialize()}), 201

@app.route('/personas', methods=['GET'])
def get_all_people():
    people = Personas.query.all() 
    all_people = [
        {
            "id_unico": person.id, 
            "nombre": person.nombre, 
            "url": url_for('get_single_person', person_id=person.id, _external=True)
        } for person in people
    ]
    return jsonify({"results": all_people}), 200

@app.route('/personas/<int:person_id>', methods=['GET']) 
def get_single_person(person_id):
    person = Personas.query.get(person_id) 
    if person is None:
        raise APIException("Personaje no encontrado", status_code=404)

    person_data = {
        "resultado": {
            "propiedades": { 
                "nombre": person.nombre,       
                "altura": person.altura,       
                "peso": person.peso,           
                "genero": person.genero,       
                "id_unico": person.id          
            },
            "descripcion": "Un personaje de Star Wars", 
            "id_unico": person.id             
        }
    }
    return jsonify(person_data), 200

@app.route('/vehiculos', methods=['GET'])
def get_all_vehicles():
    vehicles = Vehiculos.query.all() 
    all_vehicles = [
        {
            "id_unico": vehicle.id,
            "nombre": vehicle.nombre, 
            "url": url_for('get_single_vehicle', vehicle_id=vehicle.id, _external=True)
        } for vehicle in vehicles
    ]
    return jsonify({"results": all_vehicles}), 200

@app.route('/vehiculos/<int:vehicle_id>', methods=['GET']) 
def get_single_vehicle(vehicle_id):
    vehicle = Vehiculos.query.get(vehicle_id) 
    if vehicle is None:
        raise APIException("Vehiculo no encontrado", status_code=404)

    vehicle_data = {
        "resultado": { 
            "propiedades": { 
                "modelo": vehicle.modelo,             
                "fabricante": vehicle.fabricante,     
                "costo_en_creditos": vehicle.costo_en_creditos, 
                "longitud": vehicle.longitud,         
                "tripulacion": vehicle.tripulacion,   
                "pasajeros": vehicle.pasajeros,       
                "nombre": vehicle.nombre,             
                "id_unico": vehicle.id                
            },
            "descripcion": "Un vehiculo de Star Wars", 
            "id_unico": vehicle.id                
        }
    }
    return jsonify(vehicle_data), 200

@app.route('/planetas', methods=['GET'])
def get_all_planets():
    planets = Planetas.query.all() 
    all_planets = [
        {
            "id_unico": planet.id, 
            "nombre": planet.nombre, 
            "url": url_for('get_single_planet', planet_id=planet.id, _external=True)
        } for planet in planets
    ]
    return jsonify({"results": all_planets}), 200

@app.route('/planetas/<int:planet_id>', methods=['GET']) 
def get_single_planet(planet_id):
    planet = Planetas.query.get(planet_id) 
    if planet is None:
        raise APIException("Planeta no encontrado", status_code=404)

    planet_data = {
        "resultado": { 
            "propiedades": { 
                "clima": planet.clima,                
                "terreno": planet.terreno,            
                "poblacion": planet.poblacion,        
                "diametro": planet.diametro,          
                "nombre": planet.nombre,              
                "id_unico": planet.id                 
            },
            "descripcion": "Un planeta de Star Wars", 
            "id_unico": planet.id                     
        }
    }
    return jsonify(planet_data), 200

@app.route('/usuario/<int:user_id>/favoritos', methods=['POST'])
def add_favorite(user_id):
    user = User.query.get(user_id)
    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)

    body = request.get_json()

    item_id = body.get('id_unico')
    item_type = body.get('item_type')

    if not item_id or not item_type:
        raise APIException("ID unico y Tipo de Item son requeridos", status_code=400)

    valid_types = ['personas', 'vehiculos', 'planetas']
    if item_type not in valid_types:
        raise APIException(f"Tipo de item invalido. Debe ser uno de: {', '.join(valid_types)}", status_code=400)

    item_exists = False
    if item_type == 'personas':
        item_exists = Personas.query.get(item_id) is not None
    elif item_type == 'vehiculos':
        item_exists = Vehiculos.query.get(item_id) is not None
    elif item_type == 'planetas':
        item_exists = Planetas.query.get(item_id) is not None

    if not item_exists:
        raise APIException(f"El {item_type.capitalize()} con ID unico {item_id} no fue encontrado", status_code=404)

    existing_favorite = Favoritos.query.filter_by(usuario_id=user_id, item_id=item_id, item_type=item_type).first()
    if existing_favorite:
        raise APIException("El item ya esta en favoritos", status_code=409)

    favorite = Favoritos(usuario_id=user_id, item_id=item_id, item_type=item_type)
    db.session.add(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito añadido exitosamente", "id_unico_agregado": item_id, "tipo_agregado": item_type}), 201

@app.route('/usuario/<int:user_id>/favoritos', methods=['GET']) 
def get_user_favorites(user_id):
    user = User.query.get(user_id) 
    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)

    favorites = Favoritos.query.filter_by(usuario_id=user_id).all() 
    serialized_favorites = []
    for fav in favorites:
        item_data = None

        if fav.item_type == 'personas':
            item = Personas.query.get(fav.item_id) 
            if item:
                item_data = {"id": item.id, "nombre": item.nombre, "tipo": "persona"} 
        elif fav.item_type == 'vehiculos':
            item = Vehiculos.query.get(fav.item_id) 
            if item:
                item_data = {"id": item.id, "nombre": item.nombre, "tipo": "vehiculo"} 
        elif fav.item_type == 'planetas':
            item = Planetas.query.get(fav.item_id) 
            if item:
                item_data = {"id": item.id, "nombre": item.nombre, "tipo": "planeta"} 

        if item_data:
            serialized_favorites.append(item_data)

    return jsonify(serialized_favorites), 200

@app.route('/usuario/<int:user_id>/favoritos/<string:item_type>/<int:item_id>', methods=['DELETE']) 
def delete_favorite(user_id, item_type, item_id):
    user = User.query.get(user_id) 
    if user is None:
        raise APIException("Usuario no encontrado", status_code=404)

    favorite = Favoritos.query.filter_by(usuario_id=user_id, item_id=item_id, item_type=item_type).first() 
    if favorite is None:
        raise APIException("Favorito no encontrado para este usuario", status_code=404)

    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"msg": "Favorito eliminado exitosamente"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

