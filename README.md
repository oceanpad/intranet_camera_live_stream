# create python3 virtualenv
virtualenv -p python3 venv

# install requirement
pip install -r requirements.txt

# run script to send intranet camera image to remote server, need to change the url to your own url
python post_image.py

# run server on public server
python run.py
