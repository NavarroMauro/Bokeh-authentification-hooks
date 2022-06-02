# Demo Bokeh authentification hooks

run the server with:

```bash
bokeh serve --enable-xsrf-cookies --auth-module=auth.py user_1 user_2 user_3
```

# Expected behaviour:

### Once you login you will be redirected to the route of each user. For example if login with user_1 you will be redirected to /user_1. 

### That part is working as expected however I would like to keep users restricted to his own route. 