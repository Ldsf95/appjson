import json
import streamlit as st

# =====================================================================
# PARTIE 1 : L'ALGORITHME (Format HTML/Markdown Mixte pour Confluence)
# =====================================================================
def generer_format_confluence(data):
    markup = ""
    # Code couleur bleu officiel d'Atlassian/Confluence
    bleu_conf = "#00B7FF"

    # --- TITRE PRINCIPAL ---
    titre = data.get("title", data.get("name", "Règle sans titre"))
    markup += f"<h1 style='color: {bleu_conf};'>ENGIE – Détection : {titre}</h1>\n<hr>\n\n"

    # --- INFORMATIONS GÉNÉRALES ---
    markup += f"<h2 style='color: {bleu_conf};'>📌 Informations générales</h2>\n\n"

    sev = str(data.get("severity", "medium")).lower()
    if sev == "high":
        sev_display = "🔴 High"
    elif sev == "low":
        sev_display = "🟢 Low"
    else:
        sev_display = "🟡 Medium"

    markup += "| Élément | Détails |\n"
    markup += "| --- | --- |\n"
    markup += f"| **ID** | {data.get('id', '-')} |\n"
    markup += f"| **Nom** | {data.get('name', '-')} |\n"
    markup += f"| **Titre** | {titre} |\n"
    markup += f"| **Catégorie** | {str(data.get('category', '-')).capitalize()} |\n"
    markup += f"| **Sévérité** | {sev_display} |\n\n"
    markup += "<hr>\n\n"

    # --- DESCRIPTION ---
    markup += f"<h2 style='color: {bleu_conf};'>📄 Description</h2>\n\n"
    markup += f"{data.get('description', 'Aucune description.')}\n\n"
    markup += "<hr>\n\n"

    # --- SCOPE ---
    markup += f"<h2 style='color: {bleu_conf};'>🎯 Scope</h2>\n\n"
    markup += "```\n"
    markup += f"{data.get('scope', '-')}\n"
    markup += "```\n\n"
    markup += "<hr>\n\n"

    # --- CONDITIONS DE DÉTECTION ---
    markup += f"<h2 style='color: {bleu_conf};'>✅ Conditions de détection</h2>\n\n"
    markup += f"Une ressource de type `{data.get('scope', 'ressource')}` est considérée comme vide si :\n\n"

    cond_lines = []
    for c in data.get("conditions", []):
        if "logic" in c:
            logic_op = f" {c['logic'].upper()} "
            sub_rules = []
            for r in c.get("rules", []):
                sub_rules.append(
                    f"{r.get('field')} {r.get('operator')} {r.get('value', '')}".strip()
                )
            cond_lines.append(f"({logic_op.join(sub_rules)})")
        else:
            unite = f" {c.get('unit')}" if "unit" in c else ""
            cond_lines.append(
                f"{c.get('field')} {c.get('operator')} {c.get('value', '')}{unite}".strip()
            )

    markup += "```\n"
    markup += "\n AND \n".join(cond_lines) + "\n"
    markup += "```\n\n"
    markup += "<hr>\n\n"

    # --- EXCLUSIONS ---
    markup += f"<h2 style='color: {bleu_conf};'>🚫 Exclusions</h2>\n\n"
    markup += "Certaines ressources sont volontairement ignorées :\n\n"

    exclusions = data.get("exclusions", [])
    if exclusions:
        for idx, exc in enumerate(exclusions, 1):
            reason = exc.get("reason", "Aucune raison spécifiée")
            markup += f"<h4 style='color: {bleu_conf};'>{idx}. {reason}</h4>\n\n"
            markup += f"* **Champ :** `{exc.get('field', '-')}`\n"
            markup += (
                f"* **Condition :** {exc.get('operator', '-')} `{exc.get('value', 'isNotNull')}`\n"
            )
            markup += f"* **Raison :** {reason}\n\n"
    else:
        markup += "_Aucune exclusion configurée pour cette règle._\n\n"
    markup += "<hr>\n\n"

    # --- ENRICHISSEMENT DES DONNÉES ---
    markup += f"<h2 style='color: {bleu_conf};'>📊 Enrichissement des données</h2>\n\n"

    enrichment = data.get("enrichment", {})

    markup += f"<h3 style='color: {bleu_conf};'>💰 Estimation des coûts</h3>\n\n"
    markup += f"* Métrique : {enrichment.get('costEstimate', 'N/A')}\n\n"

    markup += f"<h3 style='color: {bleu_conf};'>📋 Champs supplémentaires collectés</h3>\n\n"
    fields = enrichment.get("fields", [])
    if fields:
        for f in fields:
            markup += f"* {f}\n"
    else:
        markup += "* Aucun champ supplémentaire collecté.\n"
    markup += "\n<hr>\n\n"

    # --- IMPACT ---
    markup += f"<h2 style='color: {bleu_conf};'>⚠️ Impact</h2>\n\n"
    markup += f"Une ressource spécifiée comme `{data.get('id')}` vide entraîne un **coût inutile de compute réservé**, même en l'absence d'application déployée ou d'usage réel.\n\n"
    markup += "<hr>\n\n"

    # --- RECOMMANDATION ---
    markup += f"<h2 style='color: {bleu_conf};'>💡 Recommandation</h2>\n\n"
    reco = data.get("recommendation", {})

    markup += f"<h3 style='color: {bleu_conf};'>🛠️ Action recommandée</h3>\n\n"
    markup += f"* ➡️ {reco.get('description', 'Aucune action spécifiée.')}\n\n"

    markup += f"<h3 style='color: {bleu_conf};'>📄 Détails</h3>\n\n"
    markup += f"* L'action automatisée requise est le nettoyage de type : *{str(reco.get('action', 'N/A')).upper()}*\n"
    markup += "* Optimisation directe des coûts cloud Azure.\n\n"

    risk = str(reco.get("risk", "medium")).lower()
    risk_display = (
        "🟢 Low" if risk == "low" else "🔴 High" if risk == "high" else "🟡 Medium"
    )
    markup += f"<h3 style='color: {bleu_conf};'>⚖️ Niveau de risque</h3>\n\n* {risk_display}\n\n"

    markup += f"<h3 style='color: {bleu_conf};'>💸 Économies potentielles</h3>\n\n"
    markup += (
        f"* Économies estimées : *{reco.get('savings', '100%')} des coûts associés*\n"
    )

    return markup


