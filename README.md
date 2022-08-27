# LEGGIMI

## Installare requisiti
Installare tutte le librerie necessarie dal file requisiti.txt con il comando:

```pip install -r requisiti.txt```

Nel caso del seguente errore in seguito all'installazione delle librerie:

  File "percorsoAlFile/\_\_init_\_\.py", line 16, in <module>
  
    class frozendict(collections.Mapping):
  
AttributeError: module 'collections' has no attribute 'Mapping'

1. Aprire il file: \_\_init_\_\.py
2. Trovare la riga: class frozendict(collections.Mapping)
3. Modificarla in: frozendict(collections.abc.Mapping)

Spiegazione al link: https://stackoverflow.com/questions/70749690/attributeerror-module-collections-has-no-attribute-mapping

### Avviare sistema

