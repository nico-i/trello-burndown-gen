# Trello Burndown Generator

This is a simple tool to generate a burndown chart from a Trello board using selenium and matplotlib.

## Usage

1. Create a Kanban Trello board with a *resolved* list.
2. Create a burner Trello account and invite them to your board (you can use your personal account, but it isn't recommended since this program requires the actual account password to log in)
3. Clone this repository and install the dependencies with `pip3 install -r requirements.txt`
4. Update the `config.json` file with your Trello credentials, a URL to your board and the name of the *resolved* list. See [`config.json.example`](./example.config.json) for an example.
5. Navigate into the `src` directory with `cd src`
6. Run the program with `python3 burndown_gen.py`
