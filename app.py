import json
import streamlit as st

# =====================================================================
# PARTIE 1 : L'ALGORITHME (Format HTML - Contenu Enrichi)
# =====================================================================
def generer_format_confluence(data):
    markup = ""
    bleu_conf = "#09BDEB" # Le bleu Confluence

    # --- TITRE PRINCIPAL ---
    titre = data.get("title", data.get("name", "Règle sans titre"))
    markup += f"<h1 style='color: {bleu_conf};'>ENGIE – Détection FinOps : {titre}</h1>\n"
    markup += "<p><i>Document de référence généré automatiquement pour le suivi et la gouvernance de l'infrastructure Cloud.</i></p>\n<hr>\n\n"

    # --- INFORMATIONS GÉNÉRALES ---
    markup += f"<h2 style='color: {bleu_conf};'>📌 Informations générales</h2>\n\n"
    markup += "<p>Ce tableau résume la carte d'identité de la règle de détection. Il permet aux équipes Cloud et aux Product Owners d'identifier rapidement la nature du gaspillage ciblé.</p>\n\n"

    sev = str(data.get("severity", "medium")).lower()
    if sev == "high":
        sev_display = "🔴 High (Action prioritaire)"
    elif sev == "low":
        sev_display = "🟢 Low (Optimisation de fond)"
    else:
        sev_display = "🟡 Medium (À traiter au prochain sprint)"

    markup += "| Élément | Détails |\n"
    markup += "| --- | --- |\n"
    markup += f"| **ID Unique** | {data.get('id', '-')} |\n"
    markup += f"| **Nom technique** | {data.get('name', '-')} |\n"
    markup += f"| **Catégorie FinOps** | {str(data.get('category', '-')).capitalize()} (Gaspillage / Sous-utilisation) |\n"
    markup += f"| **Sévérité / Urgence** | {sev_display} |\n\n"
    markup += "<hr>\n\n"

    # --- DESCRIPTION DÉTAILLÉE ---
    markup += f"<h2 style='color: {bleu_conf};'>📄 Description détaillée</h2>\n\n"
    markup += "<p>Dans le cadre de notre démarche d'optimisation continue (FinOps / Green IT), cette règle a été mise en place pour assainir nos environnements cloud.</p>\n"
    markup += f"<p><b>🎯 Objectif principal :</b> {data.get('description', 'Aucune description.')}</p>\n"
    markup += "<p>L'identification proactive de ces ressources permet non seulement de réduire notre facturation mensuelle Azure, mais également d'alléger la dette technique globale de notre système d'information.</p>\n\n"
    markup += "<hr>\n\n"

    # --- PÉRIMÈTRE (SCOPE) ---
    markup += f"<h2 style='color: {bleu_conf};'>🔭 Périmètre d'analyse (Scope)</h2>\n\n"
    markup += "<p>L'algorithme de détection scanne de manière continue l'architecture Cloud pour analyser spécifiquement le type de ressource suivant :</p>\n"
    markup += "```\n"
    markup += f"{data.get('scope', '-')}\n"
    markup += "```\n\n"
    markup += "<hr>\n\n"

    # --- CONDITIONS DE DÉTECTION ---
    markup += f"<h2 style='color: {bleu_conf};'>⚙️ Logique de détection</h2>\n\n"
    markup += f"<p>Une ressource appartenant au périmètre <code>{data.get('scope', 'ressource')}</code> est flagguée comme <b>non-conforme ou inutile</b> par notre moteur si elle répond strictement aux critères techniques ci-dessous :</p>\n\n"

    cond_lines = []
    for c in data.get("conditions", []):
        if "logic" in c:
            logic_op = f" {c['logic'].upper()} "
            sub_rules = []
            for r in c.get("rules", []):
                sub_rules.append(f"{r.get('field')} {r.get('operator')} {r.get('value', '')}".strip())
            cond_lines.append(f"({logic_op.join(sub_rules)})")
        else:
            unite = f" {c.get('unit')}" if "unit" in c else ""
            cond_lines.append(f"{c.get('field')} {c.get('operator')} {c.get('value', '')}{unite}".strip())

    markup += "```\n"
    markup += "\n AND \n".join(cond_lines) + "\n"
    markup += "```\n\n"
    markup += "<hr>\n\n"

    # --- EXCLUSIONS ---
    markup += f"<h2 style='color: {bleu_conf};'>🛡️ Exceptions et Exclusions</h2>\n\n"
    markup += "<p>Afin d'éviter les faux positifs et de ne pas perturber les ressources critiques de production (Business Continuity), certaines ressources sont volontairement exclues de cette politique de nettoyage :</p>\n\n"

    exclusions = data.get("exclusions", [])
    if exclusions:
        for idx, exc in enumerate(exclusions, 1):
            reason = exc.get("reason", "Raison métier non spécifiée")
            markup += f"<h4 style='color: {bleu_conf};'>Exception {idx} : {reason}</h4>\n\n"
            markup += f"<ul>\n"
            markup += f"<li><b>Critère d'exclusion :</b> Le champ <code>{exc.get('field', '-')}</code> doit valider la condition {exc.get('operator', '-')} <code>{exc.get('value', 'isNotNull')}</code>.</li>\n"
            markup += f"<li><b>Justification :</b> {reason}</li>\n"
            markup += f"</ul>\n\n"
    else:
        markup += "<p><i>Aucune exclusion n'est configurée pour cette règle. Toute ressource détectée est considérée comme éligible à la remédiation.</i></p>\n\n"
    markup += "<hr>\n\n"

    # --- IMPACT ---
    markup += f"<h2 style='color: {bleu_conf};'>⚠️ Impact Business & Écologique</h2>\n\n"
    markup += f"<p>Le maintien d'une ressource de type <code>{data.get('id')}</code> sans justification métier engendre un <b>coût inutile de compute ou de stockage réservé</b> auprès de notre fournisseur Cloud.</p>\n"
    markup += "<p>Outre l'impact financier direct sur la facture, l'accumulation de ces ressources 'orphelines' (Cloud Waste) complexifie les audits de sécurité et augmente l'empreinte carbone globale du groupe ENGIE, allant à l'encontre de nos objectifs de sobriété numérique.</p>\n\n"
    markup += "<hr>\n\n"

    # --- RECOMMANDATION & RÉSOLUTION ---
    markup += f"<h2 style='color: {bleu_conf};'>💡 Résolution et Remédiation</h2>\n\n"
    reco = data.get("recommendation", {})

    markup += f"<h3 style='color: {bleu_conf};'>🛠️ Action préconisée pour les équipes</h3>\n\n"
    markup += f"<p><b>Instruction :</b> {reco.get('description', 'Aucune action spécifiée.')}</p>\n"
    markup += f"<p>L'action requise pour assainir le système est une opération de type : <b>{str(reco.get('action', 'N/A')).upper()}</b>.</p>\n\n"

    risk = str(reco.get("risk", "medium")).lower()
    risk_display = (
        "🟢 Faible (Nettoyage sans impact sur l'applicatif)" if risk == "low" else "🔴 Élevé (Vérifier les dépendances avant action)" if risk == "high" else "🟡 Modéré (Test recommandé avant nettoyage)"
    )
    markup += f"<h3 style='color: {bleu_conf};'>⚖️ Analyse des risques opérationnels</h3>\n<p>Niveau de risque estimé de l'action de remédiation : <b>{risk_display}</b>.</p>\n\n"

    markup += f"<h3 style='color: {bleu_conf};'>💸 Gain estimé post-remédiation</h3>\n\n"
    markup += f"<p>En appliquant cette recommandation, l'équipe FinOps estime une récupération d'environ <b>{reco.get('savings', '100%')}</b> des coûts associés à cette ressource. La métrique de référence utilisée pour ce calcul est basée sur la variable : <code>{data.get('enrichment', {}).get('costEstimate', 'N/A')}</code>.</p>\n"

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
        height=600,
    )

with col2:
    st.subheader("2. Récupère ta fiche Confluence")

    if st.button("Générer la fiche détaillée", type="primary"):
        try:
            dictionnaire_json = json.loads(zone_texte_json)
            code_confluence = generer_format_confluence(dictionnaire_json)

            st.success("✅ Fiche détaillée générée avec succès !")
            
            st.write("###Copier le rendu visuel")
            st.info("💡 Sélectionne tout le texte dans le cadre ci-dessous, fais `Ctrl+C` et colle avec `Ctrl+V` dans Confluence.")
            
            with st.container(border=True):
                st.markdown(code_confluence, unsafe_allow_html=True)

        except json.JSONDecodeError as e:
            st.error(f"❌ Erreur de syntaxe JSON : {e}")
        except Exception as e:
            st.error(f"❌ Erreur lors du calcul : {e}")