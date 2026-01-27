"""
Dashboard Interactif E-commerce - Streamlit 
Auteur: Samir NZAMBA
Date: Janvier 2026
Version: 2.0
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuration de la page
st.set_page_config(
    page_title="Dashboard E-commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Dashboard E-commerce - Analyse DPIA 1 2025"
    }
)

# CSS personnalisé pour améliorer le design
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 4px solid #667eea;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Titre avec style
st.markdown('<h1 class="main-header">📊 Dashboard E-commerce</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Auteur: Samir NZAMBA | Projet DPIA 1 2026 | L\'École Multimédia</p>', unsafe_allow_html=True)
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    """Charge toutes les données nécessaires"""
    try:
        kpis = pd.read_csv('data/processed/kpis_summary.csv')
        daily = pd.read_csv('data/processed/daily_kpis.csv')
        daily['date'] = pd.to_datetime(daily['date'])
        hourly = pd.read_csv('data/processed/hourly_analysis.csv')
        products = pd.read_csv('data/processed/top_products.csv')
        ab_tests = pd.read_csv('data/processed/ab_tests_results.csv')
        return kpis, daily, hourly, products, ab_tests
    except Exception as e:
        st.error(f"❌ Erreur de chargement des données : {e}")
        return None, None, None, None, None

# Chargement
kpis, daily_kpis, hourly, products, ab_tests = load_data()

# Sidebar - Navigation 
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)
st.sidebar.title("🎛️ Panneau de Contrôle")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📑 **Sections**",
    ["🏠 Vue d'ensemble", "📈 Analyse Temporelle", "🛍️ Produits", "👥 Segmentation", "🧪 A/B Tests"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Filtres globaux
if daily_kpis is not None:
    st.sidebar.subheader("🔍 Filtres")
    
    # Filtre date
    date_min = daily_kpis['date'].min()
    date_max = daily_kpis['date'].max()
    
    date_range = st.sidebar.date_input(
        "📅 Période",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )
    
    if len(date_range) == 2:
        daily_kpis_filtered = daily_kpis[
            (daily_kpis['date'] >= pd.Timestamp(date_range[0])) & 
            (daily_kpis['date'] <= pd.Timestamp(date_range[1]))
        ]
    else:
        daily_kpis_filtered = daily_kpis
else:
    daily_kpis_filtered = daily_kpis

st.sidebar.markdown("---")
st.sidebar.info("""
💡 **Astuce :** Utilisez les filtres pour affiner votre analyse par période.
""")

# ==================== PAGE 1 : VUE D'ENSEMBLE ====================
if page == "🏠 Vue d'ensemble":
    st.header("🏠 Vue d'ensemble des Performances")
    
    if kpis is not None:
        # KPIs en colonnes avec design amélioré
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                label="📊 Événements",
                value=f"{kpis['total_events'].iloc[0]/1e6:.2f}M",
                delta="Total",
                help="Nombre total d'événements"
            )
        
        with col2:
            st.metric(
                label="👥 Visiteurs",
                value=f"{kpis['total_visitors'].iloc[0]/1e6:.2f}M",
                delta="Uniques",
                help="Visiteurs uniques"
            )
        
        with col3:
            st.metric(
                label="💰 Transactions",
                value=f"{kpis['total_transactions'].iloc[0]:,.0f}",
                delta=f"{kpis['conversion_rate_view_to_purchase'].iloc[0]:.2f}%",
                help="Nombre total d'achats"
            )
        
        with col4:
            st.metric(
                label="🛒 Conv. Panier",
                value=f"{kpis['conversion_rate_cart_to_purchase'].iloc[0]:.2f}%",
                delta="-67.6% vs normal",
                delta_color="inverse",
                help="Panier → Achat"
            )
        
        with col5:
            st.metric(
                label="🎯 Conv. Globale",
                value=f"{kpis['conversion_rate_view_to_purchase'].iloc[0]:.2f}%",
                delta="Référence",
                help="Vue → Achat"
            )
        
        st.markdown("---")
        
        # Graphiques principaux
        col_a, col_b = st.columns([2, 2])
        
        with col_a:
            st.subheader("📊 Funnel de Conversion")
            
            funnel_data = pd.DataFrame({
                'Étape': ['👁️ Vues', '🛒 Panier', '💰 Achats'],
                'Nombre': [
                    kpis['total_views'].iloc[0],
                    kpis['total_addtocart'].iloc[0],
                    kpis['total_transactions'].iloc[0]
                ]
            })
            
            fig_funnel = go.Figure(go.Funnel(
                y=funnel_data['Étape'],
                x=funnel_data['Nombre'],
                textposition="inside",
                textinfo="value+percent initial",
                marker=dict(
                    color=['#667eea', '#f093fb', '#4facfe'],
                    line=dict(width=2, color='white')
                )
            ))
            
            fig_funnel.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_funnel, use_container_width=True)
        
        with col_b:
            st.subheader("📈 Répartition des Événements")
            
            event_data = pd.DataFrame({
                'Événement': ['Vues', 'Panier', 'Achats'],
                'Nombre': [
                    kpis['total_views'].iloc[0],
                    kpis['total_addtocart'].iloc[0],
                    kpis['total_transactions'].iloc[0]
                ]
            })
            
            fig_pie = px.pie(
                event_data,
                values='Nombre',
                names='Événement',
                hole=0.4,
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
            )
            
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown("---")
        
        # Insights
        col_i1, col_i2, col_i3 = st.columns(3)
        
        with col_i1:
            st.success("""
            **✅ Conversion Normal**  
            Le taux de 0.84% est standard (1-3%)
            """)
        
        with col_i2:
            st.warning("""
            **⚠️ Abandon Élevé**  
            67.6% > 60-70% cible. Simplifier checkout
            """)
        
        with col_i3:
            st.error("""
            **🔴 Engagement Faible**  
            97.2% visiteurs passifs. Améliorer CTR
            """)

# ==================== PAGE 2 : ANALYSE TEMPORELLE ====================
elif page == "📈 Analyse Temporelle":
    st.header("📈 Analyse Temporelle")
    
    if daily_kpis_filtered is not None and hourly is not None:
        
        # Tendance avec sélection de métrique
        st.subheader("📅 Évolution des Métriques")
        
        col_metric, col_chart = st.columns([1, 4])
        
        with col_metric:
            metric_choice = st.radio(
                "Métrique :",
                ["Toutes", "Vues", "Panier", "Achats"]
            )
        
        with col_chart:
            fig_daily = go.Figure()
            
            if metric_choice in ["Toutes", "Vues"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_kpis_filtered['date'],
                    y=daily_kpis_filtered['view'],
                    name='Vues',
                    line=dict(color='#667eea', width=3),
                    fill='tonexty',
                    fillcolor='rgba(102, 126, 234, 0.1)'
                ))
            
            if metric_choice in ["Toutes", "Panier"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_kpis_filtered['date'],
                    y=daily_kpis_filtered['addtocart'],
                    name='Panier',
                    line=dict(color='#f093fb', width=3),
                    fill='tonexty'
                ))
            
            if metric_choice in ["Toutes", "Achats"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_kpis_filtered['date'],
                    y=daily_kpis_filtered['transaction'],
                    name='Achats',
                    line=dict(color='#4facfe', width=3),
                    fill='tonexty'
                ))
            
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title="Nombre",
                hovermode='x unified',
                height=450,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            
            st.plotly_chart(fig_daily, use_container_width=True)
        
        st.markdown("---")
        
        # Activité horaire
        st.subheader("🕐 Profil Horaire")
        
        fig_hourly = go.Figure()
        
        if 'view' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['view'],
                name='Vues',
                mode='lines+markers',
                line=dict(color='#667eea', width=4),
                marker=dict(size=8)
            ))
        
        if 'addtocart' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['addtocart'],
                name='Panier',
                mode='lines+markers',
                line=dict(color='#f093fb', width=4)
            ))
        
        if 'transaction' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['transaction'],
                name='Achats',
                mode='lines+markers',
                line=dict(color='#4facfe', width=4)
            ))
        
        # Ajouter pic d'activité
        peak_hour = hourly.loc[hourly['view'].idxmax(), 'hour'] if 'view' in hourly.columns else None
        
        if peak_hour is not None:
            fig_hourly.add_annotation(
                x=peak_hour,
                y=hourly.loc[hourly['view'].idxmax(), 'view'],
                text="🔥 Pic d'activité",
                showarrow=True,
                arrowhead=2
            )
        
        fig_hourly.update_layout(
            xaxis_title="Heure",
            yaxis_title="Nombre",
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_hourly, use_container_width=True)
        
        col_r1, col_r2 = st.columns(2)
        
        with col_r1:
            st.success("**⏰ Meilleurs créneaux :** 17h-21h")
        
        with col_r2:
            st.warning("**😴 Heures creuses :** 9h-11h")

# ==================== PAGE 3 : PRODUITS ====================
elif page == "🛍️ Produits":
    st.header("🛍️ Analyse Produits")
    
    if products is not None:
        
        # Sélecteur de tri
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        
        with col_s1:
            st.subheader("🏆 Top Produits")
        
        with col_s2:
            sort_by = st.selectbox(
                "Trier par :",
                ["Vues", "Achats", "Conversion"]
            )
        
        with col_s3:
            top_n = st.slider("Nombre", 5, 20, 10)
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("**📊 Top Produits les Plus Vus**")
            
            top_viewed = products.nlargest(top_n, 'views')
            
            fig_viewed = px.bar(
                top_viewed,
                x='views',
                y='itemid',
                orientation='h',
                color='views',
                color_continuous_scale='Blues',
                labels={'views': 'Vues', 'itemid': 'Produit'},
                text='views'
            )
            
            fig_viewed.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_viewed.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_viewed, use_container_width=True)
        
        with col_p2:
            st.markdown("**💰 Top Produits les Plus Achetés**")
            
            top_purchased = products.nlargest(top_n, 'purchases')
            
            fig_purchased = px.bar(
                top_purchased,
                x='purchases',
                y='itemid',
                orientation='h',
                color='purchases',
                color_continuous_scale='Reds',
                labels={'purchases': 'Achats', 'itemid': 'Produit'},
                text='purchases'
            )
            
            fig_purchased.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_purchased.update_layout(height=450, showlegend=False, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_purchased, use_container_width=True)
        
        st.markdown("---")
        
        # Analyse conversion
        st.subheader("📊 Matrice Vues vs Conversion")
        
        products_clean = products[
            (products['views'] >= 50) & 
            (products['purchases'].notna()) & 
            (products['purchases'] > 0)
        ].copy()
        
        if len(products_clean) > 0:
            fig_scatter = px.scatter(
                products_clean,
                x='views',
                y='conversion_rate',
                size='purchases',
                color='conversion_rate',
                color_continuous_scale='RdYlGn',
                labels={'views': 'Vues', 'conversion_rate': 'Conv. (%)', 'purchases': 'Achats'},
                log_x=True,
                hover_data=['itemid', 'views', 'purchases', 'conversion_rate'],
                size_max=50
            )
            
            avg_conversion = products_clean['conversion_rate'].mean()
            fig_scatter.add_hline(
                y=avg_conversion,
                line_dash="dash",
                line_color="orange",
                annotation_text=f"Moyenne: {avg_conversion:.2f}%"
            )
            
            fig_scatter.update_layout(height=550, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_scatter, use_container_width=True)

# ==================== PAGE 4 : SEGMENTATION (NOUVEAU) ====================
elif page == "👥 Segmentation":
    st.header("👥 Segmentation des Utilisateurs")
    
    if kpis is not None:
        # Stats de segmentation
        col_seg1, col_seg2, col_seg3 = st.columns(3)
        
        with col_seg1:
            st.metric("💰 Acheteurs", "23.8K", "+12% vs mois")
        
        with col_seg2:
            st.metric("🛒 Paniers Abandonnés", "1.6M", "-5% vs mois")
        
        with col_seg3:
            st.metric("👁️ Visiteurs Passifs", "1.4M", "97.2%")
        
        st.markdown("---")
        
        # Visualisations
        col_seg_v1, col_seg_v2 = st.columns(2)
        
        with col_seg_v1:
            st.subheader("📊 Répartition des Segments")
            
            segment_data = pd.DataFrame({
                'Segment': ['Acheteurs', 'Panier Abandonné', 'Visiteurs Passifs'],
                'Count': [23800, 1600000, 1400000]
            })
            
            fig_seg_pie = px.pie(
                segment_data,
                values='Count',
                names='Segment',
                hole=0.5,
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
            )
            
            fig_seg_pie.update_traces(textposition='inside', textinfo='percent+label')
            fig_seg_pie.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_seg_pie, use_container_width=True)
        
        with col_seg_v2:
            st.subheader("📈 Comportement par Segment")
            
            behavior_data = pd.DataFrame({
                'Segment': ['Acheteurs', 'Panier Abandonné', 'Passifs'],
                'Vues Moy.': [47.2, 15.3, 1.2],
                'Panier Moy.': [2.1, 1.0, 0.0],
                'Achats Moy.': [1.0, 0.0, 0.0]
            })
            
            fig_behavior = px.bar(
                behavior_data.melt(id_vars='Segment'),
                x='Segment',
                y='value',
                color='variable',
                barmode='group',
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe'],
                labels={'value': 'Moyenne', 'variable': 'Action'}
            )
            
            fig_behavior.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20))
            st.plotly_chart(fig_behavior, use_container_width=True)

# ==================== PAGE 5 : A/B TESTS ====================
elif page == "🧪 A/B Tests":
    st.header("🧪 Résultats des A/B Tests")
    
    if ab_tests is not None:
        
        st.subheader("📋 Résumé des Tests")
        
        # Afficher les tests avec design amélioré
        for idx, row in ab_tests.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### 🔬 {row['Test']}")
                st.write(f"**Contrôle (A):** {row['Groupe_A']}")
                st.write(f"**Variante (B):** {row['Groupe_B']}")
            
            with col2:
                improvement = float(row['Amélioration'].rstrip('%'))
                if improvement > 0:
                    st.success(f"📈 **+{row['Amélioration']}**")
                else:
                    st.error(f"📉 **{row['Amélioration']}**")
                
                st.write(f"**P-value:** {row['P_value']}")
            
            with col3:
                if row['Significatif'] == '✅ Oui':
                    st.success(f"**{row['Recommandation']}**")
                else:
                    st.warning("❌ Non-significatif")
            
            st.markdown("---")
        
        st.dataframe(ab_tests, use_container_width=True, hide_index=True)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Dashboard Info
**Version:** 2.0  
**Projet:** DPIA 1 2026  
**École:** L'École Multimédia  
**Auteur:** Samir NZAMBA

🔗 [GitHub](https://github.com/SNZAMBA65/ecommerce-analysis)
""")

st.sidebar.divider()
st.sidebar.caption(f"📅 Dernier MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# Footer principal
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; font-size: 0.85rem; margin-top: 2rem;'>
    <p>
    📊 Dashboard E-commerce v2.0 | 
    👤 Samir NZAMBA | 
    🎓 L'École Multimédia - DPIA 1 2026
    </p>
</div>
""", unsafe_allow_html=True)