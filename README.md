# nc Alternative in python3
with colors!!

well, I was recently pentesting a small server on my pi and i found that the regular nc was very dry with literally close to no interaction and looked ugly. 
So I implemented this python based netcat, with colors.

### TODO:
1) Keyboard handling: Support for up/down arrow keys and history. 

-- As a hack, one can use rlwrap https://github.com/hanslub42/rlwrap to simulate the history file. 
2) Color customizations 
3) Bug fixes. Its a quick and dirty work, but I'd like it to be more bug free.


#### Installation
`
pip install -r requirements.txt
`

#### Usage
```
Usage: nyacat.py [OPTIONS] COMMAND [ARGS]...

  A netcat alternatives with tonnes of colors and good looking, works in
  listener mode and  connection mode

Options:
  --help  Show this message and exit.

Commands:
  client  Connection mode: nyacat client --host=0.0.0.0 --port=6969
  listen  Listener mode: nyacat listen --port=6969
 ```

you can also remove the .py extension and add it in your path, setup the #! and revoke it directly from commandline.

Feel free to make modifications and report bugs.
