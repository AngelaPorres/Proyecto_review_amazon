import pymysql
from pymongo import MongoClient
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import configuracion

def conectar_mysql():
    return pymysql.connect(
        host=configuracion.MYSQL_HOST,
        user=configuracion.MYSQL_USER,
        password=configuracion.MYSQL_PASSWORD,
        database=configuracion.MYSQL_DATABASE
    )

def conectar_mongo():
    client = MongoClient(configuracion.MONGO_URI)
    db = client[configuracion.MONGO_DATABASE]
    return db[configuracion.MONGO_COLLECTION]


def evolucion_reviews():
    tipo = input("Introduce la categoría que deseas mostrar o 'todo': ")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if tipo != "todo":
        cursor.execute("""SELECT COUNT(*) 
                       FROM productos 
                       WHERE categoria=%s
                       """, (tipo,))
        if cursor.fetchone()[0] == 0:
            print(f"ERROR. La categoría {tipo} no existe")
            return
        
        query = """
        SELECT YEAR(reviewTime), COUNT(*)
        FROM reviews r
        JOIN productos p ON r.asin = p.asin
        WHERE categoria = %s
        GROUP BY YEAR(reviewTime)
        ORDER BY YEAR(reviewTime)
        """
        cursor.execute(query, (tipo,))
    
    else:
        cursor.execute("""
        SELECT YEAR(reviewTime), COUNT(*)
        FROM reviews
        GROUP BY YEAR(reviewTime)
        ORDER BY YEAR(reviewTime)
        """)

    datos = cursor.fetchall()

    años = []
    conteos = []

    for fila in datos:
        años.append(fila[0])
        conteos.append(fila[1])

    plt.bar(años, conteos)
    plt.title(f"Reviews por año de {tipo}")
    plt.xlabel("Años")    
    plt.ylabel("Número de reviews")
    plt.xticks(años[::2])  # Para que sean enteros
    plt.show()

def popularidad():
    tipo = input("Introduce la categoría que deseas mostrar o 'todo': ")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if tipo != "todo":
        cursor.execute("""SELECT COUNT(*) 
                       FROM productos 
                       WHERE categoria=%s
                       """, (tipo,))
        if cursor.fetchone()[0] == 0:
            print(f"ERROR. La categoría {tipo} no existe")
            return
        
        query = """
        SELECT p.asin, COUNT(*)
        FROM reviews r
        JOIN productos p ON r.asin = p.asin
        WHERE categoria = %s
        GROUP BY p.asin
        ORDER BY COUNT(*) DESC
        """
        cursor.execute(query, (tipo,))
    else:
        cursor.execute("""
        SELECT asin, COUNT(*)
        FROM reviews
        GROUP BY asin
        ORDER BY COUNT(*) DESC
        """)

    datos = cursor.fetchall()

    valores = []
    for fila in datos:
        valores.append(fila[1])

    plt.plot(valores)
    plt.title(f"Evolución de popularidad de {tipo}")
    plt.xlabel("Artículos")    
    plt.ylabel("Número de reviews")
    plt.show()

def histograma_notas():
    print("1. Categoría")
    print("2. Producto (asin)")
    print("3. Todo")

    op = input("Elige qué datos quieres representar: ")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    if op == "1":
        tipo = input("Introduce la categoría especifica: ")

        cursor.execute("""SELECT COUNT(*) 
                       FROM productos 
                       WHERE categoria=%s
                       """, (tipo,))
        if cursor.fetchone()[0] == 0:
            print(f"ERROR. La categoría {tipo} no existe")
            return
        
        query = """
        SELECT overall
        FROM reviews r
        JOIN productos p ON r.asin = p.asin
        WHERE categoria = %s
        """
        cursor.execute(query, (tipo,))

    elif op == "2":
        asin = input("Introduce el producto (asin) especifico: ")

        cursor.execute("""SELECT COUNT(*) 
                       FROM productos 
                       WHERE asin=%s
                       """, (asin,))
        if cursor.fetchone()[0] == 0:
            print(f"ERROR. El producto {asin} no existe")
            return

        cursor.execute("""SELECT overall 
                       FROM reviews 
                       WHERE asin=%s
                       """, (asin,))

    elif op == "3":
        cursor.execute("SELECT overall FROM reviews")

    else:
        print("Opción inválida")
        return

    datos = cursor.fetchall()

    notas = []
    for fila in datos:
        notas.append(fila[0])

    plt.hist(notas, bins=5)
    plt.title("Reviews por nota")
    plt.xlabel("Nota")    
    plt.ylabel("Número de reviews")
    plt.show()

