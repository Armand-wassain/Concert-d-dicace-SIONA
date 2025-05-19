
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import uuid

# Set page config
st.set_page_config(page_title="Générateur d'affiche IA", layout="centered")
st.title("📸 Générateur Automatique d'Affiche IA 2025")

st.markdown("""
Remplissez les champs ci-dessous pour générer automatiquement votre affiche personnalisée pour la Conférence IA 2025. Vous pourrez la télécharger directement.
""")

# User input
name = st.text_input("Entrez votre nom complet :")
profile_pic = st.file_uploader("Téléversez votre photo de profil :", type=["png", "jpg", "jpeg"])
generate_btn = st.button("Générer mon affiche")

if generate_btn and name and profile_pic:
    # Load profile image
    profile_img = Image.open(profile_pic).convert("RGB")
    profile_size = 400
    profile_img = profile_img.resize((profile_size, profile_size))

    # Create circular mask
    mask = Image.new('L', (profile_size, profile_size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, profile_size, profile_size), fill=255)

    # Add white border
    bordered_profile = ImageOps.expand(profile_img, border=10, fill='white')
    bordered_mask = ImageOps.expand(mask, border=10, fill=255)

    # Create base template
    width, height = 800, 1200
    background_color = (30, 30, 60)
    template = Image.new("RGBA", (width, height), background_color)
    draw = ImageDraw.Draw(template)

    # Fonts
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        title_font = ImageFont.truetype(font_path, 60)
        name_font = ImageFont.truetype(font_path, 50)
        subtitle_font = ImageFont.truetype(font_path, 36)
    except:
        title_font = name_font = subtitle_font = None

    # Add texts
    draw.text((width // 2, 50), "Conférence IA 2025", font=title_font, fill="white", anchor="mm")
    draw.text((width // 2, 1000), name, font=name_font, fill="white", anchor="mm")
    draw.text((width // 2, 1070), "Présent à l'événement", font=subtitle_font, fill="lightgray", anchor="mm")

    # Paste profile picture
    template.paste(bordered_profile, (width // 2 - profile_size // 2, 500), bordered_mask)

    # Save to BytesIO
    img_bytes = io.BytesIO()
    template.save(img_bytes, format='PNG')
    img_bytes.seek(0)

    # Display and offer download
    st.image(template, caption="Votre affiche", use_column_width=True)
    st.download_button("📥 Télécharger l'affiche", data=img_bytes, file_name=f"affiche_{uuid.uuid4().hex[:8]}.png", mime="image/png")

elif generate_btn:
    st.warning("Merci de remplir tous les champs avant de générer l'affiche.")
