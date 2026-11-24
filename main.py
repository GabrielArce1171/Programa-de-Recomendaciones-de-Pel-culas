import numpy as np

# ==========================================
# 1. DEFINICIÓN DE DATOS BASE
# ==========================================

generos = ["Acción", "Romance", "Comedia", "Ciencia Ficción", "Terror"]

# 5 películas base sobre las que se le preguntará al usuario
peliculas_base = [
    "Shrek",
    "Cómo perder a un hombre en 10 días",
    "Viernes 13",
    "Matrix",
    "Interstellar"
]

# 5 perfiles de usuarios ya existentes
usuarios = ["Ana", "Carlos", "Sofía", "Luis", "Diego"]

# Matriz de gustos por género (5 usuarios x 5 géneros), escala del 0 al 5
matriz_generos = np.array([
    [4, 2, 3, 5, 1],  # Ana: le gusta Ciencia Ficción y Acción
    [5, 1, 2, 4, 2],  # Carlos: muy fan de Acción y Ciencia Ficción
    [1, 5, 5, 1, 1],  # Sofía: le encantan Romance y Comedia
    [2, 4, 4, 2, 1],  # Luis: afinidad con Comedia y Romance
    [3, 1, 2, 2, 5]   # Diego: fanático del Terror y algo de Acción
], dtype=float)

# Matriz de calificaciones de las 5 películas base (5 usuarios x 5 películas), 0 = no vista
matriz_peliculas_base = np.array([
    [4, 2, 1, 5, 5],  # Ana
    [3, 1, 2, 5, 4],  # Carlos
    [5, 5, 4, 0, 1],  # Sofía
    [4, 4, 5, 1, 0],  # Luis
    [2, 1, 5, 4, 2]   # Diego
], dtype=float)

# Biblioteca de 15 películas nuevas para recomendar: (Título, Género principal)
catalogo_15_nuevas = [
    ("Mad Max: Furia en el camino", "Acción"),
    ("John Wick", "Acción"),
    ("Gladiador", "Acción"),
    ("Orgullo y prejuicio", "Romance"),
    ("Diario de una pasión", "Romance"),
    ("Antes del amanecer", "Romance"),
    ("Supercool", "Comedia"),
    ("¿Qué pasó ayer?", "Comedia"),
    ("Chicas pesadas", "Comedia"),
    ("Blade Runner 2049", "Ciencia Ficción"),
    ("Arrival (La llegada)", "Ciencia Ficción"),
    ("Duna", "Ciencia Ficción"),
    ("El Conjuro", "Terror"),
    ("Hereditary", "Terror"),
    ("Huye (Get Out)", "Terror")
]


# ==========================================
# 2. OPERACIONES DE ÁLGEBRA LINEAL
# ==========================================

def similitud_coseno(v1, v2):
    """Calcula la similitud coseno entre dos vectores usando producto punto y norma."""
    producto_punto = np.dot(v1, v2)
    norma_v1 = np.linalg.norm(v1)
    norma_v2 = np.linalg.norm(v2)

    if norma_v1 == 0 or norma_v2 == 0:
        return 0.0

    return float(producto_punto / (norma_v1 * norma_v2))


def encontrar_usuario_mas_afin(vec_gen_usuario, vec_pel_usuario):
    """Compara al nuevo usuario contra los 5 perfiles existentes."""
    mejor_similitud = -1.0
    mejor_idx = 0
    mejor_sim_gen = 0.0
    mejor_sim_pel = 0.0

    # Solo comparamos contra los primeros 5 usuarios preexistentes
    for i in range(5):
        sim_gen = similitud_coseno(vec_gen_usuario, matriz_generos[i])
        sim_pel = similitud_coseno(vec_pel_usuario, matriz_peliculas_base[i])

        # Combinación ponderada (50% géneros, 50% películas base)
        sim_total = 0.5 * sim_gen + 0.5 * sim_pel

        if sim_total > mejor_similitud:
            mejor_similitud = sim_total
            mejor_idx = i
            mejor_sim_gen = sim_gen
            mejor_sim_pel = sim_pel

    return mejor_idx, mejor_similitud, mejor_sim_gen, mejor_sim_pel


