Make semi-rule-based hybrid chatbots.
Convform is an a conversation design interface for creating rule-based and optionally AI powered chatbots.

Check out [wiki](https://github.com/almarsk/convform/wiki) to learn how to create, test, run and maintain chatbots.

It contains:

A Python Flask backend with a database and all the logic for developing a hybrid semi-rule-based chatbot.
A React app which contains en environment to run and test chatbots, an admin to maintain, develop and test chatbots.

To install and run:

```sh
git clone --depth 1 https://github.com/almarsk/convform.git
cd convform/convfront
npm install
npm audit fix
cd ..
chmod +x update_convfront.sh
./update_convfront.sh
python3 -m venv venv
source venv/bin/activate #.fish
pip install --upgrade pip
pip install -r requirements.txt
mv template_config.json config.json # add your openAI API key here
python app.py
```

and then in another terminal

```sh
# add your openAI API key to config.json
open http://127.0.0.1:5000/admin
```

There is a login endpoint in routes/admin/login.py\
currently let's everything through
