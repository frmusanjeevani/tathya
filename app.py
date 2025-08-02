import streamlit as st
from auth import authenticate_user, is_authenticated, logout_user, check_session_timeout, update_last_activity
from database import init_database
import pages.dashboard as dashboard
import pages.case_entry as case_entry
import pages.reviewer_panel as reviewer_panel
import pages.approver_panel as approver_panel
import pages.approver2_panel as approver2_panel
import pages.legal_panel as legal_panel
import pages.closure_panel as closure_panel
import pages.admin_panel as admin_panel
import pages.investigation_panel as investigation_panel
import pages.investigator_panel as investigator_panel
import pages.final_review_panel as final_review_panel
import pages.simple_ai_assistant as ai_suggestions
import pages.user_dashboard as user_dashboard
import pages.agency_workflow as agency_workflow
import pages.smart_verification_suite as smart_verification_suite
import pages.one_click_verification as one_click_verification
import pages.login_page as login_page
import pages.tathya_verification_lab as tathya_verification_lab

# Initialize database
init_database()

# Page configuration
st.set_page_config(page_title="Tathya - Case Management System",
                   page_icon="🔎",
                   layout="wide",
                   initial_sidebar_state="collapsed")


# Load custom CSS animations
def load_css():
    with open("static/css/animations.css", "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_login():
    """Display login form"""
    load_css()

    # Header with branding, system switcher, and ABCL logo
    header_col1, header_col2, header_col3 = st.columns([2, 1, 1])
    with header_col1:
        st.markdown("""
            <div style="margin-bottom: 5px;">
            <h3 style="color: #77787B; font-weight: 600;">
                AI-Powered Case Management Solution
            </h3>
        </div>
        """,
                    unsafe_allow_html=True)

    with header_col2:
        st.markdown("")  # Empty space

    with header_col3:
        try:
            st.image("static/images/abcl_logo.jpg", width=200)
        except:
            st.markdown("### 🏢 ABCL")

    # Layout with Tathya logo on left middle and login form on right middle
    col1, col2 = st.columns([1, 1])

    with col1:
        # Tathya logo on left middle
        st.markdown(
            "<div style='margin-top: 5px; display: flex; align-items: center; justify-content: flex-end; height: 120px;'>",
            unsafe_allow_html=True)
        try:
            st.image("static/images/tathya.png", width=250)
        except:
            st.markdown("# 🔎 Tathya")
            st.markdown("### Every Clue Counts")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        # System selector above login box - extreme right
        st.markdown(
            "<div style='margin-top: 50px; display: flex; justify-content: flex-end;'>",
            unsafe_allow_html=True)

        # Initialize system selection if not set
        if 'selected_system' not in st.session_state:
            st.session_state.selected_system = "Investigation"

        # Enhanced radio buttons with custom styling positioned on extreme right
        st.markdown("""
        <style>
        /* Custom radio button styling */
        div[data-testid="stRadio"] > div {
            display: flex !important;
            justify-content: flex-end !important;
            gap: 12px !important;
        }
        
        div[data-testid="stRadio"] > div > label {
            background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%) !important;
            border: 2px solid #e8eaed !important;
            border-radius: 20px !important;
            padding: 8px 16px !important;
            cursor: pointer !important;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            position: relative !important;
            overflow: hidden !important;
            min-width: 100px !important;
            text-align: center !important;
            font-size: 12px !important;
        }
        
        div[data-testid="stRadio"] > div > label:hover {
            transform: translateY(-1px) scale(1.05) !important;
            border-color: #4285f4 !important;
            box-shadow: 0 4px 16px rgba(66,133,244,0.2) !important;
            background: linear-gradient(135deg, #ffffff 0%, #f0f4ff 100%) !important;
        }
        
        div[data-testid="stRadio"] > div > label[data-checked="true"] {
            background: linear-gradient(135deg, #4285f4 0%, #1a73e8 100%) !important;
            color: white !important;
            border-color: #1a73e8 !important;
            transform: scale(1.05) !important;
            box-shadow: 0 6px 20px rgba(66,133,244,0.3) !important;
        }
        
        div[data-testid="stRadio"] > div > label[data-checked="true"]:hover {
            transform: scale(1.08) translateY(-1px) !important;
        }
        </style>
        """,
                    unsafe_allow_html=True)

        system_choice = st.radio("System",
                                 ["Investigation", "Tathya Verification Lab"],
                                 index=0 if st.session_state.selected_system
                                 == "Investigation" else 1,
                                 key="system_selector",
                                 horizontal=True,
                                 label_visibility="collapsed")

        # Update session state when selection changes
        if system_choice != st.session_state.selected_system:
            st.session_state.selected_system = system_choice

        st.markdown("</div>", unsafe_allow_html=True)

        # Login form section on right middle
        st.markdown("<div style='margin-top: 30px;'>", unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown("### UAT Mode")
            username = st.text_input("User ID",
                                     placeholder="Enter your User ID")
            password = st.text_input("Password",
                                     type="password",
                                     placeholder="Enter your password")

            col_a, col_b, col_c = st.columns([1, 1, 1])
            with col_b:
                login_button = st.form_submit_button("🎯 Hit",
                                                     use_container_width=True)

            if login_button:
                if username and password:
                    # Authenticate user directly
                    success, message = authenticate_user(username, password)
                    if success:
                        st.success("✅ Login successful!")
                        # Set flag to show AI tip popup after login
                        if st.session_state.get("role") in [
                                "Initiator", "Investigator", "Admin"
                        ]:
                            st.session_state.show_ai_tip = True
                        st.rerun()
                    else:
                        st.error(f"❌ {message}")
                else:
                    st.warning("⚠️ Please enter both User ID and password")

        st.markdown("</div>", unsafe_allow_html=True)

    # Footer branding for login page
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; padding: 5px 0; margin-top: 5px; color: #414042;">
        <div style="font-style: italic; font-size: 16px;">
             <span style="color: #C7222A; font-weight: italic;">Powered by Fraud Risk Management Unit</span>
        </div>
        <div style="font-size: 14px; opacity: 0.7;">
            © 2025 Aditya Birla Capital Ltd.
        </div>
    </div>
    """,
                unsafe_allow_html=True)


def show_role_selector():
    """Show role selector below ABCL logo, right-aligned"""
    if st.session_state.get("all_roles_access", False):
        # Initialize role selector visibility
        if "show_role_selector" not in st.session_state:
            st.session_state.show_role_selector = False

        # Role selector positioned extreme right below ABCL logo, same size as logo
        role_col1, role_col2 = st.columns([3.5, 1])
        with role_col2:
            # Custom CSS for extreme right positioning and wider box
            st.markdown("""
            <style>
            .role-selector-container {
                margin-top: -20px;
                padding: -10;
                display: flex;
                flex-direction: column;
                align-items: flex-end;
                width: 50%;
            }
            </style>
            """,
                        unsafe_allow_html=True)

            # Role selector button and panel with container class
            st.markdown('<div class="role-selector-container">',
                        unsafe_allow_html=True)

            # Role button with full width
            if st.button("🧑‍💼 Role",
                         help="Switch Role",
                         key="role_toggle",
                         use_container_width=True):
                st.session_state.show_role_selector = not st.session_state.show_role_selector
                st.rerun()

            # Show role selector panel if enabled with full width
            if st.session_state.get("show_role_selector", False):
                available_roles = [
                    "Initiator", "Reviewer", "Approver", "Legal Reviewer",
                    "Actioner", "Investigator"
                ]
                if st.session_state.get("user_role") == "Admin":
                    available_roles.append("Admin")

                current_role = st.session_state.get("role", "")
                current_index = 0
                if current_role in available_roles:
                    current_index = available_roles.index(current_role)

                selected_role = st.selectbox("Active Role:",
                                             available_roles,
                                             index=current_index,
                                             key="role_selector")

                if st.button("Apply",
                             key="role_apply",
                             use_container_width=True):
                    st.session_state.role = selected_role
                    st.session_state.show_role_selector = False
                    st.success(f"✅ Switched to {selected_role}")
                    st.rerun()

            st.markdown('</div>', unsafe_allow_html=True)


def show_sidebar(role):
    """Display sidebar navigation based on user role"""
    # Check session timeout
    if check_session_timeout():
        logout_user()
        st.rerun()

    load_css()

    with st.sidebar:
        # User info header with right-aligned text and left-aligned navigation buttons
        st.markdown("""
        <style>
        .user-info {
            text-align: left;
            background-color: #f8f9fa;
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
        }
        .user-info h3 {
            text-align: left;
            margin-bottom: 10px;
            color: #495057;
        }
        .user-info p {
            text-align: left;
            margin: 5px 0;
            font-size: 14px;
        }
        
        /* Left-align navigation button text in sidebar */
        .stSidebar .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 12px !important;
        }
        
        /* Left-align text in expandable sections */
        .stSidebar .stExpander .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 12px !important;
        }
        
        /* Ensure Analytics and Utility section buttons are left-aligned */
        .stSidebar div[data-testid="stVerticalBlock"] .stButton > button {
            text-align: left !important;
            justify-content: flex-start !important;
            padding-left: 12px !important;
        }
        </style>
        """,
                    unsafe_allow_html=True)

        st.markdown(f"""
        <div class="user-info">
            <h3>👤 User Information</h3>
            <p><strong>User:</strong> {st.session_state.get('username', 'Unknown')}</p>
            <p><strong>Role:</strong> {role}</p>
            <p><strong>Name:</strong> {st.session_state.get('user_name', 'N/A')}</p>
            <p><strong>Team:</strong> {st.session_state.get('user_team', 'N/A')}</p>
        </div>
        """,
                    unsafe_allow_html=True)

        # Enhanced system switcher button with animations
        st.markdown("""
        <style>
        div[data-testid="stButton"] > button[key="switch_to_lab"] {
            background: linear-gradient(135deg, #f8f9fa 0%, #e8eaed 100%) !important;
            color: #3c4043 !important;
            border: 1px solid #dadce0 !important;
            border-radius: 8px !important;
            padding: 12px 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
            position: relative !important;
            overflow: hidden !important;
        }
        
        div[data-testid="stButton"] > button[key="switch_to_lab"]:hover {
            transform: translateX(4px) scale(1.02) !important;
            background: linear-gradient(135deg, #4285f4 0%, #1a73e8 100%) !important;
            color: white !important;
            border-color: #1a73e8 !important;
            box-shadow: 0 4px 12px rgba(66,133,244,0.25) !important;
        }
        </style>
        """,
                    unsafe_allow_html=True)

        st.markdown("---")

        if role == "Admin":
            # Initialize session state for expandable panels
            if "case_management_expanded" not in st.session_state:
                st.session_state.case_management_expanded = True
            if "workflow_stages_expanded" not in st.session_state:
                st.session_state.workflow_stages_expanded = True
            if "analytics_management_expanded" not in st.session_state:
                st.session_state.analytics_management_expanded = True

            # Case Management Section
            with st.expander(
                    "Case Management",
                    expanded=st.session_state.case_management_expanded):
                # Case Management
                if st.button("New Case Registration",
                             key="admin_case_entry",
                             use_container_width=True):
                    st.session_state.current_page = "Case Entry"
                    st.rerun()
                if st.button("🔎 Tathya Investigation Intelligence",
                             key="admin_investigator",
                             use_container_width=True):
                    st.session_state.current_page = "Investigation Panel"
                    st.rerun()
                if st.button("Agency Workflow",
                             key="admin_agency_workflow",
                             use_container_width=True):
                    st.session_state.current_page = "Agency Workflow"
                    st.rerun()
                if st.button("Primary Review Center",
                             key="admin_primary_reviewer",
                             use_container_width=True):
                    st.session_state.current_page = "Reviewer Panel"
                    st.rerun()
                if st.button("Approval Authority L1",
                             key="admin_approver1_panel",
                             use_container_width=True):
                    st.session_state.current_page = "Approver Panel"
                    st.rerun()
                if st.button("Approval Authority L2",
                             key="admin_approver2_panel",
                             use_container_width=True):
                    st.session_state.current_page = "Approver 2 Panel"
                    st.rerun()
                if st.button("Final Review Authority",
                             key="admin_final_reviewer",
                             use_container_width=True):
                    st.session_state.current_page = "Final Review Panel"
                    st.rerun()
                if st.button("Legal Compliance Center",
                             key="admin_legal",
                             use_container_width=True):
                    st.session_state.current_page = "Legal Panel"
                    st.rerun()
                if st.button("Case Resolution Center",
                             key="admin_actioner",
                             use_container_width=True):
                    st.session_state.current_page = "Closure Panel"
                    st.rerun()

            # Analytics Section
            st.markdown("**Analytics**")
            if st.button("Workflow Analytics",
                         key="admin_workflow_process",
                         use_container_width=True):
                st.session_state.current_page = "Workflow Dashboard"
                st.rerun()
            if st.button("📊 Executive Dashboard",
                         key="admin_dashboard_analytics",
                         use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()

            # Utility Section
            st.markdown("**Utility**")
            if st.button("AI Case Assistant",
                         key="admin_ai_assistant",
                         use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()
            if st.button("System Administration",
                         key="admin_panel_main",
                         use_container_width=True):
                st.session_state.current_page = "Admin Panel"
                st.rerun()

            if st.button("🧠 Smart Verification Suite",
                         key="admin_smart_verification",
                         use_container_width=True):
                st.session_state.current_page = "Smart Verification Suite"
                st.rerun()

            if st.button("🎯 One-Click Verification",
                         key="admin_one_click_verification",
                         use_container_width=True):
                st.session_state.current_page = "One-Click Verification"
                st.rerun()

        elif role == "Initiator":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("📝 New Case Registration", use_container_width=True):
                st.session_state.current_page = "Case Entry"
                st.rerun()
            if st.button("AI Case Assistant", use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()

        elif role == "Investigator":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("📝 New Case Registration", use_container_width=True):
                st.session_state.current_page = "Case Entry"
                st.rerun()
            if st.button("🔎 Tathya Investigation Intelligence", use_container_width=True):
                st.session_state.current_page = "Investigator Panel"
                st.rerun()
            if st.button("🔍 Primary Review Center", use_container_width=True):
                st.session_state.current_page = "Reviewer Panel"
                st.rerun()
            if st.button("🤖 AI Case Assistant", use_container_width=True):
                st.session_state.current_page = "AI Assistant"
                st.rerun()

        elif role == "Reviewer":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("🔍 Primary Review Center", use_container_width=True):
                st.session_state.current_page = "Reviewer Panel"
                st.rerun()

        elif role == "Approver":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("✅ Approval Authority L1", use_container_width=True):
                st.session_state.current_page = "Approver Panel"
                st.rerun()
            if st.button("✅ Approval Authority L2", use_container_width=True):
                st.session_state.current_page = "Approver 2 Panel"
                st.rerun()

        elif role == "Legal Reviewer":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("🧑‍⚖️ Legal Compliance Center",
                         use_container_width=True):
                st.session_state.current_page = "Legal Panel"
                st.rerun()

        elif role == "Actioner":
            if st.button("📊 Executive Dashboard", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            if st.button("🧑‍💼 Case Resolution Center",
                         use_container_width=True):
                st.session_state.current_page = "Closure Panel"
                st.rerun()

        st.markdown("---")

        # Logout button
        if st.button("Logout", use_container_width=True):
            logout_user()
            st.rerun()


def show_main_content():
    """Display main application content based on user role"""
    role = st.session_state.get("role", "")

    # Add page transition effects and professional border styling
    st.markdown("""
    <style>
    .main .block-container {
        animation: fadeInSlide 0.5s ease-out;
        background-color: #FFFFFF !important;
        border: 1px solid rgba(0, 51, 102, 0.12) !important;
        border-radius: 15px !important;
        box-shadow: 0 3px 20px rgba(0, 0, 0, 0.08), 
                    0 1px 8px rgba(0, 0, 0, 0.04),
                    inset 0 1px 0 rgba(255, 255, 255, 0.9) !important;
        margin: 15px auto !important;
        padding: 2rem !important;
        backdrop-filter: blur(10px) !important;
        max-width: 95% !important;
    }
    
    .stApp {
        background-color: #FFFFFF !important;
    }
    
    @keyframes fadeInSlide {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    </style>
    """,
                unsafe_allow_html=True)

    # Common header with branding and logos
    header_col1, header_col2, header_col3 = st.columns([2, 1, 1])

    with header_col1:
        try:
            st.image("static/images/tathya.png", width=250)
        except:
            # No fallback text to avoid duplication
            st.markdown("")

    with header_col2:
        # Center space - no button here
        st.markdown("")

    with header_col3:
        try:
            st.image("static/images/abcl_logo.jpg", width=250)
        except:
            st.markdown("### 🏢 ABCL")

    # System switcher at extreme right below ABCL logo
    st.markdown("""
    <div style='
        margin-top: 15px; 
        display: flex; 
        justify-content: flex-end; 
        padding-right: 0px;
        position: relative;
        right: 0;
    '>
    """,
                unsafe_allow_html=True)

    # Enhanced gradient buttons with shimmer effects
    st.markdown("""
    <style>
    @keyframes shimmer {
        0% { background-position: -200px 0; }
        100% { background-position: 200px 0; }
    }
    
    /* Tathya Verification Lab Button */
    div[data-testid="stButton"] > button[key="inv_switch_to_lab"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%) !important;
        background-size: 200px 100% !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 10px 18px !important;
        font-weight: 600 !important;
        font-size: 11px !important;
        cursor: pointer !important;
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) !important;
        position: relative !important;
        overflow: hidden !important;
        min-width: 200px !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    div[data-testid="stButton"] > button[key="inv_switch_to_lab"]:hover {
        transform: translateY(-2px) scale(1.05) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
        background: linear-gradient(135deg, #764ba2 0%, #667eea 50%, #f093fb 100%) !important;
    }
    

    </style>
    """,
                unsafe_allow_html=True)

    # Single clickable button to switch
    if st.button("Switch to 🔬 Tathya Verification Lab",
                 key="inv_switch_to_lab",
                 help="Switch to Tathya Verification Lab"):
        st.session_state.selected_system = "Tathya Verification Lab"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    # Standardized AI-Enabled/Decision-Ready branding - smaller and extreme right
    st.markdown("""
    <div style='
        margin-top: 20px;
        margin-bottom: 10px;
        display: flex; 
        justify-content: flex-end; 
        padding-right: 20px;
        width: 100%;
    '>
        <div style='
            color: #003366; 
            font-weight: 700; 
            font-size: 14px; 
            font-family: "Segoe UI", "Arial Black", sans-serif;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            line-height: 1.1;
            text-shadow: 0 1px 2px rgba(0,51,102,0.2);
            text-align: right;
        '>AI-Enabled.<br>Decision-Ready</div>
    </div>
    """,
                unsafe_allow_html=True)

    # Show role selector below system switcher (right-aligned)
    show_role_selector()

    # Initialize current page
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Dashboard"

    # Update last activity
    update_last_activity()

    # Show sidebar
    show_sidebar(role)

    # Display page content based on current page
    current_page = st.session_state.get("current_page", "Dashboard")

    if current_page == "Dashboard":
        user_dashboard.show()
    elif current_page == "Case Entry":
        case_entry.show()
    elif current_page == "Reviewer Panel":
        reviewer_panel.show()
    elif current_page == "Final Review Panel":
        final_review_panel.show()
    elif current_page == "Approver Panel":
        approver_panel.show()
    elif current_page == "Approver 2 Panel":
        approver2_panel.show()
    elif current_page == "Legal Panel":
        legal_panel.show()
    elif current_page == "Closure Panel":
        closure_panel.show()
    elif current_page == "Admin Panel":
        admin_panel.show()
    elif current_page == "Investigation Panel":
        investigation_panel.show()
    elif current_page == "Investigator Panel":
        investigator_panel.show()
    elif current_page == "AI Assistant":
        ai_suggestions.show()
    elif current_page == "Workflow Dashboard":
        import pages.dashboard_workflow as dashboard_workflow
        dashboard_workflow.show()
    elif current_page == "Agency Workflow":
        agency_workflow.show()

    elif current_page == "Smart Verification Suite":
        smart_verification_suite.smart_verification_suite()
    elif current_page == "One-Click Verification":
        one_click_verification.one_click_verification()


def main():
    """Main application function"""
    if is_authenticated():
        # Route based on selected system
        selected_system = st.session_state.get("selected_system",
                                               "Investigation")

        if selected_system == "Tathya Verification Lab":
            tathya_verification_lab.show_tathya_verification_lab()
        else:
            # Default to Investigation system
            show_main_content()
    else:
        show_login()


if __name__ == "__main__":
    main()
