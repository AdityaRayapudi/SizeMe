**Windows Git Bash**:

```bash
python -m venv env
./env/scripts/activate
pip install -r requirements.txt
flask run
```

**Mac OS / Linux**:

```bash
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt
flask run
```

The app should be running on (http://localhost:5000)

If you want to edit a page, just edit stuff inside:

```
{% block content %}
here
{% endblock content %}
```
