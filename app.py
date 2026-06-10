import json
import streamlit as st


# =====================================================================
# PARTIE 1 : L'ALGORITHME (Format Markdown Moderne pour Confluence)
# =====================================================================
def generer_format_confluence(data):
    """
    Génère le code au format Markdown.
    Lors du copier-coller direct sur Confluence Cloud, il se transforme
    automatiquement en titres bleus, tableaux et sections propres.
    """
    markup = ""

    # --- TITRE PRINCIPAL ---
    titre = data.get("title", data.get("name", "Règle sans titre"))
    markup += f"# ENGIE – Détection : {titre}\n"
    markup += "---\n\n"

    # --- INFORMATIONS GÉNÉRALES ---
    markup += "## 📌 Informations générales\n\n"

    # Gestion de la couleur pour la sévérité
    sev = str(data.get("severity", "medium")).lower()
    if sev == "high":
        sev_display = "🔴 High"
    elif sev == "low":
        sev_display = "🟢 Low"
    else:
        sev_display = "🟡 Medium"

    # Tableau au format Markdown standard
    markup += "| Élément | Détails |\n"
    markup += "| --- | --- |\n"
    markup += f"| **ID** | {data.get('id', '-')} |\n"
    markup += f"| **Nom** | {data.get('name', '-')} |\n"
    markup += f"| **Titre** | {titre} |\n"
    markup += f"| **Catégorie** | {str(data.get('category', '-')).capitalize()} |\n"
    markup += f" | **Sévérité** | {sev_display} |\n\n"
    markup += "---\n\n"

    # --- DESCRIPTION ---
    markup += "## 📄 Description\n"
    markup += f"{data.get('description', 'Aucune description.')}\n\n"
    markup += "---\n\n"

    # --- SCOPE ---
    markup += "## 🎯 Scope\n"
    markup += "```\n"
    markup += f"{data.get('scope', '-')}\n"
    markup += "```\n\n"
    markup += "---\n\n"

    # --- CONDITIONS DE DÉTECTION ---
    markup += "## ✅ Conditions de détection\n"
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
    markup += "---\n\n"

    # --- EXCLUSIONS ---
    markup += "## 🚫 Exclusions\n"
    markup += "Certaines ressources sont volontairement ignorées :\n\n"

    exclusions = data.get("exclusions", [])
    if exclusions:
        for idx, exc in enumerate(exclusions, 1):
            reason = exc.get("reason", "Aucune raison spécifiée")
            markup += f"#### {idx}. {reason}\n"
            markup += f"* **Champ :** `{exc.get('field', '-')}`\n"
            markup += (
                f"* **Condition :** {exc.get('operator', '-')} `{exc.get('value', 'isNotNull')}`\n"
            )
            markup += f"* **Raison :** {reason}\n\n"
    else:
        markup += "_Aucune exclusion configurée pour cette règle._\n\n"
    markup += "---\n\n"

    # --- ENRICHISSEMENT DES DONNÉES ---
    markup += "## 📊 Enrichissement des données\n\n"

    enrichment = data.get("enrichment", {})

    markup += "### 💰 Estimation des coûts\n"
    markup += f"* Métrique : {enrichment.get('costEstimate', 'N/A')}\n\n"

    markup += "### 📋 Champs supplémentaires collectés\n"
    fields = enrichment.get("fields", [])
    if fields:
        for f in fields:
            markup += f"* {f}\n"
    else:
        markup += "* Aucun champ supplémentaire collecté.\n"
    markup += "\n---\n\n"

    # --- IMPACT ---
    markup += "## ⚠️ Impact\n"
    markup += f"Une ressource spécifiée comme `{data.get('id')}` vide entraîne un **coût inutile de compute réservé**, même en l'absence d'application déployée ou d'usage réel.\n\n"
    markup += "---\n\n"

    # --- RECOMMANDATION ---
    markup += "## 💡 Recommandation\n\n"
    reco = data.get("recommendation", {})

    markup += "### 🛠️ Action recommandée\n"
    markup += f"* ➡️ {reco.get('description', 'Aucune action spécifiée.')}\n\n"

    markup += "### 📄 Détails\n"
    markup += f"* L'action automatisée requise est le nettoyage de type : *{str(reco.get('action', 'N/A')).upper()}*\n"
    markup += "* Optimisation directe des coûts cloud Azure.\n\n"

    risk = str(reco.get("risk", "medium")).lower()
    risk_display = (
        "🟢 Low" if risk == "low" else "🔴 High" if risk == "high" else "🟡 Medium"
    )
    markup += f"### ⚖️ Niveau de risque\n* {risk_display}\n\n"

    markup += "### 💸 Économies potentielles\n"
    markup += (
        f"* Économies estimées : *{reco.get('savings', '100%')} des coûts associés*\n"
    )

    return markup


# =====================================================================
# PARTIE 2 : L'INTERFACE GRAPHIQUE (Streamlit)
# =====================================================================
st.set_page_config(page_title="ENGIE FinOps Blueprint Converter", layout="wide")

st.title("ENGIE FinOps – Convertisseur de Fichier Json en confluence")
st.caption(
    "Génération automatisée de fiches techniques Azure au format Markdown pour Confluence."
)
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
    st.subheader("2. Génére ton texte confluence")

    if st.button("Générer votre texte confluence", type="primary"):
        try:
            dictionnaire_json = json.loads(zone_texte_json)
            code_confluence = generer_format_confluence(dictionnaire_json)

            st.text_area(
                label="Copie ce bloc et colle-le DIRECTEMENT sur ta page Confluence :",
                value=code_confluence,
                height=420,
            )

            st.download_button(
                label="Télécharger la fiche technique (.txt)",
                data=code_confluence,
                file_name=f"Confluence_{dictionnaire_json.get('name', 'regle_finops')}.txt",
                mime="text/plain",
            )
            st.success(
                "Fiche technique prête ! Copie-colle directement dans Confluence."
            )

        except json.JSONDecodeError as e:
            st.error(f"❌ Erreur de syntaxe JSON : {e}")
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul : {e}")