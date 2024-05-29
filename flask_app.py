from flask import Flask, jsonify, render_template, request

from chatbot.chatbot import Chatbot
import openai

PYTHONANYWHERE_USERNAME = "Anidvisor"
PYTHONANYWHERE_WEBAPPNAME = "mysite"




app = Flask(__name__)

# Set up OpenAI API key
openai.api_key = 'OPENAI_API_KEY'

# Function to get anime recommendations based on user input
def get_anime_recommendations(preferences, top_animes, platform):
    prompt = (
        "You are an Anime Series Advisor specialized in recommending anime shows. "
        "Based on the following preferences: {preferences} and top animes: {top_animes}, "
        "suggest some anime series available on {platform}."
    ).format(preferences=preferences, top_animes=top_animes, platform=platform)
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data['message']
    
    # Simple state management for the conversation
    state = data.get('state', {})
    
    if 'top_animes' not in state:
        response = "Welche Anime-Serien gehören zu deinen Top 3?"
        state['stage'] = 'collect_top_animes'
    elif 'preferences' not in state:
        response = "Welche Genres oder Themen magst du besonders? (z.B. Action, Romantik, Fantasy)"
        state['stage'] = 'collect_preferences'
        state['top_animes'] = user_input  # Save user's top animes
    elif 'platform' not in state:
        response = "Auf welcher Streamingplattform möchtest du die Serien schauen? (z.B. Netflix, Crunchyroll)"
        state['stage'] = 'collect_platform'
        state['preferences'] = user_input  # Save user's preferences
    else:
        state['platform'] = user_input  # Save user's platform
        top_animes = state['top_animes']
        preferences = state['preferences']
        platform = state['platform']
        recommendations = get_anime_recommendations(preferences, top_animes, platform)
        response = f"Basierend auf deinen Präferenzen empfehle ich dir folgende Anime-Serien: {recommendations}. Wie zufrieden bist du mit diesen Empfehlungen auf einer Skala von 1-5?"
    
    return jsonify({"message": response, "state": state})

if __name__ == '__main__':
    app.run(debug=True)
