import streamlit as st
import random
import os
from config import image_endpoint, text_endpoint, top_k
from helper import search_by_file, search_by_text, UI, create_temp_file

endpoint = image_endpoint
matches = []

st.set_page_config(page_title="Jina meme search")

# Top section
st.markdown(UI.repo_banner, unsafe_allow_html=True)

st.markdown(
    '<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" crossorigin="anonymous">',
    unsafe_allow_html=True,
)
query_params = st.experimental_get_query_params()
tabs = ["Search by image", "Search by text"]
if "tab" in query_params:
    active_tab = query_params["tab"][0]
else:
    active_tab = "Search by image"

if active_tab not in tabs:
    st.experimental_set_query_params(tab="Home")
    active_tab = "Search by image"

li_items = "".join(
    f"""
    <li class="nav-item">
        <a class="nav-link{' active' if t==active_tab else ''}" href="/?tab={t}">{t}</a>
    </li>
    """
    for t in tabs
)
tabs_html = f"""
    <ul class="nav nav-tabs">
    {li_items}
    </ul>
"""

st.markdown(tabs_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

if active_tab == "Search by image":
    media_type = "Image"
    st.header("Search from your own image...")
    upload_cell, preview_cell =  st.columns([12, 1])
    query = upload_cell.file_uploader("Upload file")
    if query:
        uploaded_image = create_temp_file(query)
        preview_cell.image(uploaded_image)
        if st.button(label="Search"):
            if not query:
                st.markdown("Please enter a query")
            else:
                matches = search_by_file(image_endpoint, top_k, "/tmp/query.png")

    # Sample image list
    else:
        st.header("...or search from an existing meme")
        sample_files = []
        for filename in os.listdir("./samples"):
            sample_files.append(filename)
        # random.shuffle(sample_files)
        sample_cells = st.columns(len(sample_files))

        for cell, filename in zip(sample_cells, sample_files):
            meme_name = filename.split(".")[0]
            cell.image(f"samples/{filename}", width=128)
            if cell.button(f"{meme_name}", key=meme_name):
                matches = search_by_file(image_endpoint, top_k, f"samples/{filename}")

elif active_tab == "Search by subject/caption":
    media_type = "Text"
    st.subheader("Search with a meme subject and/or caption...")
    query = st.text_input("Meme subject or caption", key="text_search_box")
    search_fn = search_by_text
    if st.button("Search", key="text_search"):
        matches = search_by_text(query, text_endpoint, top_k)
    st.subheader("...or search from a sample")
    sample_texts = ["squidward school", "so you're telling me willy wonka", "seagull kitkat"]
    for text in sample_texts:
        if st.button(text):
            matches = search_by_text(text, text_endpoint, top_k)
elif active_tab == "Contact":
    st.write("If you'd like to contact me, then please don't.")
else:
    st.error("Something has gone terribly wrong.")







st.markdown(
    body=UI.css,
    unsafe_allow_html=True,
)

# media_type = st.sidebar.radio(
    # label="Search using", options=["Text", "Image"], index=1
# )

# Sidebar
st.sidebar.markdown(UI.text_block, unsafe_allow_html=True)
st.sidebar.markdown(UI.image_repo_block, unsafe_allow_html=True)

# settings = st.sidebar.expander(label="Settings")
# with settings:
    # image_endpoint = st.text_input(label="Image endpoint", value=image_endpoint, key="image_endpoint")
    # text_endpoint = st.text_input(label="Text endpoint", value=text_endpoint, key="text_endpoint")
    # top_k = st.number_input(label="Top K", value=top_k, step=1)

cell1, cell2, cell3 = st.columns(3)
cell4, cell5, cell6 = st.columns(3)
cell7, cell8, cell9 = st.columns(3)
all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

for cell, match in zip(all_cells, matches):
    if media_type == "Text":
        cell.image("http:" + match["tags"]["image_url"])
    else:
        cell.image(match["tags"]["uri_absolute"], use_column_width="auto")
