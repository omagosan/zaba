"""Resi hlavolam sudoku pomoci metody backtracking, pouziti: python sudoku.py input.csv."""

import sys
import os


class SudokuSolver:
    """Resi hlavolam sudoku klasickeho rozmeru 9 x 9 policek.

    Lze nastavit i jiny rozmer. Rozmer 9 x 9 odpovida block_size = 3.
    Pro block_size = 2 dostaneme rozmer 4 x 4.
    Pro block_size = 5 dostaneme rozmer 25 x 25.

    Attributes:
        block_size(int): velikost bloku (default 3)
        blocks_count(int): pocet bloku horizontalne i vertikalne
        values_count(int): pocet hodnot v bloku, na radce, ve sloupci
        rows_count(int): pocet radek
        cols_count(int): pocet sloupcu
        empty_value(int): hodnota reprezentujici prazdne policko
        min_value(int): minimalni pouzitelna hodnota krome empty_value (default 1)
        max_value(int): maximalni pouzitelna hodnota krome empty_value
    """

    block_size: int = 3
    blocks_count: int = block_size
    values_count: int = block_size * block_size
    rows_count: int = values_count
    cols_count: int = values_count
    empty_value: int = 0
    min_value: int = 1
    max_value: int = values_count

    def __init__(self) -> None:
        """Inicializace sudoku solveru - alokace 2D pole."""
        self.field: list[list[int]] = [
            [self.empty_value] * self.cols_count for _ in range(self.rows_count)
        ]

    def __str__(self):
        """Prevede stav sudoku solveru na textovou reprezentaci."""
        return "\n".join(str(row) for row in self.field)

    def load(self, file_path: str) -> None:
        """Nacte vychozi stav pro sudoku solver z CSV souboru.

        Ocekavany format: 9 radku o 9 sloupcich. Hodnoty 0-9. Hodnota 0
        reprezentuje prazdne policko, ale dovolime i bile znaky.
        Oddelovacem je strednik.

        Args:
            file_path: Cesta k CSV souboru.

        Raises:
            ValueError: pokud je nejaka hodnota jina nez 0-9 nebo pole neni 9x9.
        """

        # list of lists (rows)
        loaded_rows: list[list[int]] = []

        # Otevreme soubor v textovem rezimu pro cteni, kodovani znaku utf-8
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            for line in file:
                if not line.strip():  # Preskakujeme prazdne radky
                    continue

                # Neprazdny radek rozdelime na policka podle separatoru ";" a
                # kazde policko zkonvertujeme na cele cislo.
                row = [self._parse_field(field) for field in line.split(";")]

                if len(row) != self.cols_count or len(loaded_rows) == self.rows_count:
                    raise ValueError  # Neocekavany pocet sloupcu nebo prilis mnoho radek

                loaded_rows.append(row)

            if len(loaded_rows) != self.rows_count:
                raise ValueError  # Neocekavany pocet radek

        self.field = loaded_rows

    def _parse_field(self, field: str) -> int:
        field = field.strip()
        value = int(field) if len(field) >= 1 else self.empty_value
        if value == self.empty_value or self.min_value <= value <= self.max_value:
            return value

        raise ValueError  # Hodnota mimo povoleny rozsah

    def _allocate_usage_list(self) -> list[bool]:
        n = self.max_value - self.min_value + 1
        return [False] * n

    def check_row(self, row_index: int) -> bool:
        """Zkontroluje, zda radek neobsahuje duplicity (krome prazdneho symbolu).

        Args:
            row_index(int): Index radky ke kontrole.
        Returns:
            True, pokud je bez duplicit, False pokud obsahuje nejake duplicity.
        """
        used: list[bool] = self._allocate_usage_list()
        for value in self.field[row_index]:
            if value == self.empty_value:
                continue
            if used[value - self.min_value]:
                return False
            used[value - self.min_value] = True

        return True

    def check_column(self, column_index: int) -> bool:
        """Zkontroluje, zda sloupce neobsahuje duplicity (krome prazdneho symbolu).

        Args:
            column_index(int): Index sloupce ke kontrole.
        Returns:
            True, pokud je bez duplicit, False pokud obsahuje nejake duplicity.
        """
        used: list[bool] = self._allocate_usage_list()
        for i in range(len(self.field)):
            value = self.field[i][column_index]
            if value == self.empty_value:
                continue
            if used[value - self.min_value]:
                return False
            used[value - self.min_value] = True

        return True

    def check_block(self, row_index: int, column_index: int) -> bool:
        """Zkontroluje, zda blok neobsahuje duplicity (krome prazdneho symbolu).

        Args:
            row_index(int): Index radky v tabulce
            column_index(int): Index sloupce v tabulce
        Returns:
            True, pokud je bez duplicit, False pokud obsahuje nejake duplicity.
        """
        used: list[bool] = self._allocate_usage_list()

        # souradnice pocatecniho (leveho horniho) policka bloku
        i0 = row_index - row_index % self.block_size
        j0 = column_index - column_index % self.block_size

        for i in range(i0, i0 + self.block_size):
            for j in range(j0, j0 + self.block_size):
                value = self.field[i][j]
                if value == self.empty_value:
                    continue
                value -= self.min_value
                if used[value]:
                    return False
                used[value] = True

        return True

    def check_one_cell(self, row_index: int, column_index: int) -> bool:
        """Zkontroluje, zda je zadana bunka validni (splnuje pravidlo pro radek, sloupec i blok).

        Args:
            row_index(int): Index radky v tabulce
            column_index(int): Index sloupce v tabulce
        Returns:
            True, pokud je bunka validni, False pokud je nektere z pravidel poruseno.
        """
        return (
            self.check_row(row_index)
            and self.check_column(column_index)
            and self.check_block(row_index, column_index)
        )

    def solve(self) -> bool:
        """Rekurzivne vyresi sudoku."""

        # Projde celou tabulku a ulozi souradnice prazdnych policek.
        # Primarne jdeme po blocich, sekundarne prochazime kazdy blok.
        positions: list[tuple[int, int]] = []
        for block_i in range(self.blocks_count):
            for block_j in range(self.blocks_count):
                i0 = block_i * self.block_size
                j0 = block_j * self.block_size
                # Pruchod pres policka ramci bloku:
                for i in range(i0, i0 + self.block_size):
                    for j in range(j0, j0 + self.block_size):
                        if self.field[i][j] == self.empty_value:
                            positions.append((i, j))

        # Vektor reseni pro backtracking. Budeme ho vyplnovat postupne zleva doprava.
        # Sel by pouzit i stack (dequeue), mohl by byt vhodnejsi. Ale tohle staci taky.
        solution_vector = [self.empty_value] * len(positions)

        # Vyresime sudoku pomoci rekurzivniho backtrackingu.
        # Vraci prvni nalezene reseni, na tom se zastavi.
        return self._solve(solution_vector, positions, 0)

    def _set_value(
        self, solution_vector: list[int], i: int, j: int, k: int, value: int
    ) -> None:
        self.field[i][j] = value
        solution_vector[k] = value

    def _clear_value(self, solution_vector: list[int], i: int, j: int, k: int) -> None:
        self.field[i][j] = self.empty_value
        solution_vector[k] = self.empty_value

    def _solve(
        self, solution_vector: list[int], positions: list[tuple[int, int]], k: int
    ) -> bool:
        n = len(solution_vector)
        if k == n:
            print("Solution table:")  # Nalezene reseni vypiseme na vystup.
            print(self)
            print("Solution vector:")
            print(f"\tval: {solution_vector}")
            print(f"\trow: {[p[0] for p in positions]}")
            print(f"\tcol: {[p[1] for p in positions]}")
            return True  # Signalizujeme "solution found"

        # Vezmeme si souradnice policka: i-ty radek a j-ty sloupec pro zadany index k
        i, j = positions[k]

        # Policko field[i][j] je prazdne. Postupne na nem vyzkousime vsechny pouzitelne hodnoty.
        for value in range(self.min_value, self.max_value + 1):
            # Aktualne zkousenou hodnotu, ktera muze rozsirit reseni na index k,
            # ulozime do field a do solution_vector. Bude se hodit, az se dobereme vysledku.
            self._set_value(solution_vector, i, j, k, value)
            if self.check_one_cell(i, j):
                # Aktualne zkousenou hodnotu lze pouzit pro rozsireni reseni z delky k na k + 1.
                # Muzeme tedy rekurzivne dohledat zbytek reseni.
                solution_found = self._solve(solution_vector, positions, k + 1)

                # Z rekurze se vracime s nejakym vysledkem. Je to priznak, zda jsme nasli cele
                # reseni nebo ne. Pokud jsme nasli reseni, uklidime po sobe a vracime True.
                # Tim zarizneme dalsi rekurzivni prohledavani a predame signal nadrazenym volanim.
                if solution_found:
                    self._clear_value(solution_vector, i, j, k)
                    return True

            # Bud neslo hodnotu pouzit (byla duplicitni) nebo jsme v rekurzi nenasli zadne reseni.
            # Uklidime po sobe (to je zde velmi dulezite) a pokracujeme dalsi iteraci.
            self._clear_value(solution_vector, i, j, k)

        # Po vycerpani vsech moznosti jsme nenasli zadne reseni, vracime False
        return False


def main() -> None:
    input_files: list[str] = []
    if len(sys.argv) <= 1:
        default_input_file = "sudoku.csv"
        input_files.append(default_input_file)
        print(f"Using default input file: {default_input_file}", file=sys.stderr)
    else:
        input_files = sys.argv[1:] # Vsechny dalsi argumenty krome jmena skriptu

    # Pro kazdy soubor z argument
    for input_file in input_files:
        print(f"Processing {input_file}...", file=sys.stderr)

        if not os.path.exists(input_file):
            print(f"Path not found: {input_file}", file=sys.stderr)
            continue

        if not os.path.isfile(input_file):
            print(f"Not a file: {input_file}", file=sys.stderr)
            continue

        try:
            sudoku_solver = SudokuSolver()
            sudoku_solver.load(input_file)
            print("File loaded.", file=sys.stderr)
            print("Task:")
            print(sudoku_solver)
            print("Solving...")
            status = sudoku_solver.solve()
            print("Solution found!" if status else "No solution found.")
        except (OSError, ValueError) as e:
            print(f"An exception occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()
