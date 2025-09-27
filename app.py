import streamlit as st
import pandas as pd

# === Cargar datos ===
df = pd.read_csv("CLV.csv", delimiter=";")

# === Función de limpieza de números (ej. CLV) ===
def limpiar_num(col):
    serie = df[col].fillna("0").astype(str)
    serie = serie.str.strip()
    serie = serie.str.replace('.', '', regex=False)   # quitar separadores de miles
    serie = serie.str.replace(',', '.', regex=False)  # cambiar coma por punto decimal
    serie = pd.to_numeric(serie, errors='coerce')
    return serie.fillna(0)

# Crear nueva columna CLV
df["CLV"] = limpiar_num("Customer Lifetime Value")

# === Traducciones globales ===
df["Estado"] = df["State"]

df["Cobertura"] = df["Coverage"].replace({
    "Basic": "Básica",
    "Extended": "Extendida",
    "Premium": "Premium"
})

df["Canal de ventas"] = df["Sales Channel"].replace({
    "Agent": "Agente",
    "Call Center": "Centro de llamadas",
    "Branch": "Oficina física",
    "Web": "Página web"
})

df["Nivel educativo"] = df["Education"].replace({
    "Bachelor": "Pregrado",
    "Master": "Maestría",
    "High School or Below": "Bachillerato o inferior",
    "Doctor": "Doctorado",
    "College": "Universitario"
})

df["Estado civil"] = df["Marital Status"].replace({
    "Single": "Soltero(a)",
    "Married": "Casado(a)",
    "Divorced": "Divorciado(a)"
})

df["Empleo"] = df["EmploymentStatus"].replace({
    "Employed": "Empleado(a)",
    "Unemployed": "Desempleado(a)",
    "Medical Leave": "Licencia médica",
    "Disabled": "Discapacitado(a)",
    "Retired": "Jubilado(a)",
    "Student": "Estudiante"
})

df["Género"] = df["Gender"].replace({
    "M": "Masculino",
    "F": "Femenino"
})

df["Clase de vehículo"] = df["Vehicle Class"].replace({
    "Two-Door Car": "Automóvil de dos puertas",
    "Four-Door Car": "Automóvil de cuatro puertas",
    "SUV": "SUV",
    "Luxury SUV": "SUV de lujo",
    "Luxury Car": "Automóvil de lujo",
    "Sports Car": "Automóvil deportivo"
})

df["Tamaño de vehículo"] = df["Vehicle Size"].replace({
    "Small": "Pequeño",
    "Medsize": "Mediano",
    "Large": "Grande"
})

# === Interfaz Streamlit ===
st.title("Meeiko S.A. - Análisis de Clientes")

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

# === Opción 1 ===
if opcion == "Consultar cliente por ID":
    cliente_id = st.text_input("Ingrese el ID del cliente:")
    if cliente_id:
        cliente = df[df["Customer"] == cliente_id]
        if not cliente.empty:
            info = cliente.iloc[0]
            st.subheader("📌 Información del cliente")
            st.write(f"**ID Cliente:** {info['Customer']}")
            st.write(f"**Estado:** {info['Estado']}")
            st.write(f"**CLV:** {info['CLV']:,.2f}")
            st.write(f"**Cobertura:** {info['Cobertura']}")
            st.write(f"**Nivel educativo:** {info['Nivel educativo']}")
            st.write(f"**Estado civil:** {info['Estado civil']}")
            st.write(f"**Empleo:** {info['Empleo']}")
            st.write(f"**Género:** {info['Género']}")
            st.write(f"**Canal de ventas:** {info['Canal de ventas']}")
            st.write(f"**Clase de vehículo:** {info['Clase de vehículo']}")
            st.write(f"**Tamaño de vehículo:** {info['Tamaño de vehículo']}")
            st.write(f"**Monto total por reclamaciones:** {info['Total Claim Amount']}")
        else:
            st.warning("Cliente no encontrado.")

# === Opción 2 ===
elif opcion == "Top 10 clientes con mayor CLV":
    st.subheader("Top 10 clientes con mayor CLV")
    top10 = df[["Customer", "CLV"]].sort_values(by="CLV", ascending=False).head(10)
    st.dataframe(top10)

# === Opción 3 ===
elif opcion == "Promedio de CLV por estado":
    st.subheader("Promedio de CLV por estado")
    promedio_estado = df.groupby("Estado")["CLV"].mean().round(2)
    st.dataframe(promedio_estado)

# === Opción 4 ===
elif opcion == "Oportunidades por segmento de cobertura":
    st.subheader("Oportunidades por segmento de cobertura")
    promedio_cobertura = df.groupby("Cobertura")["CLV"].mean().round(2)
    st.dataframe(promedio_cobertura)

# === Opción 5 ===
elif opcion == "Promedio de CLV por canal de ventas":
    st.subheader("Promedio de CLV por canal de ventas")
    promedio_canal = df.groupby("Canal de ventas")["CLV"].mean().round(2)
    st.dataframe(promedio_canal)

# === Opción 6 ===
elif opcion == "Reportes generales":
    st.subheader("Reportes generales")
    st.write(f"**Total de clientes:** {df['Customer'].nunique()}")
    st.write(f"**Promedio general de CLV:** {df['CLV'].mean():,.2f}")
    st.write(f"**Monto total por reclamaciones:** {df['Total Claim Amount'].sum():,.2f}")
    st.write("**Distribución por cobertura:**")
    st.dataframe(df["Cobertura"].value_counts())
    st.write("**Distribución por canal de ventas:**")
    st.dataframe(df["Canal de ventas"].value_counts())