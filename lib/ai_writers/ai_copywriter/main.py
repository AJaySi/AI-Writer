"""
AI Copywriter Main Module

This module serves as the main entry point for the AI Copywriter functionality,
integrating all the copywriting components.
"""

import streamlit as st
from typing import Dict, Any

# Import formula modules
from .formulas.aida_formula import generate_aida_copy
from .formulas.pas_formula import generate_pas_copy
from .formulas.bab_formula import generate_bab_copy
# Additional imports will be added as more formula modules are created

# Import utility modules
from .formula_comparison import write_formula_comparison
from .smart_recommender import write_smart_recommender

def write_ai_copywriter():
    """Main function to run the AI Copywriter dashboard."""
    st.title("AI Copywriting Formula Generator")
    
    # Initialize session state
    if 'copywriter_view' not in st.session_state:
        st.session_state.copywriter_view = "dashboard"
    if 'selected_formula' not in st.session_state:
        st.session_state.selected_formula = None
    
    # Sidebar navigation
    st.sidebar.title("Copywriting Tools")
    
    # Main navigation options
    nav_option = st.sidebar.radio(
        "Navigation",
        ["Formula Dashboard", "Formula Comparison", "Smart Recommender"]
    )
    
    # Update view based on navigation
    if nav_option == "Formula Dashboard":
        st.session_state.copywriter_view = "dashboard"
    elif nav_option == "Formula Comparison":
        st.session_state.copywriter_view = "comparison"
    elif nav_option == "Smart Recommender":
        st.session_state.copywriter_view = "recommender"
    
    # Formula-specific navigation if a formula is selected
    if st.session_state.selected_formula:
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"Using {st.session_state.selected_formula} Formula")
        
        if st.sidebar.button("Back to Dashboard"):
            st.session_state.selected_formula = None
            st.session_state.copywriter_view = "dashboard"
            st.rerun()
    
    # Display the appropriate view
    if st.session_state.selected_formula:
        # Show the selected formula generator
        if st.session_state.selected_formula == "AIDA":
            generate_aida_copy()
        elif st.session_state.selected_formula == "PAS":
            generate_pas_copy()
        elif st.session_state.selected_formula == "BAB":
            generate_bab_copy()
        else:
            st.info(f"The {st.session_state.selected_formula} formula generator is coming soon!")
    else:
        # Show the selected view
        if st.session_state.copywriter_view == "dashboard":
            display_dashboard()
        elif st.session_state.copywriter_view == "comparison":
            write_formula_comparison()
        elif st.session_state.copywriter_view == "recommender":
            write_smart_recommender()

