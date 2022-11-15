## Python env setup
```
pyenv versions
pyenv virtualenv 3.9.11 espn-scores
pyenv local espn-scores
pyenv activate espn-scores
pipenv install
pipenv shell
pipenv install requests
```


When done:
`pyenv deactivate espn-scores`

### Pycharm
Set Python interpreter as
```
~/.pyenv/versions/espn-scores/bin/python
```

## Running LED Script
- cd to this directory (cd espn-scores)
- run script
```bash
sudo ./led_ticker.py --led-cols=64 --led-rows=32 --led-gpio-mapping=adafruit-hat --led-slowdown-gpio=3
```
