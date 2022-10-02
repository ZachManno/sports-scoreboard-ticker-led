## Python env setup
pyenv versions
pyenv virtualenv 3.9.11 sports-news-rss
pyenv local sports-news-rss
pyenv activate sports-news-rss
pipenv install
pipenv shell
pipenv install requests

### Pycharm
Set Python interpreter as
```
~/.pyenv/versions/sports-news-rss/bin/python
```