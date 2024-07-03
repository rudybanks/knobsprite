import streamlit as st
from PIL import Image
import os
import base64

# URL of the raw logo file on GitHub
logo_url = "https://raw.githubusercontent.com/rudybanks/knobsprite/main/banxmusic_logo_github.jpg"

# Website URL
website_url = "http://banxmusic.com"

# Display the logo next to the title using markdown and HTML
st.markdown(
    f"<div style='display: flex; align-items: center;'>"
    f"<a href='{website_url}' target='_blank'><img src='{logo_url}' width='50'></a>"
    f"<h1 style='margin-left: 20px;'>Knob Sprite Generator</h1>"
    f"</div>",
    unsafe_allow_html=True,
)

# Add instructions
st.markdown("**Select Output Knob Size > Update filename > Load knob png image > Generate > Download**")

# Create a variable to hold the image size
image_size = st.slider("Knob Output Size", min_value=25, max_value=400, value=200)

# Create a variable to hold the output filename
#output_filename = st.text_input("OUTPUT FILENAME: Use Default or Rename", value="sprite.png")
st.markdown("**OUTPUT FILENAME: Use Default or Rename**")
output_filename = st.text_input("", value="sprite.png")



# Create a function to handle file selection
@st.cache
def load_image(file):
    return Image.open(file)

# Create a function to generate the sprite
def generate_sprite(image_path, image_size, output_filename):
    # Load the knob image
    knob = load_image(image_path)

    # Resize the image based on the slider value
    knob = knob.resize((image_size, image_size))

    # Create a list to hold the rotated images
    frames = []

    # Rotate the knob for each step and add to frames
    for i in range(128):
        angle = -i * (280 / 127)  # Calculate the angle for this step
        rotated = knob.rotate(angle)
        frames.append(rotated)

    # Create an empty image for the sprite
    sprite = Image.new('RGBA', (image_size, image_size * 128))

    # Paste each frame into the sprite
    for i, frame in enumerate(frames):
        sprite.paste(frame, (0, i * image_size))

    # Save the sprite with the user-specified filename
    sprite.save(output_filename)

    # Convert the image file to bytes
    with open(output_filename, "rb") as img_file:
        img_bytes = img_file.read()
    return img_bytes



# Create a button to select a file
uploaded_file = st.file_uploader("Select file", type=['png'])

if uploaded_file is not None:
    # Create a button to generate the sprite
    if st.button("Generate sprite"):
        sprite_bytes = generate_sprite(uploaded_file, image_size, output_filename)
        st.success("Sprite generated successfully!")

        # Create a download button for the sprite
        st.download_button(
            label="Download sprite",
            data=sprite_bytes,
            file_name=output_filename,
            mime="image/png",
        )

# Add copyright text at the bottom
st.write("©2024 [banxmusic.com](%s)" % website_url)


