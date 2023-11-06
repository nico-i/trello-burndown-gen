# Trello Burndown Generator

A Python CLI tool to generate a burn down chart from a Trello board using selenium and matplotlib.

## Usage

1. Create a Kanban Trello board with a *resolved* and a *sprint backlog* bucket.
2. Create a burner Trello account and invite them to your board (you can use your personal account, but it isn't recommended since this program requires the actual account password to login + it may also potentially ban your account for botting, although not confirmed)
3. Clone this repository and install the dependencies with `pip3 install -r requirements.txt`
4. Add a `conf.json` to the root dir. See [`example.conf.json`](./example.conf.json) for an example or the [**Configuration** section](/#configuration) for more information.
5. Run the program in the CLI with `<python installation> burndown_gen.py`

## Configuration

