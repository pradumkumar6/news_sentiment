import streamlit as st
import requests
import json

st.title("News Sentiment Analysis & TTS System")

company = st.text_input("Enter Company Name", "Tesla")

if st.button("Get Sentiment Report"):
    try:
        response = requests.get(f"http://127.0.0.1:5000/get_news?company={company}")
        
        if response.status_code == 200:
            data = response.json()

            # Check and convert string to dictionary
            if isinstance(data, str):
                data = json.loads(data)

            # Display company name
            st.header(f"Company: {data['Company']}")
            
            # Display Articles
            for article in data["Articles"]:
                st.subheader(article["Title"])
                st.write(f"**Summary:** {article['Summary']}")
                st.write(f"**Sentiment:** {article['Sentiment']}")
                st.write(f"**Topics:** {', '.join(article['Topics'])}")
                st.write("---")
            
            # Display Comparative Sentiment Score
            st.subheader("Comparative Sentiment Score")
            st.json(data["Comparative Sentiment Score"])

            # Display Final Sentiment Analysis
            st.subheader("Final Sentiment Analysis")
            st.write(data["Final Sentiment Analysis"])

            # Display Audio
            st.subheader("Audio Output")
            audio_url = data["Audio"].split("(")[-1].strip(")")
            st.audio(audio_url)

        else:
            st.error("Failed to fetch data. Please check the API endpoint or company name.")

    except Exception as e:
        st.error(f"Error: {e}")
