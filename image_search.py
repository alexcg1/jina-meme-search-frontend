import streamlit as st
import random
import os
from config import image_endpoint, top_k
from helper import search_by_file, search_by_text, UI, create_temp_file

endpoint = image_endpoint
matches = []

st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.markdown(UI.text_block, unsafe_allow_html=True)
st.sidebar.markdown(UI.image_repo_block, unsafe_allow_html=True)

# media_type = st.sidebar.radio(
    # label="Media type", options=["Text", "Image", "Audio", "Video"], index=1
# )

settings = st.sidebar.expander(label="Settings", expanded=True)
with settings:
    endpoint = st.text_input(label="Endpoint", value=endpoint)
    top_k = st.number_input(label="Top K", value=top_k, step=1)

# Main area
# st.title(f"Search {media_type.lower()} by {media_type.lower()}")
st.title("Search memes by image")

# if media_type == "Text":
    # query = st.text_input("Search phrase")
    # search_fn = search_by_text
# else:
st.heaader("Search from your own image...")
upload_cell, preview_cell =  st.columns([12, 1])
query = upload_cell.file_uploader("Upload file")
search_fn = search_by_file
if query:
    uploaded_image = create_temp_file(query)
    preview_cell.image(uploaded_image)
    if st.button(label="Search"):
        if not query:
            st.markdown("Please enter a query")
        else:
            matches = search_by_file(endpoint, top_k, "/tmp/query.png")

# Sample image list
else:
    st.header("...or search from an existing meme")
    sample_files = []
    for filename in os.listdir("./samples"):
        sample_files.append(filename)
    random.shuffle(sample_files)
    sample_cells = st.columns(len(sample_files))

    for cell, filename in zip(sample_cells, sample_files):
        meme_name = filename.split(".")[0]
        cell.image(f"samples/{filename}", width=128)
        if cell.button(f"{meme_name}"):
            matches = search_by_file(endpoint, top_k, f"samples/{filename}")

    sample_meme = sample_files[0]
    meme_name = sample_meme.split(".")[0]
    st.image(f"samples/{sample_meme}", width=256)
    if st.button(f"{meme_name}"):
        matches = search_by_file(endpoint, top_k, f"samples/{sample_meme}")
        # if media_type == "Image" or media_type == "Video":
# Set up grid
cell1, cell2, cell3 = st.columns(3)
cell4, cell5, cell6 = st.columns(3)
cell7, cell8, cell9 = st.columns(3)
all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

for cell, match in zip(all_cells, matches):
    cell.image(match["tags"]["uri_absolute"], use_column_width="auto")
