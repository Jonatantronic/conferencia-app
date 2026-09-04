import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência de Carga", page_icon="🚚", layout="centered")

st.markdown("## 🚚 Painel de Conferência de Carga")

# --- 1. CONTROLE DO CAMINHÃO (PLACA) ---
st.subheader("📋 Identificação do Veículo")
col_p1, col_p2 = st.columns([2, 1])

with col_p1:
    placa_veiculo = st.text_input("Placa do Caminhão / Veículo:", placeholder="Ex: ABC-1234").upper()

if "caminhao_conferido" not in st.session_state:
    st.session_state.caminhao_conferido = False

with col_p2:
    st.write("") 
    st.write("")
    if placa_veiculo:
        if st.button("🟢 Liberar Caminhão" if not st.session_state.caminhao_conferido else "✅ Caminhão Conferido"):
            st.session_state.caminhao_conferido = not st.session_state.caminhao_conferido

if placa_veiculo:
    if st.session_state.caminhao_conferido:
        st.success(f"Caminhão **{placa_veiculo}** totalmente conferido e liberado! ✅")
    else:
        st.warning(f"Caminhão **{placa_veiculo}** aguardando conferência final.")

st.divider()

# --- 2. CONFIGURAÇÃO DOS TIPOS DE EMBALAGEM ---
st.subheader("📦 Regras de Conversão Automática")
tipo_produto = st.selectbox(
    "Selecione o tipo de produto do mapa:",
    [
        "Cerveja 473ml (12 un/pacote)", 
        "Cerveja 600ml (24 un/caixa)", 
        "Cerveja 1000ml (12 un/caixa)", 
        "Outro / Padrão Logístico"
    ]
)

if "473ml" in tipo_produto:
    fator = 12
    unidade_medida = "Pacotes (PAC)"
elif "600ml" in tipo_produto:
    fator = 24
    unidade_medida = "Caixas (CX)"
elif "1000ml" in tipo_produto:
    fator = 12
    unidade_medida = "Caixas (CX)"
else:
    fator = st.number_input("Informe o fator personalizado:", min_value=1, value=242)
    unidade_medida = "Unidades/Padrão"

total_unidades_lido = st.number_input("Quantidade Total em Unidades:", min_value=0, value=288, step=1)

if fator > 0:
    qtd_embalagem = total_unidades_lido // fator
    sobra_unidades = total_unidades_lido % fator
    st.info(f"📊 **Conversão:** {qtd_embalagem} {unidade_medida} e {sobra_unidades} unidades soltas.")

st.divider()

# --- 3. ITENS DO MAPA: SEPARADOR E CONFERENTE ---
st.subheader("🔍 Checklist de Itens do Mapa")

if "dados_tabela" not in st.session_state:
    st.session_state.dados_tabela = pd.DataFrame([
        {"Item": "Cerveja 473ml - Fardo 12un", "Qtd Un": 120, "Separador OK": False, "Conferente OK": False},
        {"Item": "Cerveja 600ml - Caixa 24un", "Qtd Un": 240, "Separador OK": False, "Conferente OK": False},
        {"Item": "Cerveja 1000ml - Caixa 12un", "Qtd Un": 144, "Separador OK": False, "Conferente OK": False},
    ])

for i, row in st.session_state.dados_tabela.iterrows():
    col_item, col_sep, col_conf = st.columns([3, 1, 1])
    
    with col_item:
        st.markdown(f"**{row['Item']}**<br><small>Qtd: {row['Qtd Un']} un</small>", unsafe_allow_html=True)
        
    with col_sep:
        sep_status = st.checkbox("Separado", value=row["Separador OK"], key=f"sep_{i}")
        st.session_state.dados_tabela.at[i, "Separador OK"] = sep_status
        
    with col_conf:
        conf_status = st.checkbox("✔", value=row["Conferente OK"], key=f"conf_{i}")
        st.session_state.dados_tabela.at[i, "Conferente OK"] = conf_status

st.divider()
if st.button("💾 Salvar Conferência"):
    st.success("Conferência registrada com sucesso!")
