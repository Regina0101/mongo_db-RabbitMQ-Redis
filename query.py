import redis

from connect import connect
from redis_lru import RedisLRU
from models import Author, Quote




client = redis.StrictRedis(host='localhost', port=6379, password=None)
cache = RedisLRU(client)


def search_quote(cmd, value):
    cache_key = f"{cmd}:{value}"
    cached_result = cache.get(cache_key)
    if cached_result:
        print("Results from cache:")
        for result in cached_result:
            print(result)
    else:
        if cmd == "name":
            authors = Author.objects(fullname__istartswith=value)
            if authors:
                result = []
                for author in authors:
                    quotes = Quote.objects(author=author)
                    for quote in quotes:
                        result.append(f"Author: {author.fullname}, Description: {quote.quote}")
                cache.set(cache_key, result)
                for line in result:
                    print(line)
            else:
                print(f"No authors found with name containing '{value}'")
        elif cmd == "tag":
            tag_list = value.split(',')
            tags = Quote.objects(tags__in=tag_list).all()
            tag2 = Quote.objects(tags__istartswith=value).all()
            result = []
            if tags:
                for tag in tags:
                    result.append(f"Author: {tag.author.fullname}: {tag.quote}")
            elif tag2:
                for tag in tag2:
                    result.append(f"Author: {tag.author.fullname}: {tag.quote}")
            cache.set(cache_key, result)
            for line in result:
                print(line)
        else:
            print(f"Unknown command: {cmd}")


while True:
    user_input = input("Enter command(name or tag) and Author's name or tag to find quote, or 'exit' to quit: ").strip()
    if user_input.lower() == 'exit':
        print('Bye!')
        break
    try:
        cmd, value = user_input.split()
        search_quote(cmd, value)
    except ValueError:
        print("Please enter a valid command and value.")