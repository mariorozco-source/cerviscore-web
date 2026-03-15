from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Datos de los 4 Torneos (Datasets Ficticios para Testing)
DATASETS = {
    "primaria_baja": {
        "id": "primaria_baja",
        "nombre": "Olimpiadas 1º, 2º y 3º",
        "descripcion": "Categoría Infantil - Grados 1ro, 2do y 3ro",
        "posiciones": [
            {"equipo": "3 A", "pj": 8, "pg": 7, "pe": 1, "pp": 0, "pts": 22},
            {"equipo": "3 B", "pj": 8, "pg": 6, "pe": 2, "pp": 0, "pts": 20},
            {"equipo": "2 C", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "pts": 16},
            {"equipo": "2 A", "pj": 8, "pg": 4, "pe": 2, "pp": 2, "pts": 14},
            {"equipo": "3 C", "pj": 8, "pg": 3, "pe": 3, "pp": 2, "pts": 12},
            {"equipo": "1 B", "pj": 8, "pg": 3, "pe": 1, "pp": 4, "pts": 10},
            {"equipo": "2 B", "pj": 8, "pg": 2, "pe": 2, "pp": 4, "pts": 8},
            {"equipo": "1 A", "pj": 8, "pg": 1, "pe": 1, "pp": 6, "pts": 4},
            {"equipo": "1 C", "pj": 8, "pg": 0, "pe": 1, "pp": 7, "pts": 1}
        ],
        "goleadores": [
            {"nombre": "Thiago Silva", "curso": "3A", "goles": 12},
            {"nombre": "Mateo R.", "curso": "2C", "goles": 9},
            {"nombre": "Lucas P.", "curso": "3B", "goles": 7}
        ],
        "asistidores": [
            {"nombre": "Samuel D.", "curso": "3A", "asistencias": 8},
            {"nombre": "Daniel T.", "curso": "3B", "asistencias": 6},
            {"nombre": "Felipe M.", "curso": "2A", "asistencias": 5}
        ],
        "partidos": [
            {"local": "3 A", "visitante": "2 C", "marcador": "3 - 1", "fase": "Final"},
            {"local": "3 B", "visitante": "2 C", "marcador": "1 - 2", "fase": "Semifinal"},
            {"local": "3 A", "visitante": "2 A", "marcador": "4 - 0", "fase": "Semifinal"}
        ]
    },
    "primaria_alta": {
        "id": "primaria_alta",
        "nombre": "Olimpiadas 4º y 5º",
        "descripcion": "Categoría Pre-Juvenil - Grados 4to y 5to",
        "posiciones": [
            {"equipo": "5 B", "pj": 5, "pg": 5, "pe": 0, "pp": 0, "pts": 15},
            {"equipo": "5 A", "pj": 5, "pg": 4, "pe": 0, "pp": 1, "pts": 12},
            {"equipo": "4 C", "pj": 5, "pg": 3, "pe": 0, "pp": 2, "pts": 9},
            {"equipo": "4 A", "pj": 5, "pg": 2, "pe": 0, "pp": 3, "pts": 6},
            {"equipo": "5 C", "pj": 5, "pg": 1, "pe": 0, "pp": 4, "pts": 3},
            {"equipo": "4 B", "pj": 5, "pg": 0, "pe": 0, "pp": 5, "pts": 0}
        ],
        "goleadores": [
            {"nombre": "Santiago M.", "curso": "5B", "goles": 15},
            {"nombre": "Juan Jose", "curso": "5A", "goles": 10},
            {"nombre": "David L.", "curso": "4C", "goles": 8}
        ],
        "asistidores": [
            {"nombre": "Alejandro V.", "curso": "5B", "asistencias": 10},
            {"nombre": "Tomas G.", "curso": "5A", "asistencias": 7},
            {"nombre": "Nicolas B.", "curso": "4A", "asistencias": 4}
        ],
        "partidos": [
            {"local": "5 B", "visitante": "5 A", "marcador": "2 - 1", "fase": "Final"},
            {"local": "5 B", "visitante": "4 C", "marcador": "5 - 0", "fase": "Semifinal"},
            {"local": "5 A", "visitante": "4 A", "marcador": "3 - 2", "fase": "Semifinal"}
        ]
    },
    "bachillerato_bajo": {
        "id": "bachillerato_bajo",
        "nombre": "Olimpiadas 6º, 7º y 8º",
        "descripcion": "Categoría Juvenil - Grados 6to, 7mo y 8vo",
        "posiciones": [
            {"equipo": "8 C", "pj": 8, "pg": 6, "pe": 2, "pp": 0, "pts": 20},
            {"equipo": "7 A", "pj": 8, "pg": 6, "pe": 1, "pp": 1, "pts": 19},
            {"equipo": "8 A", "pj": 8, "pg": 5, "pe": 1, "pp": 2, "pts": 16},
            {"equipo": "6 B", "pj": 8, "pg": 4, "pe": 3, "pp": 1, "pts": 15},
            {"equipo": "8 B", "pj": 8, "pg": 4, "pe": 2, "pp": 2, "pts": 14},
            {"equipo": "7 C", "pj": 8, "pg": 3, "pe": 1, "pp": 4, "pts": 10},
            {"equipo": "7 B", "pj": 8, "pg": 2, "pe": 1, "pp": 5, "pts": 7},
            {"equipo": "6 A", "pj": 8, "pg": 1, "pe": 1, "pp": 6, "pts": 4},
            {"equipo": "6 C", "pj": 8, "pg": 0, "pe": 0, "pp": 8, "pts": 0}
        ],
        "goleadores": [
            {"nombre": "Matias R.", "curso": "8C", "goles": 14},
            {"nombre": "Simon P.", "curso": "7A", "goles": 11},
            {"nombre": "Julian D.", "curso": "6B", "goles": 10}
        ],
        "asistidores": [
            {"nombre": "Felipe S.", "curso": "8C", "asistencias": 9},
            {"nombre": "Andres M.", "curso": "8A", "asistencias": 7},
            {"nombre": "Camilo T.", "curso": "7A", "asistencias": 6}
        ],
        "partidos": [
            {"local": "8 C", "visitante": "7 A", "marcador": "1 - 1", "fase": "Final (4-3 p)"},
            {"local": "8 C", "visitante": "8 A", "marcador": "2 - 0", "fase": "Semifinal"},
            {"local": "7 A", "visitante": "6 B", "marcador": "3 - 1", "fase": "Semifinal"}
        ]
    },
    "bachillerato_alto": {
        "id": "bachillerato_alto",
        "nombre": "Olimpiadas 9º, 10º y 11º",
        "descripcion": "Categoría Mayores - Grados 9no, 10mo y 11vo",
        "posiciones": [
            {"equipo": "11 B", "pj": 8, "pg": 7, "pe": 1, "pp": 0, "pts": 22},
            {"equipo": "10 A", "pj": 8, "pg": 6, "pe": 1, "pp": 1, "pts": 19},
            {"equipo": "11 A", "pj": 8, "pg": 5, "pe": 2, "pp": 1, "pts": 17},
            {"equipo": "9 C", "pj": 8, "pg": 4, "pe": 2, "pp": 2, "pts": 14},
            {"equipo": "10 C", "pj": 8, "pg": 4, "pe": 1, "pp": 3, "pts": 13},
            {"equipo": "11 C", "pj": 8, "pg": 3, "pe": 1, "pp": 4, "pts": 10},
            {"equipo": "9 A", "pj": 8, "pg": 2, "pe": 0, "pp": 6, "pts": 6},
            {"equipo": "10 B", "pj": 8, "pg": 1, "pe": 0, "pp": 7, "pts": 3},
            {"equipo": "9 B", "pj": 8, "pg": 0, "pe": 0, "pp": 8, "pts": 0}
        ],
        "goleadores": [
            {"nombre": "Sebastian 'El Tanque'", "curso": "11B", "goles": 18},
            {"nombre": "Daniel 'La Pulga'", "curso": "10A", "goles": 14},
            {"nombre": "Nicolas R.", "curso": "9C", "goles": 9}
        ],
        "asistidores": [
            {"nombre": "Juan Diego", "curso": "11B", "asistencias": 15},
            {"nombre": "Carlos F.", "curso": "11A", "asistencias": 11},
            {"nombre": "Samuel L.", "curso": "10A", "asistencias": 8}
        ],
        "partidos": [
            {"local": "11 B", "visitante": "10 A", "marcador": "3 - 2", "fase": "Final"},
            {"local": "11 B", "visitante": "9 C", "marcador": "4 - 1", "fase": "Semifinal"},
            {"local": "10 A", "visitante": "11 A", "marcador": "2 - 1", "fase": "Semifinal"}
        ]
    }
}