def evolucion_tiempo():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT categoria, unixReviewTime
    FROM reviews r
    JOIN productos p ON r.asin = p.asin
    ORDER BY categoria, unixReviewTime
    """)

    datos = cursor.fetchall()

    categorias = {}
    
    for cat, tiempo in datos:
        if cat not in categorias:
            categorias[cat] = {"tiempos": [], "acum": []}

        lista_tiempos = categorias[cat]["tiempos"]
        lista_acum = categorias[cat]["acum"]

        if len(lista_acum) == 0:
            contador = 1
        else:
            contador = lista_acum[-1] + 1

        lista_tiempos.append(tiempo)
        lista_acum.append(contador)

    for cat in categorias:
        plt.plot(categorias[cat]["tiempos"], categorias[cat]["acum"], label=cat)

    plt.title("Evolución de las reviews a lo largo del tiempo de todos los productos")
    plt.xlabel("Tiempo")    
    plt.ylabel("Número de reviews hasta ese momento")
    plt.legend()
    plt.show()

def reviews_por_usuario():
    conn = conectar_mysql()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT reviewerID, COUNT(*)
    FROM reviews
    GROUP BY reviewerID
    """)

    datos = cursor.fetchall()

    valores = []
    for fila in datos:
        valores.append(fila[1])

    max_val = max(valores)
    bins = range(1, max_val + 2)

    plt.hist(valores, bins=bins)
    plt.title("Reviews por usuario")
    plt.xlabel("Número de reviews")    
    plt.ylabel("Número de usuarios")
    plt.show()

def nube_palabras():
    tipo = input("Introduce la categoría que deseas mostrar: ")

    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("SELECT COUNT(*) FROM productos WHERE categoria=%s", (tipo,))
    if cursor.fetchone()[0] == 0:
        print(f"ERROR. La categoría {tipo} no existe")
        return

    # Obtenemos los ids de las reviews
    cursor.execute("""
    SELECT id_review
    FROM reviews r
    JOIN productos p ON r.asin = p.asin
    WHERE categoria = %s
    """, (tipo,))

    ids = [fila[0] for fila in cursor.fetchall()]

    mongo = conectar_mongo()

    # Traemos todos los docs de mongo de golpe para agilizar el proceso
    cursor_mongo = mongo.find({"review_id": {"$in": ids}}, {"summary": 1, "_id": 0})

    texto = ""
    for doc in cursor_mongo:
        palabras = doc["summary"].split()
        texto += " ".join([p for p in palabras if len(p) > 3]) + " "

    wc = WordCloud(width=800, height=400, background_color="white").generate(texto)

    plt.figure(figsize=(15, 7))
    plt.imshow(wc, interpolation="bilinear")
    plt.axis("off")
    plt.show()
    
# Gráfica extra: nota media por categoría
def grafica_extra():
    conexion = conectar_mysql()
    cursor = conexion.cursor()

    cursor.execute("""
    SELECT categoria, AVG(overall)
    FROM reviews r
    INNER JOIN productos p ON r.asin = p.asin
    GROUP BY categoria
    """)

    datos = cursor.fetchall()

    categorias = []
    medias = []

    for fila in datos:
        categorias.append(fila[0])
        medias.append(fila[1])

    plt.bar(categorias, medias)
    plt.title("Nota media por categoria")
    plt.xlabel("Categoría")
    plt.ylabel("Nota media")
    plt.show()

if __name__ == "__main__":
    while True:
        print("\n*** Menú de gráficas ***")
        print("1. Evolución reviews por año")
        print("2. Popularidad artículos")
        print("3. Histograma notas")
        print("4. Evolución temporal")
        print("5. Reviews por usuario")
        print("6. Nube de palabras")
        print("7. Gráfica extra: Nota media por categoría")
        print("0. Salir")

        opcion = input("\nElige una opción a representar: ")

        if opcion == "1":
            evolucion_reviews()
        elif opcion == "2":
            popularidad()
        elif opcion == "3":
            histograma_notas()
        elif opcion == "4":
            evolucion_tiempo()
        elif opcion == "5":
            reviews_por_usuario()
        elif opcion == "6":
            nube_palabras()
        elif opcion == "7":
            grafica_extra()
        elif opcion == "0":
            break