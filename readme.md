# Detección de Plagio de Documentos

Nahomi Bouza Rodríguez C412  
Yisell Martínez Noa C412

## Descripción del problema

El plagio es un problema común en el ámbito académico, profesional y creativo, que implica la copia no autorizada o la presentación de trabajo ajeno como propio. Con el crecimiento exponencial de la información disponible en línea y la facilidad para acceder a ella, la detección y prevención del plagio se ha vuelto más crucial que nunca. En este contexto, se plantea el desafío de desarrollar un sistema capaz de determinar el porcentaje de similitud entre dos documentos, con el fin de detectar posibles casos de plagio.

### Consideraciones

**Complejidad del Texto:** Los documentos pueden contener una variedad de estructuras gramaticales, vocabulario específico y estilos de escritura diferentes, lo que aumenta la complejidad de la detección de similitudes entre ellos.

**Manipulación de Texto:** Los autores pueden intentar evadir la detección de plagio mediante la manipulación del texto original, como el cambio de palabras, la reorganización de párrafos o la traducción a otro idioma. Esto agrega un nivel adicional de complejidad a la tarea de detección.

**Precisión y Fiabilidad:** Es fundamental que el sistema sea altamente preciso en la detección de similitudes entre documentos para evitar falsos positivos o negativos, asegurando así la confianza en los resultados obtenidos.

### Metodología utilizada

1. **Expresiones Regulares para la Detección de Citas**

    Se utilizan expresiones regulares para identificar patrones específicos que denoten citas dentro de los documentos. Estos patrones pueden incluir el uso de comillas, junto con referencias bibliográficas entre paréntesis o entre corchetes, y al final de oraciones. La detección de citas ayuda a distinguir el contenido original del citado, lo que contribuye a una mejor evaluación de la originalidad del documento.

2. **Preprocesamiento de los documentos utilizando Spacy**

    Se emplea la biblioteca Spacy para llevar a cabo la tokenización de los documentos. La tokenización implica dividir el texto en unidades más pequeñas, como palabras o símbolos, lo que facilita el procesamiento posterior del texto.

    Spacy proporciona capacidades avanzadas de tokenización y análisis lingüístico que son útiles para esta tarea.

    El algoritmo se puede resumir de la siguiente manera $^{[1]}$

    1. Iterar sobre subcadenas separadas por espacios.
    2. Comprobar si existe un caso especial definido explícitamente para esta subcadena, si existe, se usa.
    3. Buscar una coincidencia simbólica. Si existe, detener el procesamiento y conservar este token.
    4. Comprobar si existe un caso especial definido explícitamente para esta subcadena. Si existe, se usa.
    5. De lo contrario, intentar consumir un prefijo. Si consumimos un prefijo, volvemos al punto 3, para que la coincidencia del token y los casos especiales siempre tengan prioridad.
    6. Si no se consume un prefijo, se intenta consumir un sufijo y luego regresa al n.° 3.
    7. Si no podemos consumir un prefijo o un sufijo,  se busca una URL coincidente.
    8. Si no hay ninguna coincidencia de URL, se busca un caso especial.
    9. Buscar "infijos", como guiones, etc., y dividir la subcadena en tokens en todos los infijos.
    10. Una vez que se pueda consumir más cadena, se maneja como un solo token.
    11. Realizar una última pasada por el texto para comprobar si hay casos especiales que incluyan espacios o que se hayan omitido debido al procesamiento incremental de afijos.

    Luego de tokenizado el documento se eliminan tokens no relevantes como números, símbolos y stopwords.

3. **Vectorización con el Modelo Word2Vec**

    Word2vec es una técnica de procesamiento del lenguaje natural (PNL) para representar una palabra como un vector de números de alta dimensión que captura las relaciones entre palabras. En particular, las palabras que aparecen en contextos similares se asignan a vectores que están cerca, medido por la similitud del coseno. Esto indica el nivel de similitud semántica entre las palabras. Estas representaciones se estiman modelando texto en un corpus grande. Una vez entrenado, dicho modelo puede detectar palabras sinónimas o sugerir palabras adicionales para una oración parcial. $^{[2]}$

    Tanto CBOW como skip-gram son métodos para aprender un vector por palabra que aparece en el corpus. La idea de skip-gram es que el vector de una palabra debe estar cerca del vector de cada uno de sus vecinos. La idea de CBOW es que la suma vectorial de los vecinos de una palabra debe estar cerca del vector de la palabra.

    Si bien el código C original publicado por Google hace un trabajo impresionante, la implementación de Gensims es un caso en el que una implementación de código abierto es más eficiente que la original. $^{[3]}$

    Obtendremos el modelo Word2Vec entrenado en parte del conjunto de datos de Google News, que abarca aproximadamente 3 millones de palabras y frases. Un modelo de este tipo puede tardar horas en entrenarse, pero cargarlo con Gensim lleva unos minutos.

4. **División en N-gramas de $n=3$**

    Los documentos se dividen en n-gramas de longitud 3, lo que significa que se consideran secuencias de tres palabras consecutivas. Este enfoque permite capturar tanto la información local como la global dentro del texto, ya que proporciona un equilibrio entre la granularidad y la representación del contenido.

5. **Cálculo del Vector del N-grama**

    Para determinar el vector del n-grama, se calcula la media de los vectores de las tres palabras que lo componen. Este enfoque de representación promedio permite capturar la información semántica del n-grama en su conjunto. Al calcular la media de los vectores de palabras, se obtiene una representación vectorial del n-grama que conserva información relevante sobre su significado y contexto.

### Implementación