# Noticias Globales (Genéricas para la home)
noticias = [
    {
        "titulo": "¡Finalizan las Fases de Grupos!",
        "imagen": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "15 Mar 2026",
        "resumen": "Se definen los clasificados a cuartos de final en todas las categorías."
    },
    {
        "titulo": "11B Rompe Récord de Goles",
        "imagen": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "14 Mar 2026",
        "resumen": "La categoría mayores vivió una jornada histórica con la goleada de los seniors."
    },
    {
        "titulo": "Gran Nivel en Primaria Baja",
        "imagen": "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "12 Mar 2026",
        "resumen": "Los más pequeños demuestran que tienen, un gran futuro en el futbol del colegio."
    }
]

@app.route('/')
def home():
    # Por defecto mostramos el torneo de Bachillerato Alto como principal
    torneo_default = DATASETS["bachillerato_alto"]
    return render_template('index.html', noticias=noticias, torneo=torneo_default, torneos_disponibles=DATASETS)

@app.route('/torneo/<torneo_id>')
def torneo(torneo_id):
    torneo_seleccionado = DATASETS.get(torneo_id)
    if not torneo_seleccionado:
        return "Torneo no encontrado", 404
    return render_template('index.html', noticias=noticias, torneo=torneo_seleccionado, torneos_disponibles=DATASETS)

