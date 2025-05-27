import streamlit as st

def render_content_card(row, is_editing, on_edit, on_delete, on_generate, icon_map, status_color, platform_disp, type_disp, status_disp, platform_icon, type_icon, item_key):
    st.markdown(f"<div class='card-content-calendar'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;align-items:center;justify-content:space-between;gap:8px;'>", unsafe_allow_html=True)
    st.markdown(f"<div style='display:flex;align-items:center;gap:8px;min-width:0;flex:1;'>"
                f"{type_icon}<span class='content-title'>{row['title']}</span></div>", unsafe_allow_html=True)
    st.markdown("<div style='display:flex;align-items:center;gap:4px;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("⚡", key=f"generate_{item_key}", help="Generate with AI Blog Writer", use_container_width=True):
            on_generate()
    with col2:
        if st.button("✏️", key=f"edit_{item_key}", help="Edit Content", use_container_width=True):
            on_edit()
    with col3:
        if st.button("🗑️", key=f"delete_{item_key}", help="Delete Content", use_container_width=True):
            on_delete()
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='content-meta'><span class='badge-content-calendar badge-platform-{platform_disp.lower()}'>{platform_icon} {platform_disp} &nbsp;|&nbsp; {type_disp} &nbsp;|&nbsp; <span class='chip-status chip-status-{status_disp.lower()}'>{status_disp}</span></span></div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True) 