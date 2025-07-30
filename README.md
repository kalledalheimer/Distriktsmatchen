# Distriktsmatchen Resultatberäknare

Detta är ett Python-skript för att beräkna resultat för Distriktsmatchen, en ungdomsorienteringstävling mellan fyra distrikt: Värmland, Södermanland, Örebro län och Östergötland. Tävlingen består av en individuell medeldistans och en stafett, var och en med sitt eget poängsystem.

Applikationen läser in XML-resultatfiler från tävlingsarrangören, beräknar poängen enligt de definierade reglerna och presenterar slutresultatet för både individuella tävlingar och stafetter.

## Användning

För att köra skriptet, navigera till projektets rotkatalog i din terminal och använd följande kommandon:

```bash
python3 main.py [FLAGGOR]
```

### Flaggor

*   `--individual`: Beräknar endast resultat för den individuella tävlingen.
*   `--relay`: Beräknar endast resultat för stafetten.
*   `--all`: Beräknar resultat för både den individuella tävlingen och stafetten (standard om inga flaggor anges).
*   `-h`, `--help`: Visar hjälpmeddelandet och avslutar.

### Exempel

Beräkna alla resultat:
```bash
python3 main.py
```

Beräkna endast individuella resultat:
```bash
python3 main.py --individual
```

Beräkna endast stafettresultat:
```bash
python3 main.py --relay
```

## Konfiguration

Distriktsmappningen finns i `config.json`. Om distrikts-ID:n eller namnen ändras, uppdatera denna fil.

## Testning

Enhetstester finns i `tests/test_scorers.py`. För att köra testerna:

```bash
python3 -m unittest tests/test_scorers.py
```

## Licens

Detta projekt är licensierat under MIT-licensen. Se filen `LICENSE` för mer information.
