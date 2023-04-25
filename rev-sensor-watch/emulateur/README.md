# Instructions

Simply run

```bash
$ docker-compose up --build
```

or

```bash
$ docker build -f Dockerfile . -t emulateur
$ docker run --rm -p 8000:8000 --name emulateur emulateur
```

Then, visit:
http://localhost:8000/watch.html
