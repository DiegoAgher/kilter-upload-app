# Kilter Board Analysis - Streamlit Upload App

## 🎯 What This Does

- Accepts video uploads up to 200MB
- Collects user info (name, email, problem details)
- Tracks weekly submission limit (10/week)
- Logs all submissions to CSV for funnel tracking
- Shows beautiful success confirmation

---

## 📁 Project Structure

```
kilter-streamlit/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Python dependencies
├── .streamlit/
│   └── config.toml       # Config (200MB upload limit)
├── videos/               # Auto-created when first video uploads
└── submissions_tracking.csv  # Auto-created on first submission
```

---

## 🚀 DEPLOYMENT TO STREAMLIT CLOUD (5 Steps)

### Step 1: Create GitHub Repository (2 min)

1. Go to https://github.com/new
2. Repository name: `kilter-upload-app` (or whatever you want)
3. ✅ Make it **PUBLIC** (required for Streamlit free tier)
4. Click "Create repository"

### Step 2: Upload Files to GitHub (3 min)

**Option A: GitHub Web Interface (easiest)**
1. In your new repo, click "uploading an existing file"
2. Drag and drop ALL files:
   - `app.py`
   - `requirements.txt`
   - `.streamlit/config.toml` (upload this to `.streamlit` folder)
3. Click "Commit changes"

**Option B: Git Command Line**
```bash
cd kilter-streamlit
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/kilter-upload-app.git
git push -u origin main
```

### Step 3: Deploy to Streamlit Cloud (3 min)

1. Go to https://share.streamlit.io/
2. Sign in with GitHub
3. Click "New app"
4. Select:
   - Repository: `your-username/kilter-upload-app`
   - Branch: `main`
   - Main file path: `app.py`
5. Click "Deploy!"

⏳ Wait 2-3 minutes for deployment...

### Step 4: Get Your App URL (1 min)

Once deployed, you'll get a URL like:
```
https://your-username-kilter-upload-app-xxxxx.streamlit.app
```

**COPY THIS URL** - you'll need it for the landing page!

### Step 5: Test Your App (2 min)

1. Visit your Streamlit app URL
2. Try uploading a small test video
3. Check that success message appears
4. Verify weekly counter shows "9 spots remaining"

---

## 🔗 CONNECT TO LANDING PAGE

Now go back to your landing page `index.html` and update line 67:

```html
<!-- BEFORE -->
<a href="YOUR_STREAMLIT_APP_URL_HERE" class="upload-button">

<!-- AFTER -->
<a href="https://your-username-kilter-upload-app-xxxxx.streamlit.app" class="upload-button">
```

Save and redeploy your landing page to Netlify.

---

## 📊 FUNNEL TRACKING

### Where Your Data Lives

**Video Files:**
- Stored in `videos/` folder (auto-created)
- Filename format: `20260129_143022_john_doe.mp4`

**Submission Tracking:**
- File: `submissions_tracking.csv`
- Columns:
  - `timestamp` - When uploaded
  - `name` - User name
  - `email` - User email  
  - `problem_grade` - V0-V2, etc.
  - `problem_name` - Optional problem name
  - `video_filename` - Saved video filename
  - `file_size_mb` - Video size
  - `has_notes` - Boolean
  - `status` - "uploaded"

### Download Your Data

**In Streamlit Cloud:**
1. Go to your app settings
2. Click "Open app logs"
3. You'll see options to download files

**Or add a download button:**
Add this to your app.py (after line 250):

```python
# Admin section (add password protection in production!)
if st.checkbox("Show Admin Panel"):
    st.download_button(
        "📥 Download Tracking CSV",
        data=open("submissions_tracking.csv", "rb"),
        file_name="submissions_tracking.csv"
    )
```

### Weekly Metrics Calculation

Open `submissions_tracking.csv` in Google Sheets or Excel:

**Week 1 Funnel:**
1. QR Scans: (from bit.ly)
2. Landing Page Visits: (from Netlify analytics)
3. Upload Page Visits: (count Streamlit sessions)
4. Form Submissions: `COUNT(status="uploaded")`
5. Usable Videos: Manual review
6. Paid Conversions: Track separately

**Conversion Rates:**
- Scan → Landing: Visits / Scans
- Landing → Upload: Streamlit / Landing  
- Upload → Submit: Submissions / Streamlit
- Submit → Usable: Usable / Submissions

---

## 🎨 Customization

### Change Weekly Limit

Edit line 115 in `app.py`:
```python
remaining = max(0, 10 - weekly_count)  # Change 10 to whatever
```

### Add More Form Fields

Add after line 188 in `app.py`:
```python
phone = st.text_input("Phone (optional)")
```

Then update the `submission_data` dict (line 215) to include it.

### Change Colors

Edit the CSS section (lines 23-60) in `app.py`:
```python
background-color: #3B82F6;  # Blue button
background-color: #10B981;  # Green success
```

---

## 🔧 Troubleshooting

**Problem: Upload fails**
- Check file size is under 200MB
- Verify config.toml is in `.streamlit/` folder
- Check Streamlit Cloud logs for errors

**Problem: CSV not saving**
- Streamlit Cloud files are ephemeral
- Videos/CSVs reset when app restarts
- Solution: Use cloud storage (see Advanced Setup below)

**Problem: Weekly counter not resetting**
- Counter resets when app restarts
- For production, use a database

**Problem: Can't see uploaded videos**
- Files are stored on Streamlit's server
- Download via app logs or add download button

---

## 🚨 IMPORTANT: Data Persistence

**Streamlit Cloud Free Tier Limitation:**
Files (videos, CSVs) are stored temporarily and will be LOST when:
- App restarts
- App redeployments
- Server maintenance

**For MVP/Beta (Week 1-2):**
This is FINE! Just download your CSV weekly.

**For Production:**
You'll need cloud storage. See "Advanced Setup" below.

---

## 🎯 Advanced Setup (For Later)

### Option 1: Google Drive Storage
```python
# Install: pip install google-api-python-client
# Upload videos directly to Google Drive
```

### Option 2: AWS S3 Storage  
```python
# Install: pip install boto3
# Store videos in S3 bucket
```

### Option 3: Supabase (Free Database)
```python
# Install: pip install supabase
# Store tracking data in real database
```

**Don't worry about this now!** Start with the basic setup and upgrade later if you get traction.

---

## ⏱️ Total Setup Time

- Step 1: Create GitHub repo (2 min)
- Step 2: Upload files (3 min)
- Step 3: Deploy to Streamlit (3 min)
- Step 4: Get URL (1 min)
- Step 5: Test (2 min)

**Total: ~11 minutes**

---

## 📝 Next Steps Checklist

- [ ] Deploy Streamlit app to Streamlit Cloud
- [ ] Copy your Streamlit app URL
- [ ] Update landing page with Streamlit URL
- [ ] Deploy landing page to Netlify
- [ ] Create bit.ly short link for landing page
- [ ] Generate QR code pointing to bit.ly link
- [ ] Print QR codes
- [ ] Test full funnel (QR → Landing → Upload)
- [ ] Stick QR codes on gym walls
- [ ] Track Week 1 metrics!

---

**You're crushing this! 🚀**