@app.route('/api/standings/<category_id>')
def get_standings(category_id):
    dataset = DATASETS.get(category_id)
    if not dataset:
        return jsonify({"error": "Category not found"}), 404
    return jsonify(dataset)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    pregunta = data.get('pregunta', '').lower()
    
    # Inteligencia muy básica para buscar en todos los datasets
    respuesta = "No encontré esa información en mis registros. Intenta ser más específico (ej: 'goleador de primaria')."
    
    # Intentar determinar de qué torneo está hablando el usuario
    dataset_activo = None
    
    # Palabras clave para identificar el torneo
    if "primaria" in pregunta or "pequeños" in pregunta:
        if "alta" in pregunta or "4" in pregunta or "5" in pregunta:
            dataset_activo = DATASETS["primaria_alta"]
        else:
            dataset_activo = DATASETS["primaria_baja"]
    elif "bachillerato" in pregunta or "grandes" in pregunta:
        if "baja" in pregunta or "6" in pregunta or "7" in pregunta or "8" in pregunta:
            dataset_activo = DATASETS["bachillerato_bajo"]
        else:
            dataset_activo = DATASETS["bachillerato_alto"]
    
    # Si no se menciona torneo, buscamos si menciona algún curso específico
    if not dataset_activo:
        for key, torneo in DATASETS.items():
            # Buscar en los equipos de la tabla de posiciones si alguno coincide con la pregunta
            for equipo in torneo['posiciones']:
                if equipo['equipo'].lower() in pregunta:
                    dataset_activo = torneo
                    break
            if dataset_activo:
                break

    # Lógica de respuesta
    if "goleador" in pregunta or "goles" in pregunta:
        if dataset_activo:
             g = dataset_activo['goleadores'][0]
             respuesta = f"En {dataset_activo['nombre']}, el goleador es {g['nombre']} del {g['curso']} con {g['goles']} goles."
        else:
             # Respuesta por defecto (Mayores)
             g = DATASETS["bachillerato_alto"]['goleadores'][0]
             respuesta = f"En Mayores (11º), el goleador es {g['nombre']} ({g['curso']}) con {g['goles']} goles."

    elif "asistidor" in pregunta or "asistencias" in pregunta:
        if dataset_activo:
             a = dataset_activo['asistidores'][0]
             respuesta = f"El máximo asistidor en {dataset_activo['nombre']} es {a['nombre']} ({a['curso']}) con {a['asistencias']} asistencias."
        else:
             a = DATASETS["bachillerato_alto"]['asistidores'][0]
             respuesta = f"El líder en asistencias de Mayores es {a['nombre']} ({a['curso']}) con {a['asistencias']} pases gol."

    elif "lider" in pregunta or "primero" in pregunta or "punta" in pregunta:
        if dataset_activo:
             p = dataset_activo['posiciones'][0]
             respuesta = f"El líder en {dataset_activo['nombre']} es {p['equipo']} con {p['pts']} puntos."
        else:
             p = DATASETS["bachillerato_alto"]['posiciones'][0]
             respuesta = f"El líder de la categoría principal (11º) es {p['equipo']} con {p['pts']} puntos."

    elif "hola" in pregunta:
        respuesta = "¡Hola! Soy CERVISCORE AI. Pregúntame sobre cualquier categoría (ej: '¿Quién es el goleador de primaria?')."

    return jsonify({"respuesta": respuesta})

if __name__ == '__main__':
    app.run(debug=True)
