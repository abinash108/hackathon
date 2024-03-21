import streamlit as st


from SQLTOTEXT import Bot

tab1, tab2 = st.tabs(["🗃 DaTaBoT","📈 files" ])
model=Bot(mode=2)
modes=['normal_mode','analytics_mode','english_qprompt']
model.db="hr.db"
file_output=False
## Add background image

tab1.title("DaTaBoT")
st.sidebar.info("Welcome")
data,chat=False,False
def on_click_data(model):
    model.mode=2
def on_click_chat(model):
    model.mode=0    
data=st.sidebar.button("Data_mode",on_click=on_click_data(model))
chat=st.sidebar.button("Chat_mode",on_click=on_click_chat(model))
        



container_output = tab1.container(border=True,height=400)
# Define markdown with colored characters for each half

    
  
  


    
question=tab1.text_area("Enter the query",height=10,max_chars=200)

submit=tab1.button("Submit")

    
    # if submit is clicked
if submit:
    display_text=model.eng_response(question)
    container_output.write(display_text)
if model.cache_data is not None and model.mode==2:
    file_output=True
if file_output:
    tab2.write("here is the file associated with data")
    tab2.write(model.cache_data)
else:
    tab2.write("No files requested ")    