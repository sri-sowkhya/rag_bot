import streamlit as st
import google.generativeai as genai

def get_career_advice(user_input, api_key):
    """Generates career advice using the Gemini API, keeping it concise."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Provide brief and easy-to-understand career advice for a 16-year-old based on: {user_input}. Keep it short."
    response = model.generate_content(prompt)
    return response.text

def assess_skills(answers, api_key):
    """Analyzes skill assessment answers and provides a short summary."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Analyze these skill assessment answers and provide a short and easy-to-understand summary of strengths and weaknesses for a 16-year-old: {answers}. Keep it very brief."
    response = model.generate_content(prompt)
    return response.text

def recommend_careers(interests, skills, values, api_key):
    """Recommends careers in a short and simple manner."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Recommend 2-3 short and easy-to-understand career options for a 16-year-old based on: interests: {interests}, skills: {skills}, and values: {values}. Keep it short."
    response = model.generate_content(prompt)
    return response.text

def educational_pathways(career, api_key):
    """Provides short and simple educational pathway and required skill information."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"In simple terms, what are the basic educational steps and key skills needed for a 16-year-old interested in a {career} career? Keep it short."
    response = model.generate_content(prompt)
    return response.text

def resume_tips(desired_job, api_key):
    """Provides short and simple resume tips."""
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    prompt = f"Give 2-3 very short and simple resume tips for a 16-year-old applying for a {desired_job} job."
    response = model.generate_content(prompt)
    return response.text

def provide_career_guidance(user_data, api_key):
    """Provides concise and easy-to-understand career guidance."""

    interests = user_data.get("interests", "")
    skills = user_data.get("skills", "")
    values = user_data.get("values", "")
    academic_background = user_data.get("academic_background", "")
    career_goals = user_data.get("career_goals", "")
    additional_info = user_data.get("additional_info", "")

    recommendations = recommend_careers(interests, skills, values, api_key)
    st.subheader("Possible Careers:")
    st.write(recommendations)

    if career_goals:
        pathways = educational_pathways(career_goals, api_key)
        st.subheader("How to Get There & Skills Needed:")
        st.write(pathways)

    general_advice = get_career_advice(f"Interests: {interests}, Skills: {skills}, Values: {values}, Academic: {academic_background}, Goals: {career_goals}, Additional info: {additional_info}", api_key)
    st.subheader("Quick Career Advice:")
    st.write(general_advice)

    skill_analysis = assess_skills(f"Skills: {skills}, Academic: {academic_background}", api_key)
    st.subheader("Your Strengths:")
    st.write(skill_analysis)

    if career_goals:
        resume_advice = resume_tips(career_goals, api_key)
        st.subheader("Resume Tips:")
        st.write(resume_advice)

def main():
    st.title("Career Guidance Bot for Students")
    st.write("Let's explore some career options. Please answer these questions:")

    api_key = st.text_input("Enter your Google API Key:", type="password") #type password masks input.

    user_data = {}

    user_data["interests"] = st.text_input("What do you enjoy doing? (e.g., tech, art, sports)")
    user_data["skills"] = st.text_input("What are you good at? (e.g., drawing, coding, teamwork)")
    user_data["values"] = st.text_input("What's important in a job to you? (e.g., helping others, being creative)")
    user_data["academic_background"] = st.text_input("What subjects are you studying in school?")
    user_data["career_goals"] = st.text_input("What kind of job are you thinking about?")
    user_data["additional_info"] = st.text_area("Anything else you want to add? (Optional)")

    if st.button("Get Career Guidance"):
        if api_key and any(user_data.values()): #check if api key and other inputs were given.
            provide_career_guidance(user_data, api_key)
        elif not api_key :
            st.warning("Please enter your API Key.")
        else:
            st.warning("Please enter some information.")

if __name__ == "__main__":
    main()
