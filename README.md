# Status - testowanie!!!

# eSterownik.pl v3.5 - Plugin dla systemu Domoticz
Dodatek zapewnia integrację z eSterownik.pl, sterownikiem przeznaczonym do sterowania kotłów wodnych na paliwo stałe.
Informacje o sterowniku: https://esterownik.pl

# Instalacja pluginu
```
cd domoticz/plugins
git clone https://github.com/z1mEk/domoticz-eSterownik_v3.5.git eSterownik35
```
# Konfiguracja pluginu

| Parametr   | Wartość domyślna | Opis                           |
| ---------- | ---------------- | ------------------------------ |
| Adres IP   | 192.168.1.1      | Adres IP strownika             |
| Port       | 80               | Port sterownika                |
| Użytkownik | root             | Użytkownik sterownika          |
| Hasło      | root             | Hasło użytkownika              |
| ID urządzenia | 0             | Identyfikator sterownika       |
| Rejestry danych | tkot_value,t,Temp. kocioł;tpow_value,t,Temp. powrotu;tpod_value,t,Temp. podajnika;tcwu_value,t,Temp. CVU;twew_value,t,Temp. wewnętrzna;tzew_value,t,Temp. zewnętrzna;tsp_value,t,Temp. spalin;fuel_level,p,Poziom paliwa | Konfiguracja urządzeń według rejestrów eCoal.pl. Rejestry oddzielone są średnikami. Każdy rejestr posiada trzy właściwości rozdzielone przecinkami w formacie: atrybut,typ danych,nazwa rejestru. Nazwa rejestru będzie wyświetlana jako nazwa urządzenia w Domoticzu |
| Częstotliwość odczytu | 300   | Interwał odczytu danych z urządzenia podany w sekundach |
| Debug      | Nie              | Tryb zapisu zdarzeń do logu    |

## Dostępne atrybuty

| Atrybut    | Opis                                         |
| ---------- | ---------------------------------------------|
| tkot_value | temperatura zasilania (temperatura na kotle) |
| tpow_value | temperatura powrotu                          |
| tpod_value | temperatura podajnika                        |
| tcwu_value | temperatura ciepłej wody użytkowej           |
| twew_value | temperatura wewnętrzna                       |
| tzew_value | temperatura zewnętrzna                       |
| t1_value   | temperatura czujnika dodatkowego nr 1        |
| t2_value   | temperatura czujnika dodatkowego nr 2        |
| tsp_value  | temperatura spalin                           |
| fuel_level | poziom paliwa                                |

## Typy danych
| Typ | Typ urządzenia Domoticz | Jednostka | Zakładka Domoticz |
| :---: | -----------| :----: | -----|
| t | Temperatura | ℃ | Temperatura |
| p | Wartość procentowa | % | Użytkowe |
| b | Ciśnienie | bar | Użytkowe |
| c | Custom | (etykieta AXIS)  | Użytkowe |

# Opis komunikacji
Komunikacja ze sterownikiem odbywa się poprzez wywołanie metody GET dla CGI sterownika. Odpowiedź sterownika jest w formacie XML.

## Format adresu URL z zapytaniem o wartości parametrów
```
http://IP:PORT/getregister.cgi?device=0&tkot_value&tpow_value...
```
## Format odpowiedzi
```xml
<?xml version="1.0" encoding="UTF-8"?>
<cmd status="ok">
   <device id="0">
      <reg vid="0" tid="tkot_value" v="64.20" min="-50.00" max="120.00" />
      <reg vid="0" tid="tpow_value" v="57.06" min="-50.00" max="120.00" />
      <reg vid="0" tid="tpod_value" v="47.12" min="-50.00" max="120.00" />
      <reg vid="0" tid="tcwu_value" v="60.33" min="-50.00" max="120.00" />
      <reg vid="0" tid="twew_value" v="23.95" min="-50.00" max="120.00" />
      <reg vid="0" tid="tzew_value" v="6.48" min="-50.00" max="120.00" />
      <reg vid="0" tid="t1_value" v="29.60" min="-50.00" max="120.00" />
      <reg vid="0" tid="t2_value" v="27.34" min="-50.00" max="120.00" />
      <reg vid="0" tid="tsp_value" v="109.38" min="-50.00" max="600.00" />
   </device>
</cmd>
```
