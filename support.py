import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
# import plotly.express as px
import db_code as db
import time

def support_page():
    if "uid" not in st.session_state:
        st.session_state.uid = st.session_state.user
    st.set_page_config(
        page_title="Support - Home",
        page_icon="👤",
        layout="wide",
    )

    st.markdown("""
    <style>
    .stApp{
    background:white;
    color:black;
    }
    .stButton {
    display:flex;
    justify-content:flex-end;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div style='display:flex;flex-direction: column;align-items:center;background-image:linear-gradient(purple,white);padding:5px;margin:0px;border-radius:20px;'>
    <h3 style='color:white;'>Support Team Dashboard</h3>
    <p style='color:white'>Manage, track, and resolve the client queries in real time.</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([22, 2])
    with col1:
        if "show_form" not in st.session_state:
            st.session_state.show_form = False

        if st.button("Register"):
            st.session_state.show_form = not st.session_state.show_form

        if st.session_state.show_form:
            col3, col4 = st.columns([1, 2])  # center column wider

            with col4:
                with st.form('register', width=500):
                    st.markdown(
                        "<h3 style='color:black;'>Register Form</h3>", unsafe_allow_html=True)
                    username = st.text_input('Enter a Username', width=500)
                    password = st.text_input(
                        'Enter a Password', type='password', width=500)
                    role = st.selectbox(
                        'Select a Role', ['Client', 'Support'], width=500)
                    phoneno=st.text_input("Enter a Phone Number",width=500)
                    
                    submit = st.form_submit_button("Submit")                    
                    if submit:
                        if username=="" or password=="" or role==""or phoneno=="":
                            st.error("Please fill all fields")
                        else:
                            if db.insert_user(username,password,role,phoneno,created_by=st.session_state.uid):
                                st.success("Registered successfully!")
                            else:
                                st.error("The Username is Already Registered")
    with col2:
        if st.button("Logout"):
            st.session_state.role = "login"
            st.rerun()

    with st.container():
        data=db.get_all_queries()
        
        df = pd.DataFrame(data)
        st.markdown("""
        <style>
        .stMetric{
        border-left:10px solid purple;
        box-shadow:3px 3px 20px black;
        text-align:center;
        border-radius:15px;
        padding:5px;
        width:75%;
        }
        </style>
        """, unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Queries", len(df))
        with col2:
            st.metric("Open", len(df[df['status'] == 'Open']))
        with col3:
            st.metric("Closed", len(df[df['status'] == 'Closed']))
        with col4:
            st.metric("Avg", round(len(df) / df["query_cat"].nunique(), 2))

        with st.form("search"):
            col1, col2 = st.columns(2)

            with col1:
                phoneno = st.text_input("Enter a Phone Number")

            with col2:
                query_status = st.selectbox(
                    "Status", ["All", "Open", "Closed"])

            submit = st.form_submit_button("Search")

        if submit:

            filtered_df = df.copy()

            # Filter by phone number
            if phoneno:
                filtered_df = filtered_df[filtered_df["phono"].str.contains(
                    phoneno)]

            # Filter by status
            if query_status != "All":
                filtered_df = filtered_df[filtered_df["status"]
                                          == query_status]

            st.dataframe(filtered_df, hide_index=True,
                         use_container_width=True)

        else:
            st.dataframe(df, hide_index=True,
                         use_container_width=True)

        with st.form("query_closed"):
            qid = st.text_input("Enter a Query Id to Close")
            if st.form_submit_button():
                filtered = df[df["query_id"] == qid]
                if not filtered.empty:
                    if filtered['status'].iloc[0]=='Open':
                        res=db.close_query(int(qid.lstrip("Q")))
                        if res:
                            st.toast("Query Closed Successfully!!!",icon='✅')
                            time.sleep(1.5)
                            st.rerun()
                        else:
                            st.toast("Invalid Query or Query Already Closed!!!",icon="❌")
                    else:
                        st.toast("Query Already Closed!!!",icon="❌")
                else:
                    st.toast("Invalid Query ID!!!",icon="❌")

        st.markdown("""
        <style>
        .stForm{
        border:2px solid grey !important;
        }
        .stForm:hover{
            border:2px solid black !important;
        }
        </style>
        """, unsafe_allow_html=True)

        col1, col2= st.columns(2)
        with col1:
            status_counts = df["status"].value_counts()
            # Create pie chart
            fig, ax = plt.subplots()

            ax.pie(
                status_counts,
                labels=status_counts.index,
                autopct="%1.0f%%",
                startangle=90
            )

            ax.axis("equal")
            st.pyplot(fig)

        with col2:
            category_counts = df["query_cat"].value_counts()

            fig, ax = plt.subplots()

            ax.bar(
                category_counts.index,
                category_counts.values,
                color=["skyblue", "orange", "green", "purple", "red"]
            )

            ax.set_title("Queries by Category")
            ax.set_xlabel("query_cat")
            ax.set_ylabel("Count")

            plt.xticks(rotation=45)

            st.pyplot(fig)

        if "reset_form" not in st.session_state:
            st.session_state.reset_form = False

        if st.button("Reset Password"):
            st.session_state.reset_form = not st.session_state.reset_form

    if st.session_state.reset_form:
        col3, col4, col5 = st.columns([1, 2, 1])  # center column wider
        st.markdown("""
        <style>
        .stForm{
        border:2px solid grey !important;
        }
        .stForm:hover{
            border:2px solid black !important;
        }
        </style>
        """, unsafe_allow_html=True)
        with col4:
            with st.form('Reset', border=True):
                st.markdown(
                    "<h3 style='color:black;'>Password Reset</h3>", unsafe_allow_html=True)
                old_password = st.text_input(label="Old Password")
                new_password = st.text_input(label="New Password")
                confirm_password = st.text_input(label="Confirm Password")
                if st.form_submit_button():
                    if new_password != confirm_password:
                        st.toast("Password Not Matched",icon='❌')
                        return
                    else:
                        if db.update_password(username=st.session_state.uid,old_pwd=old_password,new_pwd=new_password):
                            st.toast("password Changed",icon='✅')
                        else:
                            st.toast("password unchanged",icon='❌')
    st.markdown("""
            <div style="
                background-color:#2b2f33;
                padding:20px;
                border-radius:10px;
                color:white;
                height:100%;
                display:flex;
                flex-direction:column;
                align-items:center;
            ">
            <h4>About the Support Dashboard</h4>
            <p>
                Our support team is available to assist you with any issues or inquiries.
    We aim to provide timely and effective solutions.                
            </p>
            <p>📍 <b>Chennai, Tamilnadu</b></p>
            <p>📞 +91 90804 10927</p>
            <p>✉️ support@query.com</p>
            </div>
            """, unsafe_allow_html=True)
