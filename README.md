## Abstract
**This project placed 1st for the [Fall '23 MScADS Hackathon](/UChicago-Rotational%20Hackathon%20Fall%202023.pdf), with support from the [UChicago Data Science Institute](https://datascience.uchicago.edu/) and [Rotational Labs](https://rotational.io/).**

We were tasked with using [Ensign](https://rotational.io/ensign/), a **cloud-based asynchronous data streaming tool** developed by Rotational Labs to allow for **real-time data pipelines through a publish/subscribe model**, with a goal to train **event-driven machine learning models** (such as through [River](https://riverml.xyz/0.19.0/introduction/basic-concepts/)) for practical use cases.

Our main goal is to develop a real-time flight delay prediction system to address the challenges faced by the aviation industry in mitigating the impact of flight delays, caused by combination of missed/slow connections, in-air delays, and scheduling disruptions.

For more information, our presentation can be found [here](/Hackathon%20Presentation.pdf).

Our Team - **The Three Musketeers**: 
- [Jason Chandra](https://github.com/jasoncchandra)
- [Kevin Sianto](https://github.com/ksianto)
- [Toby Chiu](https://github.com/tobytcc)


## Approach

### Objective
Our primary objective is to create a real-time flight delay prediction system tailored for consultants, helping them identify flights with expected delays, providing confidence intervals for predictions, and offering specific departure and arrival airport pair predictions to make informed travel decisions.

Given departure and arrival times for most frequent daily flights are the same, we can use historical airport/aircraft data, and flight path to predict the likelihood of delay, and update it through real-time tracking from our data pipeline.  

![Example Tracked Flight](/img/daily-flight-photo.png)

We planned on retrieving live data from multiple sources, engineering a live data pipeline that could output ~5 relevant flights per second, with 30 pieces of info per flight. This data is fed into our event-driven model, with the goal of providing a continuously-updating predicted arrival time with a confidence interval backed by historical data and live updates.

![Project Flowchart](/img/Flowchart_vFinal.png)

### Data Pipeline
1. We utilised Ensign's flight data from [OpenSky Network's live API](https://openskynetwork.github.io/opensky-api/) to grab basic flight data. Each sample in the dataset represents a specific flight with various attributes related to that flight at one point in time (updated in 15-second intervals), such as a flight's callsigns and ICAO24 registration, in-air info (velocity, altitude, horizontal/vertical headings, etc.), and flight type (aircraft model, passenger vs. cargo, etc.). We can pull 1000+ flights across the continental US per second with this model, although most flights are irrelevant and untracked by our pipeline. 

![Example Input Streamed Data](/img/input_data.png)

2. We published this info into an intermediary topic, and subscribed with a pipeline file that filtered and processed this data. If a flight is "tracked", our pipeline will take more detailed info from [FlightRadar24's API](https://pypi.org/project/FlightRadarAPI/), grabbing airport-level data and detailed historical data to supplement each flight's profile. This info is then published into a final topic, and subscribed to with our model to fetch real-time events for further training.

![Example Output Streamed Data](/img/output_data.png)

3. Our model - a basic regression model - is then updated through incremental training. We conducted feature engineering through data selection (time-based features, historical data, and airport data were prioritised), scaling, and pre-processing. Model performance is validated through data splitting (80/10/10 split) and cross-validation, then using evaluation metrics such as RMSE, MAE and R-squared.

If given more time during our hackathon, we can try more complex versions of the model (e.g. polynomial regression, decision trees, random forests, etc.) and compare through k-cross validation performance.

![Demo Output](/img/demo_output.png)

## Reflection
- Our team had a great experience! We spent lots of time bouncing ideas off one another, and spent a lot of time encouraging and coding together for a common goal. As new data scientists, it allowed us to apply our rigourous academic takeaways to a practical goal, and tackle the challenges that arose from fitting theory into practice.

- We learnt the importance of data engineering in practical data science work - it took up 75% of our time! Rotational Labs encouraged us to explore data engineering (which tends to be underappreciated), and we are much stronger at data engineering as a result.

- Getting familiar with Ensign was a challenge for our team, and we wasted lots of time on pursuing solutions that fit with Ensign. The best solutions are only as good as the data quality/tools allow for, and these solutions tend to play to the strengths and integratability of our various tools.


## Limitations
- Given the short time duration of the hackathon, we were heavily hampered by server-side unreliability issues from both APIs. OpenSky's API was heavily rate-limited and frequently timed out our pipeline (as seen below), and FlightRadar24's API could handle only ~1/50 of Ensign's input, creating a bottleneck that forced us to implement arbitrary rate limiters in our pipeline - leading to decreased data quality (unpredictable/missing/incorrect rows) and poor data consistency.

![OpenSky API Timeout](/img/timeout.png)

- The APIs could not integrate perfectly - OpenSky's API only outputted **airline** registration info (24-bit ICAO/Callsign), while FlightRadar24's API required **aircraft** registration info (tail number). **Our creative solution was to create a tiny (~0.5 sq. mile) bounding box around each tracked aircraft, and identify the correct flight in each bounding box to retrieve flight details.** This method definitely slowed our pipeline down, and did not always result in finding our flight due to data collection inaccuracies. If given more time, we would be able to come up with a more elegant solution.

- All team members were new to data science (particularly ML), and had little coding experience. We struggled massively in building event-driven models, and had to learn real-time engineering/machine learning from scratch - **this was a great experience!** If given the chance to rebuild again with our current knowledge, we would have gone a lot further in the hackathon!

## Further Expansions

- Parallel to our primary focus on Ensign and real-time flight delay prediction, our project's expansion ventured into leveraging Google Cloud Platform (GCP) and big data technologies, notably employing PySpark for advanced analytics. Through this expansion, we delved into two pivotal areas:

1. Association Mining for Targeted Marketing: Identify traveler behavior patterns by uncovering correlations between airports and preferred airlines, aiding airline marketing teams in tailoring strategies for route planning and passenger engagement.
2. Graph-Based Analysis for Delay Reduction: Utilize delay-integrated network representation to analyze delay propagation across airports and airlines, helping airline operations teams identify influential nodes and routes to minimize delays and enhance operational efficiency.

- **Association rule mining**, like FP-Growth used here, emphasizes discovering frequent patterns within transactions, beneficial for identifying strategic airline route planning rather than directly pinpointing airlines with the lowest delays for specific routes.
Specifically, we filter and analyze frequent itemsets and association rules based on high lift and support, centered on departures from ORD or MDW, aiding airlines in optimizing flight schedules and operations. Specifically, we filter and analyze frequent itemsets and association rules based on high lift and support, centered on departures from ORD or MDW, aiding airlines in optimizing flight schedules and operations.








## Further Developments
- Improve our model performance (as stated above)

- Further steps could involve real-time implementation and integration with travel platforms, enhancing the user experience for consultants and travelers.

- Future extensions: expanding the system to cover a broader range of flights and regions. Or, we could integrate additional features, such as weather data, to enhance prediction accuracy and further empower air travelers.
