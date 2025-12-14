# Contribuir a RaveXRPC

¡Gracias por tu interés en contribuir a RaveXRPC! Este documento proporciona guías y mejores prácticas para contribuir al proyecto.

## 🚀 Cómo Empezar

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/christianfm10/ravexrpc.git
   cd ravexrpc
   ```

2. **Configurar el entorno de desarrollo**
   ```bash
   # Instalar uv si no lo tienes
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Crear entorno virtual e instalar dependencias
   uv venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   uv pip install -e ".[dev]"
   ```

3. **Crear una rama para tu feature**
   ```bash
   git checkout -b feature/mi-nueva-feature
   ```

## 📝 Guías de Estilo

### Código Python

- Seguimos [PEP 8](https://pep8.org/) con algunas personalizaciones
- Usamos `ruff` para linting y formateo
- Longitud máxima de línea: 88 caracteres
- Usamos type hints en todas las funciones públicas

```bash
# Formatear código
ruff format .

# Verificar linting
ruff check .

# Auto-fix issues
ruff check --fix .
```

### Docstrings

Usamos el estilo de Google para docstrings:

```python
def mi_funcion(param1: str, param2: int) -> bool:
    """Breve descripción de una línea.
    
    Descripción más detallada si es necesaria. Puede abarcar
    múltiples líneas.
    
    Args:
        param1: Descripción del primer parámetro
        param2: Descripción del segundo parámetro
        
    Returns:
        Descripción de lo que retorna la función
        
    Raises:
        ValueError: Cuándo y por qué se lanza esta excepción
        
    Example:
        >>> mi_funcion("test", 42)
        True
    """
```

### Commits

- Usa mensajes de commit descriptivos
- Primera línea: resumen breve (50 caracteres max)
- Cuerpo: descripción detallada si es necesario
- Formato: `tipo: descripción`

Tipos de commit:
- `feat`: Nueva funcionalidad
- `fix`: Corrección de bug
- `docs`: Cambios en documentación
- `style`: Cambios de formato (sin cambio de código)
- `refactor`: Refactorización de código
- `test`: Añadir o modificar tests
- `chore`: Tareas de mantenimiento

Ejemplo:
```bash
git commit -m "feat: añadir soporte para getBalance RPC method

Implementa el método get_balance() que consulta el balance
de una cuenta en SOL. Incluye tests y documentación."
```

## 🧪 Tests

### Ejecutar Tests

```bash
# Todos los tests
pytest

# Con cobertura
pytest --cov=ravexrpc --cov-report=html

# Tests específicos
pytest tests/test_client.py

# Test específico
pytest tests/test_client.py::TestRPCClient::test_client_initialization
```

### Escribir Tests

- Todos los nuevos features deben incluir tests
- Cobertura mínima: 80%
- Usa fixtures del archivo `conftest.py`
- Mockea las llamadas RPC externas

Ejemplo de test:

```python
import pytest
from ravexrpc import RPC_Client
from ravexrpc.exceptions import RPCException

@pytest.mark.asyncio
async def test_mi_nuevo_metodo(mock_client, sample_response):
    """Test de mi nuevo método."""
    mock_client._fetch.return_value = sample_response
    
    result = await mock_client.mi_nuevo_metodo()
    
    assert result is not None
    assert result.campo == "valor_esperado"
```

## 📦 Añadir Nuevas Funcionalidades

### Nuevo Método RPC

1. **Añadir el método en `client.py`**:
   ```python
   async def nuevo_metodo(
       self,
       param1: str,
       param2: int = 10,
   ) -> NuevoResultModel:
       """Documentación completa del método."""
       # Implementación
   ```

2. **Crear modelo en `models.py`** (si es necesario):
   ```python
   class NuevoResultModel(APIBaseModel):
       """Documentación del modelo."""
       campo1: str
       campo2: int
   ```

3. **Añadir tests en `tests/test_client.py`**

4. **Actualizar README.md** con ejemplos de uso

5. **Exportar en `__init__.py`** si es parte del API público

### Nuevas Excepciones

1. Añadir en `exceptions.py`:
   ```python
   class MiNuevaException(RPCException):
       """Documentación de la excepción."""
       pass
   ```

2. Exportar en `__init__.py`

3. Añadir tests en `tests/test_exceptions.py`

## 🔍 Revisión de Código

Antes de enviar tu PR, verifica:

- [ ] El código pasa todos los tests: `pytest`
- [ ] El código está formateado: `ruff format .`
- [ ] El código pasa linting: `ruff check .`
- [ ] Añadiste tests para nuevas funcionalidades
- [ ] Actualizaste la documentación (README, docstrings)
- [ ] Los commits tienen mensajes descriptivos
- [ ] No hay conflictos con la rama `main`

## 📬 Enviar Pull Request

1. Push tu rama al fork
   ```bash
   git push origin feature/mi-nueva-feature
   ```

2. Crea un Pull Request en GitHub

3. Describe los cambios:
   - Qué problema resuelve
   - Cómo lo resuelve
   - Cualquier consideración especial

4. Espera la revisión y responde a los comentarios

## 🐛 Reportar Bugs

Usa GitHub Issues y proporciona:

- Descripción clara del problema
- Pasos para reproducir
- Comportamiento esperado vs. actual
- Versión de Python y del paquete
- Logs o stack traces relevantes

## 💡 Sugerir Features

Usa GitHub Issues con el tag `enhancement`:

- Descripción del feature
- Casos de uso
- Posible implementación
- Ejemplos de API

## 📞 Contacto

- GitHub Issues: Para bugs y features
- Email: christianmfm10@gmail.com

## 📄 Licencia

Al contribuir, aceptas que tus contribuciones se licencien bajo la misma licencia MIT del proyecto.

---

¡Gracias por contribuir a RaveXRPC! 🚀
