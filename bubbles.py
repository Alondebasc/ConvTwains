import streamlit as st
import os

def parse_chat(content):
    """
    Analyse le contenu du fichier texte et retourne les messages formatés.
    """
    chat = []
    lines = content.split("\n")
    for line in lines:
        if "USER:" in line:
            timestamp, message = line.split("USER: ")
            time = timestamp.split(" ")[1][:5]  # hh:mm
            for part in message.split("\n"):
                if part.strip():  # Ignore empty messages
                    chat.append(("user", part.strip(), time))
        elif "TWAIN:" in line:
            timestamp, message = line.split("TWAIN: ")
            time = timestamp.split(" ")[1][:5]
            for part in message.split("|"):
                if part.strip():  # Ignore empty messages
                    chat.append(("bot", part.strip(), time))
    return chat

def display_chat(chat_data):
    """
    Affiche les messages sous forme de bulles avec horodatage.
    """
    for role, message, time in chat_data:
        if role == "user":
            st.markdown(f"""
                <div style="text-align: right; margin: 5px;">
                    <div style="display: inline-block; background-color: #FFD700; color: black; padding: 10px; border-radius: 10px; max-width: 60%;">
                        <small style="font-size: 10px; color: #333333;">USER</small><br>
                        {message}
                        <div style="text-align: right; font-size: 8px; color: grey;">{time}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="text-align: left; margin: 5px;">
                    <div style="display: inline-block; background-color: #333333; color: #FFD700; padding: 10px; border-radius: 10px; max-width: 60%;">
                        <small style="font-size: 10px; color: #FFD700;">Twains</small><br>
                        {message}
                        <div style="text-align: left; font-size: 8px; color: grey;">{time}</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)

# Streamlit Interface
def main():
    st.set_page_config(page_title="Twains Chat Viewer", layout="wide")
    st.title("📜 Twains Chat Viewer")
    st.markdown("Uploadez un fichier `.txt` contenant des conversations pour les afficher sous forme de chat.")

    # Upload file
    uploaded_file = st.file_uploader("Téléchargez un fichier .txt", type=["txt"])
    
    if uploaded_file:
        try:
            content = uploaded_file.getvalue().decode("utf-8")
            chat_data = parse_chat(content)

            st.sidebar.header("Options")
            st.sidebar.write(f"📂 Nom du fichier : `{uploaded_file.name}`")
            st.sidebar.write(f"💬 Nombre de messages : `{len(chat_data)}`")

            # Display chat
            st.subheader("Discussion")
            display_chat(chat_data)
        except Exception as e:
            st.error(f"Erreur lors de l'analyse du fichier : {e}")

if __name__ == "__main__":
    main()
