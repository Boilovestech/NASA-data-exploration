import streamlit
import streamlit_shadcn_ui as ui
from streamlit_card import card
import requests as r

streamlit.set_page_config(layout="wide")

# Custom theme
streamlit.markdown("""
    <style>
        :root {
            --primary-color: #03e0ff;
            --background-color: #000000;
            --secondary-background-color: #0c3c9a;
            --text-color: #ffff;
        }
    </style>
""", unsafe_allow_html=True)
streamlit.title("NASA Data exploration")
query = ""
APOD_endpoint = "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY&count=3"
Mars_p_enpoint = "https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol=1000&api_key=DEMO_KEY"
col1, col2, col3 = streamlit.columns([1, 2, 1])
with col2:
    selected_tab = ui.tabs(options=['Astronomical picture of the day', 'Mars rover pictures', 'Info search'], default_value=None, key="kanaries")

if selected_tab is None:
    streamlit.write("Select a tab to explore!")
elif selected_tab == 'Astronomical picture of the day':
    streamlit.header("Astronomical picture of the day")
    if ui.button("Refresh"):
        streamlit.experimental_rerun()
    APOD_RESULTS = r.get(APOD_endpoint).json()
    if isinstance(APOD_RESULTS, list) and len(APOD_RESULTS) > 0:
        for apod in APOD_RESULTS[:3]:
            if 'url' in apod and 'explanation' in apod:
                img = apod['url']
                exp = apod['explanation']
                title = apod['title']
                
                with streamlit.expander(f"APOD: {title}"):
                
                    streamlit.image(img, use_column_width=True)
                    streamlit.write(exp)
    else:
        streamlit.write("Unexpected response format from APOD API")

elif selected_tab == 'Mars rover pictures':
    streamlit.header("Mars rover pictures")
    imges_m = r.get(Mars_p_enpoint)
    
    if imges_m.status_code == 200:
        data = imges_m.json()
        photos = data.get('photos', [])[:3]  # Get a maximum of 3 photos
        
        if photos:
            for i, photo in enumerate(photos):
                img_src = photo['img_src']
                streamlit.image(img_src, caption=f"Mars Rover Image {i+1}", use_column_width=True)
        else:
            streamlit.write("No Mars rover pictures available.")
    else:
        streamlit.write("Failed to fetch Mars rover pictures. Please try again later.")    
elif selected_tab == 'Info Search':
    streamlit.header("Info Search")
    
    query = streamlit.text_input("Enter keywords to get related studies")
    if query == "":
        streamlit.write("Please enter a query.")
    else:
        
        # Construct the search URL with additional parameters
        search_url = f"https://images-api.nasa.gov/search?q={query}"
        
        data = r.get(search_url)
        data = data.json()

        if data['collection']['metadata']['total_hits'] > 0:
            results = data['collection']['items'][:3]  # Limit to 3 results
            for result in results:
                if 'data' in result:
                    data = result['data']
                    for item in data:
                        if 'nasa_id' in item:
                            nasa_id = item['nasa_id']

                            title = item.get('title', 'No title available')
                            description = item.get('description', 'No description available')
                            
                            streamlit.subheader(title)
                            streamlit.write(description)
                            
                            if 'links' in result:
                                for link in result['links']:
                                    if link['rel'] == 'preview':
                                        streamlit.image(link['href'], caption=title, use_column_width=True)
                                        break
                            
                            streamlit.markdown("---")
        else:
            streamlit.write("No results found for the given query.")
