import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência de Carga", page_icon="🚚", layout="centered")

st.markdown("## 🚚 Painel de Conferência de Mapas")
st.write("Controle de placas, conversão automática e crivo do conferente.")

# --- 1. CONTROLE DO CAMINHÃO (PLACA COM BOTÃO VERDE) ---
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
        btn_label = "✅ Caminhão Conferido" if st.session_state.caminhao_conferido else "🟢 Marcar Caminhão OK"
        if st.button(btn_label):
            st.session_state.caminhao_conferido = not st.session_state.caminhao_conferido

if placa_veiculo:
    if st.session_state.caminhao_conferido:
        st.success(f"Veículo **{placa_veiculo}** conferido e com liberação verde! 🟢✅")
    else:
        st.warning(f"Veículo **{placa_veiculo}** aguardando sinalização.")

st.divider()

# --- 2. CONVERSÃO AUTOMÁTICA POR TIPO DE EMBALAGEM ---
st.subheader("📦 Conversão Automática de Unidades")

tipo_cerveja = st.selectbox(
    "Selecione o tipo de embalagem/produto:",
    [
        "Cerveja 473ml (Fardo/PAC com 12 unidades)", 
        "Cerveja 600ml (Caixa com 24 unidades)", 
        "Cerveja 1000ml / 1L (Caixa com 12 unidades)", 
        "Outro Padrão / Palete"
    ]
)

if "473ml" in tipo_cerveja:
    fator_conversao = 12
    nome_pacote = "Pacotes (PAC)"
elif "600ml" in tipo_cerveja:
    fator_conversao = 24
    nome_pacote = "Caixas (CX)"
elif "1000ml" in tipo_cerveja:
    fator_conversao = 12
    nome_pacote = "Caixas (CX)"
else:
    fator_conversao = st.number_input("Fator personalizado:", min_value=1, value=242)
    nome_pacote = "Unidades/Padrão"

total_unidades = st.number_input("Quantidade Total em Unidades (no mapa):", min_value=0, value=288, step=1)

if fator_conversao > 0:
    qtd_caixas_pac = total_unidades // fator_conversao
    sobra_unidades = total_unidades % fator_conversao
    st.info(f"📊 **Resultado da Conversão:** **{qtd_caixas_pac} {nome_pacote}** e **{sobra_unidades} unidades** soltas.")

st.divider()

# --- 3. CHECKLIST DO MAPA: SEPARADOR E O V VERDE DO CONFERENTE ---
st.subheader("🔍 Conferência de Itens do Mapa")
st.write("O separador marca o que pegou. O conferente clica na coluna para gerar o **✔ verde**.")

if "tabela_mapa" not in st.session_state:
    st.session_state.tabela_mapa = pd.DataFrame([
        {"Produto": "Cerveja 473ml", "Qtd Total": 120, "Separador": False, "Conferente_OK": False},
        {"Produto": "Cerveja 600ml", "Qtd Total": 240, "Separador": False, "Conferente_OK": False},
        {"Produto": "Cerveja 1000ml", "Qtd Total": 144, "Separador": False, "Conferente_OK": False},
    ])

for idx, row in st.session_state.tabela_mapa.iterrows():
    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        st.markdown(f"**{row['Produto']}**<br><small>Total: {row['Qtd Total']} un</small>", unsafe_allow_html=True)
        
    with c2:
        sep_val = st.checkbox("Separado", value=row["Separador"], key=f"sep_{idx}")
        st.session_state.tabela_mapa.at[idx, "Separador"] = sep_val
        
    with c3:
        conf_val = st.checkbox("✔ OK", value=row["Conferente_OK"], key=f"conf_{idx}")
        st.session_state.tabela_mapa.at[idx, "Conferente_OK"] = conf_val
        if conf_val:
            st.markdown("<span style='color:green; font-weight:bold;'>✔ Validado</span>", unsafe_allow_html=True)

st.divider()

if st.button("💾 Concluir e Salvar Conferência do Mapa"):
    st.success("Mapa conferido e salvo com sucesso! Pronto para o próximo.")

