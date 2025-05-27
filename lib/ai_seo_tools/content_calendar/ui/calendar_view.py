import streamlit as st
from .components.content_card import render_content_card
from .components.badge import render_badge

def render_calendar_view(calendar_data, icon_map, status_color, on_edit, on_delete, on_generate, get_item_key):
    if calendar_data is not None and not calendar_data.empty:
        st.markdown("### All Scheduled Content")
        calendar_data = calendar_data.sort_values(by="date")
        grouped = list(calendar_data.groupby(calendar_data['date'].dt.date))
        for i, (date, group) in enumerate(grouped):
            exp_open = (i == 0)
            with st.expander(f"{date.strftime('%B %d, %Y')}", expanded=exp_open):
                for idx, row in group.iterrows():
                    item_key = get_item_key(row)
                    is_editing = st.session_state.get("editing_item_key") == item_key
                    platform = str(row['platform'])
                    if hasattr(platform, 'value'):
                        platform = platform.value
                    platform_map = {
                        'blog': 'Blog',
                        'website': 'Blog',
                        'instagram': 'Instagram',
                        'twitter': 'Twitter',
                        'linkedin': 'LinkedIn',
                        'facebook': 'Facebook',
                    }
                    platform_disp = platform_map.get(platform.lower(), 'Blog')
                    type_disp = str(row['type'])
                    if hasattr(type_disp, 'value'):
                        type_disp = type_disp.value
                    type_disp = type_disp.replace('_', ' ').title()
                    status_disp = row['status'].capitalize()
                    platform_icon = icon_map.get(platform_disp, '🌐')
                    type_icon = icon_map.get(type_disp, '📄')
                    render_content_card(
                        row=row,
                        is_editing=is_editing,
                        on_edit=lambda r=row: on_edit(r),
                        on_delete=lambda r=row: on_delete(r),
                        on_generate=lambda r=row: on_generate(r),
                        icon_map=icon_map,
                        status_color=status_color,
                        platform_disp=platform_disp,
                        type_disp=type_disp,
                        status_disp=status_disp,
                        platform_icon=platform_icon,
                        type_icon=type_icon,
                        item_key=item_key
                    )
    else:
        st.info("No content scheduled yet. Add content to see it here.") 