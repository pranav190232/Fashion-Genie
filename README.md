

# 🌟 Fashion Genie — AI-Powered Personal Stylist

**Style smarter. Dress better. Powered by Gemini + Gradio.**

Fashion Genie is an interactive AI-powered personal stylist that provides custom outfit recommendations based on your body type, wardrobe, and preferences. Leveraging **Google Gemini AI** and a sleek **Gradio** interface, Fashion Genie delivers premium, personalized styling advice directly to you.

---

## ✨ Features

* **AI-Powered Styling**:
  Generates two personalized outfits based on wardrobe, occasion, body type, and user preferences.

* **Dynamic Inputs**:
  Automatically updates options like body type, skin tone, hair type, and occasion based on user input. Supports custom descriptions.

* **Wardrobe Integration**:
  Suggests outfits based on user’s existing wardrobe or provides new item recommendations.

* **Pro Styling Tips**:
  Includes expert-level fashion advice on each outfit suggestion.

* **Customizable User Profile**:
  Collects detailed input such as gender, size, body type, and more.

* **Optional Full-Body Image**:
  Users can upload a photo to further personalize outfit recommendations.

* **Luxury Stylist Voice**:
  Offers suggestions in a polished, premium styling tone.

---

## 🛠️ Tech Stack

* **Python**
* **Gradio** (UI Framework)
* **Google Gemini AI 2.5 Flash** (Generative AI Model)
* **Pillow (PIL)** for image handling
* **Google Cloud Platform** for deployment

---

## 🚀 How to Run the App

To get Fashion Genie running, follow these steps:

### 1. **Set Up in Google Cloud**

1. Go to the [Google Cloud Console](https://console.cloud.google.com).
2. In the search bar, type **"Cloud Shell"** and open the **Cloud Shell**.
3. Once Cloud Shell is open, click on the **"Activate Cloud Shell"** button if it's not already active.
4. In the Cloud Shell, type `gcloud init` to initialize your Google Cloud SDK.
5. Clone the repository by typing the following command in Cloud Shell:

   ```bash
   git clone https://github.com/pranav190232/Fashion-Genie.git
   cd Fashion-Genie
   ```

### 2. **Launch the App Using Google Cloud's Online IDE**

1. From Cloud Shell, click the **“Activate Google Cloud Shell Editor”** button (or go to the **Cloud Shell Editor** from the menu).
2. Once the **Google Cloud IDE** opens, click the **"Terminal"** at the bottom.
3. Inside the terminal, run the following to install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### 3. **Run the App**

Once dependencies are installed, start the app using:

```bash
python app.py
```

* You should now see a Gradio interface running locally. Follow the interface to input your styling preferences and wardrobe items.

---

## 📦 Dependencies

* **Gradio**: UI framework for building the interactive interface
* **Pillow (PIL)**: For handling image uploads
* **Google Generative AI (Gemini 2.5)**: For generating personalized styling advice


---


