# Data models (work in progress)

```mermaid
---
title: ER diagram
---
erDiagram

	Route ||--o{ Connection : "runs on"
	Connection ||--o{ Arrival : ""
	Arrival }o--|| Station : "stops at"
```


**Route**

| column name | description | example |
|-------------|-------------|----------|
| `id` | primary key | `1` |
| `name` | route name | '376', 'M1' |
| `connections` | one-to-many relation to `Connection` | |


**Connection**

| column name | description | example |
|-------------|-------------|----------|
| `id` | primary key | `1` |
| `name` | name for this connection | '376-A', 'M1 weekend' |
| `departure_cron` | the time when route departs | '5,30 6-22 * * Wed' |
| `disabled` | field showing if the connection is not used | 'True' |
| `waypoints` | one-to-many relation to `Waypoint` |  |
| `route` | many-to-one relation to `Route` |  |


**Waypoint**

| column name | description | example |
|-------------|-------------|----------|
| `id` | primary key | `1` |
| `station` | many-to-one relation to `Station` | 'Politekhnichnyi instytut' |
| `connection` | many-to-one relation to `Connection` | |
| `trip_time` | time in seconds from departure to station | '60', '3850' |
| `disabled` | field showing if the waypoint is not used | 'True' |


**Station**

| column name | description | example |
|-------------|-------------|----------|
| `id` | primary key | `1` |
| `name` | station full name | 'Politekhnichnyi instytut' |
| `city` | city where `Station` is located | 'Kyiv' |
| `address` | location of a station | 'Peremohy Ave, 35' |
| `latitude` | latitude of a station | 48.8566 |
| `longitude` | longitude of a station | 2.3522 |
| `waypoints` | one-to-many relation to `Waypoint` |  |


### Route examples

#### №1

```mermaid
flowchart LR
	Kyiv --> Lviv
```
Route has only two stations, for example from Kyiv to Lviv that 
departures at 11:30 on 1, 10 and 20 day of month.

**Route**

| id | name | connections |
|-------------|----------|----------|
| 1 | Kyiv-Lviv | connection 1 |

**Connection**

| id | name | departure_cron | first_station | disabled | waypoints | route | 
|-------------|-------------|----------|----------|----------|----------|
| 1 | 'Kyiv-Lviv' | '30 11 1,10,20 * * ' | False | waypiont 1 | route 1 | 

**Waypoint**

| id | station | connection | trip_time | disabled |
|-------------|-------------|----------|----------|----------|
| 1 | station 1 | connection 1 | 0 | False |
| 2 | station 2 | connection 1 | 492 | False |

**Station**

| id | name | city | latitude | longitude | waypoints |
|-------------|-------------|-------------|-------------|-------------|-------------|
| 1 | 'Kyiv Central Bus Station' | Kyiv | 'Nauky Ave, 1/2' | 50.406569| 30.520128 | waypoint 1 | 
| 2 | 'Lviv Bus Station' | Lviv | 'Dvirtseva Square, 1' | 49.840334 | 23.995756 | waypoint 2 |


#### №2

```mermaid
flowchart LR
	Kyiv --> Zhytomyr
	Zhytomyr --> Rivne
	Rivne --> Lviv
```

```mermaid
flowchart RL

	Lviv --> Rivne
	Rivne --> Zhytomyr
	Zhytomyr --> Kyiv
```

Route has 4 stations: Kyiv, Zhytomyr, Rivne, Lviv. It departures every 
day at 7:00 and 19:00 from Kyiv and at 9:00 and 21:00 from Lviv.

**Route**

| id | name | connections |
|-------------|----------|----------|
| 1 | Kyiv-Lviv | connection 1, connection 2 |

**Connection**

| id | name | departure_cron | disabled | waypoints | route | 
|-------------|-------------|----------|----------|----------|----------|
| 1 | 'Kyiv-Lviv' | '0 7,19 * * * ' | False | waypoint 1, waypoint 2, waypoint 3 | route 1 |
| 2 | 'Lviv-Kyiv' | '0 9,21 * * * ' | False | waypoint 4, waypoint 5, waypoint 6 | route 1 |

**Waypoint**

| id | station | connection | trip_time | disabled |
|-------------|-------------|----------|----------|----------|
| 1 | station 1 | connection 1 | 0 | False |
| 2 | station 2 | connection 1 | 154 | False |
| 3 | station 3 | connection 1 | 301 | False |
| 4 | station 4 | connection 1 | 495 | False |
| 5 | station 3 | connection 2 | 207 | False |
| 6 | station 2 | connection 2 | 350 | False |
| 7 | station 1 | connection 2 | 488 | False |

**Station**

| id | name | city | latitude | longitude | waypoints |
|-------------|-------------|-------------|-------------|-------------|-------------|
| 1 | 'Kyiv Central Bus Station' | Kyiv | 'Nauky Ave, 1/2' |  50.406569| 30.520128 | waypoint 1, waypoint 7 | 
| 2 | 'Zhytomyr Bus Station' | Zhytomyr | 'Kyivska St, 93' | 50.268499 | 28.692229 | waypoint 2, waypoint 6 |
| 3 | 'Rivne Bus Station' | Rivne | 'Kyivska St, 40' | 50.614749 | 26.282753 | waypoint 3, waypoint 5|
| 4 | 'Lviv Bus Station' | Lviv | 'Dvirtseva Square, 1' | 49.840334 | 23.995756 | waypoint 4 |


#### №3

```mermaid
flowchart LR
	Kyiv --> Zhytomyr
	Zhytomyr --> Rivne
	Rivne --> Lviv
```

