# SemanticDict

Provides easy & pythonic dictionary and cache implementations that promote collisions semantically. This means that if you add a key-value pair to the dictionary and then perform a lookup on a semantically similar key it will return the same value. 

Dict: If there is no semantically similar key, raise a KeyError.

Cache: If there is no semantically similar key, add the new key-value pair to the cache.