# Talking Web
- *level 1* to *level 18*: skipped
- *level 19*: use `curl` to send a POST request with a parameter
    - `curl -X POST -F "a=cfc37f41d6228c890aa213b3b464e521" 127.0.0.1:80`
- *level 20*: use `nc` to send a POST request with a parameter
    - get the body length `echo -n "a=2ac185aa41066e695a38ea2f04ac4a9c" | wc -c`
    - `echo -e "POST / HTTP/1.1\r\nContent-Length: 34\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\na=2ac185aa41066e695a38ea2f04ac4a9c" | nc 127.0.0.1 80`
- *level 21*: use Python to send a POST request with a parameter
    ```
    data = {'a': 'c0cf5f007cb041f19323624166547116'}
    response = requests.post(url, data=data)
    print(response.content.decode())
    ```
- *level 22*: `curl -X POST --data-urlencode "a=01378b50d28f5187e0f9a1e4b45cfb8e" --data-urlencode "b=649fe3f4 7970f94a&31663219#3339bf03" 127.0.0.1:80`
- *level 23*: use `nc`, we need to URL encode `b`'s value using Python
    ```
    encoded_b=$(python -c "import urllib.parse; print(urllib.parse.quote_plus('6c78bdd7 dc58ca4d&e4bee555#5932bb45'))")
    body="a=243612d5dea672ebd6132d1f2d6ba3dc&b=$encoded_b"
    length=$(echo -n $body | wc -c)
    echo -e "POST / HTTP/1.1\r\nContent-Length: $length\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\na=243612d5dea672ebd6132d1f2d6ba3dc&b=$encoded_b" | nc 127.0.0.1 80
    ```
- *level 24*: use Python to send a POST request, we don't need to URL encode the value manually, Python will do it for us
    ```
    data = {'a': '0d75f032b2d5b368346d1bc5d977fbe2', 'b': 'cd40b8f8 4109ddfa&32facaea#71915775'}
    response = requests.post(url, data=data)
    print(response.content.decode())
    ```
- *level 25*: send JSON data with `curl`. IMPORTANT: cannot use single quote `'` inside the string after `-d`
    ```
    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"a": "e4ba3edb7fcbeeefbbbf1d90f9650afe"}' \
        http://127.0.0.1:80
    ```
    ```
    curl -X POST \
        -H "Content-Type: application/json" \
        -d "{\"a\": \"e4ba3edb7fcbeeefbbbf1d90f9650afe\"}" \
        127.0.0.1:80
    ```
- *level 25*: send JSON data with `nc`
    ```
    body="{\"a\":\"57135f440b29331e0f065702289000c1\"}"
    length=$(echo -n $body | wc -c)
    echo -e "POST / HTTP/1.1\r\nContent-Length: $length\r\nContent-Type: application/json\r\n\r\n$body" | nc 127.0.0.1 80
    ```
- *level 25*: send JSON data with Python
    ```
    headers = {'Content-Type': 'application/json'}
    data = {'a': '0abd87d24b1e84c44e0e566903db5070'}
    response = requests.post(url, json=data, headers=headers)
    print(response.content.decode())
    ```
- *level 26*: complex JSON data with `curl`
    ```
    curl -X POST \
        -H "Content-Type: application/json" \
        -d '{"a": "039cf0eae8a451ab200b7d1ca2b5ac43", "b": {"c": "3a22eb99", "d": ["3873ad0b", "767601a3 2f6b04e1&efc83655#c2999cc8"]}}' \
        127.0.0.1:80
    ```
- *level 27*: complex JSON data with `nc`
    ```
    d="\"d\":[\"4731f1aa\",\"68fc6c1a 931ddefb&64930b03#c5c71e33\"]"
    c="\"c\":\"882012ee\""
    a="\"a\":\"811a318af1a5be5c564eb4e7c6a18a99\""
    b="\"b\":{$c,$d}"
    body="{$a,$b}"
    length=$(echo -n $body | wc -c)
    echo -e "POST / HTTP/1.1\r\nContent-Length: $length\r\nContent-Type: application/json\r\n\r\n$body" | nc 127.0.0.1 80
    ```
- *level 28*: complex JSON data with Python: pass this `data` to `json` parameter
    ```
    data = {
        'a': '5f5b9875e45c5b667c8651b81d1b0125',
        'b': {
            'c': '708972db',
            'd': ['5364a74c', '464414f3 59836e74&bbc1fb02#1bd621b5']
        }
    }
    ```
- *level 31*: follow a redirect with `curl`: `curl 127.0.0.1:80 -L`
- *level 32*: for now, I didn't find a way to automate this process, I used 2 `nc` commands, the first sent a simple GET request, and get the redirect path, the second `nc` command followed that path
- *level 33*: in Python, `request.post` and `request.get` automatically follow the redirection
- *level 34*: make 2 requests, the second will set a cookie: `-b "X:1"`
- *level 35*: `echo -e "GET / HTTP/1.1\r\nCookie: cookie=0973da6e93a50d36363bd4552ddc007f\r\n\r\n" | nc 127.0.0.1 80`
- *level 36*: after getting a response with `Set-Cookie`, Python will automatically send another request and set the cookie for us
- *level 37*: make 4 stateful requests using `curl`
    1. `curl -c cookies.txt 127.0.0.1:80`
    2. `curl -b cookies.txt -c cookies.txt 127.0.0.1:80`
    3. `curl -b cookies.txt -c cookies.txt 127.0.0.1:80`
    4. `curl -b cookies.txt -c cookies.txt 127.0.0.1:80`
- *level 38*: use `nc`
    1. `echo -e "GET / HTTP/1.1\r\n" | nc 127.0.0.1 80`
        - response (Set-Cookie): `Set-Cookie: session=eyJzdGF0ZSI6MX0.ZedUNg.RyHHOWSVQgESLUbe9BxHeufpulQ; HttpOnly; Path=/`
    2. `echo -e "GET / HTTP/1.1\r\nCookie: session=eyJzdGF0ZSI6MX0.ZedT-g.BGpmNG-oEQnjPIr_S28EDDNet3s; HttpOnly; Path=/\r\n\r\n" | nc 127.0.0.1 80`
        - response (Set-Cookie): `Set-Cookie: session=eyJzdGF0ZSI6Mn0.ZedUQw.qytddp1NZK-9nDKLvE31YujZ35g; HttpOnly; Path=/`
    3. `echo -e "GET / HTTP/1.1\r\nCookie: session=eyJzdGF0ZSI6Mn0.ZedUQw.qytddp1NZK-9nDKLvE31YujZ35g; HttpOnly; Path=/\r\n\r\n" | nc 127.0.0.1 80`
        - response (Set-Cookie): `Set-Cookie: session=eyJzdGF0ZSI6M30.ZedUuA.b3r2S_WErrYRxWOaiqSfJFJuEFk; HttpOnly; Path=/`
    4. `echo -e "GET / HTTP/1.1\r\nCookie: session=eyJzdGF0ZSI6M30.ZedUuA.b3r2S_WErrYRxWOaiqSfJFJuEFk; HttpOnly; Path=/\r\n\r\n" | nc 127.0.0.1 80`
        - response: the flag
- *level 39*: just send 1 single request, Python will do the rest for us
