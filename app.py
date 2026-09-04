import streamlit as st
import pandas as pd

st.set_page_config(page_title="Conferência de Mapas", page_icon="📦", layout="centered")

# Limpa qualquer memória antiga ao iniciar do zero
if "reset_inicial" not in st.session_state:
    st.session_state.clear()
    st.session_state.reset_inicial = True

st.markdown("## 📦 Conferência de Carga por Mapa")
st.write("Cadastre seus fatores, envie a foto do mapa e faça a conferência com conversão automática.")

# --- 1. BANCO DE DADOS DE FATORES ---
st.subheader("1️⃣ Banco de Dados de Embalagens (Fatores)")
st.write("Cadastre o produto e quantas unidades vão em cada caixa ou pacote.")

if "banco_fatores" not in st.session_state:
    st.session_state.banco_fatores = {}

with st.expander("➕ Cadastrar Novo Produto e Fator"):
    prod_nome = st.text_input("Nome do Produto:", placeholder="Ex: Cerveja Lata 473ml")
    c1, c2 = st.columns(2)
    with c1:
        prod_fator = st.number_input("Unidades por Caixa/Pacote:", min_value=1, value=12)
    with c2:
        prod_tipo = st.selectbox("Tipo:", ["PAC", "CX"])
        
    if st.button("Salvar no Banco de Dados"):
        if prod_nome:
            st.session_state.banco_fatores[prod_nome] = {"fator": prod_fator, "tipo": prod_tipo}
            st.success(f"'{prod_nome}' cadastrado com sucesso!")
            st.rerun()
        else:
            st.warning("Digite o nome do produto.")

# Mostra os produtos já cadastrados pelo usuário
if len(st.session_state.banco_fatores) > 0:
    st.write("Produtos cadastrados:")
    for p, inf in st.session_state.banco_fatores.items():
        st.caption(f"• **{p}**: {inf['fator']} un por {inf['tipo']}")
else:
    st.info("Nenhum produto cadastrado ainda. Cadastre acima para usar na conversão.")

st.divider()

# --- 2. UPLOAD DA FOTO DO MAPA ---
st.subheader("2️⃣ Upload da Foto do Mapa")
foto_mapa = st.file_uploader("Envie a foto do mapa para conferência:", type=["png", "jpg", "jpeg", "webp"])

if foto_mapa is not None:
    st.image(foto_mapa, caption="📄 Mapa enviado", use_column_width=True)
    st.success("Foto carregada com sucesso!")

st.divider()

# --- 3. LISTA DE CONFERÊNCIA E CONVERSÃO ---
st.subheader("3️⃣ Lista de Conferência do Mapa")

if "lista_conferencia" not in st.session_state:
    st.session_state.lista_conferencia = []

# Adicionar item à conferência
with st.expander("➕ Adicionar Item para Conferir"):
    if len(st.session_state.banco_fatores) > 0:
        item_escolhido = st.selectbox("Selecione o Produto:", list(st.session_state.banco_fatores.keys()), key="sel_prod")
        qtd_mapa = st.number_input("Unidades totais no mapa:", min_value=1, value=100, key="qtd_mapa")
        
        if st.button("Adicionar à Lista de Conferência"):
            st.session_state.lista_conferencia.append({
                "produto": item_escolhido,
                "unidades": qtd_mapa,
                "conferido": False
            })
            st.success("Item adicionado!")
            st.rerun()
    else:
        st.warning("Cadastre pelo menos um produto no Banco de Dados (Passo 1) antes de adicionar itens.")

st.write("---")

# Exibe a lista de itens limpa e interativa
if len(st.session_state.lista_conferencia) > 0:
    for i, item in enumerate(st.session_state.lista_conferencia):
        p_nome = item["produto"]
        p_unidades = item["unidades"]
        
        # Pega o fator cadastrado
        dados = st.session_state.banco_fatores.get(p_nome, {"fator": 12, "tipo": "PAC"})
        fator = dados["fator"]
        tipo = dados["tipo"]
        
        with st.container():
            status_icone = "🟢" if item["conferido"] else "📦"
            st.markdown(f"**{status_icone} Item {i+1}: {p_nome}**")
            
            col_a, col_b, col_c = st.columns([1.2, 1.3, 1])
            
            with col_a:
                nova_qtd = st.number_input("Unidades:", min_value=0, value=p_unidades, key=f"q_{i}")
                st.session_state.lista_conferencia[i]["unidades"] = nova_qtd
                
            with col_b:
                # Conversão automática solicitada
                qtd_convertida = nova_qtd // fator
                sobra = nova_qtd % fator
                st.markdown(f"📊 **{qtd_convertida} {tipo}** + {sobra} un")
                st.caption(f"Fator: {fator} un/{tipo}")
                
            with col_c:
                st.write("")
                # Botão de visto verde / OK
                if item["conferido"]:
                    if st.button("✅ Conferido", key=f"btn_{i}"):
                        st.session_state.lista_conferencia[i]["conferido"] = False
                        st.rerun()
                    st.success("OK ✔")
                else:
                    if st.button("⬜ Marcar OK", key=f"btn_{i}"):
                        st.session_state.lista_conferencia[i]["conferido"] = True
                        st.rerun()
                    st.warning("Pendente ⏳")
                    
            st.markdown("---")
            
    if st.button("💾 Finalizar Conferência"):
        st.success("🎉 Conferência salva com sucesso!")
else:
    st.info("Nenhum item adicionado à conferência ainda. Use a opção acima para incluir os itens do mapa.")
