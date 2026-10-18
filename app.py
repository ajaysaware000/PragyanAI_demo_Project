            use_container_width=True
        )
    with ecol2:
        st.markdown("#### Formatted Policy Brief")
        brief_text = f"""# Karnataka Skill Intelligence & Workforce Analytics Platform (K-SIWAP)
## Policy Executive Brief — District Skill Prioritisation
**Prepared by**: Policy Analytics Division (KSISU-04)
**Target Authority**: Department of Skill Development, Entrepreneurship & Livelihood (KSDEL)
---
### 1. Executive Summary
Evaluation of {len(scored_df)} districts using empirical labour demand, training capacity deficits, and skill gap indices:
- **Priority Weights Applied**:
  - Employer Demand: {int(w_demand*100)}%
  - Skill Gap Evidence: {int(w_gap*100)}%
  - Training Access Deficit: {int(w_capacity*100)}%
  - Demand Momentum: {int(w_momentum*100)}%
  - Confidence Penalty Safeguard: {'Enabled' if apply_penalty else 'Disabled'}
### 2. Immediate Action Priorities
1. **{top_district['district_name']}** (Rank #1, Score: {top_district['calculated_score']}/100)
   - Strategic Need: High regional skill shortage paired with severe ITI/Polytechnic seat deficits.
2. **Kalyana-Karnataka Affirmative Skilling**:
   - Focus vocational capital investments into Bidar, Kalaburagi, and Raichur to counteract regional economic disparity.
"""
        st.text_area("Generated Policy Brief Preview", brief_text, height=260)
        st.download_button(
            label="📄 Download Policy Memo (.md)",
            data=brief_text,
            file_name="K-SIWAP_Policy_Memo.md",
            mime="text/markdown",
            use_container_width=True
        )
