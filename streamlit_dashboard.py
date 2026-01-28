"""
Dashboard Interactif E-commerce - Streamlit 
Auteur: Samir NZAMBA
Date: Janvier 2025
Version: 2.1 - Données 100% réelles
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

# CSS personnalisé
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
</style>
""", unsafe_allow_html=True)

# Titre
st.markdown('<h1 class="main-header">📊 Dashboard E-commerce</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Auteur: Samir NZAMBA | Projet DPIA 1 2025 | L\'École Multimédia</p>', unsafe_allow_html=True)
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
        events_sample = pd.read_csv('data/processed/events_for_tableau.csv')
        return kpis, daily, hourly, products, ab_tests, events_sample
    except Exception as e:
        st.error(f"❌ Erreur de chargement des données : {e}")
        return None, None, None, None, None, None

# Chargement
kpis, daily_kpis, hourly, products, ab_tests, events_sample = load_data()

# Sidebar
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)
st.sidebar.title("🎛️ Panneau de Contrôle")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "📑 **Sections**",
    ["🏠 Vue d'ensemble", "📈 Analyse Temporelle", "🛍️ Produits", "👥 Segmentation", "🧪 A/B Tests"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")

# Filtres
if daily_kpis is not None:
    st.sidebar.subheader("🔍 Filtres")
    
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
st.sidebar.info("💡 Utilisez les filtres pour affiner l'analyse.")

# ==================== PAGE 1 : VUE D'ENSEMBLE ====================
if page == "🏠 Vue d'ensemble":
    st.header("🏠 Vue d'ensemble des Performances")
    
    if kpis is not None:
        # Calcul du taux d'abandon réel
        abandon_rate = 100 - kpis['conversion_rate_cart_to_purchase'].iloc[0]
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "📊 Événements",
                f"{kpis['total_events'].iloc[0]/1e6:.2f}M",
                help="Nombre total d'événements sur la période"
            )
        
        with col2:
            st.metric(
                "👥 Visiteurs",
                f"{kpis['total_visitors'].iloc[0]/1e6:.2f}M",
                help="Visiteurs uniques"
            )
        
        with col3:
            st.metric(
                "💰 Transactions",
                f"{kpis['total_transactions'].iloc[0]:,.0f}",
                f"{kpis['conversion_rate_view_to_purchase'].iloc[0]:.2f}%",
                help="Nombre total d'achats"
            )
        
        with col4:
            st.metric(
                "🛒 Conv. Panier",
                f"{kpis['conversion_rate_cart_to_purchase'].iloc[0]:.2f}%",
                f"-{abandon_rate:.1f}% abandon",
                delta_color="inverse",
                help="Taux de conversion panier → achat"
            )
        
        with col5:
            st.metric(
                "🎯 Conv. Globale",
                f"{kpis['conversion_rate_view_to_purchase'].iloc[0]:.2f}%",
                help="Taux de conversion vue → achat"
            )
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
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
            
            fig_funnel.update_layout(height=400)
            st.plotly_chart(fig_funnel, width='stretch')
        
        with col_b:
            st.subheader("📈 Répartition Événements")
            
            event_data = pd.DataFrame({
                'Type': ['Vues', 'Panier', 'Achats'],
                'Nombre': [
                    kpis['total_views'].iloc[0],
                    kpis['total_addtocart'].iloc[0],
                    kpis['total_transactions'].iloc[0]
                ]
            })
            
            fig_pie = px.pie(
                event_data,
                values='Nombre',
                names='Type',
                hole=0.4,
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
            )
            
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>%{value:,.0f}<br>%{percent}'
            )
            
            fig_pie.update_layout(height=400)
            st.plotly_chart(fig_pie, width='stretch')
        
        st.markdown("---")
        
        # Insights basés sur les VRAIES données
        col_i1, col_i2, col_i3 = st.columns(3)
        
        conv_rate = kpis['conversion_rate_view_to_purchase'].iloc[0]
        cart_conv = kpis['conversion_rate_cart_to_purchase'].iloc[0]
        
        with col_i1:
            if 0.8 <= conv_rate <= 3.0:
                st.success(f"✅ **Conversion normale** : {conv_rate:.2f}% (1-3% standard)")
            else:
                st.warning(f"⚠️ **Conversion à surveiller** : {conv_rate:.2f}%")
        
        with col_i2:
            if cart_conv < 40:
                st.warning(f"⚠️ **Abandon élevé** : {abandon_rate:.1f}% (cible <60%)")
            else:
                st.success(f"✅ **Abandon maîtrisé** : {abandon_rate:.1f}%")
        
        with col_i3:
            # Calculer le % de visiteurs engagés depuis les KPIs
            visitors_engaged_pct = ((kpis['total_addtocart'].iloc[0] + kpis['total_transactions'].iloc[0]) / kpis['total_visitors'].iloc[0]) * 100
            if visitors_engaged_pct < 5:
                st.error(f"🔴 **Engagement faible** : {100-visitors_engaged_pct:.1f}% passifs")
            else:
                st.success(f"✅ **Engagement correct** : {visitors_engaged_pct:.1f}% actifs")

