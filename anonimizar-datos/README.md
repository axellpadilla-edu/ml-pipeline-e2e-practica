## anonimizar-datos

Pequeño paquete educativo con utilidades para anonimizar columnas sensibles de un `pandas.DataFrame`.

### Funciones disponibles

- `hash_string(valor, sal=None)`: genera un hash SHA-256 determinista (opcionalmente salado) manteniendo `NaN`/`None` intactos.
- `anonimizar_columnas_hash(df, columnas, sal=None, inplace=False)`: aplica hashing seguro a una o varias columnas.
- `enmascarar_columnas(df, columnas, visible=4, caracter="*", inplace=False)`: oculta parcialmente los valores conservando los últimos caracteres para tareas de soporte.
- `tokenizar_columnas(df, columnas, prefijo="token")`: reemplaza valores por tokens legibles y devuelve el diccionario de equivalencias para auditoría.

### Ejemplo rápido

```python
import pandas as pd
from anonimizar_datos import (
	anonimizar_columnas_hash,
	enmascarar_columnas,
	tokenizar_columnas,
)

df = pd.DataFrame(
	{
		"cliente_id": ["CL-001", "CL-002"],
		"direccion": ["Av. Siempre Viva 123", "Calle Luna 45"],
	}
)

# Hash irreversible para identificadores
df_seguro = anonimizar_columnas_hash(df, "cliente_id", sal="demo")

# Enmascarado parcial para documentos
df_seguro = enmascarar_columnas(df_seguro, "documento_nacional", visible=3)

# Tokenización reversible para direcciones
resultado = tokenizar_columnas(df_seguro, "direccion")
print(resultado.dataframe)
print(resultado.diccionarios)
```

Integra estas utilidades antes de entrenar modelos o compartir datos para evitar exponer información personal.
