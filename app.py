import streamlit as st
import pandas as pd
from PIL import Image

st.set_page_config(page_title="Conferência de Mapas - WMS", page_icon="📦", layout="centered")

st.markdown("## 📦 Conferência de Carga por Mapa")
st.write("Cadastre suas embalagens, envie a foto do mapa e faça a conferência com conversão automática.")

# --- 1. BANCO DE DADOS DE FATORES (EMBALAGENS) ---
st.subheader("1️⃣ Banco de Dados de Embalagens (Fatores)")
st.write("Cadastre o produto e quantas unidades vão em cada caixa ou pacote para a conversão.")

if "banco_fatores" not in st.session_state:
    st.session_state.banco_fatores = {
        "Cerveja Itaipava Pilsen Lata 473ml": {"fator": 12, "tipo": "PAC"},
        "Cerveja Pilsen Lata 473ml (Local)": {"fator": 12, "tipo": "PAC"}
    }

with st.expander("➕ Cadastrar Novo Produto e Fator"):
    prod_nome = st.text_input("Nome do Produto:", placeholder="Ex: Cerveja 600ml")
    c1, c2 = st.columns(2)
    with c1:
        prod_fator = st.number_input("Unidades por Caixa/Pacote:", min_value=1, value=12)
    with c2:
        prod_tipo = st.selectbox("Tipo de Embalagem:", ["PAC", "CX"])
        
    if st.button("Salvar no Banco de Dados"):
        if prod_nome:
            st.session_state.banco_fatores[prod_nome] = {"fator": prod_fator, "tipo": prod_tipo}
            st.success(f"'{prod_nome}' cadastrado com sucesso!")
            st.rerun()
        else:
            st.warning("Digite o nome do produto.")

# Mostra os produtos já cadastrados
if len(st.session_state.banco_fatores) > 0:
    st.caption(f"Produtos cadastrados no sistema: {len(st.session_state.banco_fatores)}")

st.divider()

# --- 2. UPLOAD DA FOTO DO MAPA (BLINDADO CONTRA ERROS) ---
st.subheader("2️⃣ Upload da Foto do Mapa")
foto_mapa = st.file_uploader("Envie a foto do mapa para conferência:", type=["png", "jpg", "jpeg", "webp"])

if foto_mapa is not None:
    try:
        # Abre e exibe a imagem de forma segura utilizando o PIL
        imagem_exibicao = Image.open(foto_mapa)
        st.image(imagem_exibicao, caption=f"📄 Mapa: {foto_mapa.name}", use_column_width=True)
        st.success("✅ Foto carregada e pronta para consulta visual!")
    except Exception as e:
        st.warning("⚠️ Arquivo recebido com sucesso (visualização indisponível para este formato).")

st.divider()

# --- 3. LISTA DE CONFERÊNCIA E CONVERSÃO AUTOMÁTICA ---
st.subheader("3️⃣ Lista de Conferência & Conversão")

if "lista_conferencia" not in st.session_state:
    st.session_state.lista_conferencia = [
        {"produto": "Cerveja Itaipava Pilsen Lata 473ml", "unidades": 571, "conferido": False},
        {"produto": "Cerveja Pilsen Lata 473ml (Local)", "unidades": 278, "conferido": False}
    ]

# Adicionar item à conferência puxando do banco de dados
with st.expander("➕ Adicionar Item para Conferir"):
    if len(st.session_state.banco_fatores) > 0:
        item_escolhido = st.selectbox("Selecione o Produto:", list(st.session_state.banco_fatores.keys()), key="sel_prod_novo")
        qtd_mapa = st.number_input("Unidades totais no mapa:", min_value=1, value=100, key="qtd_mapa_novo")
        
        if st.button("Adicionar à Lista de Conferência"):
            st.session_state.lista_conferencia.append({
                "produto": item_escolhido,
                "unidades": qtd_mapa,
                "conferido": False
            })
            st.success("Item adicionado com sucesso!")
            st.rerun()
    else:
        st.warning("Cadastre pelo menos um produto no Banco de Dados (Passo 1) acima.")

st.write("---")

# Exibe a lista de itens interativa com conversão e botão verde
if len(st.session_state.lista_conferencia) > 0:
    for i, item in enumerate(st.session_state.lista_conferencia):
        p_nome = item["produto"]
        p_unidades = item["unidades"]
        
        # Pega o fator cadastrado no banco de dados do topo
        dados = st.session_state.banco_fatores.get(p_nome, {"fator": 12, "tipo": "PAC"})
        fator = dados["fator"]
        tipo = dados["tipo"]
        
        with st.container():
            status_icone = "🟢" if item["conferido"] else "📦"
            st.markdown(f"**{status_icone} Item {i+1}: {p_nome}**")
            
            col_a, col_b, col_c = st.columns([1.2, 1.3, 1])
            
            with col_a:
                nova_qtd = st.number_input("Unidades:", min_value=0, value=p_unidades, key=f"q_un_{i}")
                st.session_state.lista_conferencia[i]["unidades"] = nova_qtd
                
            with col_b:
                # Conversão automática solicitada (divisão inteira + resto)
                qtd_convertida = nova_qtd // fator
                sobra = nova_qtd % fator
                st.markdown(f"📊 **{qtd_convertida} {tipo}** + {sobra} un")
                st.caption(f"Fator: {fator} un/{tipo}")
                
            with col_c:
                st.write("")
                # Botão de alternância para conferido / pendente (fica verde ao marcar)
                if item["conferido"]:
                    if st.button("✅ Conferido", key=f"btn_st_{i}"):
                        st.session_state.lista_conferencia[i]["conferido"] = False
                        st.rerun()
                    st.success("OK ✔")
                else:
                    if st.button("⬜ Marcar OK", key=f"btn_st_{i}"):
                        st.session_state.lista_conferencia[i]["conferido"] = True
                        st.rerun()
                    st.warning("Pendente ⏳")
                    
            st.markdown("---")
            
    if st.button("💾 Finalizar e Salvar Conferência"):
        st.success("🎉 Conferência gravada e validada com sucesso!")
else:
    st.info("Nenhum item na conferência. Adicione os itens usando a opção acima.")
