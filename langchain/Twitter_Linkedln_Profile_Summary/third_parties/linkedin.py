# ------------------------------- Import Libraries -------------------------------
import os
import requests

# ------------------------------- Scrape LinkedIn Profile -------------------------------
def scrape_linkedin_profile(linkedin_profile_url: str):
    """
    Scrape information from LinkedIn profiles.
    Manually fetches the information using a proxy service.
    """
    # API endpoint and headers for the scraping service
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    headers = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}

    # Fetch the LinkedIn profile data
    response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers=headers)
    data = response.json()

    # Clean and filter the returned data
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None) and k not in ["people_also_viewed", "certifications"]
    }
    if data.get("groups"):
        for group_dict in data["groups"]:
            group_dict.pop("profile_pic_url")

    return data

