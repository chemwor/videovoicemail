# from flask import Flask, request, send_file
# from PIL import Image, ImageDraw, ImageFont
# import uuid
# import os
#
# app = Flask(__name__)
#
# @app.route('/generate-thumbnail', methods=['POST'])
# def generate_thumbnail():
#     source = request.form.get("source", "default")
#     name = request.form.get("name", "John Doe")
#
#     person_image_map = {
#         "linkedin": "person1.png"
#     }
#
#     person_img_path = os.path.join("assets", person_image_map.get(source, "person1.png"))
#     bg_img_path = os.path.join("assets", "background.png")
#
#     # Create the output folder if it doesn't exist
#     os.makedirs("generated", exist_ok=True)
#     final_path = os.path.join("generated", f"{uuid.uuid4().hex}_thumb.png")
#
#     try:
#         # Load images
#         background = Image.open(bg_img_path).convert("RGBA")
#         person = Image.open(person_img_path).convert("RGBA").resize((300, 300))
#
#         # Paste person image
#         background.paste(person, (50, 100), person)
#
#         # Draw text
#         draw = ImageDraw.Draw(background)
#         font = ImageFont.load_default()
#         draw.text((400, 150), name, font=font, fill="black")
#
#         # Save to local folder (not /tmp)
#         background.save(final_path)
#
#         print(f"Saved thumbnail to: {final_path}")
#         return send_file(final_path, mimetype='image/png')
#
#     except Exception as e:
#         return {"error": str(e)}, 500
#
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

app = Flask(__name__)
os.makedirs("generated", exist_ok=True)

@app.route('/generate-thumbnail', methods=['POST'])
def generate_thumbnail():
    name = request.form.get("name", "John Doe")
    # person_file = request.files.get("person")
    # if not person_file:
    #     return {"error": "Missing person image file"}, 400

    # Paths
    bg_path = os.path.join("assets", "background.png")
    bg = Image.open(bg_path).convert("RGBA")

    person_file = os.path.join("assets", "person1.png")
    # Load and resize person image
    person = Image.open(person_file).convert("RGBA")
    person = person.resize((300, 300), Image.LANCZOS)

    # Center person
    bg_width, bg_height = bg.size
    px, py = (bg_width - person.width) // 2, (bg_height - person.height) // 2
    bg.paste(person, (px, py), person)

    # Draw text (optional)
    draw = ImageDraw.Draw(bg)
    font = ImageFont.load_default()  # Or use truetype if you prefer
    text_x, text_y = (bg_width // 2) - 50, py + person.height + 20
    draw.text((text_x, text_y), name, font=font, fill="black")

    # Save and return
    filename = f"generated/thumbnail_{uuid.uuid4().hex}.png"
    bg.save(filename)
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)

