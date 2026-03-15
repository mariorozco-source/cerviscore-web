from flask import Flask, render_template

app = Flask(__name__)

# Datos de ejemplo para la página (simulando una base de datos)
noticias = [
    {
        "titulo": "¡Arrancan las Olimpiadas Cervantinas!",
        "imagen": "https://images.unsplash.com/photo-1579952363873-27f3bade9f55?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "15 Mar 2026",
        "resumen": "La ceremonia de apertura fue un éxito total con la participación de todos los cursos."
    },
    {
        "titulo": "Gran victoria de 11B sobre 10A",
        "imagen": "https://images.unsplash.com/photo-1517466787929-bc90951d0974?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "14 Mar 2026",
        "resumen": "Un partido reñido que terminó 3-2 a favor de los seniors."
    },
    {
        "titulo": "El equipo de intercolegiados avanza a finales",
        "imagen": "https://images.unsplash.com/photo-1522778119026-d647f0565c6a?ixlib=rb-4.0.3&auto=format&fit=crop&w=800&q=80",
        "fecha": "12 Mar 2026",
        "resumen": "Nuestros representantes dejaron en alto el nombre del Liceo de Cervantes."
    }
]

posiciones = [
    {"equipo": "11 B", "pj": 5, "pg": 4, "pe": 1, "pp": 0, "pts": 13},
    {"equipo": "10 A", "pj": 5, "pg": 3, "pe": 2, "pp": 0, "pts": 11},
    {"equipo": "9 C", "pj": 5, "pg": 3, "pe": 0, "pp": 2, "pts": 9},
    {"equipo": "11 A", "pj": 5, "pg": 2, "pe": 1, "pp": 2, "pts": 7},
]

goleadores = [
    {"nombre": "Juan Pérez", "curso": "11B", "goles": 8},
    {"nombre": "Carlos M.", "curso": "10A", "goles": 6},
    {"nombre": "Andrés R.", "curso": "9C", "goles": 5},
]

@app.route('/')
def home():
    return render_template('index.html', noticias=noticias, posiciones=posiciones, goleadores=goleadores)

if __name__ == '__main__':
    app.run(debug=True)
