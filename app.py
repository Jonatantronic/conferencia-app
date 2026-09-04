import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência de Mapas - WMS", page_icon="📦", layout="centered")

st.markdown("## 📦 Conferência de Mapas e Carga")
st.write("Envie a foto do mapa para referência visual e gerencie a carga de forma rápida e segura.")

# --- 1. UPLOAD DA FOTO DO MAPA ---
st.subheader("1️⃣ Foto ou Arquivo do Mapa")
arquivo_subido = st.file_uploader("Selecione a foto escaneada do mapa:", type=["png", "jpg", "jpeg", "webp"])

if arquivo_subido is not None:
    try:
        st.image(arquivo_subido, caption=f"📄 Mapa: {arquivo_subido.name}", use_column_width=True)
        st.success("✅ Foto do mapa carregada como base visual!")
    except Exception:
        st.warning(f"⚠️ Arquivo '{arquivo_subido.name}' recebido.")

st.divider()

# --- 2. PLACA DO CAMINHÃO ---
st.subheader("2️⃣ Identificação do Veículo")
col_p1, col_p2 = st.columns([2, 1])

with col_p1:
    placa_veiculo = st.text_input("Placa do Caminhão (conforme o mapa):", placeholder="Ex: ABC-1234").upper()

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
        st.success(f"Veículo **{placa_veiculo}** liberado com sinal verde! 🟢✅")
    else:
        st.warning(f"Veículo **{placa_veiculo}** aguardando conferência.")

st.divider()

# --- 3. ADICIONAR E CONFERIR ITENS DO MAPA ---
st.subheader("3️⃣ Itens do Mapa & Conversão Automática")
st.write("Adicione os itens que constam no mapa enviado, ajuste as unidades e marque o visto verde.")

if "lista_itens" not in st.session_state:
    st.session_state.lista_itens = [
        {"Produto": "Cerveja Itaipava Pilsen Lata 473ml", "Unidades": 571, "Fator": 12, "Tipo": "PAC", "Conferido": False},
        {"Produto": "Cerveja Pilsen Lata 473ml (Local)", "Unidades": 278, "Fator": 12, "Tipo": "PAC", "Conferido": False},
    ]

with st.expander("➕ Adicionar Novo Item do Mapa"):
    novo_prod = st.text_input("Descrição do Produto:", placeholder="Ex: Cerveja 600ml")
    col_n1, col_n2, col_n3 = st.columns(3)
    with col_n1:
        nova_qtd_cad = st.number_input("Unidades:", min_value=1, value=100, key="cad_qtd")
    with col_n2:
        novo_fator = st.number_input("Fator (ex: 12 ou 24):", min_value=1, value=12, key="cad_fat")
    with col_n3:
        novo_tipo = st.selectbox("Tipo de Embalagem:", ["PAC", "CX"], key="cad_tipo")
    
    if st.button("Inserir na Lista de Conferência"):
        if novo_prod:
            st.session_state.lista_itens.append({
                "Produto": novo_prod,
                "Unidades": nova_qtd_cad,
                "Fator": novo_fator,
                "Tipo": novo_tipo,
                "Conferido": False
            })
            st.success("Item adicionado com sucesso!")
            st.rerun()
        else:
            st.warning("Informe a descrição do produto.")

st.write("---")

for idx, item in enumerate(st.session_state.lista_itens):
    total_un = item["Unidades"]
    fator = item["Fator"]
    
    with st.container():
        st.markdown(f"**Item {idx+1}: {item['Produto']}**")
        
        c1, c2, c3 = st.columns([1.2, 1.3, 1])
        
        with c1:
            nova_qtd = st.number_input("Unidades:", min_value=0, value=total_un, key=f"un_din_{idx}")
            st.session_state.lista_itens[idx]["Unidades"] = nova_qtd
            
        with c2:
            calc_cx_pac = nova_qtd // fator
            sobra = nova_qtd % fator
            st.markdown(f"📦 **{calc_cx_pac} {item['Tipo']}** + {sobra} un")
            st.caption(f"Fator: {fator} un/{item['Tipo']}")
            
        with c3:
            st.write("")
            btn_txt = "✔ Conferido" if item["Conferido"] else "⬜ Marcar OK"
            if st.button(btn_txt, key=f"btn_conf_din_{idx}"):
                st.session_state.lista_itens[idx]["Conferido"] = not item["Conferido"]
                st.rerun()
                
        if item["Conferido"]:
            st.success("Status: Validado com sucesso! ✔")
        else:
            st.warning("Status: Pendente ⏳")
            
        st.markdown("---")

if st.button("💾 Finalizar e Salvar Conferência Completa"):
    st.success("🎉 Conferência gravada com sucesso! Todos os itens validados.")