def recomendar_de_15_nuevas(vec_gen_usuario, idx_usuario_afin):
    """Selecciona películas del catálogo de 15 nuevas según géneros y usuario afín."""
    # Determinamos los géneros favoritos del usuario nuevo (calificación >= 4)
    generos_favoritos = [
        generos[j] for j in range(len(generos)) if vec_gen_usuario[j] >= 4
    ]

    # Si no marcó ninguno con 4 o 5, tomamos el género con mayor puntaje del usuario afín
    if not generos_favoritos:
        idx_gen_afin = int(np.argmax(matriz_generos[idx_usuario_afin]))
        generos_favoritos = [generos[idx_gen_afin]]

    recomendaciones = []
    for titulo, gen in catalogo_15_nuevas:
        if gen in generos_favoritos:
            recomendaciones.append((titulo, gen))

    # Garantía: siempre devolvemos al menos 3 recomendaciones del catálogo de 15
    if len(recomendaciones) < 3:
        for titulo, gen in catalogo_15_nuevas:
            if (titulo, gen) not in recomendaciones:
                recomendaciones.append((titulo, gen))
            if len(recomendaciones) >= 3:
                break

    return recomendaciones


def pedir_calificacion(mensaje):
    """Solicita y valida un número entero del 0 al 5."""
    while True:
        try:
            valor = int(input(mensaje))
            if 0 <= valor <= 5:
                return float(valor)
            print("   ⚠️ Ingresa un número entero entre 0 y 5.")
        except ValueError:
            print("   ⚠️ Entrada inválida. Escribe un número del 0 al 5.")


# ==========================================
# 3. INTERFAZ PRINCIPAL EN CONSOLA
# ==========================================

def main():
    global matriz_generos, matriz_peliculas_base

    print("============================================================")
    print("   SISTEMA DE RECOMENDACIÓN DE PELÍCULAS - ÁLGEBRA LINEAL  ")
    print("============================================================")

    nombre = input("\nIngresa tu nombre: ").strip()
    if not nombre:
        nombre = "Invitado"

    print(f"\n¡Hola, {nombre}! Califica del 0 al 5 qué tanto te gustan estos 5 GÉNEROS:")
    vec_gen = []
    for g in generos:
        val = pedir_calificacion(f"  - {g} (0-5): ")
        vec_gen.append(val)
    vec_gen_np = np.array(vec_gen)

    print(f"\nAhora dime tu opinión (del 0 al 5; usa 0 si no la has visto) sobre estas 5 PELÍCULAS:")
    vec_pel = []
    for p in peliculas_base:
        val = pedir_calificacion(f"  - {p} (0-5): ")
        vec_pel.append(val)
    vec_pel_np = np.array(vec_pel)

    # Actualizamos dinámicamente las matrices agregando al nuevo usuario
    usuarios.append(nombre)
    matriz_generos = np.vstack([matriz_generos, vec_gen_np])
    matriz_peliculas_base = np.vstack([matriz_peliculas_base, vec_pel_np])

    idx_afin, sim_total, sim_gen, sim_pel = encontrar_usuario_mas_afin(vec_gen_np, vec_pel_np)
    usuario_afin = usuarios[idx_afin]

    print("\n------------------------------------------------------------")
    print(f"RESULTADOS PARA: {nombre}")
    print("------------------------------------------------------------")


    recs = recomendar_de_15_nuevas(vec_gen_np, idx_afin)

    print(f"\n🎬 Películas recomendadas para ti:")
    for i, (titulo, gen) in enumerate(recs, start=1):
        print(f"  {i}. {titulo} [{gen}]")
    print("============================================================\n")


if __name__ == "__main__":
    main()