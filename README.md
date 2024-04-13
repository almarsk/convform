Make semi-rule-based hybrid chatbots.
Convform is an a conversation design interface for creating rule-based chatbots optionally AI powered chatbots.

It contains:

A Python Flask backend with a database and all the logic for developing a hybrid semi-rule-based chatbot.
A React app which contains en environment to run and test chatbots, an admin to maintain, develop and test chatbots.

To install:
```sh
git clone https://github.com/almarsk/convform.git
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mv template_config.json config.json // add your openAI API key here
```

python app.py
```