# ==================== PAGE 2 : ANALYSE TEMPORELLE ====================
elif page == "📈 Analyse Temporelle":
    st.header("📈 Analyse Temporelle")
    
    if daily_kpis_filtered is not None and hourly is not None:
        
        st.subheader("📅 Évolution Quotidienne")
        
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
                    hovertemplate='<b>%{x}</b><br>Vues: %{y:,.0f}<extra></extra>'
                ))
            
            if metric_choice in ["Toutes", "Panier"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_kpis_filtered['date'],
                    y=daily_kpis_filtered['addtocart'],
                    name='Panier',
                    line=dict(color='#f093fb', width=3),
                    hovertemplate='<b>%{x}</b><br>Panier: %{y:,.0f}<extra></extra>'
                ))
            
            if metric_choice in ["Toutes", "Achats"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_kpis_filtered['date'],
                    y=daily_kpis_filtered['transaction'],
                    name='Achats',
                    line=dict(color='#4facfe', width=3),
                    hovertemplate='<b>%{x}</b><br>Achats: %{y:,.0f}<extra></extra>'
                ))
            
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title="Nombre d'événements",
                hovermode='x unified',
                height=450
            )
            
            st.plotly_chart(fig_daily, width='stretch')
        
        st.markdown("---")
        
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
                line=dict(color='#f093fb', width=4),
                marker=dict(size=8)
            ))
        
        if 'transaction' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['transaction'],
                name='Achats',
                mode='lines+markers',
                line=dict(color='#4facfe', width=4),
                marker=dict(size=8)
            ))
        
        # Annotation sur le pic d'activité (DONNÉES RÉELLES)
        if 'view' in hourly.columns:
            peak_hour = hourly.loc[hourly['view'].idxmax(), 'hour']
            peak_value = hourly['view'].max()
            
            fig_hourly.add_annotation(
                x=peak_hour,
                y=peak_value,
                text=f"🔥 Pic : {peak_hour}h",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#e74c3c",
                font=dict(size=14, color='#e74c3c'),
                bgcolor="rgba(255,255,255,0.8)"
            )
        
        fig_hourly.update_layout(
            xaxis_title="Heure de la journée",
            yaxis_title="Nombre d'événements",
            xaxis=dict(tickmode='linear', tick0=0, dtick=2),
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig_hourly, width='stretch')
        
        # Recommandations basées sur VRAIES données
        if 'view' in hourly.columns:
            # Top 3 heures
            top_hours = hourly.nlargest(3, 'view')['hour'].tolist()
            # Bottom 3 heures
            low_hours = hourly.nsmallest(3, 'view')['hour'].tolist()
            
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                st.success(f"⏰ **Meilleurs créneaux :** {top_hours[0]}h-{top_hours[-1]}h")
            
            with col_r2:
                st.warning(f"😴 **Heures creuses :** {low_hours[0]}h-{low_hours[-1]}h")

