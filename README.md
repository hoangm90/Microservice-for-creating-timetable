# Microservice-for-creating-timetable
The source code for a microservice using graph coloring algorithm to create timetables

Mikroslužbu spustíme příkazem „docker-compose up“ v rozhraní příkazového řádku<br/><br/>
Adresa URL jednoduchého uživatelského rozhraní je „http://127.0.0.1:5003/“ <br/><br/>
Způsob připojení k serveru:
+ metodou POST přes cestu „/api/makeplan“
+ prostřednictvím WebSocket přes cestu „/api/ws“

Vstupní data: ve formátu JSON, obsahující 5 páry klíč-hodnota:
+ „startDate“: slovník (dict) určující první datum v rozvrhu, tento pár klíče a hodnoty je volitelný. Pokud nebude uvedeno, první datum je 1. října 2021.
+ „events“: seznam (list) všech přednášek je třeba naplánovat.
+ „teachers“: seznam (list) všech učitelů.
+ „groups“: seznam (list) všech studijních skupin.
+ „classrooms“: seznam (list) všech učeben.

Hodnota klíče „startDate“ je slovník (dict), který obsahuje 3 páry klíč-hodnota:
+ klíč „year“ s hodnotou je celé číslo (int) udávající rok počátečního data,
+ klíč „month“ s hodnotou je celé číslo (int) udávající měsíc počátečního data,
+ klíč „day“ s hodnotou je celé číslo (int) udávající den počátečního data.

Hodnotou klíče „events“ je seznam (list) obsahující všechny přednášky, každá položka tohoto seznamu představuje jednu přednášku. Každá položka seznamu je slovník (dict) obsahující 11 párů klíč-hodnota:
+ „id“: ID přednášky (int nebo str),
+ „groupsIds“: seznam (list) ID všech studijních skupin, které se musí zúčastnit této přednášky, každá položka je ID jedné studijní skupiny (int nebo str),
+ „groupsNames“: seznam (list) jmen všech studijních skupin, které se musí této přednášky zúčastnit, každá položka je název jedné studijní skupiny (str), 
+ „teachersIds“: seznam (list) ID všech učitelů vyučujících tuto přednášku, každá položka je ID jednoho učitele (int nebo str),
+ „teachersNames“: seznam (list) jmen všech učitelů vyučujících tuto přednášku, každá položka je jméno jednoho učitele (str),
+ „classroomsIds“: seznam (list) ID dostupných učeben pro tuto přednášku, každá položka je ID jedné učebny (int nebo str),
+ „classroomsNames“: seznam (list) jmen dostupných učeben pro tuto přednášku, každá položka je název jedné učebny (str),
+ „subjectId“: ID předmětu (int nebo str), kterému tato přednáška patří, tento pár je volitelný,
+ „subjectName“: název předmětu (str), kterému tato přednáška patří, tento pár je volitelný,
+ „topicId“: ID tématu této přednášky (int nebo str), tento pár je volitelný,
+ „topic“: název tématu této přednášky (str), tento pár je volitelný.

Hodnota klíče „teachers“, „groups“ a „classrooms“ má stejnou strukturu. Každá z těchto hodnot je seznam (list) obsahující všechny učitele nebo všechny studijní skupiny nebo všechny učebny univerzity. Každá položka seznamu je slovník (dict) představující jednoho učitele (jednu studijní skupinu, jednu učebnu). Každá položka obsahuje 2 páry klíč-hodnota:
+ „id“: ID tohoto učitele (této studijní skupiny, této učebny) (int nebo str),
+ „name“: jméno tohoto učitele (této studijní skupiny, této učebny) (str).

