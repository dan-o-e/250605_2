import pandas as pd
import streamlit as st
from io import BytesIO

# 🔄 Função para gerar Excel
def gerar_excel(df, formato='xlsx'):
    buffer = BytesIO()
    if formato == 'xlsx':
        df.to_excel(buffer, index=False, engine='openpyxl')
    else:
        df.to_excel(buffer, index=False, engine='xlwt')
    buffer.seek(0)
    return buffer

# 🚀 Configuração inicial
st.set_page_config(page_title="CSV ➜ Excel com Filtros Avançados", layout="wide")
st.title("📤 Exportador de CSV para Excel com Filtros Avançados")

# 📤 Upload do CSV
uploaded_file = st.file_uploader("📁 Faça o upload do seu arquivo .csv", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.success("✅ CSV carregado com sucesso!")

        st.subheader("👁️ Visualização Inicial dos Dados")
        st.dataframe(df.head(10), use_container_width=True)

        st.subheader("🎯 Filtros Interativos")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 🔠 Filtros Categóricos")
            for coluna in df.select_dtypes(include="object").columns:
                if df[coluna].nunique() <= 30:
                    opcoes = df[coluna].dropna().unique().tolist()
                    selecionados = st.multiselect(f"{coluna}", options=opcoes, key=coluna)
                    if selecionados:
                        df = df[df[coluna].isin(selecionados)]

        with col2:
            st.markdown("#### 🔢 Filtros Numéricos")
            for coluna in df.select_dtypes(include=["int64", "float64"]).columns:
                min_val = float(df[coluna].min())
                max_val = float(df[coluna].max())
                if min_val != max_val:
                    faixa = st.slider(
                        f"{coluna}",
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                        step=(max_val - min_val) / 100,
                    )
                    df = df[df[coluna].between(faixa[0], faixa[1])]

        st.write(f"🔎 Total de registros após filtros: {len(df)}")

        st.subheader("📁 Exportar Arquivo")

        formato = st.radio("Selecione o formato para exportação:", options=["xlsx", "xls"])
        excel_data = gerar_excel(df, formato=formato)

        st.download_button(
            label=f"📥 Baixar dados filtrados (.{formato})",
            data=excel_data,
            file_name=f"{uploaded_file.name.split('.')[0]}_filtrado.{formato}",
            mime="application/vnd.ms-excel" if formato == "xls"
            else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"Erro ao processar o CSV: {e}")
else:
    st.info("🕒 Aguardando upload de um arquivo .csv.")

# Para executar a aplicação, use o comando:
# streamlit run app_excel_upload_export_filtros_full.py
