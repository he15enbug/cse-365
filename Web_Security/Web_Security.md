# Web Security
- *level 5*: we can only control `query` in `SELECT username FROM users WHERE username LIKE "{query}"`. By testing, `db.execute()` can not execute more than one separate statement at once. Use `UNION ALL` to combine the result of 2 statements, the SQL statement being executed is `SELECT username FROM users WHERE username LIKE "%" UNION ALL SELECT password FROM users; --"`
- *level 6*: this time, the table name is unknown (`table_name = f"table{hash(flag) & 0xFFFFFFFFFFFFFFFF}"`). We can use a statement `SELECT name FROM sqlite_master WHERE type='table'` to figure out the table name. To know that the server is using `sqlite`, we can just cause some error, and see the error information, e.g., `sqlite3.OperationalError: ...`
- *level 7*: an obstable is that this time, it will finally finds a user using `rowid`, and only prints out the `username` column. We can use the error information to help us to figure out 1 byte of the flag each time. Specifically, the server will first select exact one user using `username` and `password`, if the query result is empty, there will be an error `Invalid 'username' or 'password'`, what we can do is to get the server to execute this query `SELECT rowid, * FROM users WHERE username="no" UNION ALL rowid, rowid, rowid FROM users WHERE password LIKE ?; --" AND password="123"`, the `?` can be something like `pwn.college{...%`, if the prefix exists, there won't be error because the query result is not empty. Otherwise, there will be an error. So we can start from `pwn.college{`, and each time, we guess 1 character, until we get ``pwn.college{...}`
- *level 8*