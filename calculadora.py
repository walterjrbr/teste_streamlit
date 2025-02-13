import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard Avançado de Infraestrutura e Negócios")

# Simulação inicial de dados
np.random.seed(42)
time_series = pd.date_range(start="10:00", periods=50, freq="T")

cpu_usage = np.random.uniform(30, 60, 50)
mem_usage = np.random.uniform(40, 70, 50)
disk_usage = np.random.uniform(20, 85, 50)
tps = np.random.uniform(100, 500, 50)
latency = np.random.uniform(50, 200, 50)
iops = np.random.uniform(500, 1500, 50)
network = np.random.uniform(100, 1000, 50)
errors = np.random.uniform(0, 5, 50)
bill_queries = np.random.uniform(0, 100000, 50)

# Criar DataFrame
df = pd.DataFrame({
    "Tempo": time_series,
    "CPU (%)": cpu_usage,
    "Memória (%)": mem_usage,
    "Disco (%)": disk_usage,
    "TPS": tps,
    "Latência (ms)": latency,
    "IOPS": iops,
    "Rede (Mbps)": network,
    "Erros": errors,
    "Consultas Fatura": bill_queries
})

# Configuração do TPS e Consultas de Fatura dinâmicos
st.sidebar.markdown("## ⚙️ **Simulação de Carga**")
user_tps = st.sidebar.slider("Ajuste o TPS (Transações por Segundo)", 50, 1500, int(tps[-1]))
user_bill_queries = st.sidebar.slider("Ajuste o Volume de Consultas de Fatura", 0, 100000, int(bill_queries[-1]))

# Ajustando CPU e Memória com base no TPS e Consultas de Fatura
tps_base = tps[-1]
bill_queries_base = bill_queries[-1]

if user_tps > tps_base * 1.5 or user_bill_queries > bill_queries_base * 1.5:
    cpu_impact = min(100, cpu_usage[-1] * 1.8)
    mem_impact = min(100, mem_usage[-1] * 1.7)
    impact_message = "ALTA DEMANDA! Sistema próximo do limite operacional."
    impact_color = "red"
elif user_tps > tps_base * 1.3 or user_bill_queries > bill_queries_base * 1.3:
    cpu_impact = min(90, cpu_usage[-1] * 1.5)
    mem_impact = min(90, mem_usage[-1] * 1.4)
    impact_message = "SISTEMA SOB CARGA! Monitoramento recomendado."
    impact_color = "orange"
else:
    cpu_impact = cpu_usage[-1]
    mem_impact = mem_usage[-1]
    impact_message = "Sistema operando dentro da normalidade."
    impact_color = "green"

# Criando colunas para os indicadores
st.markdown("## 📊 **Dashboard Avançado - Infraestrutura e Negócios**")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

# Função para criar gauge (relógio circular)
def create_gauge(title, value, max_value, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": title, "font": {"size": 20}},
        gauge={
            "axis": {"range": [0, max_value]},
            "bar": {"color": color},
            "steps": [
                {"range": [0, max_value * 0.5], "color": "lightgray"},
                {"range": [max_value * 0.5, max_value * 0.75], "color": "yellow"},
                {"range": [max_value * 0.75, max_value], "color": "red"}
            ],
        },
    ))
    fig.update_layout(height=250)
    return fig

with col1:
    st.plotly_chart(create_gauge("CPU (%)", round(cpu_impact, 1), 100, "red"), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge("Memória (%)", round(mem_impact, 1), 100, "blue"), use_container_width=True)

with col3:
    st.plotly_chart(create_gauge("Disco (%)", round(disk_usage[-1], 1), 100, "green"), use_container_width=True)

with col4:
    st.plotly_chart(create_gauge("TPS", user_tps, 1500, "purple"), use_container_width=True)

with col5:
    st.plotly_chart(create_gauge("Latência (ms)", round(latency[-1], 1), 200, "orange"), use_container_width=True)

with col6:
    st.plotly_chart(create_gauge("Erros", round(errors[-1], 1), 10, "gray"), use_container_width=True)

with col7:
    st.plotly_chart(create_gauge("Consultas Fatura", user_bill_queries, 100000, "cyan"), use_container_width=True)

# Gráficos de Tendências
st.markdown("---")
st.markdown("### 📈 **Tendências de Utilização**")
fig = px.line(df, x="Tempo", y=["CPU (%)", "Memória (%)", "Disco (%)", "TPS", "Latência (ms)", "Erros", "Consultas Fatura"],
              labels={"value": "Uso (%)", "variable": "Recurso"},
              title="Evolução do Uso dos Recursos do Sistema",
              template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# Heatmap de Correlação
st.markdown("---")
st.markdown("### 🔍 **Correlação entre Métricas**")
correlation_matrix = df.drop(columns=["Tempo"]).corr()
fig_corr = px.imshow(correlation_matrix, text_auto=True, title="Matriz de Correlação", template="plotly_dark")
st.plotly_chart(fig_corr, use_container_width=True)

# Impacto nos Negócios
st.markdown("---")
st.markdown("## **Impacto nos Negócios**")
st.markdown(f"<h3 style='color: {impact_color}; text-align: center;'>{impact_message}</h3>", unsafe_allow_html=True)

# Simulação dinâmica
if st.button("🔄 Atualizar Dados"):
    st.rerun()
