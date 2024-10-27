import streamlit as st
from src.agente_agricola import AgenteAgricola  

agente_agricola = AgenteAgricola()

st.set_page_config(page_title="Agro Amigo", page_icon="🌾")

st.title("Agro Amigo 🌱")
st.write("""
    Bienvenido al Chat Bot Agrícola, tu asistente virtual diseñado para responder tus preguntas sobre técnicas de cultivo, 
    mejores prácticas agrícolas y consejos financieros específicos para los campesinos colombianos 👨‍🌾 
    Pregunta lo que necesites y obtén respuestas rápidas y prácticas.
""")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("¿En qué puedo ayudarte?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        respuesta = agente_agricola.preguntar(user_input) 
        message_placeholder.markdown(respuesta)

    st.session_state.messages.append({"role": "assistant", "content": respuesta})
