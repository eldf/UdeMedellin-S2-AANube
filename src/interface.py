import streamlit as st

# (Aquí importarías tu lógica de simulate_prediction)

st.title("Simulador de Fraude Bancario 🏦")
amount = st.slider("Monto de la transacción", 0, 20000, 100)
v1 = st.number_input("Parámetro V1", value=0.0)
# ... más inputs ...

if st.button("Validar Transacción"):
    # Llamas a tu modelo
    st.write("Procesando...")
    # st.success("Resultado: ...")
