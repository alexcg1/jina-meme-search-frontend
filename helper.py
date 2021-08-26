import requests
import magic
import os

repo_banner_file = os.path.abspath("./eah.svg")

class UI:

    repo_banner = """ ![](https://raw.githubusercontent.com/alexcg1/jina-meme-search-frontend/main/repo_banner.svg) """
    repo_banner = """<a href="https://github.com/jina-ai/jina/"><img src="https://raw.githubusercontent.com/alexcg1/jina-meme-search-frontend/main/repo_banner.svg"></a>"""
    # repo_banner = """
# ### Like what you see?
    # """

    text_block = """

    ### About

    This is an example meme search engine using the [Jina neural search framework](https://github.com/jina-ai/jina/).

    **Note: click the search button instead of hitting Enter. We're working on fixing this!**

    - Backend: [Jina](https://github.com/jina-ai/jina/)
    - Frontend: [Streamlit](https://www.streamlit.io/)
    - Dataset: [ImgFlip memes](https://www.kaggle.com/abhishtagatya/imgflipscraped-memes-caption-dataset)

    """

    image_repo_block = """
    ### Repos

    - [Image search backend](https://github.com/alexcg1/simple-jina-examples/tree/main/image_search)
    - [Frontend](https://github.com/alexcg1/jina-meme-search-frontend)

    ---

    <a href="https://github.com/jina-ai/jina/"><img src="https://github.com/alexcg1/jina-app-store-example/blob/a8f64332c6a5b3ae42df07d4bd615ff1b7ece4d9/frontend/powered_by_jina.png?raw=true" width=256></a>"""

    css = f"""
<style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 2rem;
        padding-left: 2rem;
        padding-bottom: 2rem;
    }}
    .reportview-container .main {{
        color: "#111";
        background-color: "#eee";
    }}
</style>
"""


headers = {"Content-Type": "application/json"}


def search_by_text(query: str, endpoint: str, top_k: int) -> dict:
    """search_by_text.

    :param query:
    :type query: str
    :param endpoint:
    :type endpoint: str
    :param top_k:
    :type top_k: int
    :rtype: dict
    """
    data = '{"top_k":' + str(top_k) + ',"mode":"search","data":["' + query + '"]}'

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()

    matches = content["data"]["docs"][0]["matches"]

    return matches


def search_by_file(endpoint, top_k, filename="query.png"):
    """search_by_file.

    :param endpoint:
    :param top_k:
    :param filename:
    """
    filetype = magic.from_file(filename, mime=True)
    filename = os.path.abspath(filename)


    data = (
        '{"parameters": {"top_k": '
        + str(top_k)
        + '}, "mode": "search",  "data": [{"uri": "'
        + filename
        + '", "mime_type": "'
        + filetype
        + '"}]}'
    )

    response = requests.post(endpoint, headers=headers, data=data)
    content = response.json()
    matches = content["data"]["docs"][0]["matches"]

    return matches


def create_temp_file(query, output_file="/tmp/query.png"):
    """create_temp_file.

    :param query:
    :param output_file:
    """
    data = query.read()

    with open(output_file, "wb") as file:
        file.write(data)

    return output_file
