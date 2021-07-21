pnbp-blog 

RESTful blogs (aka static websites) implemented in FastAPI for [pnbp](https://github.com/prettynb/pnbp/).

--- 

how it works :
- ```pnbp.Notebook``` converts #public notes to HTML and contains methods to communicate with a running **pnbp-blog/** instance. 
- **pnbp-blog/** receives HTML (& images), wraps the HTML with local extends and jinja2 template tags, and saves each statically to an .html file (avail from: notebook/[[My Next Best Note]] -> myblogurl.com/my-next-best-note and then caught and rendered by name via existence as a single slug through a general {content} view function.)
- use **nb-commit-remote** or **nb-commit-local** to update
- use **nb-commit-stage** to see the staged changes before updating
- if any page is made unpublic with #public tag removal (or #private tag addition), pnbp.Notebook will delete it from the server on next commit.
- only those notes with newer changes than most recently received will be POST-ed and images only transfer once. if you want to ensure all #public markdown files are pushed to the remote server, you can use **nb-touch-all-public**. 

--- 

**installation (for local development)** :

(1)

```bash
git clone https://github.com/prettynb/pnbp-blog/ blog
cd blog/
pip install -r requirements.txt
```

(2)

create a file **blog/.env**, it should look like this:

```bash
JWT_SECRET=long123random456alphanumeric
echo JWT_ALGO=HS256
```

^^ (pick a different **JWT_ALGO** if desired, and) generate some long alphanumeric for **JWS_SECRET** via e.g.

```py
>>> import uuid
>>> uuid.uuid4().hex
'1ab12802724b4d9ebe92e3eecae8b4f6'
```


(3) 

--> immediately available to 
--> run the server with: ```python main.py```
--> in a browser: http://127.0.0.1:8000/ 

--- 

further initialization : 

create your API user

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


personalize it by updating your **pnbp_conf.json** file :

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
    "darkmode": true,
    "hljs_light": "sublime",
    "hljs_dark": "xt256",
    "merm_light": "forest",
    "merm_dark": "default",
    "PUB_LNK_ONLY": true
}
```

```"NAV_BRAND": ""``` ... 

```"FOOTER": "<p></p>"``` ... 

``` "NAV_PAGES": {}``` *dict*ates what links are in the navbar. Notice you can create a nested drop down with a *list* value. 

```"darkmode": true``` sets the darkmode to default, while white-on-black text is still available by button in the navbar. ```_light``` and ```_dark``` values dictate additional styling on the switch.

```hljs_``` - see the [highlightjs demo pages](https://highlightjs.org/static/demo/) and [this github link](https://github.com/highlightjs/highlight.js/tree/main/src/styles) to find the correct string value for your favorite styles. 

```merm_``` - see [mermaid js](https://mermaid-js.github.io/mermaid/#/) and [this github link](https://github.com/mermaid-js/mermaid/tree/master/src/themes) for the correct string value to your favorite styles.

```"PUB_LNK_ONLY": true``` turns off rendering for any internal \[\[links\]\] to HTML that point to non- \#public notes. 

...

```py
>>> # --> commit your new settings ! 
>>> nb.blog_settings_post()
>>> # --> tag a note #public
>>> # --> 
>>> nb.post_commits_to_blog_api()
```

--- 

(included css files are to support inline [bootstrap icons](https://icons.getbootstrap.com/) by \<i\>\</i\>)


