import streamlit as st
from tempfile import NamedTemporaryFile
from config import text_endpoint, image_endpoint, images_path, top_k, image_size
import requests



def encode_to_base64(byte_string):
    import base64

    output = str(base64.b64encode(byte_string), "utf-8")

    return output


def create_query(query: str, top_k: int, endpoint: str) -> list:
    data = '{"top_k":' + str(top_k) + ', "mode": "search", "data":' + query + "}"
    response = requests.post(endpoint, headers=headers, data=data)

    content = response.json()["search"]["docs"]
    results = []
    for doc in content:
        matches = doc["matches"]
        for match in matches:
            results.append(match["uri"])

    return results


def get_images(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": ["data:image/png;base64,'
        + query
        + '"]}'
    )

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    matches = content["data"]["docs"][0]["matches"]

    return matches


def get_data(query: str, endpoint: str, top_k: int) -> dict:
    headers = {
        "Content-Type": "application/json",
    }

    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


# layout
max_width = 1200
padding = 2


st.markdown(
    f"""
<style>
    .reportview-container .main .block-container{{
        max-width: {max_width}px;
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.title("Jina Meme Search")
modality = st.sidebar.radio(
    label="I want to search using...", options=("Image", "Text")
)

settings = st.sidebar.beta_expander(label="Settings", expanded=False)
with settings:
    if modality == "Text":
        endpoint = st.text_input(label="Endpoint", value=text_endpoint)
    else:
        endpoint = st.text_input(label="Endpoint", value=image_endpoint)

    top_k = st.number_input(label="Top K", value=top_k, step=1)

st.sidebar.markdown(
    """
### About

This is an example meme search engine using the [Jina neural search framework](https://github.com/jina-ai/jina/).

**Note: click the search button instead of hitting Enter. We're working on fixing this!**

- Backend: [Jina](https://github.com/jina-ai/jina/)
- Frontend: [Streamlit](https://www.streamlit.io/)

[Visit the repo](https://github.com/alexcg1/jina-meme-search-example)

---

<a href="https://github.com/jina-ai/jina/"><img src="https://github.com/alexcg1/jina-app-store-example/blob/a8f64332c6a5b3ae42df07d4bd615ff1b7ece4d9/frontend/powered_by_jina.png?raw=true" width=256></a>
""",
    unsafe_allow_html=True,
)

if modality == "Text":
    st.title("Search memes by caption")
    query = st.text_input(label="Search for a meme based on caption")
else:
    st.title("Search memes by similar image")
    query = st.file_uploader("Upload image")
    if query is not None:
        image_data = query.read()
        query = encode_to_base64(image_data)

if st.button(label="Search"):
    if not query:
        st.markdown("Please enter a query")
    else:
        # Set up grid
        cell1, cell2, cell3 = st.beta_columns(3)
        cell4, cell5, cell6 = st.beta_columns(3)
        cell7, cell8, cell9 = st.beta_columns(3)
        all_cells = [cell1, cell2, cell3, cell4, cell5, cell6, cell7, cell8, cell9]

        if modality == "Text":
            matches = get_data(query=query, endpoint=endpoint, top_k=top_k)
        elif modality == "Image":
            matches = get_images(query=query, endpoint=endpoint, top_k=top_k)

        for cell, match in zip(all_cells, matches):
            cell.image("http:" + match["tags"]["image_url"])
