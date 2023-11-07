# Trello Burndown Generator

A Python CLI tool to generate a burn down chart from a Trello board using selenium and matplotlib. Optionally a burn down chart can be created for an individual member of the board such as in the example below.

Go from this:

![Trello Board](./docs/board-example.png)

To this:

![Burndown Chart](./docs/chart-example.png)

## Usage

1. Create a Kanban Trello board with a *resolved* and a *sprint backlog* bucket.
2. Create a burner Trello account and invite them to your board *(you can use your personal account, but it isn't recommended since this program may cause your account to be banned for botting, although this is yet to be confirmed)*
3. Clone this repository with the GUI above or with the following command:

```shell
git clone https://github.com/nico-i/trello-burndown-gen
```

1. install the dependencies:

```shell
pip install -r requirements.txt
```

5. Add a `conf.json` to the root dir. See [`example.conf.json`](./example.conf.json) for an example or the [*Configuration*](#configuration) section for more information.
6. Run the program:

```shell
py burndown_gen.py
```

## Configuration

The program can either be configured via a `conf.json` file in the root directory or via CLI arguments. The CLI arguments take precedence over the `conf.json` file. A detailed description of the configuration options can be found below.

| Option               | CLI Argument                     | Description                                                                                                      | Type                    | Default                          | Required                                             |
| -------------------- | -------------------------------- | ---------------------------------------------------------------------------------------------------------------- | ----------------------- | -------------------------------- | ---------------------------------------------------- |
| -                    | `--config` or `-c`               | The path to the config file. (only available in CLI)                                                             | `string`                | `"conf.json"`                        | Only required if not using default config file path. |
| `browser`            | `--browser` or `-b`              | The browser to use for the selenium webdriver.                                                                   | `"firefox"` \| `"chrome"`   | `"chrome"`                           | ✔️                                                    |
| `headless`           | `--headless` or `-h`             | Whether to run the browser in headless mode.                                                                     | `boolean`               | `true`                             | ✔️                                                    |
| `refetch`            | `--refetch` or `-r`              | Whether to refetch the data from Trello or use cached data. (will automatically refetch if cache does not exist) | `boolean`               | `false`                            | ✖️                                                    |
| `email`              | `--email` or `-em`               | The email of the burner Trello account.                                                                          | `string`                | -                                | ✔️                                                    |
| `password`           | `--password` or `-p`             | The password of the burner Trello account.                                                                       | `string`                | -                                | ✔️                                                    |
| `board_url`          | `--board-url` or `-burl`         | The URL of the Trello board to parse.                                                                            | `string`                | -                                | ✔️                                                    |
| `member`             | `--member` or `-m`               | The name of the burner Trello account.                                                                           | `string`                | -                                | ✖️                                                    |
| `resolved_list_name` | `--resolved-list-name` or `-rln` | The name of the resolved list.                                                                                   | `string`                | -                                | ✔️                                                    |
| `sprint_bl_name`     | `--sprint-bl-name` or `-sbln`    | The name of the sprint backlog list.                                                                             | `string`                | -                                | ✔️                                                    |
| `sprint_end_date`    | `--sprint-end-date` or `-sed`    | The end date of the sprint.                                                                                      | `"<YYYY-MM-DD>"` | The day of execution i. e. today | ✖️                                                    |
| `sprint_duration`    | `--sprint-duration` or `-sd`     | The duration of the sprint in days.                                                                              | `int`                   | `14`                               | ✖️                                                    |

## Development

To develop this program, apart from the steps mentioned above, it is recommended to create a virtual environment and install the dependencies with `pip install -r requirements.txt`.

To create a virtual environment, run:

```shell
python -m venv <path to venv>
```

To activate the virtual environment, run:

```shell
<path to venv>/Scripts/activate.bat # on Windows
```

or

```shell
<path to venv>/bin/activate # on Linux
```

To deactivate the virtual environment, run:

```shell
deactivate
```

## License

See the [LICENSE](LICENSE) file.
