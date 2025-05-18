import math

def gcd(a, b):
    """Знаходить найбільший спільний дільник двох чисел."""
    while b:
        a, b = b, a % b
    return a

class Rational:
    def __init__(self, num=0, den=1):
        """Конструктор для класу Rational.

        Приймає два цілих аргументи (чисельник та знаменник) або
        один рядковий аргумент у форматі 'n/d'.
        Забезпечує нескоротність дробу.
        """
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
        """Повертає рядкове представлення раціонального числа."""
        return f"{self.num}/{self.den}"

    def __repr__(self):
        """Повертає рядкове представлення об'єкта для налагодження."""
        return f"Rational({self.num}, {self.den})"

    def _arithmetic_check(self, other):
        """Перевіряє тип іншого операнда для арифметичних операцій."""
        if not isinstance(other, (int, Rational)):
            raise TypeError("Правий операнд повинен бути цілим числом або об'єктом Rational.")
        if isinstance(other, int):
            other = Rational(other)
        return other

    def __add__(self, other):
        """Перевантаження оператора додавання (+)."""
        other = self._arithmetic_check(other)
        new_num = self.num * other.den + other.num * self.den
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __radd__(self, other):
        """Перевантаження оператора додавання (+) для випадку, коли лівий операнд - int."""
        return self.__add__(other)

    def __sub__(self, other):
        """Перевантаження оператора віднімання (-)."""
        other = self._arithmetic_check(other)
        new_num = self.num * other.den - other.num * self.den
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __rsub__(self, other):
        """Перевантаження оператора віднімання (-) для випадку, коли лівий операнд - int."""
        return Rational(other) - self

    def __mul__(self, other):
        """Перевантаження оператора множення (*)."""
        other = self._arithmetic_check(other)
        new_num = self.num * other.num
        new_den = self.den * other.den
        return Rational(new_num, new_den)

    def __rmul__(self, other):
        """Перевантаження оператора множення (*) для випадку, коли лівий операнд - int."""
        return self.__mul__(other)

    def __truediv__(self, other):
        """Перевантаження оператора ділення (/)."""
        other = self._arithmetic_check(other)
        if other.num == 0:
            raise ZeroDivisionError("Ділення на нуль.")
        new_num = self.num * other.den
        new_den = self.den * other.num
        return Rational(new_num, new_den)

    def __rtruediv__(self, other):
        """Перевантаження оператора ділення (/) для випадку, коли лівий операнд - int."""
        if self.num == 0:
            raise ZeroDivisionError("Ділення на нуль.")
        return Rational(other) / self

    def __call__(self):
        """Перевантаження оператора круглих дужок для повернення десяткового дробу."""
        return self.num / self.den

    def __getitem__(self, key):
        """Перевантаження оператора квадратних дужок для доступу до чисельника та знаменника."""
        if key == "n":
            return self.num
        elif key == "d":
            return self.den
        else:
            raise KeyError("Неправильний ключ. Доступні ключі: 'n' (чисельник), 'd' (знаменник).")

    def __setitem__(self, key, value):
        """Перевантаження оператора квадратних дужок для встановлення чисельника та знаменника."""
        if not isinstance(value, int):
            raise TypeError("Значення повинно бути цілим числом.")
        if key == "n":
            self.num = value
            self.__init__(self.num, self.den) # Перенормалізація
        elif key == "d":
            if value == 0:
                raise ZeroDivisionError("Знаменник не може бути нулем.")
            self.den = value
            self.__init__(self.num, self.den) # Перенормалізація
        else:
            raise KeyError("Неправильний ключ. Доступні ключі: 'n' (чисельник), 'd' (знаменник).")

def evaluate_expression(expression):
    """Обчислює значення арифметичного виразу з раціональними числами."""
    tokens = expression.split()
    values = []
    operators = []

    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    def apply_op():
        op = operators.pop()
        right = values.pop()
        left = values.pop()
        if op == '+':
            values.append(left + right)
        elif op == '-':
            values.append(left - right)
        elif op == '*':
            values.append(left * right)
        elif op == '/':
            values.append(left / right)

    i = 0
    while i < len(tokens):
        token = tokens[i]
        if '/' in token:
            values.append(Rational(token))
        elif token.isdigit() or (token.startswith('-') and token[1:].isdigit()):
            values.append(Rational(int(token)))
        elif token in precedence:
            while operators and precedence.get(operators[-1], 0) >= precedence[token]:
                apply_op()
            operators.append(token)
        elif token == '(':
            operators.append(token)
        elif token == ')':
            while operators[-1] != '(':
                apply_op()
            operators.pop()  # Видалення '('
        i += 1

    while operators:
        apply_op()

    return values[0]

if __name__ == "__main__":
    filename = "input1.txt"
    try:
        with open(filename, 'r') as f:
            for line in f:
                expression = line.strip()
                try:
                    result = evaluate_expression(expression)
                    print(f"Вираз з '{filename}': {expression} = {result} ({result()})")
                except Exception as e:
                    print(f"Помилка обчислення виразу '{expression}' з '{filename}': {e}")
    except FileNotFoundError:
        print(f"Файл '{filename}' не знайдено.")

    # Приклад вмісту файлу input01.txt (створиться, якщо його немає)
    with open("input1.txt", "w") as f:
        f.write("4 - 92 - 79 * 59 * 90/16 * 75 - 55 * 82/41 * 19\n")
        f.write("1/2 + 1/3\n")
        f.write("10 * 3/5 - 2\n")
        f.write("1 / (1/2)\n")
        f.write("5 + 2 * (3 - 1/4)\n")