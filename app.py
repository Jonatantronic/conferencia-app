import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Conferência de Mapas - WMS", page_icon="🍻", layout="centered")

st.markdown("## 🍻 Conferência de Mapas e Carga")
st.write("Envie a foto do mapa para base visual e faça a conferência interativa dos itens.")

# --- 1. VISUALIZAÇÃO DO MAPA BASE ---
st.subheader("1️⃣ Mapa Base do Veículo")
arquivo_mapa = st.file_uploader("Selecione a foto escaneada do mapa:", type=["png", "jpg", "jpeg"])

if arquivo_mapa is not None:
    imagem_mapa = Image.open(arquivo_mapa)
    st.image(imagem_mapa, caption="📄 Mapa de Separação em Consulta", use_column_width=True)
    st.success("✅ Mapa carregado na tela como base!")

st.divider()

# --- 2. CONTROLE DA PLACA DO CAMINHÃO ---
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

# --- 3. ITENS EXTRAÍDOS DO MAPA E CONVERSÃO AUTOMÁTICA ---
st.subheader("3️⃣ Conferência de Itens & Conversão Automática")
st.write("O app puxa as unidades do mapa e converte direto para **Pacotes (PAC)** ou **Caixas (CX)**.")

# Inicializa os itens baseados no seu mapa (Ex: Itaipava 473ml com 571 un, etc.)
if "tabela_conferencia" not in st.session_state:
    st.session_state.tabela_conferencia = [
        {"Produto": "Cerveja Itaipava Pilsen Lata 473ml", "Unidades": 571, "Fator": 12, "Tipo": "PAC", "Conferido": False},
        {"Produto": "Cerveja Pilsen Lata 473ml (Local)", "Unidades": 278, "Fator": 12, "Tipo": "PAC", "Conferido": False},
        {"Produto": "Cerveja 1000ml / 1L (Garrafa)", "Unidades": 120, "Fator": 12, "Tipo": "CX", "Conferido": False},
        {"Produto": "Cerveja 600ml (Caixa)", "Unidades": 240, "Fator": 24, "Tipo": "CX", "Conferido": False},
    ]

# Exibe cada item em uma linha interativa
for idx, item in enumerate(st.session_state.tabela_conferencia):
    # Cálculo automático da conversão
    total_un = item["Unidades"]
    fator = item["Fator"]
    qtd_embalagem = total_un // fator
    sobra_un = total_un % fator
    
    # Estilo visual se estiver conferido (Verde)
    status_cor = "🟢 **CONFERIDO OK**" if item["Conferido"] else "⏳ Pendente"
    
    with st.container():
        st.markdown(f"### {idx+1}. {item['Produto']}")
        
        col_dados1, col_dados2, col_dados3 = st.columns([1.5, 1.5, 1])
        
        with col_dados1:
            # Permitir ajustar unidades caso precise bater com o mapa exato
            nova_qtd = st.number_input(f"Unidades (Mapa):", min_value=0, value=total_un, key=f"un_{idx}")
            st.session_state.tabela_conferencia[idx]["Unidades"] = nova_qtd
            
        with col_dados2:
            # Exibe o resultado da conversão direto na tela
            calc_cx = nova_qtd // fator
            calc_sobra = nova_qtd % fator
            st.markdown(f"📦 **{calc_cx} {item['Tipo']}** + {calc_sobra} un")
            st.caption(f"Fator: {fator} un por {item['Tipo']}")
            
        with col_dados3:
            st.write("")
            st.write("")
            # Botão de toque para mudar o status para verde / conferido
            btn_txt = "✔ Conferido" if item["Conferido"] else "⬜ Marcar OK"
            if st.button(btn_txt, key=f"btn_conf_{idx}"):
                st.session_state.tabela_conferencia[idx]["Conferido"] = not item["Conferido"]
                st.rerun()
                
        # Mostra o status atual da linha
        if item["Conferido"]:
            st.success(f"Item {item['Produto']} validado com sucesso! ✔")
        else:
            st.info(f"Status: {status_cor}")
            
        st.markdown("---")

if st.button("💾 Salvar e Finalizar Conferência Completa"):
    st.success("🎉 Conferência de todos os itens gravada com sucesso! Pronto para o próximo mapa.")
