import streamlit as st
import cv2
import face_recognition
import os
import numpy as np
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from PIL import Image
import base64

# === Setup ===
st.set_page_config(page_title="Face Attendance", layout="centered")
st.title("🎥 Face Attendance System")

# Paths
FACE_DIR = "Face_data"
CSV_FILE = "attendance.csv"
os.makedirs(FACE_DIR, exist_ok=True)
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=["Name", "Timestamp"]).to_csv(CSV_FILE, index=False)

# Admin Config
# --- Admin Authentication Setup ---
ADMIN_PASSWORD = "admin123"
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False


# Load known faces
def load_known_faces():
    encodings, names = [], []
    for file in os.listdir(FACE_DIR):
        img_path = os.path.join(FACE_DIR, file)
        img = cv2.imread(img_path)
        if img is not None:
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            enc = face_recognition.face_encodings(rgb)
            if enc:
                encodings.append(enc[0])
                names.append(os.path.splitext(file)[0])
    return encodings, names

# === Face Registration ===
st.subheader("📸 Register New Face")

reg_col1, reg_col2 = st.columns(2)

with reg_col1:
    name = st.text_input("Enter name for registration:")
    if st.button("📷 Register via Webcam"):
        if not name.strip():
            st.warning("Please enter a valid name.")
        else:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                st.error("❌ Cannot access webcam.")
            else:
                st.info("Capturing... Look into the camera.")
                success, frame = cap.read()
                cap.release()

                if not success or frame is None:
                    st.error("❌ Failed to capture image.")
                else:
                    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    faces = face_recognition.face_locations(rgb)
                    encodings = face_recognition.face_encodings(rgb, faces)
                    if encodings:
                        y1, x2, y2, x1 = faces[0]
                        crop = frame[y1:y2, x1:x2]
                        path = os.path.join(FACE_DIR, f"{name.lower()}.jpg")
                        cv2.imwrite(path, crop)
                        st.success(f"✅ Saved as {path}")
                    else:
                        st.error("❌ No face found. Try again.")

with reg_col2:
    uploaded = st.file_uploader("📁 Or Upload Face Image", type=["jpg", "png"])
    if uploaded and name.strip():
        img = Image.open(uploaded)
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)
        if encodings:
            y1, x2, y2, x1 = faces[0]
            crop = img_cv[y1:y2, x1:x2]
            path = os.path.join(FACE_DIR, f"{name.lower()}.jpg")
            cv2.imwrite(path, crop)
            st.success(f"✅ Face saved from uploaded image as {path}")
        else:
            st.error("❌ No face found in uploaded image.")

# === Live Attendance ===
st.subheader("📡 Live Attendance")

if st.button("🟢 Start Camera and Detect"):
    known_encodings, known_names = load_known_faces()
    cap = cv2.VideoCapture(0)
    st.info("Detecting faces... Press 'q' in the camera window to stop.")

    df = pd.read_csv(CSV_FILE)
    now = datetime.now()
    today = now.date()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = face_recognition.face_locations(rgb)
        encodings = face_recognition.face_encodings(rgb, faces)

        for encoding, location in zip(encodings, faces):
            matches = face_recognition.compare_faces(known_encodings, encoding)
            distances = face_recognition.face_distance(known_encodings, encoding)
            if matches:
                best = np.argmin(distances)
                if matches[best]:
                    name = known_names[best]
                    y1, x2, y2, x1 = location
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, name.upper(), (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

                    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                    if not ((df['Name'] == name) & (df['Timestamp'].dt.date == today)).any():
                        dt = now.strftime('%Y-%m-%d %H:%M:%S')
                        df.loc[len(df.index)] = [name, dt]
                        df.to_csv(CSV_FILE, index=False)
                        st.success(f"📌 Marked attendance for {name}")

        cv2.imshow("Live Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# === View Logs ===
st.subheader("🧾 Attendance Log")
df = pd.read_csv(CSV_FILE)
st.dataframe(df)

# === Per-User History ===
st.subheader("📂 Per-User History")
if not df.empty:
    user_list = sorted(df["Name"].unique())
    selected = st.selectbox("Choose user:", user_list)
    user_df = df[df["Name"] == selected]
    st.dataframe(user_df)

# === Analytics ===
st.subheader("📊 Analytics")
df['Timestamp'] = pd.to_datetime(df['Timestamp'])

tab1, tab2 = st.tabs(["Per Person", "Daily Trend"])

with tab1:
    counts = df["Name"].value_counts().reset_index()
    counts.columns = ["Name", "Count"]
    st.bar_chart(data=counts, x="Name", y="Count")

with tab2:
    df["Date"] = df["Timestamp"].dt.date
    trend = df.groupby("Date").size().reset_index(name="Total")
    fig, ax = plt.subplots()
    ax.plot(trend["Date"], trend["Total"], marker="o")
    ax.set_title("Daily Attendance")
    st.pyplot(fig)

# === SIDEBAR ADMIN PANEL ===
# === SIDEBAR ADMIN PANEL ===
st.sidebar.header("🔐 Admin Panel")

# Login Section
if not st.session_state.admin_authenticated:
    with st.sidebar.form("admin_login"):
        pwd = st.text_input("Enter Admin Password", type="password")
        login = st.form_submit_button("Login")
        if login:
            if pwd == ADMIN_PASSWORD:
                st.session_state.admin_authenticated = True
                st.sidebar.success("✅ Admin logged in.")
                st.rerun()  # 🔄 Force UI to refresh
            else:
                st.sidebar.error("❌ Incorrect password.")

# Admin Controls Section
if st.session_state.admin_authenticated:
    st.sidebar.success("🛡️ Admin Access Granted")

    # --- Reset Options ---
    st.sidebar.markdown("### 🧹 Attendance Control")

    if st.sidebar.button("🧼 Clear Today's Attendance"):
        df = pd.read_csv(CSV_FILE)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        today = datetime.now().date()
        df = df[df["Timestamp"].dt.date != today]
        df.to_csv(CSV_FILE, index=False)
        st.sidebar.success("✅ Today's attendance cleared.")

    if st.sidebar.button("🔥 Clear ALL Attendance"):
        pd.DataFrame(columns=["Name", "Timestamp"]).to_csv(CSV_FILE, index=False)
        st.sidebar.success("🗑️ All attendance data cleared.")

    # --- CSV Download ---
    st.sidebar.markdown("### 📥 Download Data")
    def get_csv_link(df):
        csv = df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        return f'<a href="data:file/csv;base64,{b64}" download="attendance.csv">⬇️ Download CSV</a>'

    st.sidebar.markdown(get_csv_link(pd.read_csv(CSV_FILE)), unsafe_allow_html=True)

    # --- Logout Button ---
    st.sidebar.markdown("### 🔓 Logout")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.admin_authenticated = False
        st.sidebar.info("You have been logged out.")
        st.rerun()
