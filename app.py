from flask import Flask, request, send_file, jsonify
from PIL import Image, ImageDraw, ImageFont
import uuid
import os

app = Flask(__name__)

@app.route('/generate-thumbnail', methods=['POST'])
def generate_thumbnail():
    source = request.form.get("source", "default")
    name = request.form.get("name", "John Doe")

    person_image_map = {
        "linkedin": "person1.png"
    }

    person_img_path = os.path.join("assets", person_image_map.get(source, "person1.png"))
    bg_img_path = os.path.join("assets", "background.png")
    output_id = uuid.uuid4().hex
    output_dir = "generated"
    os.makedirs(output_dir, exist_ok=True)

    # Sanity check: can we even write a file?
    try:
        Image.new("RGB", (100, 100), color="red").save(os.path.join(output_dir, "test_write.png"))
    except Exception as e:
        return jsonify({"error": f"Unable to write to output folder: {str(e)}"}), 500

    try:
        # === Load background ===
        if not os.path.exists(bg_img_path):
            return jsonify({"error": f"Background image not found: {bg_img_path}"}), 500

        try:
            background = Image.open(bg_img_path)
        except Exception as e:
            return jsonify({"error": f"Failed to open background image: {str(e)}"}), 500

        try:
            background = background.convert("RGBA")
        except Exception as e:
            return jsonify({"error": f"Failed to convert background to RGBA: {str(e)}"}), 500

        try:
            background.save(os.path.join(output_dir, f"stage_1_background_{output_id}.png"))
        except Exception as e:
            return jsonify({"error": f"Failed to save background image: {str(e)}"}), 500

        # === Load person image ===
        if not os.path.exists(person_img_path):
            return jsonify({"error": f"Person image not found: {person_img_path}"}), 500

        try:
            person = Image.open(person_img_path).convert("RGBA").resize((300, 300))
            person.save(os.path.join(output_dir, f"stage_2_person_resized_{output_id}.png"))
        except Exception as e:
            return jsonify({"error": f"Failed to process person image: {str(e)}"}), 500

        # === Paste ===
        try:
            composed = background.copy()
            px = (composed.width - person.width) // 2
            py = (composed.height - person.height) // 2
            composed.paste(person, (px, py), person)
            composed.save(os.path.join(output_dir, f"stage_3_pasted_{output_id}.png"))
        except Exception as e:
            return jsonify({"error": f"Failed to paste person image: {str(e)}"}), 500

        # === Text ===
        try:
            draw = ImageDraw.Draw(composed)
            font = ImageFont.load_default()
            draw.text((px, py + person.height + 10), name, font=font, fill="black")
            composed.save(os.path.join(output_dir, f"stage_4_text_{output_id}.png"))
        except Exception as e:
            return jsonify({"error": f"Failed to draw text: {str(e)}"}), 500

        # === Save final ===
        final_path = os.path.join(output_dir, f"final_{output_id}.png")
        try:
            composed.save(final_path)
        except Exception as e:
            return jsonify({"error": f"Failed to save final thumbnail: {str(e)}"}), 500

        if not os.path.exists(final_path) or os.path.getsize(final_path) == 0:
            return jsonify({"error": "Final file is missing or empty"}), 500

        return send_file(final_path, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": f"Unhandled exception: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)





