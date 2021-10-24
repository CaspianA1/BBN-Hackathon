# EXPLORANTINE
<a href="https://devpost.com/software/explorantine-nhezvm">Devpost</a><br>
<a href="https://www.youtube.com/watch?v=ALz4xrCCu2M&t=1s">Video (YouTube)</a>

# Inspiration
All of us go to school in Concord, MA, a town known for its local history. Many of these local businesses have taken a hit during the pandemic. In this time of physical isolation and political polarization, mental health issues are on the rise as well. We sought to create a solution to both of these problems.

# What it does
Explorantine helps a user decide what locally-run business they can safely visit based on their interests. Based on factors like activity, location, price range, and how the user is feeling, our site will recommend a list of activities gathered by the Google Places API. Given these qualities, the input data is processed with a filtering algorithm that matches the activity parameters with specific locations. If the user prefers an activity outside for COVID safety reasons, the user can tweak that as well. If you’re on a budget, no problem! We have you covered.

The mood feature is a result of the pandemic because many people do not know what to do to get out of their house given that their normal activities are no longer feasible. People who only have an abstract concept of what they want to do can type their mood into this feature, which correlates with several mood keywords that we have defined using the NLTK library, a vector library that correlates words based on meaning.

# How we built it
Our tech stack included Python, SQLAlchemy, Flask, spaCy, NLTK (Natural Language Toolkit), Javascript, HTML, CSS, and Bootstrap.

We used Flask to bridge the front-end with various Google Cloud Platform APIs like Places and Geolocation. The backend calculated factors like a user’s current location, which restaurants are closest to them, and which restaurants passed filters depending on price range, closeness, and whether it was indoors or not.

Before, we have not been as comfortable with using the Google Cloud APIs, but it turns out that it was very simple. We just needed a few things: An API key, some formatted parameters, and the Requests module. Problem solved!

We also built our own APIs within our app to allow for the flow of information and easy conversion from moods to activities to location types to specific places for the user.

# Challenges we faced
One obstacle we faced was in hosting our website on Glitch and Github. Because of the dependencies of our website, the project was either taking up too much memory or too much disk space. We knew that we couldn't do our website justice if we downsized our website to fit the Glitch and Github, so we reached out to organizers and were able to reach a compromise that still allowed our website to shine in the way it deserves.

We also had some trouble with using API keys in a safe way. When we made our repository public, Google managed to discover our private API keys there and notified us that it would be unsafe to leave them there. From that, we removed them from the repository. This was a bit frustrating as we knew that people wouldn't be able to use our website straight ahead.

Lastly, we tried to style and format the website without using an API or framework to do it for us, researching web design font pairs and color palettes to do so. However, we decided that the product with the styles.css edits did not look as good as the one with plain bootstrap, so we decided to keep it for version 2, as a future goal.

# Future Goals
In the future, we hope to optimize this algorithm. Currently, it takes a while because we make so many calls to the Google API, but there is an opportunity to reduce the number of calls we make by learning the full capabilities of the Google parameters and keywords.

Furthermore, we also hope to add an image for each result listing. We believe this is important because local stores and businesses often have a style that is distinct and unique to the people of this community, and we hope that Explorantine can be a place to take comfort in a shared culture despite challenges.

We also hope to add a feature that allows individuals to connect with their friends to find a common location. Each user can add their specific preferences, and we hope our algorithm can account for all of the people in this group’s preferences to find the most enjoyable activity for all of them.

Note: the private API keys have been removed from the Github repository for safety reasons. If you would like to try our project, email caspian.ahlberg@concordacademy.org for access.

# Built With
Our tech stack included Python, SQLAlchemy, Flask, spaCy, NLTK (Natural Language Toolkit), Javascript, HTML, CSS, and Bootstrap.

and love <3
