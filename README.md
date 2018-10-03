# eCoal.pl v3.5 - Plugin dla systemu Domoticz
Dodatek zapewnia integrację z eCoal.pl, sterownikiem przeznaczonym do sterowania kotłów wodnych na paliwo stałe.
Informacje o sterowniku: https://esterownik.pl/nasze-produkty/ecoal-v35

# Instalacja pluginu
...

# Konfiguracja pluginu

| Parametr   | Wartość domyślna | Opis                           |
| ---------- | ---------------- | ------------------------------ |
| Adres IP   | 192.168.1.1      | Adres IP strownika eCoal.pl    |
| Port       | 80               | Port sterownika eCoal.pl       |
| Użytkownik | root             | Użytkownik sterownika eCoal.pl |
| Hasło      | root             | Hasło użytkownika eCoal.pl     |

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


# Wymagania
...

# Opis komunikacji

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
