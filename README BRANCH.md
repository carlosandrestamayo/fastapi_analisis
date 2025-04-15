# 🧑‍💻 Guía profesional de trabajo en equipo con Git y GitHub

## 🚀 Objetivo

Establecer un flujo profesional y ordenado para trabajar en equipo usando Git y GitHub. Esta guía te explica cómo crear una rama de forma correcta y cómo colaborar en un proyecto compartido.

---

## 📌 Paso 1: Clonar el repositorio (si aún no lo tienes)

```bash
git clone https://github.com/tu-usuario/tu-repositorio.git
cd tu-repositorio
```

---

## 📌 Paso 2: Verifica en qué rama estás y actualiza tu copia local

```bash
git branch          # Muestra la rama actual
git pull origin main  # Asegura que tienes la última versión del proyecto
```

---

## 📌 Paso 3: Crea una nueva rama de forma profesional

```bash
git checkout -b feature/nombre-descriptivo
```

### Ejemplos de nombres válidos:
- `feature/bisection-endpoint`
- `fix/decimals-validation`
- `docs/setup-instructions`
- `refactor/response-structure`

---

## 📌 Paso 4: Realiza tus cambios y guárdalos

```bash
# Edita archivos, guarda cambios...

git add .
git commit -m "feat: agregar endpoint de bisección con validaciones"
```

### Convenciones para mensajes de commit:
- `feat:` nueva funcionalidad
- `fix:` corrección de error
- `refactor:` reestructuración sin cambio funcional
- `docs:` documentación

---

## 📌 Paso 5: Sube tu rama al repositorio remoto

```bash
git push origin feature/nombre-descriptivo
```

---

## 📌 Paso 6: Crear un Pull Request en GitHub

1. Ve al repositorio en GitHub.
2. Verás un botón que sugiere crear un Pull Request desde tu rama.
3. Agrega un título claro y descripción de los cambios.
4. Asigna a otro compañero como revisor si aplica.
5. Espera aprobación y merge.

---

## 🧠 Buenas prácticas

- Trabaja en ramas pequeñas y específicas.
- Siempre nombra tus ramas de forma clara y consistente.
- Revisa los Pull Requests de tus compañeros.
- Actualiza tu rama regularmente con `main` si el proyecto avanza.
- No trabajes directamente en `main` salvo que esté estrictamente permitido.

---

## 🫱🏻‍🫲🏼 ¡Felices commits y colaboración efectiva!

Esta guía es para ayudarnos a trabajar como un equipo profesional. Si tienes dudas, coméntalas en la reunión o en los Pull Requests.
