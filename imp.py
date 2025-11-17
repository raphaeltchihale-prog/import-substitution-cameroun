# ====== Onglet Fusionné : Analyse & Tableau de Bord ====== #
with tabs[0]:
    st.header("📊 Analyse & Tableau de Bord")

    # Filtre pour choisir l'indicateur à tracer
    indicateur = st.selectbox(
        "Indicateur à afficher :",
        ("Importation", "Production")
    )

    # Détection colonne importation à partir du fichier
    detected_import_col = col_import if col_import in df_f.columns else "Importation (en tonne)"

    # Palette de couleurs professionnelles
    colors = {
        "Importation": "#C0392B",  # rouge foncé
        "Production": "#27AE60"     # vert foncé
    }

    for produit in selected_produits:
        st.subheader(f"📍 Filière : {produit}")
        df_p = df_f[df_f[col_produits] == produit].sort_values(by=col_annee)
        if df_p.empty:
            st.warning(f"Aucune donnée disponible pour {produit}")
            continue

        # --- Diagramme à barres ---
        fig_bar = go.Figure()
        if indicateur == "Importation":
            fig_bar.add_trace(go.Bar(
                x=df_p[col_annee],
                y=df_p[detected_import_col],
                name="Importation",
                marker_color=colors["Importation"],
                text=df_p[detected_import_col],
                textposition="outside"
            ))
        else:
            fig_bar.add_trace(go.Bar(
                x=df_p[col_annee],
                y=df_p[col_prod],
                name="Production",
                marker_color=colors["Production"],
                text=df_p[col_prod],
                textposition="outside"
            ))

        fig_bar.update_layout(
            title=f"{indicateur} — {produit} (Diagramme à barres)",
            xaxis_title="Année",
            yaxis_title="Valeur",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # --- Courbes ---
        fig_line = go.Figure()
        if indicateur == "Importation":
            fig_line.add_trace(go.Scatter(
                x=df_p[col_annee],
                y=df_p[detected_import_col],
                mode="lines+markers",
                name="Importation",
                line=dict(color=colors["Importation"], width=3)
            ))
        else:
            fig_line.add_trace(go.Scatter(
                x=df_p[col_annee],
                y=df_p[col_prod],
                mode="lines+markers",
                name="Production",
                line=dict(color=colors["Production"], width=3)
            ))

        fig_line.update_layout(
            title=f"{indicateur} — {produit} (Courbe)",
            xaxis_title="Année",
            yaxis_title="Valeur",
            template="plotly_white",
            height=400
        )
        st.plotly_chart(fig_line, use_container_width=True)


# ====== Onglet Synthèse ====== #
with tabs[1]:
    st.header("🧮 Synthèse — Importation et Production par Produit et Année")

    # Agrégation des données par année et produit
    synth = df_f.groupby([col_annee, col_produits]).agg({
        col_import: "sum",
        col_prod: "sum"
    }).reset_index()

    # Sélection des colonnes à afficher
    synth = synth[[col_annee, col_import, col_prod]]
    synth.columns = ["Année", "Importations", "Production"]

    # Affichage du tableau
    st.dataframe(synth, use_container_width=True)


# ====== Onglet Export ====== #
with tabs[2]:
    st.header("📤 Export des Résultats")

    export_dict = {
        "Filtrage": df_f,
        "Synthèse": synth
    }

    bytes_xlsx = to_excel_bytes(export_dict)

    st.download_button(
        label="💾 Télécharger les résultats filtrés (Excel)",
        data=bytes_xlsx,
        file_name="import_substitution_filtrees.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
