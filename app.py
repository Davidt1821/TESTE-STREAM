import streamlit as st
from fpdf import FPDF
import datetime

# 1. TELA INICIAL (A "Fachada" do SketchUp)
st.title("🚀 Sistema de Vendas - Engenharia ")
st.subheader("Gerador de Orçamentos e Pedidos")

# Criando a lista de materiais na memória (o carrinho)
if 'carrinho' not in st.session_state:
    st.session_state.carrinho = []

# 2. CAIXA DE DIÁLOGO (Formulário de Inserção)
with st.form("meu_formulario"):
    material = st.text_input("Nome do Material (ex: Cimento CP-II)")
    quantidade = st.number_input("Quantidade", min_value=1)
    preco_unitario = st.number_input("Preço Unitário (R$)", min_value=0.0, format="%.2f")
    
    botao_inserir = st.form_submit_button("Inserir no Orçamento")

    if botao_inserir:
        total_item = quantidade * preco_unitario
        st.session_state.carrinho.append({
            "material": material,
            "qtd": quantidade,
            "preco": preco_unitario,
            "total": total_item
        })
        st.success(f"{material} adicionado!")

# 3. EXIBIÇÃO DOS VALORES NA TELA
if st.session_state.carrinho:
    st.write("### Itens no Pedido")
    total_geral = 0
    for item in st.session_state.carrinho:
        st.write(f"✅ {item['material']} | {item['qtd']} x R$ {item['preco']} = *R$ {item['total']:.2f}*")
        total_geral += item['total']
    
    st.markdown(f"## TOTAL DA VENDA: R$ {total_geral:.2f}")

    # 4. GERAR O PDF A4 (O "Render" Final)
    if st.button("Gerar PDF para Impressão"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="ORÇAMENTO DE MATERIAIS", ln=True, align='C')
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Data: {datetime.date.today()}", ln=True, align='L')
        pdf.ln(10) # Espaço
        
        for item in st.session_state.carrinho:
            linha = f"{item['material']} - Qtd: {item['qtd']} - Unit: R${item['preco']} - Total: R${item['total']}"
            pdf.cell(200, 10, txt=linha, ln=True)
            
        pdf.ln(10)
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(200, 10, txt=f"TOTAL GERAL: R$ {total_geral:.2f}", ln=True)
        
        pdf.output("orcamento.pdf")
        st.success("PDF gerado com sucesso! Arquivo: orcamento.pdf")

      