# pyblocks_data/lego_blocks/__init__.py

# -------------------------------
# IMPORTAR TODOS LOS MÓDULOS
# -------------------------------
from .load_data import render as load_data
from .comparar_bases import render as comparar_bases
from .conciliacion import render as conciliacion
from .eda_sweetviz import render as eda_sweetviz
from .nlp_analysis import render as nlp_analysis
from .series_temporales import render as series_temporales
from .pronostico import render as pronostico
from .evaluacion_modelos import render as evaluacion_modelos
from .export_project import render as export_project
from .project_summary import render as project_summary
from .chatbot_llm import render as chatbot_llm
from .basic_stats import render as basic_stats
from .missing_values import render as handle_missing_values
from .visualizations import render as visualizations
from .modelo_comparador import render as model_comparator
from .transformations import render as transformaciones
from .feature_enggineiring import render as ingenieria_variables
from .PCA_dimensionality import render as reduccion_dimensionalidad
from .variable_selector import render as seleccion_variables
from .modeling import render as modelado
from .clustering import render as clustering
from .outlier_detection import render as deteccion_outliers
from .estadistica_inferencial import render as estadistica_inferencial
from .correlation_analysis import render as analisis_correlacion

# -------------------------------
# BLOQUE MINI-ALADIN
# -------------------------------
from .mini_aladin import render as mini_aladin

# -------------------------------
# BLOQUES DICT AUTOMÁTICO
# -------------------------------
bloques_dict = {
    # Datos
    "📁 Cargar Datos": load_data,
    "🧹 Manejo de Nulos": handle_missing_values,
    "📊 Estadísticas Básicas": basic_stats,
    "📊 Estadística Inferencial Completa": estadistica_inferencial,
    "📈 Visualizaciones": visualizations,
    "📋 EDA Sweetviz": eda_sweetviz,
    "🆚 Comparar Bases": comparar_bases,
    "📑 Conciliación": conciliacion,
    
    # Machine Learning
    "🔄 Transformaciones": transformaciones,
    "🏗️ Ingeniería de Variables": ingenieria_variables,
    "🧬 Reducción de Dimensionalidad": reduccion_dimensionalidad,
    "🎯 Selección de Variables + Preprocesamiento": seleccion_variables,
    "🧠 Modelado": modelado,
    "📊 Comparador de Modelos": model_comparator,
    "🧪 Evaluación de Modelos": evaluacion_modelos,
    "🌐 Clustering": clustering,
    "🚨 Detección Avanzada de Outliers y Anomalías": deteccion_outliers,
    
    # Series Temporales
    "⏳ Series Temporales": series_temporales,
    "📆 Pronóstico": pronostico,
    
    # Análisis Avanzado
    "📝 Análisis de Texto": nlp_analysis,
    "📌 Análisis de Correlación": analisis_correlacion,
    
    # Proyecto
    "🧾 Resumen del Proyecto": project_summary,
    "🤖 Chatbot Analítico con LLM": chatbot_llm,
    "📤 Exportar Proyecto": export_project,
    
    # Mini-Aladin
    "🧞 Mini-Aladin": mini_aladin
}






