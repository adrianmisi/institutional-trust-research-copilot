# Script de Demostración: Research Copilot (5 Minutos)

## Parte 1: Introducción (0:00 - 0:30)
*Cámara encendida. Muestra la pantalla de inicio de la aplicación o la diapositiva del título.*

**Tú:** "Hola, mi nombre es Adrián Salinas y soy estudiante del curso de Prompt Engineering con GPT-4 (2026-01). Mi proyecto se titula **Research Copilot**. Es una plataforma avanzada de Análisis y Generación Aumentada (RAG) diseñada para investigadores.

Para este proyecto, recopilé una base de conocimientos especializada de 20 artículos de ciencias políticas que se centran en la confianza institucional, la calidad de la democracia y la corrupción en América Latina. El problema que resuelve Research Copilot es la sobrecarga de información: permite a los investigadores chatear directamente con esta biblioteca de nicho, extraer conceptos complejos y comparar metodologías al instante utilizando citas estructuradas en formato APA."

---

## Parte 2: Arquitectura del Sistema (0:30 - 1:00)
*Muestra el diagrama de arquitectura del `README.md`.*

**Tú:** "Nuestra arquitectura fluye desde la interfaz hasta nuestros modelos generativos. En la capa de extracción, utilizamos `PyPDFLoader` y fragmentación de tokens con `tiktoken` para tomar archivos locales y dividirlos en bloques semánticos limpios. 

Esos textos se incrustan utilizando los modelos de OpenAI y se almacenan en una base de datos vectorial local construida sobre `FAISS`, que permite consultas a alta velocidad. Finalmente, cuando el usuario hace una pregunta, recuperamos el contexto pertinente y lo inyectamos directamente en `GPT-3.5-Turbo` utilizando plantillas de ingeniería de prompts especializadas que yo mismo construí usando `LangChain`."

---

## Parte 3: Demostración en Vivo (1:00 - 3:00)
*Ve a tu sitio web de Streamlit. Haz clic en "Chat Interface".*

**Tú:** "Ahora les mostraré cómo funciona en vivo a través de nuestra interfaz web."

**(Acción 1: Pregunta Factual Simple)**
*Escribe: "What is the main argument made by Acemoglu, Johnson, and Robinson (2001) regarding colonial origins?"*
**Tú:** "Primero, le haré una pregunta factual simple de nuestro catálogo. Como podemos ver, el asistente extrae el argumento clave sobre las tasas de mortalidad y los patrones de asentamiento, proporcionando instantáneamente la cita APA exacta debajo."

**(Acción 2: Pregunta Compleja/Múltiples Fuentes)**
*Escribe: "How do Morris's findings on corruption in Mexico compare to the general theory of institutional trust?"*
**Tú:** "A continuación, vamos con una pregunta que requiere síntesis de múltiples documentos. El sistema ahora está agrupando el contexto de diferentes documentos para explicar la relación negativa entre la corrupción y la confianza, citando los artículos específicos involucrados."

**(Acción 3: Pregunta Fuera de Contexto)**
*Escribe: "What does the author think about quantum mechanics?"*
**Tú:** "Finalmente, si pregunto algo fuera del alcance como la física, el modelo se adhiere estrictamente a nuestros límites de Prompt Engineering y responde que no lo sabe para evitar alucinaciones."

**(Acción 4: Filtros y Catálogo)**
*Haz clic en "Papers" y en los filtros laterales.*
**Tú:** "La barra lateral incluye opciones dinámicas para filtrar nuestros vectores por año y por autor, lo que afina el contexto. También tenemos un explorador de todos los artículos incluidos y un panel de análisis (Analytics)."

---

## Parte 4: Discusión Técnica (3:00 - 4:00)
*Ve a la pestaña de "Settings" en la interfaz.*

**Tú:** "La principal innovación es nuestra capacidad para cambiar estrategias técnicas sobre la marcha. 

Primero, implementé múltiples configuraciones de partición o *chunking* (Small de 256 tokens, Medium de 512 y Large de 1024). Noté que las ventanas de contexto más grandes generan una recuperación mucho mejor para las preguntas complejas, mientras que el *chunking* pequeño funciona para recuperar definiciones precisas.

También programé 4 estrategias diferentes de Prompting que el usuario puede cambiar aquí. Tenemos instrucciones con delimitadores para mayor velocidad, formato JSON estricto para integraciones de software, Few-Shot Learning para forzar el tono exacto de las citas, y Chain-of-Thought (Cadena de Razonamiento) para comparaciones analíticas profundas."

---

## Parte 5: Conclusiones (4:00 - 5:00)

**Tú:** "En conclusión, construir RAG desde cero me enseñó lo crítico que es el procesamiento de los datos antes de introducirlos al LLM. La ingeniería de prompts no soluciona unos malos datos.

**Las 3 limitaciones actuales son:**
1. Los archivos son estáticos; los usuarios aún no pueden cargar PDFs en vivo en el sitio web.
2. `PyPDFLoader` a veces extrae ruido cuando hay fórmulas matemáticas complicadas.
3. El sistema depende de la API de OpenAI, por lo que incurre en costos con el tiempo.

**Para el futuro, me gustaría implementar estas 3 mejoras:**
1. Búsqueda Híbrida combinando palabras clave (BM25) con FAISS.
2. Un botón de carga interactivo en Streamlit para añadir artículos bajo demanda.
3. Integrar LangSmith para hacer evaluaciones de calidad del modelo a escala.

¡Gracias por su atención!"
