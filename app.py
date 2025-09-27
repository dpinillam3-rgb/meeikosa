import streamlit as st
import pandas as pd

# === Título ===
st.title("Meeiko S.A. - Análisis de Clientes")
st.write("Iniciando la app...")

# === Cargar CSV con manejo de errores ===
try:
    df = pd.read_csv("CLV.csv", delimiter=";")
    st.success(f"CSV cargado correctamente. Filas: {len(df)}, Columnas: {len(df.columns)}")
except FileNotFoundError:
    st.error("No se encontró el archivo 'CLV.csv'. Asegúrate de que esté en la misma carpeta que 'app.py'.")
    st.stop()
except Exception as e:
    st.error(f"Error al cargar CSV: {e}")
    st.stop()

# === Función de limpieza de números ===
def limpiar_num(col):
    if col not in df.columns:
        st.warning(f"Columna '{col}' no encontrada en el CSV. Se llenará con ceros.")
        return pd.Series([0]*len(df))
    
    serie = df[col].fillna("0").astype(str).str.strip()
    serie = serie.str.replace('.', '', regex=False)
    serie = serie.str.replace(',', '.', regex=False)
    serie = pd.to_numeric(serie, errors='coerce')
    return serie.fillna(0)

# Crear nueva columna CLV
df["CLV"] = limpiar_num("Customer Lifetime Value")

# === Traducciones globales ===
column_map = {
    "State": "Estado",
    "Coverage": "Cobertura",
    "Sales Channel": "Canal de ventas",
    "Education": "Nivel educativo",
    "Marital Status": "Estado civil",
    "EmploymentStatus": "Empleo",
    "Gender": "Género",
    "Vehicle Class": "Clase de vehículo",
    "Vehicle Size": "Tamaño de vehículo"
}

for col_en, col_es in column_map.items():
    if col_en in df.columns:
        df[col_es] = df[col_en]
    else:
        st.warning(f"Columna '{col_en}' no encontrada. Se creará vacía.")
        df[col_es] = ""

# Reemplazos específicos
df["Cobertura"] = df["Cobertura"].replace({
    "Basic": "Básica",
    "Extended": "Extendida",
    "Premium": "Premium"
})
df["Canal de ventas"] = df["Canal de ventas"].replace({
    "Agent": "Agente",
    "Call Center": "Centro de llamadas",
    "Branch": "Oficina física",
    "Web": "Página web"
})
df["Nivel educativo"] = df["Nivel educativo"].replace({
    "Bachelor": "Pregrado",
    "Master": "Maestría",
    "High School or Below": "Bachillerato o inferior",
    "Doctor": "Doctorado",
    "College": "Universitario"
})
df["Estado civil"] = df["Estado civil"].replace({
    "Single": "Soltero(a)",
    "Married": "Casado(a)",
    "Divorced": "Divorciado(a)"
})
df["Empleo"] = df["Empleo"].replace({
    "Employed": "Empleado(a)",
    "Unemployed": "Desempleado(a)",
    "Medical Leave": "Licencia médica",
    "Disabled": "Discapacitado(a)",
    "Retired": "Jubilado(a)",
    "Student": "Estudiante"
})
df["Género"] = df["Género"].replace({"M": "Masculino", "F": "Femenino"})
df["Clase de vehículo"] = df["Clase de vehículo"].replace({
    "Two-Door Car": "Automóvil de dos puertas",
    "Four-Door Car": "Automóvil de cuatro puertas",
    "SUV": "SUV",
    "Luxury SUV": "SUV de lujo",
    "Luxury Car": "Automóvil de lujo",
    "Sports Car": "Automóvil deportivo"
})
df["Tamaño de vehículo"] = df["Tamaño de vehículo"].replace({
    "Small": "Pequeño",
    "Medsize": "Mediano",
    "Large": "Grande"
})

# === Interfaz Streamlit ===
opcion = st.sidebar.selectbox(
    "Seleccione una opción:",
    [
        "Consultar cliente por ID",
        "Top 10 clientes con mayor CLV",
        "Promedio de CLV por estado",
        "Oportunidades por segmento de cobertura",
        "Promedio de CLV por canal de ventas",
        "Reportes generales"
    ]
)

# === Opción 1: Consultar cliente por ID ===
if opcion == "Consultar cliente por ID":
    cliente_id = st.text_input("Ingrese el ID del cliente:")
    if cliente_id:
        if "Customer" not in df.columns:
            st.warning("Columna 'Customer' no encontrada en el CSV.")
        else:
            cliente = df[df["Customer"] == cliente_id]
            if not cliente.empty:
                info = cliente.iloc[0]
                st.subheader("Información del cliente")
                for col in ["Customer", "Estado", "CLV", "Cobertura", "Nivel educativo", "Estado civil",
                            "Empleo", "Género", "Canal de ventas", "Clase de vehículo", "Tamaño de vehículo", "Total Claim Amount"]:
                    if col in df.columns:
                        valor = info[col]
                        if col == "CLV" or col == "Total Claim Amount":
                            st.write(f"{col}: {valor:,.2f}")
                        else:
                            st.write(f"{col}: {valor}")
            else:
                st.warning("Cliente no encontrado.")

# === Otras opciones ===
elif opcion == "Top 10 clientes con mayor CLV":
    st.subheader("Top 10 clientes con mayor CLV")
    if "CLV" in df.columns and "Customer" in df.columns:
        top10 = df[["Customer", "CLV"]].sort_values(by="CLV", ascending=False).head(10)
        st.dataframe(top10)
    else:
        st.warning("Columnas necesarias no encontradas para esta opción.")

elif opcion == "Promedio de CLV por estado":
    st.subheader("Promedio de CLV por estado")
    if "CLV" in df.columns and "Estado" in df.columns:
        promedio_estado = df.groupby("Estado")["CLV"].mean().round(2)
        st.dataframe(promedio_estado)
    else:
        st.warning("Columnas necesarias no encontradas para esta opción.")

elif opcion == "Oportunidades por segmento de cobertura":
    st.subheader("Oportunidades por segmento de cobertura")
    if "CLV" in df.columns and "Cobertura" in df.columns:
        promedio_cobertura = df.groupby("Cobertura")["CLV"].mean().round(2)
        st.dataframe(promedio_cobertura)
    else:
        st.warning("Columnas necesarias no encontradas para esta opción.")

elif opcion == "Promedio de CLV por canal de ventas":
    st.subheader("Promedio de CLV por canal de ventas")
    if "CLV" in df.columns and "Canal de ventas" in df.columns:
        promedio_canal = df.groupby("Canal de ventas")["CLV"].mean().round(2)
        st.dataframe(promedio_canal)
    else:
        st.warning("Columnas necesarias no encontradas para esta opción.")

elif opcion == "Reportes generales":
    st.subheader("Reportes generales")
    st.write(f"Total de clientes: {df['Customer'].nunique() if 'Customer' in df.columns else 0}")
    st.write(f"Promedio general de CLV: {df['CLV'].mean():,.2f}" if 'CLV' in df.columns else "CLV no disponible")
    st.write(f"Monto total por reclamaciones: {df['Total Claim Amount'].sum():,.2f}" if 'Total Claim Amount' in df.columns else "Total Claim Amount no disponible")
    for col in ["Cobertura", "Canal de ventas"]:
        if col in df.columns:
            st.write(f"Distribución por {col}:")
            st.dataframe(df[col].value_counts())
