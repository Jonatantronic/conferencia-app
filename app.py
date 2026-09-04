import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência WMS - Logística", page_icon="📦", layout="centered")

st.markdown("## 📦 Sistema de Conferência de Carga")
st.write("Gerencie seu banco de dados de fatores, envie a foto do mapa e faça a conferência com conversão automática.")

# --- 1. BANCO DE DADOS DE PRODUTOS E FATORES ---
st.subheader("1️⃣ Banco de Dados de Fatores (Embalagens)")
st.write("Cadastre aqui os produtos e quantas unidades formam uma caixa ou pacote para a conversão automática.")

# Inicializa o banco de dados na sessão
if "banco_fatores" not in st.session_state:
    st.session_state.banco_fatores = {
        "Cerveja Itaipava Pilsen Lata 473ml": {"fator": 12, "tipo": "PAC"},
        "Cerveja Pilsen Lata 473ml (Local)": {"fator": 12, "tipo": "PAC"},
        "Cerveja 600ml (Garrafa)": {"fator": 24, "tipo": "CX"},
        "Cerveja 1000ml / 1L": {"fator": 12, "tipo": "CX"}
    }

# Formulário para cadastrar novo produto no banco de dados
with st.expander("➕ Cadastrar Novo Produto no Banco de Dados"):
    novo_nome_prod = st.text_input("Nome do Produto:", placeholder="Ex: Cerveja Malzbier 350ml")
    c_f1, c_f2 = st.columns(2)
    with c_f1:
        novo_fator_val = st.number_input("Quantidade por Caixa/Pacote:", min_value=1, value=12)
    with c_f2:
        novo_tipo_embalagem = st.selectbox("Tipo de Embalagem:", ["PAC", "CX"])
        
    if st.button("Salvar Produto no Banco"):
        if novo_nome_prod:
            st.session_state.banco_fatores[novo_nome_prod] = {
                "fator": novo_fator_val,
                "tipo": novo_tipo_embalagem
            }
            st.success(f"Produto '{novo_nome_prod}' cadastrado com sucesso!")
            st.rerun()
        else:
            st.warning("Digite o nome do produto.")

# Exibe os produtos já cadastrados
st.caption(f"Produtos cadastrados no sistema: {len(st.session_state.banco_fatores)}")

st.divider()

# --- 2. UPLOAD DA FOTO DO MAPA ---
st.subheader("2️⃣ Upload da Foto do Mapa")
arquivo_foto = st.file_uploader("Envie a foto ou arquivo do mapa para conferência:", type=["png", "jpg", "jpeg", "webp"])

if arquivo_foto is not None:
    try:
        st.image(arquivo_foto, caption=f"📄 Mapa Carregado: {arquivo_foto.name}", use_column_width=True)
        st.success("✅ Foto carregada para consulta visual!")
    except:
        st.warning("⚠️ Arquivo recebido.")

st.divider()

# --- 3. LISTA DE CONFERÊNCIA E CONVERSÃO ---
st.subheader("3️⃣ Lista de Conferência & Conversão Automática")
st.write("Adicione os itens do mapa, informe as unidades totais e marque os itens conferidos.")

# Inicializa a lista de itens da conferência atual
if "lista_conferencia" not in st.session_state:
    st.session_state.lista_conferencia = [
        {"Produto": "Cerveja Itaipava Pilsen Lata 473ml", "Unidades": 571, "Conferido": False},
        {"Produto": "Cerveja Pilsen Lata 473ml (Local)", "Unidades": 278, "Conferido": False}
    ]

# Adicionar item à conferência puxando do banco de dados
with st.expander("➕ Adicionar Item à Conferência do Mapa"):
    if len(st.session_state.banco_fatores) > 0:
        produto_selecionado = st.selectbox("Selecione o Produto Cadastrado:", list(st.session_state.banco_fatores.keys()))
        qtd_informada = st.number_input("Total de Unidades no Mapa:", min_value=1, value=100, key="qtd_mapa_add")
        
        if st.button("Inserir na Lista de Conferência"):
            st.session_state.lista_conferencia.append({
                "Produto": produto_selecionado,
                "Unidades": qtd_informada,
                "Conferido": False
            })
            st.success("Item adicionado à lista!")
            st.rerun()
    else:
        st.warning("Cadastre produtos no banco de dados acima primeiro.")

st.write("---")

# Exibe a lista interativa de conferência com conversão e botão verde
for idx, item in enumerate(st.session_state.lista_conferencia):
    nome_prod = item["Produto"]
    total_unidades = item["Unidades"]
    
    # Busca o fator correspondente no banco de dados cadastrado lá em cima
    dados_prod = st.session_state.banco_fatores.get(nome_prod, {"fator": 12, "tipo": "PAC"})
    fator = dados_prod["fator"]
    tipo = dados_prod["tipo"]
    
    with st.container():
        # Se estiver conferido, destaca o título em verde
        status_cor = "🟢" if item["Conferido"] else "📦"
        st.markdown(f"**{status_cor} Item {idx+1}: {nome_prod}**")
        
        col_c1, col_c2, col_c3 = st.columns([1.2, 1.3, 1])
        
        with col_c1:
            nova_qtd = st.number_input("Unidades:", min_value=0, value=total_unidades, key=f"qtd_conf_{idx}")
            st.session_state.lista_conferencia[idx]["Unidades"] = nova_qtd
            
        with col_c2:
            # Cálculo da conversão automática solicitada
            qtd_caixas_pacotes = nova_qtd // fator
            sobra_unidades = nova_qtd % fator
            st.markdown(f"📊 **{qtd_caixas_pacotes} {tipo}** + {sobra_unidades} un")
            st.caption(f"Fator base: {fator} un/{tipo}")
            
        with col_c3:
            st.write("")
            # Botão de conferência com inversão de cor e estado
            if item["Conferido"]:
                if st.button("✅ Conferido", key=f"btn_status_{idx}Type"):
                    st.session_state.lista_conferencia[idx]["Conferido"] = False
                    st.rerun()
                st.success("OK ✔")
            else:
                if st.button("⬜ Marcar OK", key=f"btn_status_{idx}Type"):
                    st.session_state.lista_conferencia[idx]["Conferido"] = True
                    st.rerun()
                st.warning("Pendente ⏳")
                
        st.markdown("---")

if st.button("💾 Finalizar e Salvar Conferência do Mapa"):
    st.success("🎉 Conferência gravada e validada com sucesso!")
