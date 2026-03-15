import streamlit as st
from pathlib import Path
import base64

st.set_page_config(layout="centered")

profile_pic = Path(__file__).parent.parent.parent / "assets" / "headshot.jpg"
linkedin = Path(__file__).parent.parent.parent / "assets" / "linkedin2.png"
github = Path(__file__).parent.parent.parent / "assets" / "github2.png"
email = Path(__file__).parent.parent.parent / "assets" / "email4.png"
cv = Path(__file__).parent.parent.parent / "assets" / "cv.png"
cv_pdf = Path(__file__).parent.parent.parent / "assets" / "resume_web.pdf"

PAGE_TITLE = "Digital CV | Corey Kirkwood"
PAGE_ICON = ":wave:"
NAME = "Corey Kirkwood"
DESCRIPTION = """
Veteran | Leader | Data Scientist
"""
EMAIL = "coreymkirkwood@gmail.com"
st.markdown(
    """
    <style>
        /* This targets the image inside the column */
        [data-testid="stImage"] img {
            border-radius: 50%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
        }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns(2, gap="small")
with col1:
    st.image(profile_pic, width=230)

with col2:
    st.title(NAME)
    st.write(DESCRIPTION)
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(
                """<a href="https://www.linkedin.com/in/corey-kirkwood-836ab4271/">
                <img src="data:image/png;base64,{}" width="25">
                </a>""".format(
                    base64.b64encode(open(linkedin, "rb").read()).decode()
                ),
                unsafe_allow_html=True,
            )
            st.markdown("<br>",unsafe_allow_html=True)
        with col2:
            st.markdown(
                """<a href="https://github.com/kirkwodoster">
                <img src="data:image/png;base64,{}" width="25">
                </a>""".format(
                    base64.b64encode(open(github, "rb").read()).decode()
                ),
                unsafe_allow_html=True,
            )
            st.markdown("<br>",unsafe_allow_html=True)
        
        with col3:
            st.markdown(
            """<a href="mailto:coreymkirkwood@gmail.com">
                <img src="data:image/png;base64,{}" width="25">
                </a>""".format(
                    base64.b64encode(open(email, "rb").read()).decode()
                ),
                unsafe_allow_html=True,
            )
            st.markdown("<br>",unsafe_allow_html=True)

        with col4:
            # If your PDF is in the same directory as your app
            with open(cv_pdf, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
            
            # Encode PDF to base64 for the link
            encoded_pdf = base64.b64encode(pdf_bytes).decode()
            
            # Create download link for PDF
            st.markdown(
                f"""<a href="data:application/pdf;base64,{encoded_pdf}" download="filename.pdf">
                <img src="data:image/png;base64,{base64.b64encode(open(cv, 'rb').read()).decode()}" width="25">
                </a>""",
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)
        # with col4:
        #     st.markdown(
        #         """<a href="h">
        #         <img src="data:image/png;base64,{}" width="25">
        #         </a>""".format(
        #             base64.b64encode(open(cv, "rb").read()).decode()
        #         ),
        #         unsafe_allow_html=True,
        #     )
        #     st.markdown("<br>",unsafe_allow_html=True)

       

st.subheader("Experience & Qulifications", divider='gray')
st.write(
    """
- :white_check_mark: Strong hands on experience and knowledge in Python, SQL and Excel
- :white_check_mark: Good understanding of statistical principles and their respective applications
- :white_check_mark: Meticulous and detail-oriented, ensuring accuracy and thoroughness in all tasks 
- :white_check_mark: Excellent team-player and displaying strong sense of initiative on tasks
"""
)
st.write('\n')
st.subheader("Hard Skills", divider='gray')
st.write(
    """
- 👩‍💻 Programming: Python, SQL, and R
- :open_book: Data Science, Data Analysis, Machine Learning, Deep Learning
- :bar_chart: Data Visulization
- :books: Data Modeling, Exploratory Data Analysis, Data Mining
- 🗄️Cloud: AWS, Google Cloud, Azure
"""
)
st.write('\n')
st.subheader("Work History", divider='gray')
st.write(
    """
- :helicopter: US Army AH-64E Apache Helicopter Pilot: 2020 - Present
- :heavy_dollar_sign: Operations Research Analyst (Cost Analyst): 2019 - 2020
- :ship: US Navy Master-at-Arms (Military Police): 2013 - 2020 

"""
)