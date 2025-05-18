import math

def gcd(a, b):

    while b:
        a, b = b, a % b
    return a

class Rational:
    def __init__(self, num=0, den=1):

        if isinstance(num, str):
            parts = num.split('/')
            if len(parts) != 2:
                raise ValueError("Неправильний формат рядка для раціонального числа. Очікується 'n/d'.")
            self.num = int(parts[0])
            self.den = int(parts[1])
        elif isinstance(num, int) and isinstance(den, int):
            if den == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем.")
            common_divisor = gcd(abs(num), abs(den))
            self.num = num // common_divisor
            self.den = den // common_divisor
            if self.den < 0:
                self.num *= -1
                self.den *= -1
        elif isinstance(num, Rational):
            # Конструктор копіювання
            self.num = num.num
            self.den = num.den
        else:
            raise TypeError("Неправильні типи аргументів для конструктора.")

    def __str__(self):

        return f"{self.num}/{self.den}"

    def __repr__(self):

        return f"Rational({self.num}, {self.den})"

    def _arithmetic_check(self, other):

        if not isinstance(other, (int, Rational)):
            raise TypeError("Правий операнд повинен бути цілим числом або об'єктом Rational.")
        if isinstance(other, int):
            other = Rational(other)
        return other

    def __add__(self, other):

        other = self._arithmetic_check(other)
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __radd__(self, other):

        return self.__add__(other)

    def __sub__(self, other):

        other = self._arithmetic_check(other)
        new_num = self.num * other.den - other.num * self.den
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __rsub__(self, other):

        return Rational(other) - self

    def __mul__(self, other):

        other = self._arithmetic_check(other)
        new_num = self.num * other.num
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __rmul__(self, other):

        return self.__mul__(other)

    def __truediv__(self, other):

        other = self._arithmetic_check(other)
        if other.num == 0:
            raise ZeroDivisionError("Ділення на нуль.")
        new_num = self.num * other.den
        new_den = self.den * other.num
        return Rational(new_num, new_den)

    def __rtruediv__(self, other):

        if self.num == 0:
            raise ZeroDivisionError("Ділення на нуль.")
        return Rational(other) / self

    def __call__(self):

        return self.num / self.den

    def __getitem__(self, key):

        if key == "n":
            return self.num
        elif key == "d":
            return self.den
        else:
            raise KeyError("Неправильний ключ. Доступні ключі: 'n' (чисельник), 'd' (знаменник).")

    def __setitem__(self, key, value):

        if not isinstance(value, int):
            raise TypeError("Значення повинно бути цілим числом.")
        if key == "n":
            self.num = value
            self.__init__(self.num, self.den)
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем.")
            self.den = value
            self.__init__(self.num, self.den)
        else:
            raise KeyError("Неправильний ключ. Доступні ключі: 'n' (чисельник), 'd' (знаменник).")

class RationalList:
    def __init__(self, initial_list=None):

        self._data = []
        if initial_list is not None:
            for item in initial_list:
                self.append(item)

    def _ensure_rational(self, value):

        if isinstance(value, Rational):
            return value
        elif isinstance(value, int):
            return Rational(value)
        elif isinstance(value, str) and '/' in value:
            return Rational(value)
        else:
            raise TypeError("Елементи списку повинні бути об'єктами Rational, цілими числами або рядками у форматі 'n/d'.")

    def append(self, value):

        self._data.append(self._ensure_rational(value))

    def __getitem__(self, index):

        return self._data[index]

    def __setitem__(self, index, value):

        self._data[index] = self._ensure_rational(value)

    def __len__(self):

        return len(self._data)

    def __add__(self, other):

        new_list = RationalList(self._data)
        if isinstance(other, RationalList):
            new_list._data.extend(other._data)
        elif isinstance(other, (int, str)):
            new_list.append(other)
        else:
            raise TypeError("Правий операнд '+' повинен бути RationalList, цілим числом або рядком у форматі 'n/d'.")
        return new_list

    def __iadd__(self, other):

        if isinstance(other, RationalList):
            self._data.extend(other._data)
        elif isinstance(other, (int, str)):
            self.append(other)
        else:
            raise TypeError("Правий операнд '+=' повинен бути RationalList, цілим числом або рядком у форматі 'n/d'.")
        return self

    def sum(self):

        total = Rational(0)
        for item in self._data:
            total += item
        return total

def read_rational_list_from_file(filename):

    rational_list = RationalList()
    try:
        with open(filename, 'r') as f:
            for line in f:
                numbers_str = line.strip().split()
                for num_str in numbers_str:
                    try:
                        rational_list.append(num_str)
                    except ValueError as e:
                        print(f"Помилка при обробці '{num_str}' у файлі '{filename}': {e}")
                    except TypeError as e:
                        print(f"Помилка типу для '{num_str}' у файлі '{filename}': {e}")
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")
    return rational_list

if __name__ == "__main__":
    filenames = ["01.txt", "02.txt", "03.txt"]
    for filename in filenames:
        rational_list = read_rational_list_from_file(filename)
        if rational_list:
            total_sum = rational_list.sum()
            print(f"Сума чисел у файлі '{filename}': {total_sum} ({total_sum()})")
            print(f"Кількість елементів у файлі '{filename}': {len(rational_list)}")
            print(f"Перший елемент: {rational_list[0]}, останній елемент: {rational_list[-1]}")


            rational_list += 5
            print(f"Після додавання 5: {rational_list}")
            rational_list += "1/4"
            print(f"Після додавання '1/4': {rational_list}")
            another_list = RationalList([1, "3/2"])
            combined_list = rational_list + another_list
            print(f"Об'єднаний список: {combined_list}")
            print("-" * 30)
        else:
            print(f"Не вдалося обробити файл '{filename}'.")
            print("-" * 30)


    with open("01.txt", "w") as f:
        f.write("1 2 3/4 5\n")
        f.write("6/7 8 9/2\n")

    with open("02.txt", "w") as f:
        f.write("10 -5 1/3\n")
        f.write("-2/5 7 11\n")

    with open("03.txt", "w") as f:
        f.write("0 1/10 2/100\n")
        f.write("3 4 5/2 6\n")