# Análisis de Reviews de Amazon con Bases de Datos Híbridas

Proyecto académico de Bases de Datos centrado en el almacenamiento, procesamiento y análisis de reseñas de 
Amazon combinando herramientas como MySQL, MongoDB y Neo4j.

El proyecto trabaja con 474.344 reseñas pertenecientes a cuatro categorías de productos y 
utiliza diferentes modelos de bases de datos en función de la información almacenada.

## Descripción

El objetivo del proyecto es diseñar un sistema capaz de gestionar y analizar un conjunto de datos de gran tamaño combinando tres tecnologías de bases de datos:

- **MySQL** para almacenar información estructurada de usuarios, productos y valoraciones.
- **MongoDB** para gestionar el contenido textual de las reseñas.
- **Neo4j** para representar y analizar relaciones de similitud entre usuarios.

## Funcionalidades

### Diseño y Carga de Datos
- Arquitectura : datos estructurados en MySQL, textos en MongoDB, relaciones en Neo4j
- Carga eficiente de JSONs sin cargar todo en memoria
- Normalización de fechas a formato DATE
- Gestión de usuarios duplicados entre categorías

### Visualización Interactiva (8 gráficos)
- **Evolución temporal:** reviews por año (histograma)
- **Popularidad de productos:** ranking por número de reviews (curva)
- **Distribución de puntuaciones:** histograma por nota (1-5 estrellas)
- **Tendencia acumulada:** reviews totales a lo largo del tiempo
- **Actividad de usuarios:** histograma de reviews por usuario
- **Análisis de texto:** nube de palabras por categoría
- **Grafos de relaciones:** matriz de similaridad entre usuarios (Neo4j)
- **Visualización personalizada:** gráfica adicional a elegir

### Análisis con Grafos (Neo4j)
- Construcción de grafo de similaridad de usuarios
- Cálculo de coeficiente de Pearson entre perfiles
- Identificación de comunidades de usuarios similares

## 🛠️ Estructura del Proyecto

```
proyecto/
├── configuracion.py          # Credenciales y rutas de datos
├── load_data.py              # Carga inicial de datos (MySQL + MongoDB)
├── inserta_dataset.py        # Inserción de nuevas categorías
├── neo4Proyecto.py           # Procesamiento y grafos (Neo4j)
├── apartado_cinco.py         # Análisis avanzado
├── menu_visualizacion.py     # Interfaz interactiva con plots                     
└── README.md

```

## Instalación y Uso

### 1. Instalar dependencias
```bash
pip install pymysql pymongo neo4j matplotlib seaborn wordcloud numpy pandas
```

### 2. Configurar credenciales
Edita `configuracion.py`:
```python
MYSQL_HOST = "localhost"
MYSQL_USER = "tu_usuario"
MYSQL_PASSWORD = "tu_contraseña"
MYSQL_DATABASE = "amazon_reviews"

MONGO_URI = "mongodb://localhost:27017"
```

### 3. Cargar los datos (primera vez)
```bash
python load_data.py
python neo4Proyecto.py
```

### 4. Ejecutar la aplicación
```bash
python menu_visualizacion.py
```

Se abrirá un menú interactivo donde podrás elegir qué visualización ver.

##  Detalles Técnicos

### Arquitectura de Bases de Datos

| Base de Datos | Datos Almacenados | Razón |
|---|---|---|
| **MySQL** | Usuarios, productos, notas, metadatos | Datos estructurados, búsquedas rápidas |
| **MongoDB** | Texto completo (reviewText, summary) | Almacenamiento flexible, análisis de texto |
| **Neo4j** | Similaridad usuario-usuario | Análisis de grafos y relaciones complejas |

### Métricas Implementadas
- **Similitud de usuarios:** Coeficiente de Pearson entre patrones de valoración
- **Popularidad de productos:** Número de reviews normalizados
- **Tendencias temporales:** Análisis de series temporales de reviews

##  Autor

**Ángela Porres Cobb**  
Proyecto Final de Bases de Datos - 2º B IMAT (2026)