# =====================================================================
# PARTIE 2 : L'INTERFACE GRAPHIQUE (Streamlit)
# =====================================================================
st.set_page_config(page_title="ENGIE FinOps Converter", layout="wide", page_icon="☁️")

st.title("☁️ ENGIE FinOps – Convertisseur JSON vers Confluence")
st.write("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Dépose ton fichier JSON")
    fichier_uploade = st.file_uploader(
        "Glisse ton fichier .json ici :", type=["json"]
    )

    if fichier_uploade is not None:
        valeur_zone_texte = fichier_uploade.read().decode("utf-8")
    else:
        valeur_zone_texte = """{
  "id": "image_orphan",
  "name": "ENGIE-Azure-Image-Orphan",
  "title": "Image VM orpheline (source VM supprimée)",
  "category": "waste",
  "description": "Détecte les images de VM Azure dont la VM source a été supprimée.",
  "scope": "Microsoft.Compute/images",
  "conditions": [{ "field": "sourceVirtualMachineExists", "operator": "equals", "value": false }],
  "exclusions": [],
  "enrichment": { "costEstimate": "lastMonthCost", "fields": ["properties.timeCreated"] },
  "severity": "medium",
  "recommendation": { "action": "delete", "description": "Supprimer l'image VM.", "risk": "medium", "savings": "100%" }
}"""

    zone_texte_json = st.text_area(
        label="Code source JSON de la règle :",
        value=valeur_zone_texte,
        height=500,
    )

with col2:
    st.subheader("2. Récupère ta fiche Confluence")

    if st.button("Générer la fiche", type="primary"):
        try:
            dictionnaire_json = json.loads(zone_texte_json)
            code_confluence = generer_format_confluence(dictionnaire_json)

            st.success("✅ Fiche générée avec succès !")
            
            st.write("###Option 1 : Copier le rendu visuel (Recommandé)")
            st.info("💡 **Comment faire ?** Sélectionne tout le texte dans le cadre ci-dessous, fais `Ctrl+C` et colle avec `Ctrl+V` dans Confluence. Les titres seront parfaitement bleus !")
            
            # Le paramètre unsafe_allow_html=True permet d'interpréter notre code couleur HTML
            with st.container(border=True):
                st.markdown(code_confluence, unsafe_allow_html=True)

            st.write("---")
            st.write("### 💻 Option 2 : Code source (Alternative)")
            st.write("Si besoin du code brut pour l'insérer avec la commande `/html` de Confluence :")
            st.code(code_confluence, language="html")

        except json.JSONDecodeError as e:
            st.error(f"❌ Erreur de syntaxe JSON : {e}")
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul : {e}")