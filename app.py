
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps
import io
import uuid
import os

# Configuration de la page
st.set_page_config(page_title="Concert Dédicace - Chorale Siona", layout="centered")
st.title("🎶 Générateur d'Affiche - Concert Dédicace 2025")

st.markdown("""
Participez au **Concert Dédicace** du *Premier Album de la Chorale Siona* 🎤

📅 **Sabbat 31 Mai 2025 à partir de 15h00**  
📍 **Église Adventiste du Septième Jour de Garoua-Centre**

Veuillez remplir les champs ci-dessous pour générer automatiquement votre affiche personnalisée.
""")

# Entrées utilisateur
name = st.text_input("Entrez votre nom complet :")
profile_pic = st.file_uploader("Téléversez votre photo de profil :", type=["png", "jpg", "jpeg"])
generate_btn = st.button("🎨 Générer mon affiche")

if generate_btn and name and profile_pic:
    # Charger image de fond
    image_path = os.path.join(os.path.dirname(__file__), "Blue, Black and Red Illustrative Modern Music Festival Promotion Flyer.jpg")
    background = Image.open(image_path).convert("RGBA")
    width, height = background.size
    template = background.copy()

    # ✅ Photo de profil de 3/4 format A5 (1311px)
    profile_size = 1311
    profile_img = Image.open(profile_pic).convert("RGB").resize((profile_size, profile_size))
    mask = Image.new('L', (profile_size, profile_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse((0, 0, profile_size, profile_size), fill=255)

    # ✅ Bordure blanche large
    # Ajouter un cercle plus grand blanc en dessous comme vraie bordure
border_size = 40
big_size = profile_size + 2 * border_size

circle_border = Image.new("RGB", (big_size, big_size), "white")
circle_mask = Image.new("L", (big_size, big_size), 0)
draw_mask = ImageDraw.Draw(circle_mask)
draw_mask.ellipse((0, 0, big_size, big_size), fill=255)

# Coller la photo dans le cercle blanc
circle_border.paste(profile_img, (border_size, border_size), mask)


    # ✅ Position bien placée
    pos_x = width - profile_size - 80
    pos_y = 240
    template.paste(circle_border, (pos_x, pos_y), circle_mask)

    # ✅ Texte clair et espacé
    draw = ImageDraw.Draw(template)
    try:
        font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
        name_font = ImageFont.truetype(font_path, 72)
        msg_font = ImageFont.truetype(font_path, 58)
    except:
        name_font = msg_font = None

    name_x = pos_x + profile_size // 2
    name_y = pos_y + profile_size + 70
    msg_y = name_y + 80

    draw.text((name_x, name_y), name, font=name_font, fill="white", anchor="mm")
    draw.text((name_x, msg_y), "Je serai là !", font=msg_font, fill="white", anchor="mm")

    # Sauvegarde et affichage
    output = io.BytesIO()
    template.save(output, format="PNG")
    output.seek(0)

    st.image(template, caption="Votre affiche personnalisée", use_container_width=True)
    st.download_button("📥 Télécharger l'affiche", data=output, file_name=f"affiche_siona_{uuid.uuid4().hex[:8]}.png", mime="image/png")

elif generate_btn:
    st.warning("Merci de remplir tous les champs (nom + photo) pour générer votre affiche.")