def display_dashboard():
    """Display the main copywriting dashboard."""
    st.write("Create persuasive, high-converting copy using proven copywriting formulas.")
    
    # Featured formulas section
    st.subheader("Featured Formulas")
    
    # Create a 2x2 grid for featured formulas
    col1, col2 = st.columns(2)
    
    with col1:
        with st.container():
            st.markdown("""
            ### 🎯 AIDA Formula
            **Attention, Interest, Desire, Action**
            
            The classic marketing formula that guides prospects through a purchase decision.
            
            **Best for:** Landing pages, sales emails, product descriptions
            """)
            
            if st.button("Use AIDA Formula"):
                st.session_state.selected_formula = "AIDA"
                st.rerun()
    
    with col2:
        with st.container():
            st.markdown("""
            ### 🔧 PAS Formula
            **Problem, Agitation, Solution**
            
            Identify a problem, agitate it, then present your solution.
            
            **Best for:** Social ads, blog intros, sales pages
            """)
            
            if st.button("Use PAS Formula"):
                st.session_state.selected_formula = "PAS"
                st.rerun()
    
    col3, col4 = st.columns(2)
    
    with col3:
        with st.container():
            st.markdown("""
            ### 🌉 BAB Formula
            **Before, After, Bridge**
            
            Show the current state, desired state, and how to get there.
            
            **Best for:** Case studies, testimonials, video scripts
            """)
            
            if st.button("Use BAB Formula"):
                st.session_state.selected_formula = "BAB"
                st.rerun()
    
    with col4:
        with st.container():
            st.markdown("""
            ### 🏆 4Ps Formula
            **Promise, Picture, Proof, Push**
            
            Make a promise, paint a picture, provide proof, push for action.
            
            **Best for:** Sales pages, webinar scripts, video sales letters
            
            **Status:** Coming Soon
            """)
            
            st.button("Use 4Ps Formula", disabled=True)
    
    # Tools section
    st.markdown("---")
    st.subheader("Copywriting Tools")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🔍 Formula Finder
        
        Answer a few questions to find the perfect formula for your needs.
        """)
        
        if st.button("Open Formula Finder"):
            st.session_state.copywriter_view = "comparison"
            st.rerun()
    
    with col2:
        st.markdown("""
        ### 🧠 Smart Recommender
        
        Let AI analyze your brief and recommend the best formula.
        """)
        
        if st.button("Open Smart Recommender"):
            st.session_state.copywriter_view = "recommender"
            st.rerun()
    
    # Resources section
    st.markdown("---")
    st.subheader("Copywriting Resources")
    
    with st.expander("Copywriting Best Practices"):
        st.markdown("""
        ### Copywriting Best Practices
        
        1. **Know your audience** - Understand their pain points, desires, and language
        2. **Focus on benefits, not features** - Show how your product improves lives
        3. **Use clear, concise language** - Avoid jargon and unnecessary words
        4. **Create compelling headlines** - 80% of people only read headlines
        5. **Include social proof** - Testimonials, reviews, and case studies build trust
        6. **Address objections** - Anticipate and overcome potential concerns
        7. **Use power words** - Emotional and persuasive words drive action
        8. **Create urgency** - Give people a reason to act now
        9. **Have a clear call-to-action** - Tell people exactly what to do next
        10. **Test and optimize** - Continuously improve your copy based on results
        """)
    
    with st.expander("Headline Formulas"):
        st.markdown("""
        ### Powerful Headline Formulas
        
        1. **How to [Achieve Desired Outcome]**
           - *Example:* "How to Lose 10 Pounds Without Giving Up Your Favorite Foods"
        
        2. **[Number] Ways to [Solve Problem]**
           - *Example:* "7 Ways to Increase Your Website Conversion Rate"
        
        3. **The Secret of [Desired Outcome]**
           - *Example:* "The Secret of Successful Entrepreneurs"
        
        4. **Who Else Wants [Desired Outcome]?**
           - *Example:* "Who Else Wants to Work From Home and Make $100,000 a Year?"
        
        5. **[Do Something] Like [Expert/Celebrity]**
           - *Example:* "Write Emails Like a 7-Figure Copywriter"
        
        6. **Warning: [Negative Consequence]**
           - *Example:* "Warning: Your Retirement Plan May Be at Risk"
        
        7. **The Ultimate Guide to [Topic]**
           - *Example:* "The Ultimate Guide to Content Marketing in 2023"
        """)
    
    with st.expander("Power Words List"):
        st.markdown("""
        ### Power Words for Persuasive Copy
        
        #### Urgency Words
        - Now
        - Limited
        - Hurry
        - Quick
        - Deadline
        - Today only
        - Last chance
        
        #### Exclusivity Words
        - Exclusive
        - Members only
        - Insider
        - Private
        - Selected
        - Elite
        - Invitation
        
        #### Value Words
        - Free
        - Save
        - Discount
        - Bonus
        - Complimentary
        - Bargain
        - Affordable
        
        #### Curiosity Words
        - Secret
        - Revealed
        - Discover
        - Unlock
        - Hidden
        - Surprising
        - Uncover
        
        #### Emotional Words
        - Amazing
        - Stunning
        - Remarkable
        - Incredible
        - Breathtaking
        - Sensational
        - Extraordinary
        """)

if __name__ == "__main__":
    write_ai_copywriter()