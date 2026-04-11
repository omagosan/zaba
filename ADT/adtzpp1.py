import os
from dataclasses import dataclass
from collections import defaultdict

@dataclass
class Record:
    time: int
    id_cust: int

def load_data(data_path: str, city: str, shop: str, day: str = "1-Mon") -> \
        dict[str, list[Record]] | None:
    """ Funkce načte data z daného souboru a vrátí je jako slovník.
    Klíčem je název checkpointu a hodnotou je list záznamů.

    Args:
        data_path (str): cesta k adresáři se všemi daty
        city (str): název města, které chceme načíst
        shop (str): název obchodu, který chceme načíst
        day (str, optional): Konkrétní den, který chceme načíst. Defaults to "1-Mon".

    Returns:
        dict[str, list[Record]] | None: slovník s načtenými daty nebo None pokud soubor neexistuje
    """

    city_data: dict[str, list[Record]] = {}

    print("loading", city)

    shop_path = os.path.join(data_path, city, day, f"{shop}.txt")
    if not os.path.exists(shop_path):
        print("soubor neexistuje", shop_path)
        return None

    with open(shop_path, "r", encoding="utf8") as fd:
        _ = fd.readline()  # skip header

        lines = fd.readlines()
        for line in lines:
            clean_line = line.replace("\n", "")  # remove newline character

            spl = clean_line.split(";")
            try:
                r = Record(int(spl[0]), int(spl[2]))
                key = spl[1]
                if key not in city_data:
                    city_data[key] = []
                city_data[key].append(r)
            except ValueError:
                print("chyba v souboru ValueError neocekavana hodnota", shop_path, "\n", line)
                continue
            except IndexError:
                print("chyba v souboru IndexError neocekavany pocet hodnot", shop_path, "\n", line)
                continue

    return city_data

def get_passed_set(data: dict[str, list[Record]], key_words: list[str]) -> set[int]:
    """Funkce vrátí množinu zákazníků, kteří prošli alespoň jedním z checkpointů s prefixem
    předaných jako key_words. Do funkce tedy nevstupuje celé jméno checkpointu ale pouze
    jeho prefix (např. vege místo vege_1).

    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data
        key_words (list[str]): prefixové označení checkpointů, které chceme sledovat

    Returns:
        set[int]: Funkce vrací množinu identifikačních čísel zákazníků.
    """
    customers: set[int] = set()

    for k, d in data.items():
        # Díky prefixování klíče checkpointu (vege_1, vege_2, ...) můžeme snadno zjistit,
        # zda checkpoint obsahuje některé z klíčových slov.
        # Díky tomu můžeme např. snadno posčítat zákazníky, kteří prošli jakýmkoli vege_X.

        d_ckpt_gen = k.split("_")[0]  # vege_1 -> vege
        if d_ckpt_gen in key_words:
            for r in d:
                customers.add(r.id_cust)

    return customers

def filter_data_time(data: dict[str, list[Record]], cond_time: int) -> dict[str, list[Record]]:
    """Funkce vrátí data omezená na záznamy s časem menším nebo rovným než je cond_time.
    Args:
        data (dict[str, list[Record]]): data načtená z datového souboru funkcí load_data
        cond_time (int): časový limit v sekundách
    Returns:
        dict[str, list[Record]]: vrací data omezená na záznamy s časem menším nebo rovným cond_time.
    """
    ret: dict[str, list[Record]] = defaultdict(list)

    for k, d in data.items():
        for r in d:
            if r.time <= cond_time:
                ret[k].append(r)
            else:
                # Protože jsou data seřazená podle času, můžeme v momentě, kdy narazíme
                # na záznam s vyšším časem, cyklus ukončit.
                break

    return ret

def get_q_size(data: dict[str, list[Record]], seconds: int) -> int:
    """Funkce vrátí velikost fronty v daném čase.
    Velikost fronty je dána počtem zákazníků, kteří prošli některým z checkpointů
    (vege, frui, meat) a ještě neprošli pokladnou.
    """
    data_time = filter_data_time(data, seconds)

    # Zákazníci, kteří prošli některým z checkpointů (vege, frui, meat)
    # Tito zákazníci jsou potenciálně ve frontě před pokladnou
    passed_set = get_passed_set(data_time, ["vege", "frui", "meat"])

    # Zákazníci, kteří již prošli pokladnou
    # Tito zákazníci již frontu opustili
    checkout_set = get_passed_set(data_time, ["final-crs"])

    # Velikost fronty je rozdíl mezi množinou přišlých a množinou odešlých zákazníků
    return len(passed_set - checkout_set)

def histogram(data: dict[str, list[Record]]) -> None:
    for i in range(8, 20):
        print(f"{i}:00 {get_q_size(data, i * 3600)}")

def compute_hourly_usage_per_checkpoint(data: dict[str, list[Record]]) -> dict[str, list[int]]:
    """
    Určí, kolik lidí v průběhu každé hodiny prošlo skrz každý checkpoint.

    Pro každou hodinu dne (0-23hod) se počítají všechny příchody mezi
    HH:00:01 a HH+1:00:00 včetně obou krajních bodů.
    """
    stats = {ckpt: [] for ckpt in data}


    cas = 0
    for records in data.values():
        for j in records:
            if j.time > cas:
                cas = j.time

    hodina = 0
    while hodina <= cas:
        fronta = get_q_size(data, hodina)
        
        print(f"počet zákazníků ve frontě: {len(fronta)} ({fronta}) za {hodina} s/{hodina // 3600} hodin")
        hodina = hodina + 3600
        
        for ckpt, time in stats:
            if time not in stats:
                stats[ckpt] = []

                
        
    



    return stats

def find_most_used_checkpoint_at_hour(hourly_result: dict[str, list[int]], hour: int) -> str:
    """
    Pro danou hodinu (hour) nalezne checkpoint s nejvíce průchody zákazníků.
    """
    most_customers = 0
    checkpoint_name = ""




    return checkpoint_name

def main() -> None:
    # funkci main si můžete uzpůsobit jak chcete,
    # slouží pouze pro vyzkoušení programu, nikoliv hodnocení
    data_path = "output"
    city = "Plzeň"
    shop = "shop_a"

    data = load_data(data_path, city, shop)

    if not data:
        print("Data could not be loaded.")
        return

    result = compute_hourly_usage_per_checkpoint(data)

    print("vytíženost checkpointů v 15hod:")
    for ckpt, values in result.items():
            print(f"{ckpt} - {values[15]} lidí")

    most_congested = find_most_used_checkpoint_at_hour(result, 15)
    print(f"Nejvytíženějším je {most_congested}")

if __name__ == "__main__":
    main()
