import numpy as np

# 1. Definimos las películas y 5 usuarios base en la base de datos
peliculas = ["Matrix", "Inception", "Interstellar", "Toy Story", "Shrek", "El Padrino"]
usuarios = ["Ana", "Carlos", "Sofía", "Luis", "Diego"]

# 2. Matriz de Calificaciones Base (5 usuarios x 6 películas)
matriz_calificaciones = np.array([
    [5, 5, 4, 0, 0, 1],  # Ana
    [4, 0, 5, 0, 0, 2],  # Carlos
    [0, 0, 0, 5, 4, 0],  # Sofía
    [1, 2, 0, 4, 5, 0],  # Luis
    [5, 4, 0, 0, 1, 4]   # Diego
])

# 3. Función para calcular la Similitud Coseno entre vectores
def similitud_coseno(v1, v2):
    producto_punto = np.dot(v1, v2)
    norma_v1 = np.linalg.norm(v1)
    norma_v2 = np.linalg.norm(v2)
    
    if norma_v1 == 0 or norma_v2 == 0:
        return 0.0
    
    return producto_punto / (norma_v1 * norma_v2)

# 4. Función de recomendación basada en vectores
def recomendar_peliculas(usuario_idx):
    usuario_actual = matriz_calificaciones[usuario_idx]
    mejor_similitud = -1
    usuario_similar_idx = -1
    
    # Comparamos tu vector con todos los demás usuarios de la matriz
    for i in range(len(matriz_calificaciones)):
        if i == usuario_idx:
            continue  # No te compares contigo mismo
        
        sim = similitud_coseno(usuario_actual, matriz_calificaciones[i])
        if sim > mejor_similitud:
            mejor_similitud = sim
            usuario_similar_idx = i
            
    print(f"\n--------------------------------------------------")
    print(f"📊 RESULTADOS DEL ANÁLISIS VECTORIAL")
    print(f"--------------------------------------------------")
    print(f"Tu perfil (vector en R^6): {usuario_actual}")
    print(f"Usuario con gustos más afines: {usuarios[usuario_similar_idx]} (Similitud Coseno: {mejor_similitud:.4f})")
    
    # Buscamos películas que le gustaron al usuario similar (>= 4) que tú no has visto (== 0)
    recomendaciones = []
    for p_idx in range(len(peliculas)):
        if matriz_calificaciones[usuario_similar_idx][p_idx] >= 4 and usuario_actual[p_idx] == 0:
            recomendaciones.append(peliculas[p_idx])
            
    # Garantía/Fallback: Si por alguna razón la lista está vacía, te recomendamos las mejores del usuario afín
    if not recomendaciones:
        for p_idx in range(len(peliculas)):
            if matriz_calificaciones[usuario_similar_idx][p_idx] >= 3:
                recomendaciones.append(peliculas[p_idx])
        # Si aún así estuviera vacío, tomamos las primeras dos
        if not recomendaciones:
            recomendaciones = [peliculas[0], peliculas[1]]
            
    return recomendaciones

# --- INTERFAZ INTERACTIVA EN LA TERMINAL ---
if __name__ == "__main__":
    print("==================================================")
    print("   SISTEMA DE RECOMENDACIÓN DE CINE (ÁLGEBRA)     ")
    print("==================================================")
    
    # Pedir nombre del usuario
    nombre_usuario = input("¿Cuál es tu nombre?: ").strip()
    if not nombre_usuario:
        nombre_usuario = "Usuario_Invitado"
        
    print(f"\n¡Hola, {nombre_usuario}! Para calcular tus recomendaciones,")
    print("califica las siguientes películas del 0 al 5.")
    print("(Usa 0 si no la has visto o no te llama la atención).\n")
    
    nuevo_vector = []
    for pelicula in peliculas:
        while True:
            try:
                calificacion = int(input(f"  -> ¿Qué calificación le das a '{pelicula}' (0-5)?: "))
                if 0 <= calificacion <= 5:
                    nuevo_vector.append(calificacion)
                    break
                else:
                    print("     ⚠️ Ingresa un número válido entre 0 y 5.")
            except ValueError:
                print("     ⚠️ Error: Debes ingresar un número entero.")
                
    # 5. Agregar el nuevo usuario y expandir la matriz usando NumPy (vstack)
    usuarios.append(nombre_usuario)
    matriz_calificaciones = np.vstack([matriz_calificaciones, np.array(nuevo_vector)])
    
    # Tu índice será el último elemento de la matriz
    tu_indice = len(usuarios) - 1
    
    # Generar y mostrar recomendaciones
    peliculas_recomendadas = recomendar_peliculas(tu_indice)
    
    print(f"\n🎬 Películas recomendadas especialmente para ti, {nombre_usuario}:")
    for idx, peli in enumerate(peliculas_recomendadas, 1):
        print(f"   {idx}. ⭐ {peli}")
    print("==================================================\n")