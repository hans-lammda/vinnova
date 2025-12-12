# Vinnova

<details>
<summary><strong>Innehåll</strong></summary>

- [Kravspecifikation](#krav)
- [ChatGPT](#ChatGPT)
- [Exekvering](#exekvering)
- [Todo](#todo)

</details>

## Krav
Jag vill veta vilka projekt som Vinnova beviljat medel. 

Informationen finns att nå via Vinnovas projektdatabas

[https://data.vinnova.se/api/projekt/](https://data.vinnova.se/api/projekt/)



```csv
Diarienummer,Ärenderubrik,BeviljatBidrag,ProjektStart,ProjektSlut,Status,Projektkoordinator
2015-02516,CEBOT - Certificate Enrollment,2168728,2015-09-01,2017-06-30,Avslutat,RISE SICS AB
```


## Prompt till Chat-GPT 
Detta är vad som kallas [Vibecodning](https://www.advania.se/ordforradet/vibe-coding) 

- Jag har ett behov, dvs mina krav
- Jag vill gärna ha det i Python, eftersom det jag använder mest 
- Jag vill kunna specificera följande 
  - Intervall, dvs första och sista datum ur projektdatabasen
  - Formatet ska vara csv, lätt att ta in i Excel 

Istället för att hålla på med design och implementation enligt den gamla skolan, 

skriver man direkt till CHAT-GPT eller något annat liknande AI-verktyg. 



```prompt

Jag vill hämta data från Vinnovas databas via deras API
specifikt alla beviljade projekt
Filtrera på tidsintervall
t.ex. mellan 2015–2025
med möjlighet att justera intervallet

Bygga ett Python-program med CLI

argument som:
--from-year 2015-01-01
--to-year 2025-12-31
--output data.csv 

```

## Exekvering 

De som jobbar med öppen källkod, förväntar sig följande 
- Koden finns på Github eller något liknande Repository
- En README file, som du just nu läser
- Källkoden (cli.py)
- Makefile ( Denna tar hand om allt krångel för att bygga, testa och exekvera programmet cli.py )



Makefile 
```make
get:
        python3 cli.py --from-date 2015-01-01 --to-date 2025-12-31 --output data.csv
```
### Exekvering 
```bash
$ make get
  python3 cli.py --from-date 2015-01-01 --to-date 2025-12-31 --output data.csv

````

## Todo

Det är vanligt att man vill hitta på nya saker, men sedan kanske man inte har tid implementera detta. 
Då skriver man en önskelista, har man tur, hör någon av sig och då kan man få ett betalt uppdrag. 
Just detta lilla program är lätt att ändra, vidare har jag talat om hur CHAT-GPT gjort jobbet, det är därför osannolikt att jag får ett uppdrag. 
Det är tveksamt om det uppfyller kriterierna för patent, eftersom det är låg uppfinningshöjd. 

### Vidareutveckling 

#### Projektpartner 
Det är endast koordinatorn som presenteras, inte övriga projektpartners. Det vore intressant att veta om det är en mix av 
- Stora företag
- Små företag
- Akademiska institutioner
- Offentlig sektor
#### Mapping av företag 
Forskningsinstitur som [RISE](https:ri.se) består av dotterbolag, dessa borde listas i en fil och sedan presenteras som endast RISE. 

#### Koppling till rapporter
På senare tid ställer Vinnova krav på lärdomsrapporter, det vore bra om varje projekt hade en länk, även om projektet havererade så är även det en  nyttig lärdom. 

#### Koppling till patent 
Man kan tycka vad man vill om patent, men till skillnad från rapporter som har en tendens att försvinna, så kommer ett patent finnas tillgängligt tills dess att solen brinner upp. 




  








