# SemanticDict
SemanticDict provides a natural pythonic dictionary implementation that promotes collisions between semantically similar keys.

Say you add the key-value pair `"Hello World I am Jack": 53` to a dictionary. In a normal dictionary if you then perform a lookup for `Hello World - Jack` a `KeyError` will be raised. With SemanticDict, the dictionary automatically understands that the two have similar meanings and would return `53` instead of a `KeyError`

### Use Case
This project was designed to assist in caching LLM responses. Everytime a request (query) is made it first checks the prompt against the SemanticDict where key-value pairs corresponsd to prompts-responses. If a similar prompt is found, the response is returned. If not, the request is made to the LLM API and then the new key-value can be added to the SemanticDict. 

```python
try:
    response = semantic_dict[prompt]
except KeyError:
    response = llm(prompt)
    semantic_dict[prompt] = response
```

### Usage
```python
sd = SemanticDict()
sd["Hello World I am Jack"] = 53
sd["This is SemanticDict"] #KeyError
sd["Hello World - Jack"] #53
```

### Threshold
The threshold argument (`SemanticDict(threshold=0.2)`) is used to set how similar two keys need to be to collide.
> greater threshold = keys have to be less similar to match

### Overwrite
The overwrite argument (`SemanticDict(overwrite=False)`) is used to change the behavior of how keys-value pairs are added. If overwrite is enabled (default), when a key-value pair is set, if a semantically similar key already exists, its value is overwritten with the new value. If overwrite is set to false, the new key-value pair is just added to the dictionary. 

```python
sd = SemanticDict(overwrite=True)
sd["Hello World I am Jack"] = 53
sd["Hello World - Jack"] #53

# with overwrite 
sd["Hello World from Jack"] = 20
sd["Hello World I am Jack"] #20 (not 53 anymore)

# without overwrite
sd["Hello World from Jack"] = 20
sd["Hello World I am Jack"] #53
```

### Limitations
- Only supports 1 `SemanticDict` per process. 
- Only supports `str` keys