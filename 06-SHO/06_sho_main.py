import random
from collections import deque
from dataclasses import dataclass



@dataclass
class Worker:
    name: str
    source: deque
    dest: deque
    period: int
    spread_factor: float = 0.0
    timer: int = 0


def get_delay(period: int, spread_factor: float) -> int:
    return int(random.gauss(period, period * spread_factor))


def worker_tick(worker: Worker) -> None:
    worker.timer -= 1

    if worker.timer <= 0:
        if len(worker.source) == 0:
            return

        customer = worker.source.popleft()
        worker.dest.append(customer)
        worker.timer = get_delay(worker.period, worker.spread_factor)


def print_snapshot(time: int, queues: list[tuple[str, deque]]) -> None:
    print(end=f"{time//3600:02d}:{(time%3600)//60:02d}:{time%60:02d}\t")

    queue_strings = []

    for name, queue in queues:
        queue_strings.append(f"{name} ({len(queue)})")

    print(" -> ".join(queue_strings))


def main() -> None:
    # print_snapshot(3800, [
    #     ("fronta1", deque(range(1000))),
    #     ("fronta2", deque(range(10))),
    #     ("fronta3", deque(range(1000))),
    # ])
    people_number = 1000
    people_in_the_city = deque(list(range(people_number)))

    # 1. Vytvoření front
    gate_q = deque()
    vege_q = deque()
    final_q = deque()

    # Seznam pro výpis (jméno, fronta)
    queues_to_observe = [
        ("gate_q", gate_q),
        ("vege_q", vege_q),
        ("final_q", final_q),
    ]

    # Parametry simulace (střední hodnoty časů v sekundách)
    day_m = 30  # Každých 30s přijde někdo z ulice
    gate_m = 15  # Gate keeper každého odbavuje 5s
    vege_m = 45  # Vážení zeleniny trvá 45s
    final_m = 2 * 60  # Pokladna zabere 2 minuty

    # 2. Vytvoření pracovníků (Worker)
    # Worker(jméno, zdroj, cíl, perioda, spread_factor)
    workers = [
        Worker("Generator", people_in_the_city, gate_q, day_m),
        Worker("GateKeeper", gate_q, vege_q, gate_m),
        Worker("VegeMan", vege_q, final_q, vege_m),
        Worker("Cashier1", final_q, people_in_the_city, final_m),
        Worker("Cashier2", final_q, people_in_the_city, final_m),
        Worker("Cashier3", final_q, people_in_the_city, final_m),
    ]

    # 3. Hlavní smyčka simulace
    for second in range(200 * 3600):
        for worker in workers:
            worker_tick(worker)

        if second % 200 == 0:
            print_snapshot(second, queues_to_observe)

if __name__ == "__main__":
    main()