```mermaid
flowchart LR

	Lviv --> Ternopil
	Ternopil --> Vinnytsya
```

```mermaid
flowchart LR

	Vinnytsya --> Zhytomyr
	Zhytomyr --> Kyiv
```

Route has 6 stations: Kyiv, Zhytomyr, Rivne, Lviv, Ternopil, Vinnytsya. 
It departures every day at 7:00 and 19:00 from Kyiv, at 9:00 and 
21:00 from Lviv and at 8:00 and 20:00 from Vinnytsya.

**Route**

| id | name | connections |
|-------------|----------|----------|
| 1 | 567 | connection 1, connection 2, connection 3 |

**Connection**

| id | name | departure_cron | disabled | waypoints | route | 
|-------------|-------------|----------|----------|----------|----------|----------|
| 1 | 'Kyiv-Lviv' | '0 7,19 * * * ' | False | waypoint 1, waypoint 2, waypoint 3 | route 1 |
| 2 | 'Lviv-Vinnytsya' | '0 9,21 * * * ' | False | waypoint 4, waypoint 5 | route 1 |
| 3 | 'Vinnytsya-Kyiv' | '0 8,20 * * * ' | False | waypoint 6, waypoint 7 | route 1 |

**Waypoint**

| id | station | connection | trip_time | disabled |
|-------------|-------------|----------|----------|----------|
| 1 | station 1 | connection 1 | 0 | False |
| 2 | station 2 | connection 1 | 154 | False |
| 3 | station 3 | connection 1 | 301 | False |
| 4 | station 4 | connection 1 | 495 | False |
| 5 | station 4 | connection 2 | 0 | False |
| 6 | station 5 | connection 2 | 119 | False |
| 7 | station 6 | connection 2 | 328 | False |
| 8 | station 6 | connection 3 | 0 | False |
| 9 | station 2 | connection 3 | 118 | False |
| 10 | station 1 | connection 3 | 240 | False |

**Station**

| id | name | city | latitude | longitude | waypoints |
|-------------|-------------|-------------|-------------|-------------|-------------|
| 1 | 'Kyiv Central Bus Station' | Kyiv | 'Nauky Ave, 1/2' | 50.406569| 30.520128 | waypoint 1, waypoint 10 | 
| 2 | 'Zhytomyr Bus Station' | Zhytomyr | 'Kyivska St, 93' | 50.268499 | 28.692229 | waypoint 2, waypoint 9 |
| 3 | 'Rivne Bus Station' | Rivne | 'Kyivska St, 40' | 50.614749 | 26.282753 | waypoint 3 |
| 4 | 'Lviv Bus Station' | Lviv | 'Dvirtseva Square, 1' | 49.840334 | 23.995756 | waypoint 4, waypoint 5 |
| 5 | 'Ternopil Bus Station' | Ternopil | 'Torhovytsia St, 7' | 49.544143 | 25.596867 | waypoint 6 |
| 6 | 'Vinnytsya Central Bus Station' | Vinnytsya | 'Kyivs'ka St, 8' | 49.236517 | 28.483181 | waypoint 7, waypoint 8 |


#### №4

```mermaid
flowchart
	Kyiv --> Zhytomyr
	Zhytomyr --> Rivne
	Rivne --> Lviv

	Lviv --> Ternopil
	Ternopil --> Vinnytsya

	Vinnytsya --> Kyiv
```

Route is circular and has 6 stations: Kyiv, Zhytomyr, Rivne, Lviv, 
Ternopil, Vinnytsya. It departures every day at 7:00 and 19:00 from 
Kyiv.

**Route**

| id | name | connections |
|-------------|----------|----------|
| 1 | '567' | connection 1 | 

**Connection**

| id | name | departure_cron | disabled | waypoints | route | 
|-------------|-------------|----------|----------|----------|----------|----------|
| 1 | '567' | '0 7,19 * * * ' | False | waypoint 1, waypoint 2, waypoint 3, waypoint 4, waypoint 5, waypoint 6, waypoint 7 | route 1 |

**Waypoint**

| id | station | connection | trip_time | disabled |
|-------------|-------------|----------|----------|----------|
| 1 | station 1 | connection 1 | 0 | False |
| 2 | station 2 | connection 1 | 154 | False |
| 3 | station 3 | connection 1 | 301 | False |
| 4 | station 4 | connection 1 | 495 | False |
| 5 | station 5 | connection 1 | 614 | False |
| 6 | station 6 | connection 1 | 823 | False |
| 7 | station 1 | connection 1 | 1081 | False |

**Station**

| id | name | city | latitude | longitude | waypoints |
|-------------|-------------|-------------|-------------|-------------|-------------|
| 1 | 'Kyiv Central Bus Station' | Kyiv | 'Nauky Ave, 1/2' | 50.406569| 30.520128 | waypoint 1, waypoint 7 | 
| 2 | 'Zhytomyr Bus Station' | Zhytomyr | 'Kyivska St, 93' | 50.268499 | 28.692229 | waypoint 2 |
| 3 | 'Rivne Bus Station' | Rivne | 'Kyivska St, 40' | 50.614749 | 26.282753 | waypoint 3|
| 4 | 'Lviv Bus Station' | Lviv | 'Dvirtseva Square, 1' | 49.840334 | 23.995756 | waypoint 3 |
| 5 | 'Ternopil Bus Station' | Ternopil | 'Torhovytsia St, 7' | 49.544143 | 25.596867 | waypoint 5 |
| 6 | 'Vinnytsya Central Bus Station' | Vinnytsya | 'Kyivs'ka St, 8' | 49.236517 | 28.483181 | waypoint 6 |