Para ejecutar el proyecto, se debe abrir una consola en la raíz del proyecto y ejecutar el siguiente comando:

``` shell
    python main.py {suspicious_path} {reference_path} {similarity_threshold}
```

Donde suspicious_path es el path al archivo en el que queremos detectar si se realizó algún plagio, reference_path el path al original y similarity_threshold el umbral de similaridad para determinar si es plagio o no. Este último tiene un valor por defecto de 0.8.

El algoritmo se puede resumir de la siguiente manera:

1. Se carga el documento sospechoso en memoria.
2. Eliminación de citas con comillas utilizando expresiones regulares.
3. Preprocesamiento del documento utilizando Spacy.
4. Eliminación de citas al final de oraciones.
5. Se carga el documento original en memoria.
6. Preprocesamiento del documento utilizando Spacy.
7. División en N-gramas de $n=3$.
8. Vectorización de ambos documentos con el Modelo Word2Vec.
9. Por cada combinación de ngramas se halla la distancia coseno entre estos. Si es mayor que un umbral, se almacena como match.
10. Se dermina la similitud como el máximo entre la proporción de ngramas que se determinaron como `match` en el documento sospechoso y en el original.

### Validación y pruebas

El corpus MSRParaphraseCorpus es un conjunto de datos que contiene 5801 pares de oraciones recopiladas durante un período de 18 meses a partir de diversas fuentes de noticias en línea. Cada par de oraciones en el corpus viene acompañado de una etiqueta que refleja si múltiples anotadores humanos consideraron que las dos oraciones eran lo suficientemente similares en significado como para ser consideradas parafraseadas cercanas.

Para validar el algoritmo de detección de plagio, se utilizó el corpus MSRParaphraseCorpus como conjunto de datos de prueba. Se compararon los resultados generados por el algoritmo con las etiquetas proporcionadas en el corpus para determinar si el algoritmo podía identificar correctamente los pares de oraciones que se consideraban parafraseadas cercanas por los anotadores humanos.

#### Métricas

Con apoyo de las métricas estudiadas en clase práctica para sistemas de recuperación de información, se implementaron las siguientes métricas:

1. Precision (Precisión):

    La precisión se refiere a la proporción de plagios detectados, contra los plagios reales.

    **Interpretación:** Un valor alto de precisión indica que la mayoría de los documentos detectados como plagio lo eran realmentente. Es útil cuando se desea minimizar el número de falsos positivos.

2. Recall (Sensibilidad):

    La sensibilidad se refiere a la proporción de documentos con plagio que fueron dectados.

    **Interpretación:** Un valor alto de sensibilidad indica que la mayoría de los documentos con plagio fueron detectados. Es útil cuando se desea maximizar la detección de plagio, incluso si eso significa tener falsos positivos adicionales.

3. F1 Score (Puntaje F):

    El puntaje F es una medida que combina precisión y sensibilidad en un solo valor. Se calcula como la media armónica de precisión y sensibilidad.

    **Interpretación:** Un valor alto de puntaje F indica un buen equilibrio entre precisión y sensibilidad. Es útil cuando se desea una métrica que tenga en cuenta tanto la precisión como la exhaustividad del sistema.

4. Fallout (Índice de falsos positivos):

    El `fallout` se refiere a la proporción de documentos detectados que no se consideran plagio.

    **Interpretación:** Un valor alto de `fallout` indica que muchos de los documentos detectados no eran plagio. Es útil cuando se desea evaluar el grado de contaminación en los resultados.

#### Resultados

| Metric      |   Value |
|-------------|---------|
| precision   |   0.7   |
| recall      |   0.7   |
| f1          |   0.7   |
| fallout     |   0.75  |

El índice de fallout, que alcanza 0.75 según los resultados, resalta un área donde el algoritmo muestra cierta debilidad. Aunque logra una alta precisión y sensibilidad en la detección de parafraseo, el fallout señala que aproximadamente el 75% de las veces el algoritmo identifica incorrectamente oraciones como parafraseadas cuando en realidad no lo son. Este aspecto sugiere la necesidad de ajustes adicionales para mejorar la capacidad del algoritmo para discernir entre parafraseo genuino y coincidencias superficiales.

### Limitaciones y mejoras propuestas

1. La principal limitación identificada es la velocidad y escalabilidad del modelo actual. Para mejorar este aspecto, se pueden explorar técnicas de optimización de código, paralelización y distribución de tareas para acelerar el procesamiento de grandes volúmenes de datos. Además, considera el uso de herramientas y plataformas de procesamiento distribuido, como Apache Spark, para manejar eficientemente la carga de trabajo en entornos distribuidos.

2. Se propone explorar métodos de vectorización de texto más avanzados que puedan capturar de manera más efectiva la semántica y el contexto de las palabras. Por ejemplo, considera el uso de modelos de representación de palabras contextualizados, como BERT o GPT, que pueden proporcionar representaciones más ricas y precisas del texto.

3. Se propone ampliar la validación del modelo en conjuntos de datos más diversos y representativos. Esto ayudará a evaluar la robustez y generalización del modelo en diferentes dominios y contextos, lo que puede proporcionar información valiosa sobre su rendimiento en situaciones del mundo real.

### Referencias

1. Linguistic features · SPACY usage documentation. (s. f.). Linguistic Features. <https://spacy.io/usage/linguistic-features#how-tokenizer-works>
2. Wikipedia contributors. (2024, 26 marzo). Word2Vec. Wikipedia. <https://en.wikipedia.org/wiki/Word2vec>
3. Srinivasa-Desikan, B. (2018). Natural Language Processing and Computational Linguistics.