Příklad vstupních dat: <br />
{ <br />
    "startDate": {"year": 2021, "month": 12, "day": 22}, <br />
    "events": [ <br />
    {"id": "771BBE8",  <br />
    "subjectId": 336, <br />
    "subjectName": "Letecké informační systémy", <br />
    "topic": "9. Specifika instalace leteckého informačního systému", <br />
    "topicId": 389, <br />
    "groupsIds": ["6593E980-7819-11EB-9A9C"],<br />
    "groupsNames": ["22-2KIT-C"],<br />
    "classroomsIds": [18], <br />
    "classroomsNames": ["Č1/108"], <br />
    "teachersIds": [1000],<br />
    "teachersNames": ["Novák, Jan"]}<br />
    ],<br />
    "teachers": [<br />
    {"id": 1000, "name": "Novák, Jan"}<br />
    ],<br />
    "groups": [<br />
    {"id": "6593E980-7819-11EB-9A9C", "name": "22-2KIT-C"}<br />
    ],<br />
    "classrooms": [<br />
    {"id": 18, "name": "Č1/108"}<br />
 ]}

Výstupní data: ve formátu JSON, obsahující 4 páry klíč-hodnota:
+ „events“: seznam (list) všech plánovaných přednášek.
+ „teachers“: seznam (list) všech učitelů.
+ „groups“: seznam (list) všech studijních skupin.
+ „classrooms“: seznam (list) všech učeben.

Seznam všech učitelů, seznam všech studijních skupin a seznam všech učeben ve výstupu je stejný jako ve vstupních datech. 
Výstupní seznam přednášek má určité odlišnosti od vstupního seznamu přednášek. První rozdíl je v tom, že každá položka výstupního seznamu přednášek obsahuje nejen 11 párů klíč-hodnota jako položky ve vstupním seznamu, ale obsahuje také 4 nových párů klíč-hodnota:
+ „startTime“: slovník (dict) udávající čas začátku přednášky. Slovník má 2 páry klíč-hodnota, první klíč je „hours“ s hodnotou udávající počáteční hodinu (int), druhý klíč je „minutes“ s hodnotou udávající počáteční minutu (int).
+ „endTime“: slovník (dict) udávající čas ukončení přednášky. Slovník má 2 páry klíč-hodnota, první klíč je „hours“ s hodnotou označující koncovou hodinu (int), druhý klíč je „minutes“ s hodnotou označující koncovou minutu (int).
+ „dateCode“: datum konání přednášky (str) ve formátu „rrrr-MM-dd“.
+ „date“: slovník (dict) udávající datum konání přednášky. Slovník má 3 páry klíč-hodnota, první klíč je „day“ s hodnotou udávající den konání (int), druhý klíč je „month“ s hodnotou udávající měsíc konání (int), třetí klíč je „year“ s hodnotou udávající rok konání (int).

Druhý rozdíl mezi výstupním seznamem přednášek a vstupním seznamem přednášek je v tom, že byla upravena hodnota klíče „classroomsIds“ a hodnota klíče „classroomsNames“. Hodnoty těchto klíčů ve výstupním seznamu jsou pouze ID a název učebny přiřazené k této přednášce, namísto všech možných učeben:
+ „classroomsIds“: seznam (list), jehož položkou je ID učebny přiřazené k této přednášce (int nebo str),
+ „classroomsNames“: seznam (list), jehož položkou je název učebny přiřazené k této přednášce (str).

Příklad jedné položky výstupního seznamu přednášek:<br />
    {<br />
    "id":"771BBE8",<br />
    "startTime":{"hours":16,"minutes":20},<br />
    "endTime":{"hours":17,"minutes":50},<br />
    "dateCode":"2021-10-06",<br />
    "date":{"day":6,"month":10,"year":2021},<br />
    "subjectId":336,<br />
    "subjectName":"Letecké informační systémy",<br />
    "topic":"9. Specifika instalace leteckého informačního systému",<br />
    "topicId":389,<br />
    "groupsIds":["6593E980-7819-11EB-9A9C"],<br />
    "groupsNames":["22-2KIT-C"],<br />
    "classroomsIds":[18],<br />
    "classroomsNames":["Č1/108"],<br />
    "teachersIds":[1000],<br />
    "teachersNames":["Novák, Jan"],<br />
    }
