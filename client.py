import streamlit as st
import db_code as db

def client_page():
    if "uid" not in st.session_state:
        st.session_state.uid = st.session_state.user
    if "pno" not in st.session_state:
        st.session_state.pno = st.session_state.phono
    st.set_page_config(
        page_title="Client - Home",
        page_icon="👤",
        layout="wide",
    )
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
    <div style='display:flex;flex-direction: column;align-items:center;background-image:linear-gradient(purple,white);padding:5px;margin:0px;border-radius:20px;width: 100%;'>
    <h3 style='color:white;'>Client Portal</h3>
    <p style='color:white'>Hello {st.session_state.uid} - submit a query or track your existing ones.</p>    
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([20, 2])
    with col2:
        if st.button("Logout"):
            st.session_state.role = "login"
            st.rerun()

    st.markdown("""
        <style>
        .stContainer{
        border:2px solid black !important;    
        }
        </style>
        """, unsafe_allow_html=True)
    with st.container():
        st.subheader("Submit a New Query")

        with st.form("new_query_form"):

            col1, col2, col3 = st.columns(3)

            with col1:
                email = st.text_input("Email Address *")

            with col2:
                mobile = st.text_input("Mobile Number *",value=st.session_state.pno,disabled=True)
            with col3:
                category = st.selectbox(
                    "Query Category *",
                    [
                        "Login Issue",
                        "Payment Failed",
                        "Refund Request",
                        "Account Locked",
                        "Wrong Item Delivered",
                        "Slow App Performance",
                        "Subscription Renewal",
                        "Profile Update Error",
                        "Password Reset",
                        "Order Tracking",
                        "Billing Discrepancy",
                        "Feature Request",
                        "Data Export Issue",
                        "Notification Settings",
                        "Other"
                    ]
                )
            description = st.text_area("Query Description")
            submit = st.form_submit_button("Submit Query")

        if submit:
            if email == "" or mobile == "" or description == "":
                st.error("Please fill all required fields")
            else:
                res=db.insert_query(email,mobile,category,description)
                if res:
                    st.toast(f"Query submitted successfully!",icon='✅')
                else:
                    st.error("Invalid Datas!")

    with st.container():
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
        st.subheader("📋 My Query History")
        df=db.get_all_queries()
        df=df[df['phono']==st.session_state.pno]
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Queries", len(df))

        with col2:
            st.metric("Open", (df['status'] == 'Open').sum())

        with col3:
            st.metric("Closed", (df['status'] == 'Closed').sum())
        st.markdown("""
                    <style>
                    .ticket-card {
                        border: 1px solid #e5e7eb;
                        border-left: 6px solid #22c55e;
                        border-radius: 8px;
                        padding: 16px;
                        background-color: #f9fafb;
                        margin-bottom: 10px;
                    }

                    .ticket-title {
                        font-size: 22px;
                        font-weight: 600;
                    }

                    .ticket-meta {
                        color: #6b7280;
                        font-size: 14px;
                    }

                    .ticket-desc {
                        margin-top: 8px;
                        color: #374151;
                    }

                    .status-badge {
                        float: right;
                        background-color: #d1fae5;
                        color: #065f46;
                        padding: 4px 10px;
                        border-radius: 20px;
                        font-size: 13px;
                        font-weight: 600;
                    }
                    </style>
                    """, unsafe_allow_html=True)
        
        st.table(df)
        tickets = []

        for i in range(len(df)):
            ticket = {
                "id": df['query_id'].iloc[i],
                "title": df['query_cat'].iloc[i],
                "submitted": df['created_time'].iloc[i],
                "closed": df['closed_time'].iloc[i],
                "description": df['query_des'].iloc[i],
                "status": df['status'].iloc[i]
            }
            tickets.append(ticket)

            status_color = "green" if ticket['status'] == "Closed" else "red"

            st.markdown(f"""
        <div class="ticket-card">
            <div class="status-badge" style="background-color:{status_color}; color:white;">
                {ticket['status']}
            </div>
            <div class="ticket-title">#{ticket['id']} — {ticket['title']}</div>
            <div class="ticket-meta">
                ☐ Submitted: {ticket['submitted']} &nbsp;&nbsp;&nbsp;
                ☐ Closed: {ticket['closed']}
            </div>
            <div class="ticket-desc">
                {ticket['description']}
            </div>
        </div>
        """, unsafe_allow_html=True)
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
                            st.toast("Password Not Matched")
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
            <h4>About the Client Dashboard</h4>
                <p>
                This system helps clients raise and track queries easily.  
                You can submit issues, monitor progress, and receive support quickly.
                </p>
                <p>📍 <b>Chennai, Tamilnadu</b></p>
                <p>📞 +91 90804 10927</p>
                <p>✉️ support@query.com</p>            
                
            </div>
            """, unsafe_allow_html=True)
