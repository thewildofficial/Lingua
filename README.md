# Core Information
name: linguaRep (liable to change)
prefix: *
# Spaced Revision bot
you commit whatever task you need to study to a bot, this bot will judge priorities (you could assign test dates as well) and will make you revise every so often based on how many tasks you have per time period and how much you usually revise per day
for example, if a math exam come closer (with chapter X) and if the priority for X is high,the odds of having to study that chapter will increase (by an incrementing % chance) once your revision is done, it will go back down and give you another chapter to revise :)



Inputs would be:
- Date of nearest exam
- priority (0,1,2)
- Date of the last revision (a revision that happened a long time ago would be prioritized over a revision that happened more recently)



# Language Learning Discord Bot
## Idea
I got this idea from a  video by nathaniel drew on language learning:
(https://www.youtube.com/watch?v=95NgtNgmnWA)
i was inspired by a comment by a viewer:
> I achieved reading fluency in German in around a month and a half by making an anki deck of the 5000 most common words. I coded a webscrapper that takes the text from a website (mostly used wikipedia and newspapers), parses it, gets an example of use, and provides a route translation (just with Google's API). Went through a hundred new words a day (just for recognition, can easily just go from german to english), and was able to read novels within a month.

>  I just set up a web-scrapper and mined ~5 mil words of modern German. For mass amounts of written text, I would suggest checking news websites, wikipedia (you'll need to filter for the specific topics) or finding written literature (though, these can be quite old fashioned).If it's something that doesn't have as much as an online presence, you might have to turn to twitter, Reddit, or local forums (many cities have something that has a significant amount of text). People use modern vocab and if you filter well enough (age of account, native speaker, average length of posts), it's competently written. This does often mean you have to dig for APIs, or brute force the stuff, though. You can also use things like opensubtitles (film and movie scripts) or youtube for getting an idea of spoken language vocab use. Unfortunately, for listening comprehension, you kind of just have to jump into it. I started listening to some german podcasts after a few weeks (once I knew around 1-2k works), and made sure to pause after every sentence to ensure that I understood it (takes direct work).

Language learning can be really quick if you target what you want to do.

this gave me the idea of making a discord bot with the following capacities:
- learns new information from places like reddit,wikipedia and news papers	here are more information links
	- https://mediastack.com/sources/france-news-api
	- https://public-apis.io/open-government-france-api
	- user inputted blog posts
	- https://www.reddit.com/r/French/
	- French Wikipedia
- utililize a spaced repitition model
- streak system
- find an example of the phrase and translate it in english

# Requirements
- Web Scrapping
- NLP (NLTK)
- Neural Network
- Database