from flask import Flask, render_template
from pathlib import Path
from platformdirs import user_data_dir
import json

data_dir = user_data_dir("krivoruchko-dev", "krivoruchko-dev")
DATA_DIR = Path(data_dir)
DATA_DIR.mkdir(parents=True, exist_ok=True)

DB_PATH = DATA_DIR / "data.txt"
DB_PATH.touch(exist_ok=True)

app = Flask(__name__)

@app.route("/")
def hello_world():
    services = None
    with open('services.json', 'r') as file:
        services = json.load(file)

    time_visited = 0

    with open(str(DB_PATH), 'r') as file:
         file_content = file.read()
         time_visited = 0 if file_content == '' else int(file_content)

    with open(str(DB_PATH), 'w') as file:
        time_visited += 1
        file.write(str(time_visited))

    return render_template("index.html", services=services, visited=f'time visited {time_visited}')

if __name__ == "__main__":
    app.run()