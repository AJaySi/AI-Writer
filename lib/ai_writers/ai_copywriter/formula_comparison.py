"""
Copywriting Formula Comparison Tool

This module provides functionality to compare different copywriting formulas
and help users select the most appropriate one for their needs.
"""

import streamlit as st
import pandas as pd
from typing import Dict, List

def formula_comparison_data() -> Dict:
    """Return comparison data for copywriting formulas."""
    return {
        "formulas": [
            {
                "name": "AIDA",
                "full_name": "Attention, Interest, Desire, Action",
                "structure": ["Attention", "Interest", "Desire", "Action"],
                "best_for": ["Landing Pages", "Sales Emails", "Product Descriptions"],
                "length": "Medium",
                "complexity": "Low",
                "emotional_appeal": "Medium",
                "logical_appeal": "Medium",
                "description": "The classic marketing formula that guides prospects through a purchase decision",
                "example": "Tired of wasting time on social media? Our tool saves busy professionals 10 hours per week. With automated scheduling and AI-powered content suggestions, you'll never struggle with social media again. Try it free for 14 days!",
                "strengths": ["Versatile", "Easy to implement", "Follows natural decision process"],
                "weaknesses": ["Can be predictable", "May need adaptation for different channels"]
            },
            {
                "name": "PAS",
                "full_name": "Problem, Agitation, Solution",
                "structure": ["Problem", "Agitation", "Solution"],
                "best_for": ["Social Ads", "Blog Intros", "Sales Pages"],
                "length": "Short to Medium",
                "complexity": "Low",
                "emotional_appeal": "High",
                "logical_appeal": "Medium",
                "description": "Identify a problem, agitate it, then present your solution",
                "example": "Running out of storage space? Every day you delay, more precious memories and important files are at risk of being lost forever. Our cloud storage solution gives you unlimited space and automatic backups for peace of mind.",
                "strengths": ["Emotionally powerful", "Works well for pain-point solutions", "Concise"],
                "weaknesses": ["Can feel manipulative if overdone", "Less effective for positive-motivation products"]
            },
            {
                "name": "BAB",
                "full_name": "Before, After, Bridge",
                "structure": ["Before", "After", "Bridge"],
                "best_for": ["Case Studies", "Testimonials", "Video Scripts"],
                "length": "Medium",
                "complexity": "Low",
                "emotional_appeal": "High",
                "logical_appeal": "Medium",
                "description": "Show the current state, desired state, and how to get there",
                "example": "Before: You're struggling with manual data entry, wasting hours each week. After: Imagine all your data automatically organized and analyzed, giving you insights in seconds. Bridge: Our automation platform makes this transformation possible in just 3 easy steps.",
                "strengths": ["Visually compelling", "Transformation-focused", "Easy to understand"],
                "weaknesses": ["Can oversimplify complex solutions", "Requires clear before/after states"]
            },
            {
                "name": "4Ps",
                "full_name": "Promise, Picture, Proof, Push",
                "structure": ["Promise", "Picture", "Proof", "Push"],
                "best_for": ["Sales Pages", "Webinar Scripts", "Video Sales Letters"],
                "length": "Medium to Long",
                "complexity": "Medium",
                "emotional_appeal": "Medium",
                "logical_appeal": "High",
                "description": "Make a promise, paint a picture, provide proof, push for action",
                "example": "We promise you'll lose 10 pounds in 30 days. Picture yourself with more energy, fitting into your favorite clothes again, and feeling confident. Our clinical studies show 95% of participants achieved these results. Ready to transform your life? Join our program today.",
                "strengths": ["Balanced emotional and logical appeal", "Evidence-based", "Clear value proposition"],
                "weaknesses": ["Requires strong proof elements", "Less effective for impulse purchases"]
            },
            {
                "name": "FAB",
                "full_name": "Features, Advantages, Benefits",
                "structure": ["Features", "Advantages", "Benefits"],
                "best_for": ["Product Pages", "Brochures", "Sales Presentations"],
                "length": "Short to Medium",
                "complexity": "Low",
                "emotional_appeal": "Low",
                "logical_appeal": "High",
                "description": "Connect product features to customer benefits",
                "example": "Our smartphone features a 48MP camera (Feature) that captures 4x more detail than standard phones (Advantage), so you'll never miss a precious moment with your family (Benefit).",
                "strengths": ["Product-focused", "Logical progression", "Connects features to outcomes"],
                "weaknesses": ["Can lack emotional appeal", "May feel technical"]
            }
        ]
    }

