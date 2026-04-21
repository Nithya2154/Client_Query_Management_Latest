import client
import streamlit as st
import support
import db_code as db
st.set_page_config(
    page_title="CQMS - Login",
    page_icon="🎯",
    layout="wide",                    # "centered" (default) or "wide"
)
st.markdown("""
<style>
.st-emotion-cache-zy6yx3 {
    width: 100%;
    padding: 2rem 1rem 0rem;
    max-width: initial;
    min-width: auto;
}
.stApp{
margin:0px;
background-image:linear-gradient(purple,white);
}
h1,h2{
color:white !important;
}
h2{
text-decoration: underline solid white 2px !important;
}
.stTextInput label p, 
.stSelectbox label p {
    font-size:15px !important;
}
.stForm{
background:white;
}
.stForm:hover{
border-color:white;
box-shadow: 3px 3px 15px white !important;
}
</style>
""", unsafe_allow_html=True)
# st.title("CLIENT QUERY MANAGEMENT SYSTEM")
if "role" not in st.session_state:
    st.session_state.role = "login"
if "user" not in st.session_state:
    st.session_state.user = ""
if "password" not in st.session_state:
    st.session_state.password = ""
if "reset_form" not in st.session_state:
    st.session_state.reset_form = False
if st.session_state.role == "login":
    col1, col2, col3 = st.columns(3)
    with col2:
        st.header("Login Page")
        if st.session_state.reset_form:
            st.session_state.user = ""
            st.session_state.password = ""
            st.session_state.reset_form = False
        with st.form("login_form"):
            username = st.text_input(label="Username", key="user")
            user_error = st.empty()
            password = st.text_input(
                label="Password", type="password", key="password")
            pass_error = st.empty()
            role = st.selectbox(options=["Client", "Support"], label="Role")
            col1, col2 = st.columns([6, 2])
            loginbutton = col1.form_submit_button("Login")
            cancel = col2.form_submit_button("Cancel")
            if loginbutton:
                valid = True
                if not username:
                    valid = False
                    user_error.error("Please Enter a Username")
                else:
                    user_error.empty()
                if not password:
                    valid = False
                    pass_error.error("Please Enter a Password")
                else:
                    pass_error.empty()
                res=db.check_login(username,password,role)
                # print(res)
                if res[0]:
                    valid=True
                else:
                    st.error(res[1])
                    valid=False
                if valid:
                    if role == 'Client':
                        st.session_state.role = "client"
                        if "phono" not in st.session_state:
                              st.session_state.phono = res[2]
                        st.rerun()
                    elif role == 'Support':
                        st.session_state.role = "support"
                        st.rerun()
            if cancel:
                st.session_state.reset_form = True
                st.rerun()

if st.session_state.role == "client":
    client.client_page()

if st.session_state.role == "support":
    support.support_page()
