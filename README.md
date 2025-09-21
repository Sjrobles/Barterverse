# Barter - Plataforma de Trueques

**Equipo de Desarrollo - Diseño de Software II**  



---

## Descripción
Barter es una plataforma e-commerce especializada en trueques, que permite a los usuarios intercambiar productos o servicios sin utilizar dinero como medio de pago. El proyecto está desarrollado usando una arquitectura de microservicios basada en **Clean Architecture**, con tecnologías modernas que garantizan **escalabilidad, mantenibilidad y facilidad de integración**.

---

### Casos de uso clave incluidos en esta primera versión:
- **Registro de ofertas de trueque** con detalle, condiciones y un comentario libre del usuario.  
- **Análisis del comentario de la oferta**:
  - Extracción de palabras clave.  
  - Detección de sentimientos.  
  - Generación de embeddings para búsqueda semántica.  
- **Exploración/búsqueda de trueques existentes** por:
  - Categoría  
  - Palabra clave  
  - Afinidad semántica (recomendaciones inteligentes)  
- **Cierre del trueque y registro del intercambio**.  
- **Calificación de los usuarios** tras concretar el intercambio.  
- **Panel de administración básico** para supervisión de operaciones y actividad de recomendaciones.  

Estos procesos permiten probar la propuesta de valor e iterar en desarrollo, validando tanto la experiencia de intercambio como la relevancia de las recomendaciones basadas en lenguaje natural.

---

## Selección de frameworks, lenguajes, DB y herramientas

### Backend Core (negocio)
- **NestJS (Node.js + TypeScript)** → catálogo de trueques, usuarios, negociación, notificaciones.  

### Microservicios de IA/NLP
- **Python (FastAPI)** → microservicios especializados para:
  - Procesar comentarios de usuarios.  
  - Analizar sentimientos.  
  - Extraer palabras clave.  
  - Generar embeddings semánticos.  

### Bases de datos
- **PostgreSQL + Prisma** → base relacional principal para usuarios, trueques, historial, calificaciones. Incluye soporte geoespacial para filtrar por cercanía.  
- **ChromaDB** → base vectorial para almacenar embeddings y realizar búsquedas por similitud semántica en descripciones/comentarios.  

### Mensajería
- **Kafka** (si se espera alto volumen) o **RabbitMQ** (si se prioriza facilidad).  
Facilitan la comunicación asíncrona entre microservicios, por ejemplo, entre el catálogo y el servicio de NLP.  

### Contenerización e integración
- **Docker y docker-compose** → empaquetado portable de microservicios.  

### Documentación API
- **Swagger/OpenAPI** → generación automática y exploración de contratos de servicios para los microservicios en TS y Python.  

### Infraestructura y despliegue futuro
- **Kubernetes (Minikube en local)** → para orquestación y escalabilidad futura en producción.  

---

## Estructura del Proyecto
El repositorio contiene la estructura inicial basada en microservicios con carpetas organizadas por capas, integrando:

- Microservicios independientes con sus propias bases de datos.
- Esqueleto de los servicios con contratos y documentación OpenAPI.
- Configuración para el ambiente local con `docker-compose.dev.yml`.
- Scripts para pruebas unitarias y generación de reportes.
- Manifiestos básicos para despliegue en Kubernetes.
- Configuración inicial para Service Mesh con Istio o Linkerd.

---

## Instalación y Ejecución Local

1. Clonar el repositorio y levantar la BD:

```bash
git clone <repo-url>
cd barter
docker-compose -f docker-compose.dev.yml up -d
