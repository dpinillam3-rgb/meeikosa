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

# Estado
df["Estado"] = df["State"]

# Cobertura
df["Cobertura"] = df["Coverage"].replace({
    "Basic": "Básica",
    "Extended": "Extendida",
    "Premium": "Premium"
})

# Canal de ventas
df["Canal de ventas"] = df["Sales Channel"].replace({
    "Agent": "Agente",
    "Call Center": "Centro de llamadas",
    "Branch": "Oficina física",
    "Web": "Página web"
})

# Nivel educativo
df["Nivel educativo"] = df["Education"].replace({
    "Bachelor": "Pregrado",
    "Master": "Maestría",
    "High School or Below": "Bachillerato o inferior",
    "Doctor": "Doctorado",
    "College": "Universitario"
})

# Estado civil
df["Estado civil"] = df["Marital Status"].replace({
    "Single": "Soltero(a)",
    "Married": "Casado(a)",
    "Divorced": "Divorciado(a)"
})

# Empleo
df["Empleo"] = df["EmploymentStatus"].replace({
    "Employed": "Empleado(a)",
    "Unemployed": "Desempleado(a)",
    "Medical Leave": "Licencia médica",
    "Disabled": "Discapacitado(a)",
    "Retired": "Jubilado(a)",
    "Student": "Estudiante"
})

# Género
df["Género"] = df["Gender"].replace({
    "M": "Masculino",
    "F": "Femenino"
})

# Clase de vehículo
df["Clase de vehículo"] = df["Vehicle Class"].replace({
    "Two-Door Car": "Automóvil de dos puertas",
    "Four-Door Car": "Automóvil de cuatro puertas",
    "SUV": "SUV",
    "Luxury SUV": "SUV de lujo",
    "Luxury Car": "Automóvil de lujo",
    "Sports Car": "Automóvil deportivo"
})

# Tamaño del vehículo
df["Tamaño de vehículo"] = df["Vehicle Size"].replace({
    "Small": "Pequeño",
    "Medsize": "Mediano",
    "Large": "Grande"
})

# === Menú principal ===
def menu():
    while True:
        print("\n=== Bienvenido a Meeiko S.A. ===")
        print("Seleccione una opción:")
        print("1. Consultar cliente por ID")
        print("2. Top 10 clientes con mayor CLV")
        print("3. Promedio de CLV por estado")
        print("4. Oportunidades por segmento de cobertura")
        print("5. Promedio de CLV por canal de ventas")
        print("6. Reportes generales")
        print("7. Salir")

        opcion = input("Ingrese su opción: ")

        # === Opción 1 ===
        if opcion == "1":
            cliente_id = input("Ingrese el ID del cliente: ")
            cliente = df[df["Customer"] == cliente_id]
            if not cliente.empty:
                info = cliente.iloc[0]
                print("\n Información del cliente:")
                print(f"ID Cliente: {info['Customer']}")
                print(f"Estado: {info['Estado']}")
                print(f"CLV: {info['CLV']:,.2f}")
                print(f"Cobertura: {info['Cobertura']}")
                print(f"Nivel educativo: {info['Nivel educativo']}")
                print(f"Estado civil: {info['Estado civil']}")
                print(f"Empleo: {info['Empleo']}")
                print(f"Género: {info['Género']}")
                print(f"Canal de ventas: {info['Canal de ventas']}")
                print(f"Clase de vehículo: {info['Clase de vehículo']}")
                print(f"Tamaño de vehículo: {info['Tamaño de vehículo']}")
                print(f"Monto total por reclamaciones: {info['Total Claim Amount']}")
            else:
                print("Cliente no encontrado.")

        # === Opción 2 ===
        elif opcion == "2":
            print("\n Top 10 clientes con mayor CLV:\n")
            top10 = df[["Customer", "CLV"]].sort_values(by="CLV", ascending=False).head(10)
            print(top10.to_string(index=False))

        # === Opción 3 ===
        elif opcion == "3":
            print("\n Promedio de CLV por estado:\n")
            promedio_estado = df.groupby("Estado")["CLV"].mean().round(2)
            print(promedio_estado)

        # === Opción 4 ===
        elif opcion == "4":
            print("\n Oportunidades por segmento de cobertura:\n")
            promedio_cobertura = df.groupby("Cobertura")["CLV"].mean().round(2)
            print(promedio_cobertura)

        # === Opción 5 ===
        elif opcion == "5":
            print("\nPromedio de CLV por canal de ventas:\n")
            promedio_canal = df.groupby("Canal de ventas")["CLV"].mean().round(2)
            print(promedio_canal)

        # === Opción 6 ===
        elif opcion == "6":
            print("\n Reportes generales:\n")
            print(f"Total de clientes: {df['Customer'].nunique()}")
            print(f"Promedio general de CLV: {df['CLV'].mean():,.2f}")
            print(f"Monto total por reclamaciones: {df['Total Claim Amount'].sum():,.2f}")
            print("Distribución por cobertura:")
            print(df["Cobertura"].value_counts())
            print("\nDistribución por canal de ventas:")
            print(df["Canal de ventas"].value_counts())

        # === Opción 7 ===
        elif opcion == "7":
            print("👋 Gracias por usar Meeiko S.A. ¡Hasta pronto!")
            break

        else:
            print("⚠️ Opción no válida. Intente nuevamente.")

# Ejecutar menú
menu()