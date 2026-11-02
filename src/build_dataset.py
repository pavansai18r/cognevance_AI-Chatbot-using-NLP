"""Generates data/intents.json (conversational training data).
Each intent has many user patterns + several responses. Edit and re-run to extend."""
import json, pathlib

INTENTS = {
 "greeting": (["hi","hello","hey there","good morning","good evening","hey","hello bot","hi there","greetings","is anyone there","howdy","good afternoon"],
   ["Hello! How can I help you today?","Hi there! What can I do for you?","Hey! Nice to see you. How can I assist?"]),
 "goodbye": (["bye","goodbye","see you later","talk to you soon","i have to go","good night","catch you later","see you","that is all bye","exit","quit"],
   ["Goodbye! Have a great day.","See you later! Come back anytime.","Bye! Take care."]),
 "thanks": (["thanks","thank you","thanks a lot","that was helpful","many thanks","thank you so much","appreciate it","great thanks","cheers","awesome thank you"],
   ["You are welcome!","Happy to help!","Anytime! Anything else?"]),
 "bot_identity": (["who are you","what are you","what is your name","tell me about yourself","are you a robot","are you human","introduce yourself","what should i call you","are you a bot"],
   ["I am an NLP-powered chatbot built for the Cognevance project. I classify your intent and reply accordingly."]),
 "capabilities": (["what can you do","how can you help me","what are your features","help me","what do you know","what topics can you talk about","show me your skills","can you help","what services do you provide"],
   ["I can chat, tell jokes, share the time, explain AI/NLP/ML basics, and answer questions about courses, support and pricing."]),
 "how_are_you": (["how are you","how are you doing","how is it going","whats up","how do you do","are you okay","how have you been","how is your day"],
   ["I am doing great, thanks for asking! How about you?","All systems running smoothly! How can I help?"]),
 "joke": (["tell me a joke","say something funny","make me laugh","do you know any jokes","joke please","i want to hear a joke","got any jokes","cheer me up with a joke","tell me something funny"],
   ["Why do programmers prefer dark mode? Because light attracts bugs!","I told my computer I needed a break, and it said: no problem, I will go to sleep.","Why was the neural network bad at parties? It kept overfitting to the small talk."]),
 "time": (["what time is it","tell me the time","current time","what is the time now","do you have the time","time please","whats the time","show me the clock"],
   ["__TIME__"]),
 "date": (["what is the date today","todays date","what day is it","which day is today","tell me the date","current date","what is today","whats the date"],
   ["__DATE__"]),
 "what_is_ai": (["what is artificial intelligence","explain ai","define ai","tell me about artificial intelligence","what does ai mean","ai meaning","how does ai work","what is ai"],
   ["Artificial Intelligence (AI) is the field of building machines that perform tasks normally requiring human intelligence, such as understanding language, recognising images and making decisions."]),
 "what_is_ml": (["what is machine learning","explain machine learning","define ml","how do machines learn","machine learning meaning","what is ml","tell me about machine learning","how does ml work"],
   ["Machine Learning (ML) is a branch of AI where algorithms learn patterns from data instead of being explicitly programmed."]),
 "what_is_nlp": (["what is nlp","explain natural language processing","define nlp","what does nlp mean","tell me about nlp","how do computers understand language","natural language processing meaning","how does nlp work"],
   ["Natural Language Processing (NLP) lets computers read, understand and generate human language, using steps like tokenization, stemming, vectorization and classification."]),
 "what_is_deep_learning": (["what is deep learning","explain neural networks","define deep learning","how do neural networks work","what is a neural network","deep learning meaning","tell me about deep learning"],
   ["Deep Learning uses multi-layer neural networks to learn complex patterns from large amounts of data, powering modern vision and language systems."]),
 "programming_language": (["which programming language should i learn","best language for ai","should i learn python","what language is used for machine learning","recommend a programming language","is python good for ai","where do i start coding"],
   ["Python is the most popular choice for AI and data science thanks to libraries like NumPy, scikit-learn, TensorFlow, PyTorch and spaCy."]),
 "courses": (["what courses do you offer","tell me about your courses","available programs","which internships are available","list your training programs","do you have data science courses","what can i learn here","course details"],
   ["We offer programs in Data Science, Machine Learning, Web Development and AI. Visit our website or email support for the full catalogue."]),
 "pricing": (["how much does it cost","what is the price","pricing details","is it free","what are the fees","cost of the program","how much do i have to pay","any charges"],
   ["Pricing depends on the program. Please contact support for current fees and any available discounts."]),
 "contact_support": (["how can i contact support","i need to talk to a human","customer care number","support email","who do i contact for help","i want to report a problem","contact details","reach your team"],
   ["You can reach the support team by email at support@cognevance.online."]),
 "certificate": (["will i get a certificate","do you provide certificates","internship certificate","how do i get my certificate","is there a completion certificate","certification details"],
   ["Yes, a completion certificate is issued after you successfully submit all assigned projects."]),
 "submission": (["how do i submit my project","submission process","where to upload my work","how to submit github link","project submission instructions","what should i submit","where do i send my repository"],
   ["Create one GitHub repo per project named cognevance_projectName, add a README, then email all repository links to support@cognevance.online."]),
 "weather": (["what is the weather","is it going to rain","weather forecast","how hot is it today","will it be sunny","temperature outside","tell me the weather"],
   ["I cannot check live weather, but a weather app or your local forecast site will give accurate results."]),
 "feeling_sad": (["i am sad","i feel low","i am depressed","i am feeling lonely","i am stressed","i feel anxious","im having a bad day","i feel down","i am upset"],
   ["I am sorry you are feeling this way. Talking to a friend, family member or a professional can really help. I am here to chat if you want."]),
 "compliment": (["you are smart","good bot","you are awesome","nice work","you are great","i like you","well done","you are amazing","you are helpful"],
   ["Thank you, that is kind of you!","Aww, thanks! I am glad I could help."]),
 "insult": (["you are stupid","you are useless","bad bot","i hate you","you are dumb","worst chatbot ever","you suck","shut up"],
   ["I am sorry I let you down. I am still learning, so please try rephrasing and I will do my best."]),
 "yes": (["yes","yeah","yep","sure","ok","okay","of course","absolutely","alright"], ["Great! Please go ahead."]),
 "no": (["no","nope","not really","no thanks","nah","maybe later","not now"], ["No problem. Let me know if you need anything else."]),
}
EXTRA = {
 "greeting": ["hello friend","hey bot","hi buddy","morning","yo","hey how are things","hello again","hi good day"],
 "goodbye": ["bye bye","farewell","see you tomorrow","i am leaving now","take care bye","gotta run","talk later","ok bye then"],
 "how_are_you": ["how are things","how is everything","how are you today","are you doing well","hows life","how do you feel","you good"],
 "compliment": ["you are so smart","great job","you are the best","i love this bot","brilliant answer","excellent work","you are so clever","good job bot","impressive"],
 "insult": ["you are an idiot","this bot is terrible","you are so bad","useless bot","i dislike you","you are annoying","you are the worst","stupid bot","you make me angry"],
 "no": ["no i do not","no way","definitely not","i do not think so","not interested","no that is all","i dont want that","negative"],
 "yes": ["yes please","yes i do","sure thing","definitely","that is right","correct","go ahead","yes i want that"],
 "pricing": ["what is the fee","is the course free","how much is the internship","do i need to pay","what is the cost","are there any fees","price of the course","is it paid"],
 "contact_support": ["how can i reach support","how do i reach you","i need help from a person","email address for support","talk to customer service","where can i complain","support contact","how to contact you"],
 "courses": ["what courses are available","which courses can i take","what programs do you have","list of courses","what do you teach","tell me about the internship programs","what subjects are offered","available internships"],
 "feeling_sad": ["i feel very lonely","i am very sad today","i feel really low","i am so stressed","i feel hopeless","i am feeling anxious","i am so down today","i feel miserable"],
 "programming_language": ["which language is best for ai","best programming language for data science","what language should i start with","is python good for machine learning","which language do ai engineers use","what should i code in","python or java for ai"],
 "weather": ["how is the weather","is it raining today","weather today","will it rain tomorrow","is it cold outside","whats the temperature","check the weather"],
 "bot_identity": ["what is your name","who made you","what do i call you","who is this","tell me your name","are you an ai","what kind of bot are you"],
 "thanks": ["thanks so much","thank you very much","thanks for helping","much appreciated","thank you bot","thx","ty"],
 "certificate": ["will i receive a certificate","how to get certificate","is a certificate provided","do i get a certificate after completion","certificate after internship"],
 "submission": ["how do i send my github link","where do i submit the repository","how to submit assignments","what is the submission format","submit my project link","how should i name my repo"],
 "joke": ["tell me a funny joke","crack a joke","tell me another joke","know any funny jokes","say a joke","make me smile with a joke"],
 "time": ["what is the time","what time is it now","can you tell me the time","current time please","time now"],
 "date": ["what is the date","what is todays date","which date is it today","tell me todays date","day and date"],
 "capabilities": ["what can you help me with","what do you do","how can you assist","what are you able to do","list your abilities"],
 "what_is_ai": ["what is ai exactly","explain artificial intelligence","ai definition","what do you mean by ai"],
 "what_is_ml": ["what is ml exactly","explain ml","ml definition","how machine learning works","what do you mean by machine learning"],
 "what_is_nlp": ["what is nlp exactly","nlp definition","explain nlp to me","what do you mean by nlp"],
 "what_is_deep_learning": ["what is a deep neural network","explain deep learning","deep learning definition","what are neural networks"],
}
for _t, _ps in EXTRA.items():
    INTENTS[_t][0].extend(p for p in _ps if p not in INTENTS[_t][0])

FALLBACK = ["Sorry, I did not quite understand that. Could you rephrase?",
            "I am not sure I can help with that yet. Try asking about AI, courses, support or submissions."]

def main():
    data = {"fallback": FALLBACK,
            "intents": [{"tag": t, "patterns": p, "responses": r} for t, (p, r) in INTENTS.items()]}
    out = pathlib.Path(__file__).resolve().parent.parent / "data" / "intents.json"
    out.write_text(json.dumps(data, indent=2))
    n = sum(len(v[0]) for v in INTENTS.values())
    print(f"Wrote {out} | {len(INTENTS)} intents | {n} patterns")

if __name__ == "__main__":
    main()
