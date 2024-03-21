
import hydralit as hy
import streamlit as st

from SQLTOTEXT import Bot

## Configure Genai Key
## text to sql model
model=Bot(mode=2)
modes=['normal_mode','analytics_mode','english_qprompt']
model.db="hr.db"
app = hy.HydraApp(title='Secure Hydralit Data Explorer',favicon="🐙",hide_streamlit_markers=True,use_navbar=True, navbar_sticky=True)
st.sidebar.success("Chat")

@app.addapp()
def AiSho():



    ## Streamlit App

    
    st.header("Your AI assistant")

    question=st.text_area(" ")

    submit=st.button("Ask the question")

    # if submit is clicked
    if submit:
        display_text=model.eng_response(question)
        st.header(display_text)

app.run()






