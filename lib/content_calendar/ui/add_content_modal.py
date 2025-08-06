import streamlit as st

def render_add_content_modal(selected_date, on_add_content, on_generate_with_ai):
    if st.button("+ Add Content", key="open_add_content_dialog_bottom"):
        st.session_state['show_add_content_dialog'] = True
    if st.session_state.get('show_add_content_dialog', False):
        st.markdown("### Add Content")
        with st.form("quick_add_form_dialog_bottom"):
            title = st.text_input("Title")
            platform = st.selectbox("Platform", ["Blog", "Instagram", "Twitter", "LinkedIn", "Facebook"])
            content_type = st.selectbox("Content Type", ["Article", "Social Post", "Video", "Newsletter"])
            publish_date = st.date_input("Publish Date", selected_date)
            col_add, col_ai = st.columns([0.6, 0.4])
            with col_add:
                if st.form_submit_button("Add Content"):
                    on_add_content(title, platform, content_type, publish_date)
            with col_ai:
                if st.form_submit_button("Generate with AI"):
                    on_generate_with_ai(title, platform, content_type)
        if st.button("Close", key="close_add_content_dialog_bottom"):
            st.session_state['show_add_content_dialog'] = False 