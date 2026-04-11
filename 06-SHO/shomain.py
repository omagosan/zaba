import random
from collections import deque
from dataclasses import dataclass


@dataclass
class Worker:
    name: str
    source: deque   # Odkud beru lidi (vstupní fronta)
    dest: deque     # Kam je posílám (výstupní fronta)
    period: int     # Průměrná doba obsluhy
    spread_factor: float = 0.0  # Faktor rozptylu doby obsluhy (volitelné)
    timer: int = 0      # Odpočet času do dokončení aktuální práce


def get_delay(period: int, spread_factor: float) -> int:
    return int(random.gauss(period, period * spread_factor))



def worker_tick(worker: Worker) -> None:
    if worker.timer > 0:
        worker.timer -= 1
        return
    
    if len(worker.source) > 0:
        chosen_one = worker.source.popleft() # Vyjmutí zákazníka ze začátku fronty
        worker.dest.append(chosen_one) # Poslání tohoto zákazníka dál
        worker.timer = get_delay(worker.period, worker.spread_factor) # "Uspání" workeru po obsloužení zákazníka  


def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:
    # Přepočet sekund na hodiny a minuty
    h = time // 3600
    m = (time%3600) // 60
    s = time % 60

    format_time = f"{h:02d}:{m:02d}:{s:02d}"

    # Postupné ukládání částí řetězců k výpisu do listu
    to_print = [f"{format_time}: \t"]
    for name, q in queues:
        to_print.append(f"{name}({len(q)})")

    formatted = "->".join(to_print) # Použití metody join na spojení listu na řetězec 
    print(formatted)


def main() -> None:
    people_number = 1000
    people_in_the_city = deque(list(range(people_number)))

    # 1. Vytvoření front
    door_q = people_in_the_city
    gate_q = deque()
    vege_q = deque()
    cash_q = deque()
    final_q = deque()


    # Seznam pro výpis (jméno, fronta)
    queues_to_observe = [
        ("Door", door_q),
        ("Gate", gate_q),
        ("Vege", vege_q),
        ("Cashier", cash_q),
        ("Done", final_q)
    ]

    # Parametry simulace (střední hodnoty časů v sekundách)
    day_m = 30  # Každých 30s přijde někdo z ulice
    gate_m = 15  # Gate keeper každého odbavuje 15s
    vege_m = 45  # Vážení zeleniny trvá 45s
    final_m = 2 * 60  # Pokladna zabere 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    # Worker(jméno, zdroj, cíl, perioda, spread_factor)

    door = Worker("DoorMan", door_q, gate_q, day_m)
    gate = Worker("GateMan", gate_q, vege_q, gate_m)
    vege = Worker("VegeMan", vege_q, cash_q, vege_m, 0.2)
    cash = Worker("Cashier", cash_q, final_q, final_m, 0.1)

    workers = [door, gate, vege, cash]

    # 3. Hlavní smyčka simulace
    total_time = 7200 # 2 hodiny simulace

    for time in range(total_time):
        for worker in workers:
            worker_tick(worker) # Děláme tick "hodin" u každého workera

        if time % 60 == 0: # Každých 60 vteřin zavoláme výpis
            print_snapshot(time, queues_to_observe)

if __name__ == "__main__":
    main()