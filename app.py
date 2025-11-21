import gradio as gr
import base64
import io
from PIL import Image
import google.generativeai as genai  # SIMPLE + DIRECT

# ---------------------------------------------------------
# 🔑 SET YOUR GEMINI API KEY HERE
# ---------------------------------------------------------
GEMINI_API_KEY = "keep your own key by creating on google ai studio"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------------------------------------------------
# UI STYLING (unchanged)
# ---------------------------------------------------------
custom_css = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Lato:wght@300;400&display=swap');

.gradio-container {
    background-color: #121212 !important;
    color: #F5F5F5 !important;
    font-family: 'Lato', sans-serif !important;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #D4AF37 !important;
    font-weight: 700 !important;
}

textarea, input {
    background-color: #1E1E1E !important;
    border: 1px solid #333 !important;
    color: #E0E0E0 !important;
}

button.primary-btn {
    background: linear-gradient(135deg, #D4AF37, #C5A028) !important;
    color: #121212 !important;
    font-family: 'Playfair Display', serif !important;
    border: none !important;
}

.markdown-text {
    background-color: #1A1A1A !important;
    padding: 25px;
    border-left: 3px solid #D4AF37;
    border-radius: 4px;
}
"""

# ---------------------------------------------------------
# BODY TYPES (improved dropdowns and input types)
# ---------------------------------------------------------
BODY_TYPES_FEMALE = [
    "Hourglass (Balanced bust & hips, defined waist)",
    "Pear / Triangle (Hips wider than shoulders)",
    "Apple / Round (Weight carried around midsection)",
    "Inverted Triangle (Shoulders wider than hips)",
    "Rectangle / Athletic (Straight silhouette, few curves)",
    "Petite (Under 5'3, proportional)",
    "Other (Please describe)"
]

BODY_TYPES_MALE = [
    "Trapezoid (Broad shoulders, slightly tapered waist)",
    "Inverted Triangle (Broad shoulders, narrow waist)",
    "Rectangle (Straight silhouette)",
    "Triangle (Hips wider than shoulders)",
    "Oval (Rounder midsection)",
    "Other (Please describe)"
]

SKIN_TONE_OPTIONS = ["Fair", "Medium", "Olive", "Dark", "Deep", "Other (Please describe)"]
HAIR_TYPE_OPTIONS = ["Straight", "Wavy", "Curly", "Coily", "Other (Please describe)"]

SIZES = ["XS", "S", "M", "L", "XL", "XXL", "XXXL"]

# ---------------------------------------------------------
# BODY TYPE UPDATE FUNCTION
# ---------------------------------------------------------
def update_body_options(gender):
    if gender == "Female":
        return gr.Dropdown(choices=BODY_TYPES_FEMALE, value=BODY_TYPES_FEMALE[0], interactive=True)
    elif gender == "Male":
        return gr.Dropdown(choices=BODY_TYPES_MALE, value=BODY_TYPES_MALE[0], interactive=True)
    else:
        combined = list(set(BODY_TYPES_FEMALE + BODY_TYPES_MALE))
        return gr.Dropdown(choices=combined, value=combined[0], interactive=True)

# ---------------------------------------------------------
# Show description input when 'Other' is selected for body type, skin tone, or hair type
# ---------------------------------------------------------
def show_custom_input(option):
    if "Other" in option:
        return gr.update(visible=True)
    else:
        return gr.update(visible=False)

# ---------------------------------------------------------
# ⭐ AI CALL — CLEAN VERSION WITH ADDED TEXT INPUT
# ---------------------------------------------------------
def get_stylist_advice(gender, body_type, size, height_weight, skin_tone, hair_type, occasion, styling_preference, wardrobe, user_image, characteristics_text, body_type_other, skin_tone_other, hair_type_other, occasion_other):

    # Consolidate "Other" descriptions
    if body_type == "Other (Please describe)" and body_type_other:
        body_type = f"Other: {body_type_other}"
    if skin_tone == "Other (Please describe)" and skin_tone_other:
        skin_tone = f"Other: {skin_tone_other}"
    if hair_type == "Other (Please describe)" and hair_type_other:
        hair_type = f"Other: {hair_type_other}"
    if occasion == "Other" and occasion_other:
        occasion = f"Other: {occasion_other}"

    # Dynamic instructions based on styling preference
    if styling_preference == "From My Wardrobe":
        outfit_instructions = """
- Provide 2 detailed outfits exclusively from the client's provided wardrobe.
- If the wardrobe is insufficient, suggest 1-2 key items to acquire that would complete the looks.
"""
        outfit_format = """
## Outfit 1 — From Your Wardrobe
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 

## Outfit 2 — From Your Wardrobe
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 
"""
    elif styling_preference == "Suggest New Items":
        outfit_instructions = "- Provide 2 detailed 'Shop the Look' outfits with new item suggestions."
        outfit_format = """
## Outfit 1 — Shop the Look
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 

## Outfit 2 — Shop the Look
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 
"""
    else: # Both
        outfit_instructions = """
- Provide 2 detailed outfits:
  1. From Their Wardrobe
  2. Shop The Look
"""
        outfit_format = """
## Outfit 1 — From Your Wardrobe
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 

## Outfit 2 — Shop the Look
* **Top:** 
* **Bottom:** 
* **Shoes:** 
* **Why This Works:** 
"""

    prompt = f"""
You are an elite luxury fashion stylist.

### CLIENT PROFILE
Gender: {gender}
Body Type: {body_type} 
Size: {size}
Height/Weight: {height_weight}
Skin Tone: {skin_tone}
Hair Type: {hair_type}
Occasion: {occasion}
Wardrobe: {wardrobe}
Physical Characteristics & Style Persona: {characteristics_text}

### INSTRUCTIONS
- Use a premium, luxury stylist tone (e.g., Nordstrom, Stitch Fix).
{outfit_instructions}
- Focus on fit, functionality, and color coordination.
- Include quick reasons why each outfit works.

### FORMAT EXACTLY LIKE THIS:
{outfit_format}
## Pro Styling Tips
1. 
2. 
"""

    # If an image is uploaded, attach it to the request
    inputs = [prompt]

    if user_image:
        buffer = io.BytesIO()
        user_image.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
        inputs.append({"mime_type": "image/jpeg", "data": img_bytes})

    response = model.generate_content(inputs)
    return response.text

# ---------------------------------------------------------
# UI
# ---------------------------------------------------------
with gr.Blocks(css=custom_css) as app:

    gr.Markdown("""
    # Fashion Genie  
    ### Style smarter dress better  
    """)
    
    with gr.Row():
        with gr.Column():
            gender_input = gr.Radio(["Female", "Male", "Non-Binary"], label="Gender", value="Female")
            size_input = gr.Dropdown(SIZES, label="Size", value="M")
            body_type_input = gr.Dropdown(choices=BODY_TYPES_FEMALE, label="Body Type", value="Hourglass")
            body_type_other_input = gr.Textbox(label="Describe your body type", visible=False, interactive=True)
            height_weight_input = gr.Textbox(label="Height & Weight", placeholder="e.g., 5'6, 140 lbs")
            skin_tone_input = gr.Dropdown(SKIN_TONE_OPTIONS, label="Skin Tone", value="Medium")
            skin_tone_other_input = gr.Textbox(label="Describe your skin tone", visible=False, interactive=True)
            hair_type_input = gr.Dropdown(HAIR_TYPE_OPTIONS, label="Hair Type", value="Straight")
            hair_type_other_input = gr.Textbox(label="Describe your hair type", visible=False, interactive=True)
            occasion_input = gr.Dropdown(["Casual", "Formal", "Evening", "Date Night", "Office", "Wedding", "Other"], label="Occasion")
            occasion_other_input = gr.Textbox(label="Describe the occasion", visible=False, interactive=True)
            styling_preference_input = gr.Radio(["From My Wardrobe", "Suggest New Items", "Both"], label="Styling Preference", value="Both")
            wardrobe_input = gr.Textbox(label="Wardrobe Items", lines=3, placeholder="e.g., black jeans, white blouse, leather jacket")
            characteristics_input = gr.Textbox(label="Describe Your Physical Characteristics & Style Persona (Optional)", lines=4, placeholder="e.g., Broad shoulders, long torso, athletic legs. I prefer minimalist, high-quality basics and have a classic, slightly edgy style.")
            image_input = gr.Image(type="pil", label="Upload Full Body Photo (Optional)")

            submit_btn = gr.Button("GENERATE MY STYLE EDIT", elem_classes=["primary-btn"])

        with gr.Column():
            output_area = gr.Markdown("Your stylist results will appear here...", elem_classes=["markdown-text"])

    gr.Markdown("""
    ---
    ### Need Help Describing Yourself? 
    For a detailed physical and style description to paste above, copy the prompt below and use it with an AI model like GPT-4 or Claude. Just replace the bracketed text with your own details.
    
    `Act as a personal stylist's assistant. I need to create a detailed client profile. Based on the photos I provide, write a concise, well-structured paragraph describing my physical characteristics making sure skintone , hairtype ,body type and all important parameters are covered`
    """)
    gender_input.change(update_body_options, inputs=gender_input, outputs=body_type_input)

    # Show custom input when 'Other' is selected
    body_type_input.change(show_custom_input, inputs=body_type_input, outputs=body_type_other_input)
    skin_tone_input.change(show_custom_input, inputs=skin_tone_input, outputs=skin_tone_other_input)
    hair_type_input.change(show_custom_input, inputs=hair_type_input, outputs=hair_type_other_input)
    occasion_input.change(show_custom_input, inputs=occasion_input, outputs=occasion_other_input)

    submit_btn.click(
        get_stylist_advice,
        inputs=[gender_input, body_type_input, size_input, height_weight_input, skin_tone_input, hair_type_input, occasion_input, styling_preference_input, wardrobe_input, image_input, characteristics_input, body_type_other_input, skin_tone_other_input, hair_type_other_input, occasion_other_input],
        outputs=output_area
    )


if __name__ == "__main__":
    app.launch()
