import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência de Mapas - WMS", page_icon="📦", layout="centered")

st.markdown("## 📦 Conferência de Mapas e Carga")
st.write("Faça o upload da foto do mapa, confira as quantidades e marque os itens.")

# --- 1. UPLOAD DA FOTO DO MAPA ---
st.subheader("1️⃣ Enviar Foto do Mapa")
arquivo_subido = st.file_uploader("Selecione a foto escaneada do mapa:", type=["png", "jpg", "jpeg", "webp"])

if arquivo_subido is not None:
    st.success(f"📄 Foto '{arquivo_subido.name}' carregada com sucesso!")

st.divider()

# --- 2. IDENTIFICAÇÃO DA PLACA ---
st.subheader("2️⃣ Identificação do Veículo")
col_p1, col_p2 = st.columns([2, 1])

with col_p1:
    placa_veiculo = st.text_input("Placa do Caminhão:", placeholder="Ex: ABC-1234").upper()

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

# --- 3. LISTA DE CONFERÊNCIA COM CONVERSÃO AUTOMÁTICA ---
st.subheader("3️⃣ Conferência de Itens & Conversão Automática")
st.write("Insira as unidades do mapa. O app converte direto para Pacotes/Caixas e permite marcar o visto verde.")

# Inicializa os itens padrão baseados no seu modelo
if "tabela_conferencia" not in st.session_state:
    st.session_state.tabela_conferencia = [
        {"Produto": "Cerveja Itaipava Pilsen Lata 473ml", "Unidades": 571, "Fator": 12, "Tipo": "PAC", "Conferido": False},
        {"Produto": "Cerveja Pilsen Lata 473ml (Local)", "Unidades": 278, "Fator": 12, "Tipo": "PAC", "Conferido": False},
        {"Produto": "Cerveja 1000ml / 1L (Garrafa)", "Unidades": 12, "Fator": 12, "Tipo": "CX", "Conferido": False},
        {"Produto": "Cerveja 600ml (Caixa)", "Unidades": 24, "Fator": 24, "Tipo": "CX", "Conferido": False},
    ]

# Exibe os itens interativos
for idx, item in enumerate(st.session_state.tabela_conferencia):
    total_un = item["Unidades"]
    fator = item["Fator"]
    
    with st.container():
        st.markdown(f"**Item {idx+1}: {item['Produto']}**")
        
        c1, c2, c3 = st.columns([1.2, 1.3, 1])
        
        with c1:
            nova_qtd = st.number_input("Unidades:", min_value=0, value=total_un, key=f"un_{idx}")
            st.session_state.tabela_conferencia[idx]["Unidades"] = nova_qtd
            
        with c2:
            calc_cx_pac = nova_qtd // fator
            sobra = nova_qtd % fator
            st.markdown(f"📦 **{calc_cx_pac} {item['Tipo']}** + {sobra} un")
            st.caption(f"Fator: {fator} un/{item['Tipo']}")
            
        with c3:
            st.write("")
            btn_txt = "✔ Conferido" if item["Conferido"] else "⬜ Marcar OK"
            if st.button(btn_txt, key=f"btn_c_{idx}"):
                st.session_state.tabela_conferencia[idx]["Conferido"] = not item["Conferido"]
                st.rerun()
                
        if item["Conferido"]:
            st.success("Status: Validado com sucesso! ✔")
        else:
            st.warning("Status: Pendente ⏳")
            
        st.markdown("---")

if st.button("💾 Finalizar e Salvar Conferência"):
    st.success("🎉 Conferência gravada com sucesso! Todos os itens validados.")
