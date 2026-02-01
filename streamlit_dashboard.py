"""
Dashboard E-commerce - Analyse des Performances
Auteur: Samir NZAMBA
Formation: DPIA 1 - L'École Multimédia
Date: Janvier 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# Configuration
st.set_page_config(
    page_title="Dashboard E-commerce",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style
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

# En-tête
st.markdown('<h1 class="main-header">📊 Tableau de Bord E-commerce</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Analyse des performances du site | Samir NZAMBA | L\'École Multimédia</p>', unsafe_allow_html=True)
st.markdown("---")

# Chargement des données
@st.cache_data
def load_data():
    try:
        kpis = pd.read_csv('data/processed/kpis_summary.csv')
        daily = pd.read_csv('data/processed/daily_kpis.csv')
        daily['date'] = pd.to_datetime(daily['date'])
        hourly = pd.read_csv('data/processed/hourly_analysis.csv')
        products = pd.read_csv('data/processed/top_products.csv')
        ab_tests = pd.read_csv('data/processed/ab_tests_results.csv')
        events = pd.read_csv('data/processed/events_for_tableau.csv')
        return kpis, daily, hourly, products, ab_tests, events
    except Exception as e:
        st.error(f"Erreur de chargement : {e}")
        return None, None, None, None, None, None

kpis, daily_kpis, hourly, products, ab_tests, events = load_data()

# Menu latéral
st.sidebar.image("https://img.icons8.com/fluency/96/combo-chart.png", width=80)
st.sidebar.title("Navigation")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Choisissez une section :",
    [
        "🏠 Résumé Général",
        "📅 Activité par Jour et Heure",
        "🛍️ Performance des Produits",
        "👥 Types de Visiteurs",
        "🧪 Tests d'Optimisation"
    ]
)

st.sidebar.markdown("---")

# Filtre de date
if daily_kpis is not None:
    st.sidebar.subheader("Filtrer par période")
    
    date_min = daily_kpis['date'].min()
    date_max = daily_kpis['date'].max()
    
    date_range = st.sidebar.date_input(
        "Sélectionnez les dates :",
        value=(date_min, date_max),
        min_value=date_min,
        max_value=date_max
    )
    
    if len(date_range) == 2:
        daily_filtered = daily_kpis[
            (daily_kpis['date'] >= pd.Timestamp(date_range[0])) & 
            (daily_kpis['date'] <= pd.Timestamp(date_range[1]))
        ]
    else:
        daily_filtered = daily_kpis
else:
    daily_filtered = daily_kpis

st.sidebar.markdown("---")
st.sidebar.info("💡 Cliquez sur les graphiques pour interagir avec les données")

# ==================== PAGE 1 : RÉSUMÉ GÉNÉRAL ====================
if page == "🏠 Résumé Général":
    st.header("🏠 Résumé Général des Performances")
    
    if kpis is not None:
        
        st.subheader("📊 Chiffres Clés")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric(
                "Événements totaux",
                f"{kpis['total_events'].iloc[0]/1e6:.1f} millions"
            )
        
        with col2:
            st.metric(
                "Visiteurs uniques",
                f"{kpis['total_visitors'].iloc[0]/1e6:.1f} millions"
            )
        
        with col3:
            st.metric(
                "Achats réalisés",
                f"{kpis['total_transactions'].iloc[0]:,.0f}".replace(',', ' ')
            )
        
        with col4:
            cart_conv = kpis['conversion_rate_cart_to_purchase'].iloc[0]
            st.metric(
                "Taux de finalisation",
                f"{cart_conv:.1f}%",
                help="Pourcentage de paniers qui deviennent des achats"
            )
        
        with col5:
            global_conv = kpis['conversion_rate_view_to_purchase'].iloc[0]
            st.metric(
                "Taux de conversion global",
                f"{global_conv:.2f}%",
                help="Pourcentage de visiteurs qui achètent"
            )
        
        st.markdown("---")
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.subheader("📉 Parcours d'Achat")
            
            funnel_data = pd.DataFrame({
                'Étape': ['Consultation de produits', 'Ajout au panier', 'Achat finalisé'],
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
            
            fig_funnel.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_funnel, width='stretch')
            
            st.caption("Ce graphique montre comment les visiteurs progressent de la consultation à l'achat")
        
        with col_b:
            st.subheader("📊 Répartition des Actions")
            
            event_data = pd.DataFrame({
                'Type': ['Consultations', 'Ajouts panier', 'Achats'],
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
                hovertemplate='<b>%{label}</b><br>%{value:,.0f} actions<br>%{percent}'
            )
            
            fig_pie.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20),
                showlegend=False
            )
            st.plotly_chart(fig_pie, width='stretch')
            
            st.caption("Proportion de chaque type d'action effectuée par les visiteurs")
        
        st.markdown("---")
        
        st.subheader("🔍 Diagnostic Rapide")
        
        col_i1, col_i2, col_i3 = st.columns(3)
        
        conv_rate = kpis['conversion_rate_view_to_purchase'].iloc[0]
        cart_conv = kpis['conversion_rate_cart_to_purchase'].iloc[0]
        abandon_rate = 100 - cart_conv
        
        with col_i1:
            if 0.8 <= conv_rate <= 3.0:
                st.success("✅ **Taux de conversion normal**")
                st.write(f"{conv_rate:.2f}% des visiteurs achètent")
                st.write("📌 Objectif : entre 1% et 3%")
            else:
                st.warning("⚠️ **Taux de conversion à améliorer**")
                st.write(f"{conv_rate:.2f}% des visiteurs achètent")
        
        with col_i2:
            if abandon_rate > 60:
                st.warning("⚠️ **Beaucoup de paniers abandonnés**")
                st.write(f"{abandon_rate:.1f}% des paniers non finalisés")
                st.write("📌 Objectif : moins de 60%")
            else:
                st.success("✅ **Abandon de panier maîtrisé**")
                st.write(f"{abandon_rate:.1f}% des paniers non finalisés")
        
        with col_i3:
            engaged_pct = ((kpis['total_addtocart'].iloc[0] + kpis['total_transactions'].iloc[0]) / kpis['total_visitors'].iloc[0]) * 100
            passive_pct = 100 - engaged_pct
            
            if passive_pct > 95:
                st.error("🔴 **Beaucoup de visiteurs passifs**")
                st.write(f"{passive_pct:.1f}% ne font qu'observer")
                st.write("📌 Opportunité d'activation")
            else:
                st.success("✅ **Bon engagement des visiteurs**")
                st.write(f"{engaged_pct:.1f}% de visiteurs actifs")

# ==================== PAGE 2 : ACTIVITÉ TEMPORELLE ====================
elif page == "📅 Activité par Jour et Heure":
    st.header("📅 Quand les Visiteurs Sont-ils Actifs ?")
    
    if daily_filtered is not None and hourly is not None:
        
        st.subheader("📈 Activité Jour par Jour")
        
        col_metric, col_chart = st.columns([1, 4])
        
        with col_metric:
            metric_choice = st.radio(
                "Afficher :",
                ["Tout", "Consultations", "Ajouts panier", "Achats"]
            )
        
        with col_chart:
            fig_daily = go.Figure()
            
            if metric_choice in ["Tout", "Consultations"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_filtered['date'],
                    y=daily_filtered['view'],
                    name='Consultations',
                    line=dict(color='#667eea', width=3),
                    fill='tonexty',
                    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>%{y:,.0f} consultations<extra></extra>'
                ))
            
            if metric_choice in ["Tout", "Ajouts panier"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_filtered['date'],
                    y=daily_filtered['addtocart'],
                    name='Ajouts panier',
                    line=dict(color='#f093fb', width=3),
                    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>%{y:,.0f} ajouts<extra></extra>'
                ))
            
            if metric_choice in ["Tout", "Achats"]:
                fig_daily.add_trace(go.Scatter(
                    x=daily_filtered['date'],
                    y=daily_filtered['transaction'],
                    name='Achats',
                    line=dict(color='#4facfe', width=3),
                    hovertemplate='<b>%{x|%d/%m/%Y}</b><br>%{y:,.0f} achats<extra></extra>'
                ))
            
            fig_daily.update_layout(
                xaxis_title="Date",
                yaxis_title="Nombre d'actions",
                hovermode='x unified',
                height=450,
                margin=dict(l=20, r=20, t=20, b=40)
            )
            
            st.plotly_chart(fig_daily, width='stretch')
            st.caption("Évolution de l'activité sur la période sélectionnée")
        
        st.markdown("---")
        
        st.subheader("🕐 Activité Heure par Heure")
        
        fig_hourly = go.Figure()
        
        if 'view' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['view'],
                name='Consultations',
                mode='lines+markers',
                line=dict(color='#667eea', width=4),
                marker=dict(size=10),
                fill='tonexty',
                hovertemplate='<b>%{x}h</b><br>%{y:,.0f} consultations<extra></extra>'
            ))
        
        if 'addtocart' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['addtocart'],
                name='Ajouts panier',
                mode='lines+markers',
                line=dict(color='#f093fb', width=4),
                marker=dict(size=10),
                hovertemplate='<b>%{x}h</b><br>%{y:,.0f} ajouts<extra></extra>'
            ))
        
        if 'transaction' in hourly.columns:
            fig_hourly.add_trace(go.Scatter(
                x=hourly['hour'],
                y=hourly['transaction'],
                name='Achats',
                mode='lines+markers',
                line=dict(color='#4facfe', width=4),
                marker=dict(size=10),
                hovertemplate='<b>%{x}h</b><br>%{y:,.0f} achats<extra></extra>'
            ))
        
        if 'view' in hourly.columns:
            peak_hour = hourly.loc[hourly['view'].idxmax(), 'hour']
            peak_value = hourly['view'].max()
            
            fig_hourly.add_annotation(
                x=peak_hour,
                y=peak_value,
                text=f"Pic d'activité à {peak_hour}h",
                showarrow=True,
                arrowhead=2,
                arrowcolor="#e74c3c",
                font=dict(size=14, color='#e74c3c', family='Arial Black'),
                bgcolor="rgba(255,255,255,0.9)",
                bordercolor="#e74c3c",
                borderwidth=2
            )
        
        fig_hourly.update_layout(
            xaxis_title="Heure de la journée",
            yaxis_title="Nombre d'actions",
            xaxis=dict(
                tickmode='array',
                tickvals=list(range(0, 24, 2)),
                ticktext=[f"{h}h" for h in range(0, 24, 2)]
            ),
            hovermode='x unified',
            height=500,
            margin=dict(l=20, r=20, t=20, b=40)
        )
        
        st.plotly_chart(fig_hourly, width='stretch')
        st.caption("Distribution de l'activité sur 24 heures")
        
        st.markdown("---")
        
        if 'view' in hourly.columns:
            top_hours = sorted(hourly.nlargest(3, 'view')['hour'].tolist())
            low_hours = sorted(hourly.nsmallest(3, 'view')['hour'].tolist())
            
            col_r1, col_r2 = st.columns(2)
            
            with col_r1:
                st.success("### 🔥 Meilleurs moments")
                st.write(f"**Entre {top_hours[0]}h et {top_hours[-1]}h**")
                st.write("C'est le moment idéal pour :")
                st.write("• Lancer des promotions flash")
                st.write("• Envoyer des emails marketing")
                st.write("• Diffuser des publicités")
            
            with col_r2:
                st.info("### 😴 Moments calmes")
                st.write(f"**Entre {low_hours[0]}h et {low_hours[-1]}h**")
                st.write("Période idéale pour :")
                st.write("• Maintenance du site")
                st.write("• Mise à jour des produits")
                st.write("• Tests techniques")

# ==================== PAGE 3 : PRODUITS ====================
elif page == "🛍️ Performance des Produits":
    st.header("🛍️ Quels Produits Fonctionnent le Mieux ?")
    
    if products is not None:
        
        col_s1, col_s2 = st.columns([3, 1])
        
        with col_s1:
            st.subheader("🏆 Classement des Produits")
        
        with col_s2:
            top_n = st.slider("Nombre à afficher", 5, 20, 10)
        
        sort_choice = st.radio(
            "Trier par :",
            ["🔥 Plus consultés", "💰 Plus achetés", "🎯 Meilleur taux de conversion"],
            horizontal=True
        )
        
        if sort_choice == "🔥 Plus consultés":
            top_products = products.nlargest(top_n, 'views')
            metric = 'views'
            label = 'Consultations'
            color_scale = 'Blues'
        elif sort_choice == "💰 Plus achetés":
            top_products = products.nlargest(top_n, 'purchases')
            metric = 'purchases'
            label = 'Achats'
            color_scale = 'Greens'
        else:
            top_products = products[products['conversion_rate'] > 0].nlargest(top_n, 'conversion_rate')
            metric = 'conversion_rate'
            label = 'Taux de conversion (%)'
            color_scale = 'RdYlGn'
        
        fig_top = px.bar(
            top_products,
            x=metric,
            y='itemid',
            orientation='h',
            color=metric,
            color_continuous_scale=color_scale,
            text=metric
        )
        
        if metric == 'conversion_rate':
            fig_top.update_traces(
                texttemplate='%{text:.1f}%',
                textposition='outside',
                hovertemplate='<b>Produit %{y}</b><br>Taux : %{x:.2f}%<extra></extra>'
            )
        else:
            fig_top.update_traces(
                texttemplate='%{text:,.0f}',
                textposition='outside',
                hovertemplate='<b>Produit %{y}</b><br>%{x:,.0f}<extra></extra>'
            )
        
        fig_top.update_layout(
            xaxis_title=label,
            yaxis_title="Identifiant Produit",
            height=500,
            showlegend=False,
            margin=dict(l=20, r=80, t=20, b=40)
        )
        
        st.plotly_chart(fig_top, width='stretch')
        
        st.markdown("---")
        
        st.subheader("💡 Produits à Fort Potentiel")
        st.write("Ces produits sont beaucoup consultés mais peu achetés. Améliorer leurs pages peut booster les ventes.")
        
        products_analysis = products[
            (products['views'] >= 100) & 
            (products['purchases'] > 0)
        ].copy()
        
        if len(products_analysis) > 0:
            
            def categorize(rate):
                if rate >= 2.0:
                    return '🟢 Excellent'
                elif rate >= 1.0:
                    return '🟡 Bon'
                elif rate >= 0.5:
                    return '🟠 Moyen'
                else:
                    return '🔴 Faible'
            
            products_analysis['Performance'] = products_analysis['conversion_rate'].apply(categorize)
            
            col_perf1, col_perf2 = st.columns(2)
            
            with col_perf1:
                st.markdown("**Répartition par Performance**")
                
                perf_counts = products_analysis['Performance'].value_counts()
                
                fig_perf = px.bar(
                    x=perf_counts.values,
                    y=perf_counts.index,
                    orientation='h',
                    color=perf_counts.index,
                    color_discrete_map={
                        '🟢 Excellent': '#27ae60',
                        '🟡 Bon': '#f39c12',
                        '🟠 Moyen': '#e67e22',
                        '🔴 Faible': '#e74c3c'
                    },
                    text=perf_counts.values
                )
                
                fig_perf.update_traces(
                    texttemplate='%{text} produits',
                    textposition='outside',
                    hovertemplate='<b>%{y}</b><br>%{x} produits<extra></extra>'
                )
                
                fig_perf.update_layout(
                    height=300,
                    showlegend=False,
                    xaxis_title="Nombre de produits",
                    yaxis_title="",
                    margin=dict(l=20, r=100, t=20, b=40)
                )
                
                st.plotly_chart(fig_perf, width='stretch')
            
            with col_perf2:
                low_perf = len(products_analysis[products_analysis['conversion_rate'] < 1])
                total_perf = len(products_analysis)
                pct_low = (low_perf / total_perf) * 100
                
                st.metric(
                    "Produits à optimiser",
                    f"{low_perf}",
                    f"{pct_low:.0f}% du total"
                )
                
                st.write("")
                st.write("**Pistes d'amélioration :**")
                st.write("• Photos de meilleure qualité")
                st.write("• Descriptions plus détaillées")
                st.write("• Avis clients")
                st.write("• Révision des prix")
            
            st.markdown("---")
            
            priority = products_analysis[
                (products_analysis['views'] >= 500) & 
                (products_analysis['conversion_rate'] < 1)
            ].nlargest(15, 'views')
            
            if len(priority) > 0:
                st.subheader(f"🎯 Top {len(priority)} Produits Prioritaires")
                st.caption("Produits très consultés mais avec un faible taux de conversion")
                
                fig_priority = go.Figure()
                
                fig_priority.add_trace(go.Bar(
                    x=priority['itemid'],
                    y=priority['views'],
                    name='Consultations',
                    marker_color='#3498db',
                    yaxis='y',
                    hovertemplate='<b>%{x}</b><br>%{y:,.0f} consultations<extra></extra>'
                ))
                
                fig_priority.add_trace(go.Scatter(
                    x=priority['itemid'],
                    y=priority['conversion_rate'],
                    name='Taux de conversion',
                    mode='lines+markers',
                    marker=dict(size=12, color='#e74c3c', symbol='diamond'),
                    line=dict(width=3, color='#e74c3c'),
                    yaxis='y2',
                    hovertemplate='<b>%{x}</b><br>%{y:.2f}% de conversion<extra></extra>'
                ))
                
                fig_priority.update_layout(
                    xaxis=dict(title='Identifiant Produit', tickangle=-45),
                    yaxis=dict(title='Nombre de consultations', side='left'),
                    yaxis2=dict(title='Taux de conversion (%)', side='right', overlaying='y'),
                    hovermode='x unified',
                    height=500,
                    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
                    margin=dict(l=20, r=20, t=60, b=100)
                )
                
                st.plotly_chart(fig_priority, width='stretch')
                
                st.success(f"""
                💡 **Opportunité majeure** : En optimisant ces {len(priority)} produits, 
                les ventes pourraient augmenter de 20 à 30% sur ces références.
                """)

# ==================== PAGE 4 : SEGMENTATION ====================
elif page == "👥 Types de Visiteurs":
    st.header("👥 Qui Visite le Site ?")
    
    if events is not None:
        
        st.write("Les visiteurs sont classés en 3 catégories selon leur comportement :")
        
        user_behavior = events.groupby('visitorid').agg({
            'event': 'count',
            'itemid': 'nunique'
        }).rename(columns={'event': 'total_events', 'itemid': 'unique_products'})
        
        user_views = events[events['event'] == 'view'].groupby('visitorid').size()
        user_cart = events[events['event'] == 'addtocart'].groupby('visitorid').size()
        user_buy = events[events['event'] == 'transaction'].groupby('visitorid').size()
        
        user_behavior['views'] = user_views.fillna(0)
        user_behavior['addtocart'] = user_cart.fillna(0)
        user_behavior['purchases'] = user_buy.fillna(0)
        
        def categorize(row):
            if row['purchases'] > 0:
                return '💰 Clients (ont acheté)'
            elif row['addtocart'] > 0:
                return '🛒 Intéressés (panier non finalisé)'
            else:
                return '👁️ Visiteurs (observation simple)'
        
        user_behavior['Type'] = user_behavior.apply(categorize, axis=1)
        counts = user_behavior['Type'].value_counts()
        
        col_seg1, col_seg2, col_seg3 = st.columns(3)
        
        total = len(user_behavior)
        
        with col_seg1:
            clients = counts.get('💰 Clients (ont acheté)', 0)
            pct = (clients / total) * 100
            st.metric(
                "💰 Clients",
                f"{clients:,}".replace(',', ' '),
                f"{pct:.1f}% des visiteurs"
            )
            st.caption("Ont effectué au moins un achat")
        
        with col_seg2:
            interested = counts.get('🛒 Intéressés (panier non finalisé)', 0)
            pct = (interested / total) * 100
            st.metric(
                "🛒 Intéressés",
                f"{interested:,}".replace(',', ' '),
                f"{pct:.1f}% des visiteurs"
            )
            st.caption("Ont ajouté au panier sans acheter")
        
        with col_seg3:
            passive = counts.get('👁️ Visiteurs (observation simple)', 0)
            pct = (passive / total) * 100
            st.metric(
                "👁️ Visiteurs",
                f"{passive:,}".replace(',', ' '),
                f"{pct:.1f}% des visiteurs"
            )
            st.caption("Consultent sans interagir")
        
        st.markdown("---")
        
        col_v1, col_v2 = st.columns(2)
        
        with col_v1:
            st.subheader("📊 Répartition des Visiteurs")
            
            fig_pie = px.pie(
                values=counts.values,
                names=counts.index,
                hole=0.5,
                color_discrete_sequence=['#27ae60', '#f39c12', '#3498db']
            )
            
            fig_pie.update_traces(
                textposition='inside',
                textinfo='percent',
                hovertemplate='<b>%{label}</b><br>%{value:,} visiteurs<br>%{percent}'
            )
            
            fig_pie.update_layout(
                height=400,
                margin=dict(l=20, r=20, t=20, b=20)
            )
            st.plotly_chart(fig_pie, width='stretch')
        
        with col_v2:
            st.subheader("📈 Comportement Moyen")
            
            avg_behavior = user_behavior.groupby('Type')[['views', 'addtocart', 'purchases']].mean().reset_index()
            avg_behavior_melted = avg_behavior.melt(id_vars='Type')
            avg_behavior_melted['variable'] = avg_behavior_melted['variable'].map({
                'views': 'Consultations',
                'addtocart': 'Ajouts panier',
                'purchases': 'Achats'
            })
            
            fig_bar = px.bar(
                avg_behavior_melted,
                x='Type',
                y='value',
                color='variable',
                barmode='group',
                color_discrete_sequence=['#667eea', '#f093fb', '#4facfe'],
                labels={'value': 'Moyenne par visiteur', 'variable': 'Action'}
            )
            
            fig_bar.update_layout(
                height=400,
                xaxis_title="",
                legend_title="",
                margin=dict(l=20, r=20, t=20, b=40)
            )
            st.plotly_chart(fig_bar, width='stretch')
        
        st.markdown("---")
        
        st.subheader("📋 Statistiques Détaillées")
        
        for segment_name in counts.index:
            segment_data = user_behavior[user_behavior['Type'] == segment_name]
            segment_count = len(segment_data)
            segment_pct = (segment_count / total) * 100
            
            with st.expander(f"{segment_name} - {segment_count:,} visiteurs ({segment_pct:.1f}%)".replace(',', ' ')):
                col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
                
                with col_stat1:
                    st.metric("Consultations moyennes", f"{segment_data['views'].mean():.1f}")
                
                with col_stat2:
                    st.metric("Produits vus différents", f"{segment_data['unique_products'].mean():.1f}")
                
                with col_stat3:
                    st.metric("Ajouts panier moyens", f"{segment_data['addtocart'].mean():.1f}")
                
                with col_stat4:
                    st.metric("Achats moyens", f"{segment_data['purchases'].mean():.1f}")

# ==================== PAGE 5 : A/B TESTS ====================
elif page == "🧪 Tests d'Optimisation":
    st.header("🧪 Tests d'Amélioration Réalisés")
    
    st.write("Des tests ont été effectués pour comparer différentes versions du site et identifier les meilleures solutions.")
    
    if ab_tests is not None:
        
        st.markdown("---")
        
        col_o1, col_o2, col_o3 = st.columns(3)
        
        with col_o1:
            st.metric("Nombre de tests", len(ab_tests))
        
        with col_o2:
            significant = len(ab_tests[ab_tests['Significatif'] == '✅ Oui'])
            st.metric("Tests concluants", f"{significant}/{len(ab_tests)}")
        
        with col_o3:
            improvements = ab_tests['Amélioration'].str.rstrip('%').astype(float)
            avg = improvements.mean()
            st.metric("Amélioration moyenne", f"+{avg:.0f}%")
        
        st.markdown("---")
        
        for idx, row in ab_tests.iterrows():
            with st.expander(f"📊 {row['Test']}", expanded=(idx==0)):
                
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("### Test réalisé")
                    st.write(f"**Indicateur mesuré :** {row['Métrique']}")
                    st.write(f"**Version A :** {row['Groupe_A']}")
                    st.write(f"**Version B :** {row['Groupe_B']}")
                    
                    st.markdown("---")
                    
                    improvement_val = float(row['Amélioration'].rstrip('%'))
                    
                    if improvement_val > 0:
                        st.success(f"**Résultat :** +{row['Amélioration']} d'amélioration")
                        st.write(f"La version B performe **{row['Amélioration']} mieux** que la version A")
                    else:
                        st.error(f"**Résultat :** {row['Amélioration']}")
                        st.write("La version B performe moins bien que la version A")
                
                with col2:
                    st.markdown("### Fiabilité")
                    
                    if row['Significatif'] == '✅ Oui':
                        st.success("✅ **Résultat fiable**")
                        st.write(f"P-value : {row['P_value']}")
                        st.write("")
                        st.write("Ce résultat est statistiquement valide.")
                        st.write("")
                        st.info(f"💡 {row['Recommandation']}")
                    else:
                        st.warning("⚠️ **Résultat incertain**")
                        st.write(f"P-value : {row['P_value']}")
                        st.write("")
                        st.write("Ce résultat pourrait être dû au hasard.")
        
        st.markdown("---")
        
        st.subheader("📋 Tableau Récapitulatif")
        
        st.dataframe(
            ab_tests,
            width='stretch',
            hide_index=True,
            column_config={
                "Test": "Nom du test",
                "Métrique": "Indicateur",
                "Groupe_A": "Version A",
                "Groupe_B": "Version B",
                "Amélioration": "Gain",
                "P_value": "P-value",
                "Significatif": "Fiable ?",
                "Recommandation": "Action suggérée"
            }
        )
        
        st.info("""
        💡 **Note importante :** Les recommandations détaillées et le plan d'action complet 
        sont disponibles dans le rapport d'analyse.
        """)

# ==================== FOOTER ====================
st.sidebar.markdown("---")
st.sidebar.markdown("""
**📊 Informations**

**Projet :** DPIA 1 2025  
**École :** L'École Multimédia  
**Auteur :** Samir NZAMBA

[📂 Voir le code sur GitHub](https://github.com/SNZAMBA65/ecommerce-analysis)
""")

st.sidebar.caption(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y à %H:%M')}")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #95a5a6; font-size: 0.9rem; padding: 20px 0;'>
    <p><strong>Dashboard E-commerce</strong> - Analyse des performances</p>
    <p>Samir NZAMBA | L'École Multimédia | Janvier 2026</p>
</div>
""", unsafe_allow_html=True)