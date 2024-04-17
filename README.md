Make semi-rule-based hybrid chatbots.
Convform is an a conversation design interface for creating rule-based chatbots optionally AI powered chatbots.

It contains:

A Python Flask backend with a database and all the logic for developing a hybrid semi-rule-based chatbot.
A React app which contains en environment to run and test chatbots, an admin to maintain, develop and test chatbots.

To install and run:

```sh
git clone https://github.com/almarsk/convform.git
cd convform/convfront
npm install
cd ..
chmod +x update_convfront.sh
./update_convfront.sh
python3 -m venv venv
source venv/bin/activate //.fish
pip install --upgrade pip
pip install -r requirements.txt
mv template_config.json config.json // add your openAI API key here
python app.py
open 127.0.0.1/admin
```

More about how to create, test, run and maintain chatbots in [wiki](https://github.com/almarsk/convform/wiki)
