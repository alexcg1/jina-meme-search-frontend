import streamlit as st
from config import text_endpoint, image_endpoint, images_path, top_k, image_size
from helper import UI, search_by_text, search_by_file, create_temp_file


st.markdown(
    UI.css,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Jina Meme Search")
# modality = st.sidebar.radio(
# label="I want to search using...", options=("Text", "Image")
# )

settings = st.sidebar.beta_expander(label="Settings", expanded=False)
with settings:
    # if modality == "Text":
    endpoint = st.text_input(label="Endpoint", value=text_endpoint)
    # else:
    # endpoint = st.text_input(label="Endpoint", value=image_endpoint)

    top_k = st.number_input(label="Top K", value=top_k, step=1)

st.sidebar.markdown(
    UI.text_block,
    unsafe_allow_html=True,
)

# if modality == "Text":
st.title("Search memes by caption")
query = st.text_input(label="Search for a meme based on caption")
# else:
# st.title("Search memes by similar image")
# st.markdown("### Coming soon. Still a work in progress!")
# query = st.file_uploader("Upload image")
# if query is not None:
# image_data = query.read()
# query = encode_to_base64(image_data)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:
        # Set up grid
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)
        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        # if modality == "Text":
        matches = search_by_text(query=query, endpoint=endpoint, top_k=10)
        # elif modality == "Image":
        # matches = get_images(query=query, endpoint=endpoint, top_k=top_k)

        for cell, match in zip(all_cells, matches):
            # st.write(match)
            cell.image("http:" + match["tags"]["image_url"])
