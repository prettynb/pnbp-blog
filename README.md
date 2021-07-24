pnbp-blog 

RESTful blogs (aka static websites) implemented in FastAPI for [pnbp](https://github.com/prettynb/pnbp/).

--- 

**blog** 
- (1) receives HTML and images (wrapping HTMLwith jinja2 template tags),
- (2) saves each page statically to an .html file,
- (3) -> catching and rendering by name via existence as a single slug through a general {content} view function ...
- e.g.  notebook/[[My Next Best Note]] -> myblogurl.com/my-next-best-note 

via **pnbp**
-  (1) conversion of **\#public** notes to HTML,
-  (2) communicating with : 
    -  ... **```nb-commit-remote```** (or **```nb-commit-local```**) to commit changes
    -  ... **```nb-commit-stage```** to see the staged changes before updating

**...** 
-  any note made unpublic between commits (e.g. #public tag removal or #private tag addition), are deleted from the server on next commit.
- only those notes with newer changes than most recently received will be POST-ed and images only transfer once. if you want to ensure all #public markdown files are pushed to the remote server, you can use **```nb-touch-all-public```**. 

--- 

#### **installation (for local development)** :

--- 

##### (1) -> ```nb-git-clone-pnbp-blog```

or do it manually : 

```bash
git clone https://github.com/prettynb/pnbp-blog/ blog
cd blog/
```

```
pip install -r requirements.txt
```

--- 

##### (2) -> **blog/** **.env** :

```nano .env```

```bash
JWT_SECRET=long123random456alphanumeric
JWT_ALGO=HS256
```

```py
>>> ^^ pick a different **JWT_ALGO** if desired,  
>>> and generate your own **JWS_SECRET**, e.g. 
>>> import uuid
>>> uuid.uuid4().hex
'1ab12802724b4d9ebe92e3eecae8b4f6'
```

--- 

##### (3) -> hello, world! : 

-->  run server: ```python main.py```
--> see browser: http://127.0.0.1:8000/ 

--- 

##### (4) -> create your API user : 

```py
>>> import pnbp
>>> nb = pnbp.Notebook()
>>> nb.create_api_user(username="alice")
>>> nb.refresh_token()
>>> # username: 
>>> # password: 
>>> nb.get_authed_user()
{"username": "alice"}
>>> # ^^ properly authenticating!
>>> # also available:
>>> nb.reset_api_password()
>>> nb.refresh_token() # even while same password, now old token rejected
```

--- 

##### (5) -> personalize ( [**pnbp_conf.json**](https://github.com/prettynb/pnbp/blob/master/conf_template.json) ) :

```json
    ...
    "NAV_BRAND": "alice.io",
    "NAV_PAGES": {
        "about": "/about/",
        "content": [
            {
                "topic a": "/topic-a/"
            },
            {
                "topic b": "/topic-b/"
            },
        ]
    },
    "FOOTER": "<p>email: fake@email.com</p>",
    "TITLE": "Alice's Blog",
    "darkmode": true,
    "hljs_light": "sublime",
    "hljs_dark": "xt256",
    "merm_light": "forest",
    "merm_dark": "default",
    "PUB_LNK_ONLY": true,
    "COMMIT_TAG": "#blog"
}
```

```"TITLE": ""``` ... 

```"NAV_BRAND": ""``` ... 

```"FOOTER": "<p></p>"``` ... 

``` "NAV_PAGES": {}``` *dict*ates what links are in the navbar. Notice you can create a nested drop down with a *list* value. 

```"darkmode": true``` sets the darkmode to default, while white-on-black text is still available by button in the navbar. ```_light``` and ```_dark``` values dictate additional styling on the switch.

```hljs_``` - see the [highlightjs demo pages](https://highlightjs.org/static/demo/) and [this github link](https://github.com/highlightjs/highlight.js/tree/main/src/styles) to find the correct string value for your favorite styles. 

```merm_``` - see [mermaid js](https://mermaid-js.github.io/mermaid/#/) and [this github link](https://github.com/mermaid-js/mermaid/tree/master/src/themes) for the correct string value to your favorite styles.

```"PUB_LNK_ONLY": true``` turns off rendering for any internal \[\[links\]\] to HTML that point to non- \#public notes. 

```"COMMIT_TAG": "#blog"``` - choose which \#tag your notebook publishes against (default: \#public).

```"EXCLUDE_TAG": "#noblog"``` - choose which \#tag your notebook won't publish even if also tagged \#private (default: \#private).

```"HIDE_COMMIT_TAG": true``` - turns off rendering the actual "\#public" tag from the published contents (e.g. "# this is a great #public blog page!" -> "\<h1\>this is a great  blog page!\<\\h1\>") (default: ```false```). 


--- 

##### -> **POST commits !**

directly in the python repl : 

```py
>>> # --> commit your new settings ! 
>>> nb.blog_settings_post()
>>> # --> tag a note #public
>>> # --> 
>>> nb.post_commits_to_blog_api()
```

from the command-line : 
- ```nb-commit-settings```
- ```nb-commit-local```

--- 

**\*\***
-  the only [included css](https://github.com/prettynb/pnbp-blog/tree/master/static/css) files are to support inline \<i\> [bootstrap icons](https://icons.getbootstrap.com/) \</i\>. 


