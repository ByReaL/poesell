# PRE ALPHA VERSION 

# poesell
The purpose of this software is to allow to make a fair sale of an item in Path of Exile game.
it will grab data from:
- personal stash
- game log for whispers
- poe.trade

it will monitor live the whispers and for each whisper will print history for that item

it will make recommendations based on interest in an item:
- no whispers in more than 7 days -> lower the price or vendor the item
- more than 3 whispers per day -> increase the price
- less than 3 whispers per day -> make the sale

# usage
rename 'RENAME_ME_settings.py' to 'settings.py' and fill in the required options
* NEVER UPLOAD 'settings.py' FILE OR SHARE IT

pip install -r requirements.txt

python main.py

# don't stick your screwdriver in your eye
this software comes AS-IS <BR>
use at your own risk

