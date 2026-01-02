import streamlit as st
import base64
from pathlib import Path

def img_to_bytes(img_path):
    """Converts an image file to a Base64 string."""
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

# Create a dummy PNG file for demonstration purposes (replace with your actual file)
# In a real scenario, ensure 'my_image.png' exists in your directory
try:
    from PIL import Image
    import numpy as np
    img_data = np.zeros((150, 200, 3), dtype=np.uint8)
    img_data[25:125, 25:175] = [255, 0, 0] # Red rectangle
    img = Image.fromarray(img_data, 'RGB')
    img.save('my_image.png')
except ImportError:
    st.warning("Install Pillow (`pip install Pillow`) to run the dummy image creation part.")


png_path = 'logo.png'
png_base64 = img_to_bytes(png_path)

svg_string = f"""
<svg width="64" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
    <image href="data:image/png;base64,{png_base64}" x="0" y="0" width="100%" height="100%"/>
</svg>
"""

st.markdown("### Displaying PNG inside an SVG tag via Markdown")
st.markdown(svg_string, unsafe_allow_html=True)