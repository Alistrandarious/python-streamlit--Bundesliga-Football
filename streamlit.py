from cgi import test
import pandas as pd
from pyparsing import col
import streamlit as st
import altair as alt
import plotly.express as px

top_scorers = pd.read_pickle("./data/topScorersCleaned.pkl")

# Streamlit
st.title("Analyzing Bundesliga 1 for the 2021 season: Top Scorers")
st.markdown(("Football is a sport played both domestically and internationally,"
             " drawing crowds from around the world to spectate a thriling game of two teams going head to head to score the most goals and win the game,"
             " or towards a greater goal of tournement victory. This analysis focuses on the top scores for Germany's Bundesliga tournement for 2021."))

st.header("Dataset Introduction")
st.markdown("This dataset was found at API-Football. This was a free service that gives access to API data for football."
            " Data cleaning was done - standardizing the format in the places of intergets and adding in a new column for the percentage of goals scored *(shots on / shots total)*")
st.dataframe(top_scorers)

# Top Scorers

# Shots on target
st.header("Shots on Target")
st.markdown("In this section I will be running a few analyses to pull out some views on the data in terms of top performers - or who had the most impact when it came to goals and scoring them.")
st.subheader("Who had the most shots on target?")
fig = px.bar(top_scorers, x="player.name",
             y="statistics.0.shots.on", color="statistics.0.games.position", title="Top Scorers in Bundesliga 2021 (coloured by position)")
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("It is interesting that the data look similar to a Pareto Distrubition. We can see that Bayern Munich's R.Lewandowski had 75 goals on target - almost the total of the 2nd and 3rd place scorers.")

# Best Precision
st.subheader("Who had the best precision of shots taken?")
fig = px.bar(top_scorers, x="player.name",
             y="statistics.0.shots.percentage", color="statistics.0.games.position", title="Top Scorers in Bundesliga 2021 (coloured by position)")
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("In 1st place we have C. Nkunku - whom featured 5th highest in total shots. Incredibly, he has a 66.67% of his shots being on target as a mid fielder."
            " It appears that the Bundesliga tournement's most precise footballers were midfielders - which is suprising. This, R. Lewandowski scores's shots are 62.5% on target. I believe "
            "it is becomming apparent that of the midfielders present in the dataset, they are truly the exceptional players - able to cover a variety of strategic positions effectively.")

fig = px.violin(top_scorers, y="statistics.0.shots.percentage",
                x="statistics.0.games.position", color="statistics.0.games.position")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Visually, we can observe the incredible nature of the midfielders. 15% above the lowest attacker, and almost 5% above the highest attacker. The mid-range appears to be equal across both classes.")

# Shots on - due to the amount of games one was in?
st.subheader(
    "Who has the mosts shots on target, as an average of games played?")

fig = px.bar(top_scorers, x="player.name",
             y="statistics.0.shots.avpergame", color="statistics.0.games.position", title="Top Scorers in Bundesliga 2021 (coloured by position)")
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("It is no wonder that R. Lewandowski is top of the amount of attempts made. We can see he makes almost 4 shots on the goal on average per game."
            " What's more, is that we can see the decrease in the prescence of midfielders at the top end of the data. This may well be due to the lack of opportunities"
            " they have to actually shoot on target.")


fig = px.scatter(top_scorers, x="statistics.0.games.appearences",
                 y="statistics.0.shots.percentage", trendline="ols")
st.plotly_chart(fig, use_container_width=True)
st.markdown("Ultimately to win a match, one must score the goals. Therefore in the top 20 highest goal scorers we can see a trend that the more games you are featured in, "
            "the more that you will make a precise shot on the goal. Perhaps this is experience manifested in data?")


st.header(
    "Goals Analysis")
st.subheader("Who scored the most goals?")
st.markdown("Above we have explored the shots on target - a fair metric to determine precision devoid of other variables. But do we think the data will change a lot - will R. Lewandowski reign supreme?")

fig = px.bar(top_scorers, x="player.name",
             y="statistics.0.goals.total", color="statistics.0.games.position", color_discrete_sequence=px.colors.qualitative.Antique)
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig, use_container_width=True)
st.markdown("As expected, our top-performing shooter (total) makes the most goals. Let's analyze their striking skills further.")

st.subheader(
    "Who has the best rate of scoring as a percentage of total attempts?")
fig = px.bar(top_scorers, x="player.name",
             y="statistics.0.goals.percentage", color="statistics.0.games.position", color_discrete_sequence=px.colors.qualitative.Antique)
fig.update_layout(barmode='stack', xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig, use_container_width=True)

st.markdown("Incredibly, the midfielders rise again despite having some of the lowest total shots. C. Nkunku with an incredible 35.29% features at the top of the distribution as a midfielder."
            "Once again the midfielders are proving their worth.")


fig = px.scatter(top_scorers, x="statistics.0.shots.total", y="statistics.0.goals.total",
                 size="statistics.0.games.appearences", color="statistics.0.games.position",  color_discrete_sequence=px.colors.qualitative.Antique,
                 hover_name="player.name", trendline="ols")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Naturally, the more shots you make the more goals you get. It's good to see there isn't a diminishing return here. Though the R value is 0.88 - suggesting other factors outside of just shoot"
            "ing must be taken into account...")

st.header("Aggression.")
st.markdown("This is an experimental section. Having analyzed and covered top performers to the best of my football knowledge and ability, I wanted to do something unique. So let's look into aggression.")
st.markdown("I am defining aggression as, 'the desperation of winning, and therefore rulebreaking'. Within football, are you rewarded for breaking the rules?")
st.markdown("I have created a new column within the dataset. I have added up the amount of cards a player has received. Indicating severity to at least mimic realworld decision-making I have allocated "
            "additional scoring to cards as they get more severe. Yellows are worth 1, 2 Yellows (YellowRed) is worth 1.5, and a flat out Red is worth 2.")

fig = px.violin(top_scorers, y="statistics.0.cards.rulebreaker",
                x="statistics.0.games.position", color="statistics.0.games.position")
st.plotly_chart(fig, use_container_width=True)
st.markdown("I feel a natural expectation from the attacker's role is to be more aggressive, or get more cards. Very much the onus is on you to score - and your reputation is on the line on a global stage."
            "Bundesliga features a unique tournement based in Germany with one of the world's greatest teams - it makes sense to push it to the limit.")

fig = px.scatter(top_scorers, x="statistics.0.cards.rulebreaker", y="statistics.0.goals.total",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hover_name="player.name", trendline="ols")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Even based on the top performers - where the best results exist, it appears that aggression is not a rewarded strategy... But what happens if we remove M. Diaby?")


top_scorers_no_outlier = top_scorers[top_scorers["player.name"] != "M. Diaby"]

fig = px.scatter(top_scorers_no_outlier, x="statistics.0.cards.rulebreaker", y="statistics.0.goals.total",
                 color_discrete_sequence=px.colors.qualitative.Set1,
                 hover_name="player.name", trendline="ols")
st.plotly_chart(fig, use_container_width=True)

st.markdown("Still, aggression is not rewarded. In fact, it has a slight negative impact on the performance overall.")