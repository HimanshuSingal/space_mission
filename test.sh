cd ~/code/space
nodejs server/start-server.js &
sleep 2
cd clients/python/
source venv/bin/activate
python cli.py --ai dummy &
python cli.py --ai your_ai &