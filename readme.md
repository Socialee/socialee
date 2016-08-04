##Socialee
###Lokale Entwicklungsumgebung installieren, Systemvoraussetzungen

1. NodeJS: [https://nodejs.org/dist/v4.4.7/node-v4.4.7.pkg](https://nodejs.org/dist/v4.4.7/node-v4.4.7.pkg) (eigentlich brauchen wir das nur, um npm nutzen zu können)
2. Bower: [https://bower.io](https://bower.io) 	`sudo npm install -g bower`
3. Homebrew: [http://brew.sh](https://bower.io)	`/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)“`
4. Sassc: [http://brewformulas.org/sassc](https://bower.io)	`brew install sassc`
5. pyenv: [https://github.com/yyuu/pyenv](https://bower.io)	`brew install pyenv`
6. pyenv-virtualenv: [https://github.com/yyuu/pyenv-virtualenv](https://bower.io) `brew install pyenv-virtualenv`
7. python in pyenv installieren: [https://github.com/yyuu/pyenv#basic-github-checkout](https://bower.io) `pyenv install 3.5.1`
8. Postgres:  [http://postgresapp.com](https://bower.io)
9. .bash-profile anpassen, siehe unten.
10. Clone Socialee from gitHub: [https://github.com/Socialee/socialee.git](https://bower.io)
11. `cd socialee`
12. virtual-environment erstellen: `pyenv virtualenv 3.5.1 socialee`
13. to automatically activate/deactivate virtualenv: `pyenv local socialee`
  

**.bash-profile**

```
export PYENV_ROOT=/usr/local/var/pyenv
if which pyenv > /dev/null; then eval "$(pyenv init -)"; fi
if which pyenv-virtualenv-init > /dev/null; then eval "$(pyenv virtualenv-init -)"; fi
export PS1='\W \$ '
export PATH=$PATH:/Applications/Postgres.app/Contents/Versions/latest/bin 
```

Zur Installation von pyenv lohnt sich der Guide auf [https://github.com/yyuu/pyenv](https://github.com/yyuu/pyenv) und zum Verständnis der virtualenv der auf [https://github.com/yyuu/pyenv-virtualenv](https://github.com/yyuu/pyenv-virtualenv).

Sehera hatte noch folgende Issues:

* zlib from comandline developer tools mostly already installed
`xcode-select --install`
* need pip-tools
`pip install pip-tools`
* pip should be upto date
`pip install --upgrade pip`
* need these two packages `pip install django-contrib-comments`
`pip install django-tagging`

-
###Liste der addons, plugins, apps, snippets
* Sekizai (inheritance/verschachtelung für css/js)[https://django-sekizai.readthedocs.io/en/latest](https://django-sekizai.readthedocs.io/en/latest/)
* Django-Allauth (User-Verwaltung, onboarding, facebook-login, etc.) [https://github.com/pennersr/django-allauth](https://github.com/pennersr/django-allauth)
* Zinnia (Blog-System) [https://github.com/Fantomas42/django-blog-zinnia](https://github.com/Fantomas42/django-blog-zinnia)

-
###und sonst so?
* Socialee wird (derzeit noch) gehostet bei:
	* Staging [https://socialee-stage.herokuapp.com](https://socialee-stage.herokuapp.com)
	* Production [https://socialee.herokuapp.com](https://socialee.herokuapp.com)
* Lokal verwenden wir sqlite, in staging und production postgresql 
* Müssen noch eine bestpractice im Umgang mit Datenbanken und migrations entwickeln, bisher wird die db.sqlite nicht committet, was im Grunde auch Sinn macht aber oft zu Konflikten mit migrations führt. Any ideas anyone?
* Dieses Readme darf von jedem erweitert werden :-)