# ==================== PAGE 3 : PRODUITS ====================
elif page == "🛍️ Produits":
    st.header("🛍️ Analyse Produits")
    
    if products is not None:
        
        col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
        
        with col_s1:
            st.subheader("🏆 Top Produits")
        
        with col_s2:
            sort_by = st.selectbox("Trier par :", ["Vues", "Achats", "Conversion"])
        
        with col_s3:
            top_n = st.slider("Nombre", 5, 20, 10)
        
        col_p1, col_p2 = st.columns(2)
        
        with col_p1:
            st.markdown("**📊 Plus Vus**")
            
            top_viewed = products.nlargest(top_n, 'views')
            
            fig_viewed = px.bar(
                top_viewed,
                x='views',
                y='itemid',
                orientation='h',
                color='views',
                color_continuous_scale='Blues',
                text='views',
                labels={'views': 'Nombre de vues', 'itemid': 'ID Produit'}
            )
            
            fig_viewed.update_traces(
                texttemplate='%{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>Produit %{y}</b><br>Vues: %{x:,.0f}<extra></extra>'
            )
            fig_viewed.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig_viewed, width='stretch')
        
        with col_p2:
            st.markdown("**💰 Plus Achetés**")
            
            top_purchased = products.nlargest(top_n, 'purchases')
            
            fig_purchased = px.bar(
                top_purchased,
                x='purchases',
                y='itemid',
                orientation='h',
                color='purchases',
                color_continuous_scale='Reds',
                text='purchases',
                labels={'purchases': 'Nombre d\'achats', 'itemid': 'ID Produit'}
            )
            
            fig_purchased.update_traces(
                texttemplate='%{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>Produit %{y}</b><br>Achats: %{x:,.0f}<extra></extra>'
            )
            fig_purchased.update_layout(height=450, showlegend=False)
            st.plotly_chart(fig_purchased, width='stretch')
        
        st.markdown("---")
        
        st.subheader("📊 Vues vs Conversion")
        
        # Filtrer produits valides
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
                log_x=True,
                size_max=50,
                labels={
                    'views': 'Nombre de vues',
                    'conversion_rate': 'Taux de conversion (%)',
                    'purchases': 'Achats'
                },
                hover_data=['itemid', 'views', 'purchases', 'conversion_rate']
            )
            
            # Ligne de moyenne RÉELLE
            avg_conversion = products_clean['conversion_rate'].mean()
            fig_scatter.add_hline(
                y=avg_conversion,
                line_dash="dash",
                line_color="orange",
                annotation_text=f"Moyenne: {avg_conversion:.2f}%",
                annotation_position="right"
            )
            
            fig_scatter.update_layout(height=550)
            st.plotly_chart(fig_scatter, width='stretch')
            
            # Stats réelles
            low_conversion_count = len(products_clean[products_clean['conversion_rate'] < 1])
            st.warning(f"⚠️ **{low_conversion_count} produits** avec forte vue mais faible conversion (<1%)")

# ==================== PAGE 4 : SEGMENTATION ====================
elif page == "👥 Segmentation":
    st.header("👥 Segmentation des Utilisateurs")
    
    if events_sample is not None:
        
        # Calculer les segments depuis les VRAIES données
        user_behavior = events_sample.groupby('visitorid').agg({
            'event': 'count',
            'itemid': 'nunique'
        }).rename(columns={'event': 'total_events', 'itemid': 'unique_products'})
        
        user_views = events_sample[events_sample['event'] == 'view'].groupby('visitorid').size()
        user_addtocart = events_sample[events_sample['event'] == 'addtocart'].groupby('visitorid').size()
        user_purchases = events_sample[events_sample['event'] == 'transaction'].groupby('visitorid').size()
        
        user_behavior['views'] = user_views.fillna(0)
        user_behavior['addtocart'] = user_addtocart.fillna(0)
        user_behavior['purchases'] = user_purchases.fillna(0)
        
        # Segmentation
        def categorize_user(row):
            if row['purchases'] > 0:
                return '💰 Acheteurs'
            elif row['addtocart'] > 0:
                return '🛒 Panier Abandonné'
            else:
                return '👁️ Visiteurs Passifs'
        
        user_behavior['segment'] = user_behavior.apply(categorize_user, axis=1)
        
        # Compter segments
        segment_counts = user_behavior['segment'].value_counts()
        
        # KPIs RÉELS
        col_seg1, col_seg2, col_seg3 = st.columns(3)
        
        total_users = len(user_behavior)
        
        with col_seg1:
            acheteurs = segment_counts.get('💰 Acheteurs', 0)
            pct_acheteurs = (acheteurs / total_users) * 100
            st.metric(
                "💰 Acheteurs",
                f"{acheteurs:,}",
                f"{pct_acheteurs:.1f}% des visiteurs"
            )
        
        with col_seg2:
            paniers = segment_counts.get('🛒 Panier Abandonné', 0)
            pct_paniers = (paniers / total_users) * 100
            st.metric(
                "🛒 Paniers Abandonnés",
                f"{paniers:,}",
                f"{pct_paniers:.1f}% des visiteurs"
            )
        
        with col_seg3:
            passifs = segment_counts.get('👁️ Visiteurs Passifs', 0)
            pct_passifs = (passifs / total_users) * 100
            st.metric(
                "👁️ Visiteurs Passifs",
                f"{passifs:,}",
                f"{pct_passifs:.1f}% des visiteurs"
            )
        
        st.markdown("---")
        
        # Visualisations
        col_seg_v1, col_seg_v2 = st.columns(2)
        
        with col_seg_v1:
            st.subheader("📊 Répartition des Segments")
            
            fig_seg_pie = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                hole=0.5,
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe']
            )
            
            fig_seg_pie.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>%{value:,} utilisateurs<br>%{percent}'
            )
            
            fig_seg_pie.update_layout(height=400)
            st.plotly_chart(fig_seg_pie, width='stretch')
        
        with col_seg_v2:
            st.subheader("📈 Comportement Moyen")
            
            # Moyennes RÉELLES
            segment_avg = user_behavior.groupby('segment')[['views', 'addtocart', 'purchases']].mean().reset_index()
            
            fig_seg_bar = px.bar(
                segment_avg.melt(id_vars='segment'),
                x='segment',
                y='value',
                color='variable',
                barmode='group',
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe'],
                labels={'value': 'Moyenne', 'variable': 'Action', 'segment': 'Segment'}
            )
            
            fig_seg_bar.update_layout(height=400)
            st.plotly_chart(fig_seg_bar, width='stretch')
        
        st.markdown("---")
        
        # Stats détaillées RÉELLES
        st.subheader("📋 Statistiques Détaillées")
        
        for segment_name in segment_counts.index:
            segment_data = user_behavior[user_behavior['segment'] == segment_name]
            segment_count = len(segment_data)
            segment_pct = (segment_count / total_users) * 100
            
            with st.expander(f"{segment_name} ({segment_count:,} utilisateurs - {segment_pct:.1f}%)"):
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric("Vues moy.", f"{segment_data['views'].mean():.1f}")
                
                with col_stat2:
                    st.metric("Produits vus", f"{segment_data['unique_products'].mean():.1f}")
                
                with col_stat3:
                    st.metric("Panier moy.", f"{segment_data['addtocart'].mean():.1f}")
                
                with col_stat4:
                    st.metric("Achats moy.", f"{segment_data['purchases'].mean():.1f}")

