# LEGGIMI
Installare tutte le librerie necessarie dal file requirements.txt

Nel caso del seguente errore in seguito all'installazione delle librerie: \n
  File "percorsoAlFile\__init__.py", line 16, in <module>
    class frozendict(collections.Mapping):
AttributeError: module 'collections' has no attribute 'Mapping'

1. Aprire il file: __init__.py
2. Trovare la riga: class frozendict(collections.Mapping)
3. Modificarla in: frozendict(collections.abc.Mapping)

Spiegazione al link: https://stackoverflow.com/questions/70749690/attributeerror-module-collections-has-no-attribute-mapping

