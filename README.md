pnbp-blog is a FastAPI implementation of publishing static websites (aka blog) against #public .md notes in a pretty notebook - handling for (most) from https://obsidian.md/ (e.g. mermaid-js).

see: https://github.com/prettynb/pnbp/


--- 
how it works (w/ pnbp):

- pnbp.Notebook converts #public notes to HTML -> contains methods to communicate with running pnbp-blog/ api instance -> which receives HTML (& images), wraps it with local extends and jinja2 template tags, and saves each publicly-made notebook "page" statically to an .html file (avail from: notebook/[[My Next Best Note]] -> myblogurl.com/my-next-best-note via existence as a single slug through a single general {content} view function.)
- use **nb-commit-remote** or **nb-commit-local** 
- if page made unpublic with #public removal, pnbp.Notebook deletes from server on next push
- use **touch-all-public** if you want to ensure all #public markdown files are pushed to the remote server, otherwise only pushes those pages with newer changes than most recently received. 
- images only transfer once

--- 
**installing pnbp-blog (local dev)**

```sh
git clone https://github.com/prettynb/pnbp-blog/ blog
cd blog/
pip install -r requirements.txt
nano .env
```

generate long alphanumeric JWS_SECRET via e.g. 

```py
>>> import uuid
>>> uuid.uuid4().hex
'1ab12802724b4d9ebe92e3eecae8b4f6'
```

+ (pick a non-default JWT_ALGO if desired)

--> 

add these values to the blog/.env file:
```py
JWT_SECRET=long123random456alphanumeric
JWT_ALGO=HS256
```

--> 

```sh
python main.py
\# then in browser see: https://127.0.0.1:8000/ 
```

...

--- 
Place a version of **blog-settings.json** locally into your nb.NOTE_PATH
e.g. 

```json
{
    "NAV_BRAND": "<i class='bi bi-globe2'></i><i class='bi bi-book-fill'></i> ",
    "NAV_PAGES": {
        "content": "/index/",
        "about": "/about/",
        "contact": [
            {
                "github": "https://github.com/pretty-nb/"
            },
            {
                "subname2": "/subroute2/"
            }
        ]
    },
    "FOOTER": "&nbsp;| <small>powered by <a href=\"https://www.python.org/\">Python</a>&nbsp;,&nbsp;<a href=\"https://fastapi.tiangolo.com/\">FastAPI</a>&nbsp;,&nbsp;<a href=\"https://getbootstrap.com/\">Bootstrap</a>&nbsp;,&nbsp;and&nbsp;</a><a href=\"https://obsidian.md/\">Obsidian</a>&nbsp;via&nbsp;<a href=\"https://daringfireball.net/projects/markdown/\">markdown</a>.</small></p>",
    "darkmode": false,
    "hljs_light": "default",
    "hljs_dark": "xt256",
    "merm_light": "default",
    "merm_dark": "dark"
}
```

--- 

further initialization:

```py
>>> import pnbp
>>> nb = pnbp.Notebook()
>>> nb.create_api_user()
>>> nb.refresh_token()
>>> # username: 
>>> # password: 
>>> # --> can test commit with
>>> nb.get_authed_user()
>>> # --> commit your new settings ! 
>>> nb.blog_settings_post()
>>> # --> tag a note #public
>>> # --> 
>>> nb.post_commits_to_blog_api()
>>> # ^^ equiv to avail commands
>>> # % nb-commit-remote 
>>> # or 
>>> # % nb-commit-local
```

also available:

```py
>>> nb.reset_api_password()
>>> nb.refresh_token() # even while same password, now old token rejected
```

--- 