# ==================== PAGE 5 : A/B TESTS ====================
elif page == "🧪 A/B Tests":
    st.header("🧪 Résultats A/B Tests")
    
    if ab_tests is not None:
        
        # Vue d'ensemble
        col_overview1, col_overview2, col_overview3 = st.columns(3)
        
        with col_overview1:
            st.metric("Tests Réalisés", len(ab_tests))
        
        with col_overview2:
            significant_count = len(ab_tests[ab_tests['Significatif'] == '✅ Oui'])
            st.metric("Tests Significatifs", f"{significant_count}/{len(ab_tests)}")
        
        with col_overview3:
            # Calculer amélioration moyenne RÉELLE
            improvements = ab_tests['Amélioration'].str.rstrip('%').astype(float)
            avg_improvement = improvements.mean()
            st.metric("Amélioration Moy.", f"+{avg_improvement:.0f}%")
        
        st.markdown("---")
        
        st.subheader("📋 Détail des Tests")
        
        for idx, row in ab_tests.iterrows():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"### {row['Test']}")
                st.write(f"**Métrique :** {row['Métrique']}")
                st.write(f"**Contrôle (A) :** {row['Groupe_A']}")
                st.write(f"**Variante (B) :** {row['Groupe_B']}")
            
            with col2:
                improvement_val = float(row['Amélioration'].rstrip('%'))
                if improvement_val > 0:
                    st.success(f"📈 **{row['Amélioration']}**")
                else:
                    st.error(f"📉 **{row['Amélioration']}**")
                
                st.write(f"**P-value :** {row['P_value']}")
                st.write(f"**Significatif :** {row['Significatif']}")
            
            with col3:
                if row['Significatif'] == '✅ Oui':
                    st.success(f"✅ **{row['Recommandation']}**")
                else:
                    st.warning("❌ Non significatif")
            
            st.markdown("---")
        
        # Tableau récapitulatif
        st.subheader("📊 Tableau Récapitulatif")
        st.dataframe(ab_tests, width='stretch', hide_index=True)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
### 📊 Dashboard Info
**Version:** 2.1  
**Projet:** DPIA 1 2025  
**École:** L'École Multimédia  
**Auteur:** Samir NZAMBA

🔗 [GitHub](https://github.com/SNZAMBA65/ecommerce-analysis)
""")

st.sidebar.caption(f"📅 MAJ: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #6c757d; font-size: 0.85rem;'>
    📊 Dashboard E-commerce v2.1 | Samir NZAMBA | L'École Multimédia - DPIA 1 2025
</div>
""", unsafe_allow_html=True)