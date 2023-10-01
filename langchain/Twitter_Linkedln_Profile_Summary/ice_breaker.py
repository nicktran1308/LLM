# ------------------------------- Import Libraries -------------------------------
from typing import Tuple
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from agents.twitter_lookup_agent import lookup as twitter_lookup_agent
from chains.custom_chains import (
    get_summary_chain,
    get_interests_chain,
    get_ice_breaker_chain,
)
from third_parties.linkedin import scrape_linkedin_profile
from third_parties.twitter import scrape_user_tweets
from output_parsers import (
    summary_parser,
    topics_of_interest_parser,
    ice_breaker_parser,
    Summary,
    IceBreaker,
    TopicOfInterest,
)

# ------------------------------- Ice Break Interaction -------------------------------
def ice_break_with(name: str) -> Tuple[Summary, IceBreaker, TopicOfInterest, str]:
    """
    Generates and retrieves summary, interests, icebreakers, and profile picture URL
    for a given name by integrating with LinkedIn and Twitter.
    """
    # Fetch LinkedIn username and scrape their profile data
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    
    # Fetch Twitter username and scrape their tweets
    twitter_username = twitter_lookup_agent(name=name)
    tweets = scrape_user_tweets(username=twitter_username)
    
    # Generate a summary for the given user
    summary_chain = get_summary_chain()
    summary_and_facts = summary_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    summary_and_facts = summary_parser.parse(summary_and_facts)
    
    # Identify interests for the given user
    interests_chain = get_interests_chain()
    interests = interests_chain.run(information=linkedin_data, twitter_posts=tweets)
    interests = topics_of_interest_parser.parse(interests)
    
    # Generate icebreakers for the given user
    ice_breaker_chain = get_ice_breaker_chain()
    ice_breakers = ice_breaker_chain.run(
        information=linkedin_data, twitter_posts=tweets
    )
    ice_breakers = ice_breaker_parser.parse(ice_breakers)

    # Return the collected and generated data
    return (
        summary_and_facts,
        interests,
        ice_breakers,
        linkedin_data.get("profile_pic_url"),
    )

# ------------------------------- Main Execution -------------------------------
if __name__ == "__main__":
    pass
