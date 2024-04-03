import streamlit as st
from langchain import PromptTemplate
from langchain_community.llms import OpenAI
import os

template = """
 You are a marketing copywriter with 20 years of experience. You are analyzing customer's background to write personalized product description that only this customer will receive; 
    PRODUCT input text: {content};
    CUSTOMER household size: {household_size};
    CUSTOMER favorite color: {color_preference};
    TASK: Write a product description that is tailored into this customer's Household size and color preference.;
    FORMAT: Present the result in the following order: (PRODUCT DESCRIPTION), (BENEFITS), (USE CASE);
    PRODUCT DESCRIPTION: describe the product in 5 sentences;
    BENEFITS: describe in 3 sentences why this product is perfect considering customers household size and color preference;
    USE CASE: write a story in 5 sentences, of an example weekend activity taking into account color preference {color_preference} and household size {household_size}, write a story in first person, example "I started my Saturday morning with ..." OUTPUT TEXT in Estonian;
"""

prompt = PromptTemplate(
    input_variables=["household_size", "color_preference", "content"],
    template=template,
)

def load_LLM(openai_api_key):
    llm = OpenAI(model_name='gpt-3.5-turbo-instruct', temperature=.7, openai_api_key=openai_api_key)
    return llm

st.set_page_config(page_title="Customer tailored content", page_icon=":robot:")
st.header("Personaliseeritud turundusteksti konverter")

col1, col2 = st.columns(2)

with col1:
    st.markdown("Otstarve: tootetutvustustekstide personaliseerimine igale kliendile või kliendigruppidele; väljundtekst on kohandatud kliendi a) leibkonna suuruse ja b) värvieelistuse alusel; sisendtekstiks on neutraalses vormis tootekirjeldus. \
    \n\n Kasutusjuhend: 1) valmista ette tootekirjeldus (sisendtekst). 2) määra tarbijasegemendid lähtuvalt leibkonna suuruse ja värvieelistuste kombinatsioonidest. 3) sisesta ükshaaval tarbijasegmentide lõikes eeltoodud info äpi kasutajaliideses, saada ära. \
    4) kopeeri ükshaaval tarbijasegmentide lõikes äpi väljundteksti kõnealuse toote tutvustuslehele.")

with col2:
    st.image(image='companylogo.jpg', caption='Natural and healthy wooden garden houses for everybody')

st.markdown("## Enter Your Content To Convert")

def get_api_key():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if openai_api_key:
        return openai_api_key
    # If OPENAI_API_KEY environment variable is not set, prompt user for input
    input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
    return input_text

openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    option_household_size = st.selectbox(
        'What is the size of the household?',
        ('1-2', '3-4', '5-6', '7-8', '9-10'))
    
def get_color_preference():
    input_text = st.text_input(label="Customer's favorite color", key="color_preference_input")
    return input_text

color_preference_input = get_color_preference()

def get_text():
    input_text = st.text_area(label="Content Input", label_visibility='collapsed', placeholder="Your content...", key="content_input")
    return input_text

content_input = get_text()

if len(content_input.split(" ")) > 700:
    st.write("Please enter a shorter content. The maximum length is 700 words.")
    st.stop()

def update_text_with_example():
    print ("in updated")
    st.session_state.content_input = "Wooden garden houses, various sizes and designs, high-quality wood, eco-friendly production"

st.button("*GENERATE TEXT*", type='secondary', help="Click to see an example of the content you will be converting.", on_click=update_text_with_example)

st.markdown("### Your customer tailored content:")

if content_input:
    llm = load_LLM(openai_api_key=openai_api_key)
    prompt_with_content = prompt.format(household_size=option_household_size, color_preference=color_preference_input, content=content_input)
    formatted_content = llm(prompt_with_content)
    st.write(formatted_content)
