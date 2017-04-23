
from create_db import db,News, Topic, InputNews
from sentiment_analyzer import SentimentAnalyzer
from news_scraper import NewsScraper
from datetime import date
from dateutil.relativedelta import relativedelta
from natural_language_processor import NaturalLanguageProcessor as NLP
from database_manager import DatabaseManager as DB


number_of_top_words = 10000
minimum_match_word = 2

class ReliabilityEvaluator:

    sentiment_analyzer = SentimentAnalyzer()

    def compute_for_reliability_score(self, input_string):

        input_news = InputNews(input_string, NLP.count_occurrence(input_string))

        if not self.identify_topic_for_news(input_news) == None:
            reliability = self.sentiment_analyzer.identify_reliability(input_news)
            return reliability
        else:
            return None


    def identify_topic_for_news(self, news):
        topics = Topic.query.all()
        news_topic = self.find_news_a_topic(news, topics)

        if news_topic:
            return news.topic
        else:
            return None


    def assert_news_belong_to_topic(self, news, topic):
        match_words = 0
        
        if not news.topic is None:
            return True
        
        for news_word in sorted(news.news_words)[:number_of_top_words]:
            for topic_word in topic.words:
                if news_word.word.word == topic_word.word:
                    match_words +=1

        if match_words >= minimum_match_word:
            news.topic = topic
            DB.commit_db()
            return True
        else:
            return False



    def find_news_a_topic(self, news, topics):
        for topic in topics:
            if self.assert_news_belong_to_topic(news,topic):
                return news.topic

        return None


    def create_new_topic_for_news(self, news):
        topic_word = []
        for news_word in sorted(news.news_words)[:number_of_top_words]:
            topic_word.append(news_word.word)

        if len(topic_word) == 0:
            return None

        new_topic = Topic(topic_word)
        return new_topic


    #only called when news list data is to be updated
    def scrape_news_starting_from(self,date):
        channels = ['GMA', 'RAPPLER', 'CNN', 'MANILABULLETIN', 'PHILSTAR'];
        rssurl = {'GMA': 'http://www.gmanetwork.com/news/rss/news/nation',
            'RAPPLER': 'http://feeds.feedburner.com/rappler/',
            'CNN': 'http://rss.cnn.com/rss/edition_asia.rss',
            'MANILABULLETIN': 'http://mb.com.ph/mb-feed/', 
            'PHILSTAR' : 'http://www.philstar.com/rss/nation'}

        #scrape news from 6 months ago
        for i in range(0,5): 
            NewsScraper.scrape(channels[i], rssurl[channels[i]], date, "20170301");

    #only called when generating data set
    def generate_topics(self):
        topics = []
        count = 0

        newslist = News.query.all()

        for news in newslist:
            count += 1
            if not news.topic is None:
                continue

            if not self.find_news_a_topic(news, topics):
                new_topic = self.create_new_topic_for_news(news)
                news.topic = new_topic
                if not new_topic == None:
                    topics.append(new_topic)
                    DB.add_topic_to_db(new_topic)

        DB.commit_db()
        return topics


    def get_news_without_topic(self):
        return News.query.filter_by(topic = None).all()
    
    def get_topics_of_news_content(self):
        input_news_list = News.query.all()
        count = 0
        with_topic_count = 0
        with_positive_reliability = 0

        for input_news in input_news_list:
            count += 1
            if not self.identify_topic_for_news(input_news) == None:
                #if self.sentiment_analyzer.identify_reliability(input_news) > 0:
                #    with_positive_reliability += 1 
                with_topic_count += 1
                print("count" + str(count))

        print("With topic count " + str(with_topic_count) + " of " + str(count))
        #print("With topic count " + str(with_topic_count) + " of " + str(count))
        return

re = ReliabilityEvaluator()
#rel = re.compute_for_reliability_score("To assert sovereign rights over Philippine territories in the disputed West Philippine Sea (South China Sea), President Rodrigo Duterte said he has ordered the military to occupy islands there. I have ordered the Armed Forces to occupy all the so many islands, I think 9 or 10. Lagyan ng structures (Build structures) and the Philippine flag, said Duterte on Thursday, April 6, a move that could provoke rival claimants including Beijing. The President made the statement during a press briefing in Puerto Princesa, Palawan, the province on the frontlines of the sea row with China. He was there to visit soldiers in Camp Artemio Ricarte. Before the briefing, he had given a speech in front of them. Duterte pointed out the need to maintain jurisdiction over the West Philippine Sea. In particular, he wants to fortify disputed Pag-asa by building bunkers and other structures there. Mukhang agawan kasi ito ng isla eh and whats ours now, at least kunin na natin and make a strong point there that its ours, said Duterte. (This looks like island-grabbing so whats ours now, at least lets get them and make a strong point there that its ours.) Changing tune Dutertes insistence on military presence in Philippine territories in the South China Sea is a departure from his passive approach to it upon assuming the presidency. It comes amid his bid to strike warmer ties with China which is claiming virtually the entire sea. In September 2016, National Security Adviser Hermogenes Esperon Jr had in fact said that the President wanted to demilitarize the area to improve the chances of a peaceful settlement of the maritime dispute. Pag-asa Island, also being claimed by China, is the 2nd biggest naturally occurring island in the South China Sea and the only one with civilian presence. It is the seat of power of the Kalayaan Group of Islands (Spratlys) that is attached to the province of Palawan. More facilities Defense Secretary Delfin Lorenzana clarified that Filipino troops already occupy 9 islands in the Spratlys including Pag-asa. We have [Marine] troops in everyone of them, Lorenzana said in a statement Thursday. The President wants facilities built such as: barracks for the men, water (desalination) and sewage disposal systems, power generators (conventional and renewable), light houses, and shelters for fishermen, Lorenzana explained. On Thursday, Esperon bared government plans to repair the runway in Pag-asa Island. The President said he fully supports this as it would help fortify the island. The development there has my full support, gagastos ako sa fortification diyan (I will spend for the fortification there), he said. Trip to Pag-asa Duterte is so eager to assert the countrys rights on Pag-asa Island that, come Independence Day in June, he plans to go there himself to plant the Philippine flag. Coming Independence Day natin (This coming Independence Day), I might, I may go to Pag-asa Island to raise the flag there, he said. The last time Duterte spoke of raising a flag on disputed territory, he later on admitted he was just joking. He had promised, as a presidential candidate, to jetski to Scarborough Shoal (Panatag Shoal) to plant the Philippine flag. When he became President, he ridiculed media for believing his statement.")
#rel = re.compute_for_reliability_score("Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories PhilippinesPhilippines is dead Duterte in of the rights over territories Philippines is dead Duterte in of the rights over territories Philippines")

#Topic.query.delete()
#print("topics" + str(Topic.query.all()))
#re.generate_topics()
#print("topics" + str(Topic.query.all()))
#re.get_topics_of_news_content()



