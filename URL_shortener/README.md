# URL shortener

### URL shortening is a technique on URL may be made substantially shorter and still direct to the required page.

<hr>

convert the URL to random 8 characters which follows "BASE62"

so it goes like this..

```python
# BASE62
def convert():
    encoding = ['a','b','c','d','e','f','g','h','i','j','k','l',
                'm','n','o','p','q','r','s','t','u','v','w','x',
                'y','z',
                'A','B','C','D','E','F','G','H','I','J','K','L',
                'M','N','O','P','Q','R','S','T','U','V','W','X',
                'Y','Z',
                '0','1','2','3','4','5','6','7','8','9']
    while True:
        new_url = ''.join(random.sample(encoding, 8))
        try:
            url = URL.objects.get(new_link=new_url)
        except:
            return new_url
```

<hr>

### experiment on postman
