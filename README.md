# SemanticDict
SemanticDict provides a natural pythonic dictionary implementation that promotes collisions between semantically similar keys.

Say you add the key-value pair `"Hello World I am Jack": 53` to a dictionary. In a normal dictionary if you then perform a lookup for `Hello World - Jack` a `KeyError` will be raised. With `SemanticDict`, the dictionary automatically understands that the two have similar meanings and would return `53` instead of a `KeyError`

### Usage
```python
sd = SemanticDict()
sd["Hello World I am Jack"] = 53
sd["This is SemanticDict"] #KeyError
sd["Hello World - Jack"] #53
```

### Threshold
The threshold argument (`sd  = SemanticDict(threshold = 0.2)`) is used to set how similar two keys need to be to collide.
> Greater threshold = less collisions

### Overwrite
The overwrite argument (`sd  = SemanticDict(overwrite = True)`) is used to change the behavior of how keys-value pairs are added. When overwrite is enabled when a key-value pair is set, if a semantically similar key already exists, its value is overwritten with the new value. Normally, the new key-value pair is just added to the dictionary. 
```python
sd = SemanticDict(overwrite=True)
sd["Hello World I am Jack"] = 53
sd["This is SemanticDict"] #KeyError
sd["Hello World - Jack"] #53

sd["Hello World from Jack"] = 20
sd["Hello World I am Jack"] #20 (not 53 anymore)
```

### Limitations
- Only supports 1 `SemanticDict` per process. 
