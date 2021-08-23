"""
ISC License

Copyright (c) 2021, Koviubi56

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
"""
from time import sleep

if __name__ == "__main__":
    DEFAULT = "log.log"
    repeat = False
    fnotfound = False
    print("\n" * 80)
    user = input(f"File ({DEFAULT})> ")
    user = DEFAULT if user == "" else user
    while True:
        try:
            with open(user) as file:
                fnotfound = False
                print("-" * 180)
                print('{:>180}'.format(user))
                print("\n" * 40)
                content = []
                for line in file:
                    # pass
                    print(line[:-1] if line.endswith("\n") else line)
                    content.append(line)
                repeat = False
            while not repeat:
                sleep(0.1)
                with open(user) as file:
                    x = file.readlines()
                    if x != content:
                        repeat = True
        except FileNotFoundError:
            if not fnotfound:
                print('{:>180}'.format('File not found. Retry after 0.5s'))
                fnotfound = True
            sleep(0.5)
