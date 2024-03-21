
import hydralit as hy
import streamlit as st

from SQLTOTEXT import Bot

## Configure Genai Key
## text to sql model
model=Bot()
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
        english_res=model.eng_response(question)
        st.header(english_res)

@app.addapp()
def Payroll ():
    pass

@app.addapp()
def Leave():
    pass

def Calender ():
    pass

@app.addapp()
def Training():
    pass

@app.addapp()
def Analytics():
    pass

app.run()