def write_formula_comparison():
    """Display the formula comparison tool."""
    st.title("Copywriting Formula Comparison Tool")
    st.write("Compare different copywriting formulas to find the best one for your needs.")
    
    # Get formula data
    data = formula_comparison_data()
    formulas = data["formulas"]
    
    # Create tabs for different comparison views
    tab1, tab2, tab3 = st.tabs(["Formula Finder", "Side-by-Side Comparison", "Detailed Breakdown"])
    
    with tab1:
        st.subheader("Find the Right Formula")
        st.write("Answer a few questions to get a personalized formula recommendation.")
        
        # Questionnaire
        goal = st.selectbox(
            "What's your primary goal?",
            ["Make a sale", "Generate leads", "Build awareness", "Educate audience", "Drive engagement"]
        )
        
        content_type = st.selectbox(
            "What type of content are you creating?",
            ["Landing page", "Email", "Social media post", "Blog post", "Video script", "Product description"]
        )
        
        audience_knowledge = st.select_slider(
            "How familiar is your audience with your product/service?",
            options=["Not at all", "Slightly", "Moderately", "Very", "Extremely"]
        )
        
        complexity = st.select_slider(
            "How complex is your product/service?",
            options=["Very simple", "Simple", "Moderate", "Complex", "Very complex"]
        )
        
        appeal_preference = st.slider(
            "Do you prefer emotional or logical appeal?",
            min_value=1, max_value=10, value=5,
            help="1 = Highly emotional, 10 = Highly logical"
        )
        
        # Calculate recommendations based on inputs
        if st.button("Get Recommendations"):
            st.subheader("Recommended Formulas")
            
            # This is a simplified recommendation algorithm
            # In a real implementation, this would be more sophisticated
            recommendations = []
            
            # Add scoring logic based on user inputs
            for formula in formulas:
                score = 0
                
                # Goal matching
                if goal == "Make a sale" and any(x in formula["best_for"] for x in ["Sales Pages", "Product Descriptions"]):
                    score += 2
                elif goal == "Generate leads" and any(x in formula["best_for"] for x in ["Landing Pages", "Sales Emails"]):
                    score += 2
                elif goal == "Build awareness" and any(x in formula["best_for"] for x in ["Social Ads", "Blog Intros"]):
                    score += 2
                elif goal == "Educate audience" and any(x in formula["best_for"] for x in ["Case Studies", "Blog Intros"]):
                    score += 2
                elif goal == "Drive engagement" and any(x in formula["best_for"] for x in ["Social Ads", "Video Scripts"]):
                    score += 2
                
                # Content type matching
                if content_type == "Landing page" and "Landing Pages" in formula["best_for"]:
                    score += 2
                elif content_type == "Email" and "Sales Emails" in formula["best_for"]:
                    score += 2
                elif content_type == "Social media post" and "Social Ads" in formula["best_for"]:
                    score += 2
                elif content_type == "Blog post" and "Blog Intros" in formula["best_for"]:
                    score += 2
                elif content_type == "Video script" and "Video Scripts" in formula["best_for"]:
                    score += 2
                elif content_type == "Product description" and "Product Descriptions" in formula["best_for"]:
                    score += 2
                
                # Audience knowledge matching
                if audience_knowledge in ["Not at all", "Slightly"] and formula["name"] in ["PAS", "BAB"]:
                    score += 1
                elif audience_knowledge in ["Moderately"] and formula["name"] in ["AIDA", "4Ps"]:
                    score += 1
                elif audience_knowledge in ["Very", "Extremely"] and formula["name"] in ["FAB"]:
                    score += 1
                
                # Complexity matching
                if complexity in ["Very simple", "Simple"] and formula["complexity"] == "Low":
                    score += 1
                elif complexity in ["Moderate"] and formula["complexity"] == "Medium":
                    score += 1
                elif complexity in ["Complex", "Very complex"] and formula["complexity"] == "High":
                    score += 1
                
                # Appeal preference matching
                if appeal_preference <= 3 and formula["emotional_appeal"] == "High":
                    score += 1
                elif 4 <= appeal_preference <= 7 and formula["emotional_appeal"] == "Medium":
                    score += 1
                elif appeal_preference >= 8 and formula["logical_appeal"] == "High":
                    score += 1
                
                recommendations.append({
                    "formula": formula,
                    "score": score
                })
            
            # Sort recommendations by score
            recommendations.sort(key=lambda x: x["score"], reverse=True)
            
            # Display top 3 recommendations
            for i, rec in enumerate(recommendations[:3]):
                formula = rec["formula"]
                match_percentage = min(100, rec["score"] * 10)  # Convert score to percentage
                
                st.markdown(f"""
                ### {i+1}. {formula["name"]} ({formula["full_name"]}) - {match_percentage}% match
                
                **Description:** {formula["description"]}
                
                **Best for:** {", ".join(formula["best_for"])}
                
                **Example:**
                _{formula["example"]}_
                
                **Why it's a good match:** This formula works well for your {content_type} with {complexity.lower()} complexity and {audience_knowledge.lower()} audience familiarity.
                """)
                
                if st.button(f"Use {formula['name']} Formula", key=f"use_{formula['name']}_{i}"):
                    # This would link to the specific formula generator
                    st.session_state.selected_formula = formula["name"]
                    st.rerun()
    
    with tab2:
        st.subheader("Side-by-Side Comparison")
        
        # Select formulas to compare
        selected_formulas = st.multiselect(
            "Select formulas to compare",
            options=[f["name"] for f in formulas],
            default=[formulas[0]["name"], formulas[1]["name"]]
        )
        
        if selected_formulas:
            # Filter formulas based on selection
            filtered_formulas = [f for f in formulas if f["name"] in selected_formulas]
            
            # Create comparison table
            comparison_data = []
            for formula in filtered_formulas:
                comparison_data.append({
                    "Formula": formula["name"],
                    "Full Name": formula["full_name"],
                    "Structure": " → ".join(formula["structure"]),
                    "Best For": ", ".join(formula["best_for"]),
                    "Length": formula["length"],
                    "Emotional Appeal": formula["emotional_appeal"],
                    "Logical Appeal": formula["logical_appeal"]
                })
            
            # Display comparison table
            st.table(pd.DataFrame(comparison_data))
            
            # Display examples side by side
            st.subheader("Examples")
            cols = st.columns(len(filtered_formulas))
            for i, formula in enumerate(filtered_formulas):
                with cols[i]:
                    st.markdown(f"**{formula['name']}**")
                    st.markdown(f"_{formula['example']}_")
        else:
            st.info("Please select at least one formula to compare.")
    
    with tab3:
        st.subheader("Detailed Formula Breakdown")
        
        # Select a formula for detailed view
        selected_formula = st.selectbox(
            "Select a formula to view details",
            options=[f["name"] for f in formulas]
        )
        
        # Get the selected formula
        formula = next((f for f in formulas if f["name"] == selected_formula), None)
        
        if formula:
            st.markdown(f"""
            ## {formula["name"]} ({formula["full_name"]})
            
            **Description:** {formula["description"]}
            
            ### Structure
            {" → ".join(formula["structure"])}
            
            ### Best Used For
            {", ".join(formula["best_for"])}
            
            ### Characteristics
            - **Length:** {formula["length"]}
            - **Complexity:** {formula["complexity"]}
            - **Emotional Appeal:** {formula["emotional_appeal"]}
            - **Logical Appeal:** {formula["logical_appeal"]}
            
            ### Example
            _{formula["example"]}_
            
            ### Strengths
            {", ".join(formula["strengths"])}
            
            ### Potential Weaknesses
            {", ".join(formula["weaknesses"])}
            """)
            
            # Structure breakdown
            st.subheader("Structure Breakdown")
            
            for part in formula["structure"]:
                with st.expander(f"{part}"):
                    if part == "Attention" or part == "Problem":
                        st.markdown("""
                        **Purpose:** Grab the reader's attention by identifying a relevant problem or using a hook.
                        
                        **Techniques:**
                        - Ask a provocative question
                        - Share a surprising statistic
                        - Make a bold claim
                        - Tell a short story
                        - Highlight a pain point
                        
                        **Example:**
                        "Are you tired of spending hours on social media with little to show for it?"
                        """)
                    elif part == "Interest" or part == "Agitation":
                        st.markdown("""
                        **Purpose:** Build interest by elaborating on the problem or agitating the pain point.
                        
                        **Techniques:**
                        - Describe consequences of inaction
                        - Share relatable scenarios
                        - Provide context and background
                        - Highlight industry trends
                        - Create emotional connection
                        
                        **Example:**
                        "Every hour spent on manual posting is an hour you could be growing your business. Meanwhile, your competitors are automating their social media and pulling ahead."
                        """)
                    elif part == "Desire" or part == "Solution" or part == "After":
                        st.markdown("""
                        **Purpose:** Create desire by presenting your solution and its benefits.
                        
                        **Techniques:**
                        - Highlight key features and benefits
                        - Paint a picture of success
                        - Share testimonials or case studies
                        - Provide proof points
                        - Address objections
                        
                        **Example:**
                        "Our platform automates your entire social media workflow, saving you 10+ hours every week while increasing engagement by an average of 43%."
                        """)
                    elif part == "Action" or part == "Bridge" or part == "Push":
                        st.markdown("""
                        **Purpose:** Prompt the reader to take the next step.
                        
                        **Techniques:**
                        - Use clear, direct language
                        - Create urgency or scarcity
                        - Make the next step easy
                        - Reduce risk (guarantees, free trials)
                        - Reinforce key benefits
                        
                        **Example:**
                        "Start your free 14-day trial today — no credit card required. Join 10,000+ businesses saving time and growing their social presence."
                        """)
                    else:
                        st.markdown(f"Details for {part} coming soon.")
            
            if st.button(f"Use {formula['name']} Formula"):
                # This would link to the specific formula generator
                st.session_state.selected_formula = formula["name"]
                st.rerun()