# Progetto ICON a.a. 21/22

## Presentazione
Questa è la repository per l'esame Ingegneria della Conoscenza, a.a. 21/22 - Università di Bari.

Il progetto contiene:

1. Un sistema esperto per la raccolta e l'elaborazione dei dati al fine di scegliere un set di indumenti consono alla giornata
2. I risultati vengono elaborati accedendo a delle informazioni salvate in un'ontologia
3. Nel caso di una emergenza meteo viene calcolata la probabilità di prendersi un malanno attraverso una rete bayesiana

Studente:
* De Cosmis Ivan, 716486, i.decosmis@studenti.uniba.it

## Installare requisiti
Installare tutte le librerie necessarie dal file requisiti.txt con il comando da console nella directory del file ```requisiti.txt```:

```pip install -r requisiti.txt```

Se python in windows restituisce un errore provare con:

```python.exe -m pip install -r requisiti.txt```

Nel caso del seguente errore in seguito all'installazione delle librerie:
```
  File "percorsoAlFile/__init__.py", line 16, in <module>
    class frozendict(collections.Mapping):
AttributeError: module 'collections' has no attribute 'Mapping'
```

1. Aprire il file: \_\_init_\_\.py
2. Trovare la riga: class frozendict(collections.Mapping)
3. Modificarla in: frozendict(collections.abc.Mapping)

Spiegazione al link: https://stackoverflow.com/questions/70749690/attributeerror-module-collections-has-no-attribute-mapping

## Avviare sistema
  Per avviare il sistema utilizzare il comando:
  ```python main.py```
  dalla directory del file ```main.py```

