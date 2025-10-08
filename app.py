# =========================================================
# ✏️ Agregar o actualizar estudiante
# =========================================================
elif menu == "✏️ Actualizar o Agregar Estudiante":
    st.header("✏️ Actualizar o Agregar Estudiante")

    # Dropdown de grados
    grados_existentes = sorted(df["Grado"].dropna().unique())
    grado = st.selectbox("Selecciona el grado", grados_existentes)

    # Filtrar estudiantes de ese grado
    estudiantes_grado = df[df["Grado"] == grado]["Nombre"].tolist()
    estudiantes_opciones = estudiantes_grado + ["Nuevo estudiante"]
    nombre = st.selectbox("Selecciona un estudiante o Nuevo estudiante", estudiantes_opciones)

    # Si es nuevo estudiante, pedir nombre
    if nombre == "Nuevo estudiante":
        nombre = st.text_input("Escribe el nombre del estudiante:")

    if nombre:
        # Verificar si ya existe
        existe = ((df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())).any()

        if existe:
            st.subheader(f"📄 Editar datos de {nombre} ({grado})")
            estudiante = df[(df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())].iloc[0]
        else:
            st.subheader(f"🆕 Registrar nuevo estudiante ({grado})")
            estudiante = {
                "Desempeño Académico": 3.0,
                "Disciplina": 5,
                "Aspecto Emocional": 5,
                "Observaciones Docente": ""
            }

        # Formulario de edición o creación
        with st.form("form_estudiante"):
            nuevo_academico = st.slider("Desempeño Académico (1.0 - 5.0)", 1.0, 5.0, float(estudiante["Desempeño Académico"]))
            nueva_disciplina = st.slider("Disciplina (0 - 10)", 0, 10, int(estudiante["Disciplina"]))
            nuevo_emocional = st.slider("Aspecto Emocional (0 - 10)", 0, 10, int(estudiante["Aspecto Emocional"]))
            nuevas_observaciones = st.text_area("Observaciones Docente", value=estudiante["Observaciones Docente"])

            submit = st.form_submit_button("💾 Guardar Cambios")

            if submit:
                if existe:
                    idx = df[(df["Grado"] == grado) & (df["Nombre"].str.lower() == nombre.lower())].index[0]
                    df.loc[idx, "Desempeño Académico"] = nuevo_academico
                    df.loc[idx, "Disciplina"] = nueva_disciplina
                    df.loc[idx, "Aspecto Emocional"] = nuevo_emocional
                    df.loc[idx, "Observaciones Docente"] = nuevas_observaciones
                    df.loc[idx, "Última Actualización"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success(f"✅ Datos de {nombre} actualizados correctamente.")
                else:
                    nuevo_id = df["ID"].max() + 1 if "ID" in df.columns and not df.empty else 1200
                    nuevo = pd.DataFrame([{
                        "ID": int(nuevo_id),
                        "Nombre": nombre,
                        "Grado": grado,
                        "Desempeño Académico": nuevo_academico,
                        "Disciplina": nueva_disciplina,
                        "Aspecto Emocional": nuevo_emocional,
                        "Observaciones Docente": nuevas_observaciones,
                        "Última Actualización": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }])
                    df = pd.concat([df, nuevo], ignore_index=True)
                    st.success(f"🆕 Nuevo estudiante {nombre} agregado correctamente.")

                guardar_datos(df)
