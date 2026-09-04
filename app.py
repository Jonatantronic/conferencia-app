    import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Conferência de Mapas - Importação", page_icon="📁", layout="centered")

st.markdown("## 📁 Painel de Conferência por Importação de Mapas")
st.write("Envie arquivos PDF ou fotos dos mapas escaneados pelo seu telemóvel para fazer a conferência.")

# --- 1. IMPORTAÇÃO DE MÚLTIPLOS MAPAS (PDF ou FOTO) ---
st.subheader("1️⃣ Importar Mapas (PDF ou Imagem)")
arquivos_enviados = st.file_uploader(
    "Selecione um ou vários mapas escaneados:", 
    type=["pdf", "png", "jpg", "jpeg"], 
    accept_multiple_files=True
)

if arquivos_enviados:
    st.success(f"📂 {len(arquivos_enviados)} mapa(s) importado(s) com sucesso!")
    
    # Mostra uma prévia ou o nome dos arquivos carregados
    for arq in arquivos_enviados:
        st.write(f"📄 **Arquivo carregado:** {arq.name}")

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

    # --- 3. CONVERSÃO AUTOMÁTICA DE CAIXAS / PACOTES ---
    st.subheader("3️⃣ Conversão por Tipo de Embalagem")
    
    tipo_cerveja = st.selectbox(
        "Selecione o padrão do produto:",
        [
            "Cerveja 473ml (Fardo/PAC com 12 un)", 
            "Cerveja 600ml (Caixa com 24 un)", 
            "Cerveja 1000ml / 1L (Caixa com 12 un)", 
            "Outro Padrão / Palete"
        ]
    )

    if "473ml" in tipo_cerveja:
        fator = 12
        nome_emb = "Pacotes (PAC)"
    elif "600ml" in tipo_cerveja:
        fator = 24
        nome_emb = "Caixas (CX)"
    elif "1000ml" in tipo_cerveja:
        fator = 12
        nome_emb = "Caixas (CX)"
    else:
        fator = st.number_input("Fator personalizado:", min_value=1, value=242)
        nome_emb = "Unidades"

    total_unidades_lido = st.number_input("Total de Unidades no mapa:", min_value=0, value=288, step=1)

    if fator > 0:
        qtd_cx_pac = total_unidades_lido // fator
        sobra = total_unidades_lido % fator
        st.info(f"📊 **Resultado:** **{qtd_cx_pac} {nome_emb}** e **{sobra} unidades**.")

    st.divider()

    # --- 4. CHECKLIST DO SEPARADOR E O V VERDE DO CONFERENTE ---
    st.subheader("4️⃣ Conferência de Itens")
    st.write("O separador valida o que pegou. O conferente dá o **✔ verde** final.")

    if "tabela_itens" not in st.session_state:
        st.session_state.tabela_itens = pd.DataFrame([
            {"Produto": "Cerveja 473ml", "Separador": False, "Conferente_OK": False},
            {"Produto": "Cerveja 600ml", "Separador": False, "Conferente_OK": False},
            {"Produto": "Cerveja 1000ml", "Separador": False, "Conferente_OK": False},
        ])

    for idx, row in st.session_state.tabela_itens.iterrows():
        c1, c2, c3 = st.columns([2, 1, 1])
        
        with c1:
            st.markdown(f"**{row['Produto']}**")
            
        with c2:
            sep = st.checkbox("Separado", value=row["Separador"], key=f"s_{idx}")
            st.session_state.tabela_itens.at[idx, "Separador"] = sep
            
        with c3:
            conf = st.checkbox("✔ OK", value=row["Conferente_OK"], key=f"c_{idx}")
            st.session_state.tabela_itens.at[idx, "Conferente_OK"] = conf
            if conf:
                st.markdown("<span style='color:green; font-weight:bold;'>✔ Validado</span>", unsafe_allow_html=True)

    st.divider()

    if st.button("💾 Finalizar Conferência Destes Mapas"):
        st.success("Conferência dos mapas salvos com sucesso!")
else:
    st.info("👆 Por favor,importe ao menos um mapa (PDF ou foto) para iniciar a conferência.")
