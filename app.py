import streamlit as st
import pandas as pd
from datetime import datetime
import os
from pathlib import Path

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Kilter Board Analysis - Upload",
    page_icon="🧗",
    layout="centered"
)

# ==========================================
# CUSTOM STYLING
# ==========================================
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean header */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Custom styling */
    h1 {
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        color: #1F2937 !important;
        margin-bottom: 0.5rem !important;
    }
    
    .stButton>button {
        background-color: #3B82F6;
        color: white;
        font-weight: 600;
        padding: 0.75rem 2rem;
        border-radius: 0.5rem;
        border: none;
        font-size: 1.1rem;
        width: 100%;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background-color: #2563EB;
        transform: translateY(-2px);
    }
    
    /* Success message */
    .success-box {
        background: linear-gradient(135deg, #10B981 0%, #059669 100%);
        color: white;
        padding: 2rem;
        border-radius: 1rem;
        text-align: center;
        margin: 2rem 0;
    }
    
    /* Info boxes */
    .info-box {
        background: #F3F4F6;
        padding: 1.5rem;
        border-radius: 0.75rem;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def save_video(uploaded_file, user_name):
    """Save uploaded video to videos folder"""
    # Create videos directory if it doesn't exist
    videos_dir = Path("videos")
    videos_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = user_name.replace(" ", "_").lower()
    file_extension = uploaded_file.name.split('.')[-1]
    filename = f"{timestamp}_{safe_name}.{file_extension}"
    
    # Save file
    filepath = videos_dir / filename
    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    return str(filepath)


def log_submission(data):
    """Log submission to CSV for tracking"""
    csv_file = "submissions_tracking.csv"
    
    # Create DataFrame
    df_new = pd.DataFrame([data])
    
    # Append to existing CSV or create new one
    if os.path.exists(csv_file):
        df_existing = pd.read_csv(csv_file)
        df = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df = df_new
    
    df.to_csv(csv_file, index=False)


def get_weekly_count():
    """Get number of submissions this week"""
    csv_file = "submissions_tracking.csv"
    
    if not os.path.exists(csv_file):
        return 0
    
    df = pd.read_csv(csv_file)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Get current week submissions
    now = datetime.now()
    week_start = now - pd.Timedelta(days=now.weekday())
    week_submissions = df[df['timestamp'] >= week_start]
    
    return len(week_submissions)


# ==========================================
# MAIN APP
# ==========================================

def main():
    # Header
    st.title("🧗 Upload Your Kilter Send")
    st.markdown("**Get personalized technique feedback in 24 hours**")
    
    # Check weekly limit
    weekly_count = get_weekly_count()
    remaining = max(0, 10 - weekly_count)
    
    if remaining > 0:
        st.markdown(f"""
        <div class="info-box">
            <strong>🎯 {remaining} spots remaining this week</strong><br>
            First-come, first-served basis
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("⚠️ This week's 10 free analyses are full. Check back next week!")
        st.stop()
    
    st.markdown("---")
    
    # Initialize session state
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    if not st.session_state.submitted:
        # Upload Form
        with st.form("upload_form"):
            st.subheader("📹 Your Video")
            uploaded_file = st.file_uploader(
                "Upload your successful Kilter problem send",
                type=['mp4', 'mov', 'avi', 'mkv'],
                help="Max file size: 200MB (default Streamlit limit)"
            )
            
            st.subheader("👤 Your Information")
            name = st.text_input("Name*", placeholder="John Doe")
            email = st.text_input("Email*", placeholder="john@example.com")
            
            st.subheader("🧗 Problem Details")
            problem_grade = st.selectbox(
                "Problem Grade*",
                ["V0-V2", "V3-V4", "V5-V6", "V7-V8", "V9+"]
            )
            problem_name = st.text_input(
                "Problem Name (optional)",
                placeholder="e.g., Crimpy Goodness"
            )
            notes = st.text_area(
                "Additional Notes (optional)",
                placeholder="Anything specific you want feedback on?",
                max_chars=500
            )
            
            st.subheader("✅ Consent")
            st.markdown("""
            By submitting, you consent to:
            - Video being used for ML training (anonymized)
            - Testimonial requests (optional participation)
            - Follow-up for paid product offers
            """)
            
            consent = st.checkbox("I agree to the terms above*")
            
            # Submit button
            submitted = st.form_submit_button("🚀 Submit Video")
            
            if submitted:
                # Validation
                errors = []
                
                if not uploaded_file:
                    errors.append("Please upload a video")
                if not name or not email:
                    errors.append("Name and email are required")
                if not consent:
                    errors.append("You must agree to the consent terms")
                
                if errors:
                    for error in errors:
                        st.error(f"❌ {error}")
                else:
                    # Check file size
                    file_size_mb = uploaded_file.size / (1024 * 1024)
                    
                    if file_size_mb > 200:
                        st.error(f"❌ File too large ({file_size_mb:.1f}MB). Maximum is 200MB.")
                    else:
                        # Save video
                        with st.spinner("Uploading your video..."):
                            try:
                                filepath = save_video(uploaded_file, name)
                                
                                # Log submission for tracking
                                submission_data = {
                                    'timestamp': datetime.now().isoformat(),
                                    'name': name,
                                    'email': email,
                                    'problem_grade': problem_grade,
                                    'problem_name': problem_name,
                                    'video_filename': os.path.basename(filepath),
                                    'file_size_mb': round(file_size_mb, 2),
                                    'has_notes': bool(notes),
                                    'status': 'uploaded'
                                }
                                
                                log_submission(submission_data)
                                
                                # Update session state
                                st.session_state.submitted = True
                                st.session_state.user_name = name
                                st.rerun()
                                
                            except Exception as e:
                                st.error(f"❌ Upload failed: {str(e)}")
                                st.error("Please try again or contact support.")
    
    else:
        # Success state
        st.markdown(f"""
        <div class="success-box">
            <h2 style="color: white; margin: 0;">✅ Upload Successful!</h2>
            <p style="font-size: 1.2rem; margin-top: 1rem; color: white;">
                Thanks {st.session_state.user_name}! Your video has been received.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        ### What happens next?
        
        1. **Analysis** - We'll review your technique within 24 hours
        2. **Feedback** - You'll receive personalized tips via email
        3. **Follow-up** - Optional: Join our beta group for early access to the full product
        
        ---
        
        Questions? Reply to the confirmation email you'll receive shortly.
        """)
        
        if st.button("Submit Another Video"):
            st.session_state.submitted = False
            st.rerun()


# ==========================================
# ADMIN PANEL (PASSWORD PROTECTED)
# ==========================================

def admin_panel():
    """Secure admin panel for downloading data and viewing stats"""
    
    st.markdown("---")
    st.markdown("### 🔐 Admin Panel")
    
    # Check if admin is logged in
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if not st.session_state.admin_authenticated:
        # Login form
        with st.form("admin_login"):
            st.write("**Admin Access Only**")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                # Get password from secrets
                try:
                    correct_password = st.secrets["admin"]["password"]
                except:
                    st.error("⚠️ Admin password not configured. See README for setup instructions.")
                    st.stop()
                
                if password == correct_password:
                    st.session_state.admin_authenticated = True
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password")
    
    else:
        # Admin is authenticated - show admin panel
        st.success("🔓 Admin authenticated")
        
        # Logout button
        if st.button("🚪 Logout"):
            st.session_state.admin_authenticated = False
            st.rerun()
        
        st.markdown("---")
        
        # STATS SUMMARY
        st.subheader("📊 Week Summary")
        
        csv_file = "submissions_tracking.csv"
        
        if os.path.exists(csv_file):
            df = pd.read_csv(csv_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            # Current week stats
            now = datetime.now()
            week_start = now - pd.Timedelta(days=now.weekday())
            week_df = df[df['timestamp'] >= week_start]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Submissions", len(df))
            with col2:
                st.metric("This Week", len(week_df))
            with col3:
                remaining = max(0, 10 - len(week_df))
                st.metric("Spots Remaining", remaining)
            
            # Recent submissions table
            st.markdown("**Recent Submissions:**")
            recent_df = df.tail(10)[['timestamp', 'name', 'email', 'problem_grade', 'file_size_mb']].sort_values('timestamp', ascending=False)
            st.dataframe(recent_df, use_container_width=True)
            
        else:
            st.info("No submissions yet")
        
        st.markdown("---")
        
        # DOWNLOAD CSV
        st.subheader("📥 Download Data")
        
        if os.path.exists(csv_file):
            with open(csv_file, "rb") as file:
                st.download_button(
                    label="📊 Download Submissions CSV",
                    data=file,
                    file_name=f"kilter_submissions_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("No CSV file yet - no submissions")
        
        # LIST VIDEOS
        st.markdown("---")
        st.subheader("🎥 Uploaded Videos")
        
        videos_dir = Path("videos")
        if videos_dir.exists():
            videos = list(videos_dir.glob("*"))
            
            if videos:
                st.write(f"**Total videos:** {len(videos)}")
                
                # Show video list with download buttons
                for video in sorted(videos, reverse=True):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.text(video.name)
                    
                    with col2:
                        size_mb = video.stat().st_size / (1024 * 1024)
                        st.text(f"{size_mb:.1f} MB")
                    
                    with col3:
                        with open(video, "rb") as file:
                            st.download_button(
                                label="⬇️",
                                data=file,
                                file_name=video.name,
                                mime="video/mp4",
                                key=f"download_{video.name}"
                            )
            else:
                st.info("No videos uploaded yet")
        else:
            st.info("Videos folder not created yet")
        
        st.markdown("---")
        
        # DANGER ZONE
        with st.expander("⚠️ Danger Zone"):
            st.warning("**These actions cannot be undone!**")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🗑️ Clear This Week's Count"):
                    # This just resets the counter, doesn't delete data
                    st.info("Week counter will reset automatically on Monday")
            
            with col2:
                if st.button("🗑️ Delete All Data"):
                    st.error("This feature is disabled for safety. Manually delete files if needed.")


if __name__ == "__main__":
    main()
    
    # Add admin panel at the bottom
    admin_panel()
