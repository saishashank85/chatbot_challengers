# Chatbot Challengers Multi-lingual Chatbot (Hello India)
This chatbot is a faq bot built for the banking domain which can handle some basic user queries in hindi/english such as : 
1. Account Opening and Closing
2. Branch Information
3. Login Issues
4. transaction queries
5. Card Related
6. Biometrics
7. Fund Transfers ( upi/rtgs/mobile )
8. Loan related
10. Deposit related ( FD/RD ) 
12. Report Fraud
13. Account info
# Installation 
1. Clone the project
    `git clone url`  
2. Install the python moudles from requirements.txt
 3. 
  - a. Place the files from /hugging_face in "site-packages/rasa/nlu/utils/hugging_face/"

  - b. Run the run_installs.sh file `bash run_installs.sh`
4. Download the multilingual transformers model and place the path(unzip the model) in the `config.yml` file. 
  - 4.1. https://storage.googleapis.com/ai4bharat-public-indic-nlp-corpora/models/indic-bert-v1.tar.gz
   
# How to use 
1. Run the project with `rasa run` in terminal from the main project folder.
2. To get responses from the api send a `POST` request to the server address `(default:localhost:5005/)` with key as `message` in JSON format. 
  - 2.1 
Example : `{
              'message' : ' i need a loan ' ,
              'sender' : 'user123'
              }`
          
3. To get the response from the NLU model and fetch the intent prediction rankings , entities send a `POST` request to `localhost:5005/model/parse/` with key as `text` in JSON      format. 
  - 3.1 
Example : `{
              'text' : ' i need a loan ' ,
              'sender' : 'user123'
              }`
4. To train the chatbot , run the `rasa train` command . This trains the chatbot with the data in NLU & Domain Files using the `config.yml` pipeline . 

# Folder Structure
  ### data/ :
    This folder defines 3 files :
      a. NLU.yml
      b. rules.yml
      c. stories.yml
    NLU.yml : This file contains the training data used for the intent and entity classifier.
              We have also define synonyms , lookup tables & regex's in this file for the banking terms .
    rules.yml : Rules contain stories that the `RulePolicy` in rasa trains on . If the `RulePolicy` is used , when ever any rules is met it would be the default response                         irrespective of other actions .
    stories.yml : This file contains user stories that the `Rasa Core` trains on . The conversation flow is decided by the model based on this training data.
  ### domain/ :
    This file defines all the intents , entities , responses , actions , session_config and any other requires information that the bot may need .
    
# High Level Design
-image architecture from dbs laptop [todo]

1. Language Detection : All indian languages ( Native Script ) & Hindi written in English
   - For detecting native script languages we are using `textblob` package.
   - For detecting hinglish ( hindi written in english ) we have trained our custom model using supervised classification on a hinglish corpus.
   
2. Standardisation : We do the spell check and abbrivation expansion . We also normalise all numbers written in text to their numeric form.
   - Example : ` Mera acc se ten thousand transfer karna he` -----> `Mere account se 10000 transfer karna he`
   
3. Dense Multilingual Embeddings : We hava used a custom component and integrate `indic-bert` a multi-lingual AlBert model which was specially trained on 12 major indic                                            languages. 

4. Rasa NLU : Rasa NLU takes input training data as well as the trained classfication models and contextualy predict the appropriate responses to the user.
- images : config.yml [todo]

5. DiET Classifier : Dual Intent and Entity classifier takes all the dense and sparse features created by the other components in the pipeline and outputs the intents and                            entities in the user data and their confidenses . These are then used by the Rasa Core. 

   - Examples : `I want to make a [upi](transaction_type) transaction` 
      -          Entity : transaction_type 
      -          Value : 'upi'

6. Custom Entity Detection : We open-source NER framework specialised for indian languages . This recognises the dates , currency , amount , phone number and time . 
   - Time : Detect time from given text.
      - Example : tomorrow morning at 5
      -           कल सुबह ५ बजे, 
      -           kal subah 5 baje
      - Languages : 'en', 'hi', 'gu', 'bn', 'mr', 'ta'
      
    - Date : Detect date from given text.
      - Exmaple : next monday
      -           agle somvar
      -           अगले सोमवार
      - Languages : 'en', 'hi', 'gu', 'bn', 'mr', 'ta'
    - Numbers : Detect number and units from given text
      - Example : 50 rs per person
      -           ५ किलो चावल
      -           मुझे एक लीटर ऑइल चाहिए
      -           ९८३३४३०५३५
      - Languages : 'en', 'hi', 'gu', 'bn', 'mr', 'ta'
      
7. FallBack Policy : If the Rasa NLU model prediction confidence is low for a given user query , we can define our own custom actions and also modify the thresholds for the policy. This avoids giving improper responses if the user input is not understood / classified properly. We can also define our custom actions to ask the user for the closest possible predictions for their query(TwoStageFallBack Policy)
      
# Features 
1. Indic Bert in the Chatbot enables us to train the chatbot in 12 indian languages independently without the need for multiple models irrespective of the user stories logic. 
2. Allows for defining complex user stories and allows us to customise with several policies.
3. Custom entity recognition for indian languages . The custom components and models built can directly be used in an already existing rasa chatbot with mininal training.
4. Easy to deploy as a docker container . Rasa provides a docker image ready to deploy in dockerhub. This comes with a ci/cd workflow pipeline. 
5. Rasa SDK provides easy integration with FB Messenger , Slack , Microsoft Teams , Telegram and other major communication platforms.
6. Several third party frontends available to manage , train and annotate the data. 
7. Ability to collect user data for annotation and constantly improve with minimal human intervention. 
8. The bot does not fail on unrecognised input and tries to navigate the user to the required intent. 

# Future scope / Improvements : 
1. Add training data in other indic languages. 
2. Add slots for collecting user data and use for custom action . 
3. Implement a custom action for TwoStageFallback Policy for un-handled queries. 





