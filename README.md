# cldx
Causal Loop Diagrams with networkx


## installation

```sh
python setup.py install
```

## Usage

```python
from cldx import CausalLoopDiagram

cld = CausalLoopDiagram()
cld = CausalLoopDiagram()
cld.add_causal_links([
    ('Birth rate of Lynx',"Lynx population", 1),
    ('Death rate of Lynx',"Lynx population", -1),
    ("Lynx population", "Food supply of Lynx", -1),
    ("Starvation of Lynx", "Death rate of Lynx", 1),
    ("Food supply of Lynx", "Starvation of Lynx", 1),
    ("Food supply of Lynx", "Birth rate of Lynx", 1),
    ])
cld.draw(loops=loops)
```
![causal loop diagram](example.png)

You can also find loops in the diagram:

```python
>>> cld.find_loops()
[{'nodes': ['Birth rate of Lynx', 'Lynx population', 'Food supply of Lynx'],
  'type': 'S'},
 {'nodes': ['Lynx population',
   'Food supply of Lynx',
   'Starvation of Lynx',
   'Death rate of Lynx'],
  'type': 'R'}]
```

