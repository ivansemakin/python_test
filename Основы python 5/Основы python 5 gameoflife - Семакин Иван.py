from PIL import Image, ImageDraw
import sys

INPUT_FILE = 'init01.csv'
OUTPUT_FILE_CSV = 'generation.csv'
OUTPUT_FILE_PNG = 'generation.png'
GENERATIONS = 10
DEBUG = True
CELL_SIZE = 20
BORDER_WIDTH = 2
BASE_COLOR = (0, 0, 255)  # Синий цвет по умолчанию
AGE_MAP = {}


def live_neighbors(grid, row, col):
    """
    @requires: grid which is a list of lists where
    each list contains either 0 or 1 meaning the cell
    is alive (1) or dead (0). The size of all inner lists
    must be the same.
    E.g.,
    [[0, 1, 0],
     [0, 0, 0],
     [1, 1, 0]]

    row and col are integers such that 0 <= row <= number of rows in grid
    and 0 <= col <= number of columns in grid

    @modifies: None
    @effects: None
    @raises: None
    @returns:
    the number of cells whose value is 1 around the cell at (row, col)
    """
    rows = len(grid)
    cols = len(grid[0])
    min_r = max(0, row - 1)
    max_r = min(rows - 1, row + 1)
    min_c = max(0, col - 1)
    max_c = min(cols - 1, col + 1)
    count = 0
    for idx_y in range(min_r, max_r + 1):
        for idx_x in range(min_c, max_c + 1):
            if idx_y == row and idx_x == col:
                continue
            if grid[idx_y][idx_x] == 1:
                count += 1
    return count


def model(grid):
    """
    @requires: grid which is a list of lists where
    each list contains either 0 or 1 meaning the cell
    is alive (1) or dead (0).
    The size of all inner lists must be the same.
    E.g.,
    [ [0, 1, 0],
      [0, 0, 0],
      [1, 1, 0] ]

    @modifies: None
    @effects: None
    @raises: None
    @returns: a new grid which follows the format of the
    input grid but with cell values that correspond to the new
    generation. The new generation is determined by applying
    the following rules:
    1. Any live cell with fewer than two neighbours dies, as if by underpopulation.
    2. Any live cell with two or three live neighbours lives on to the next generation.
    3. Any live cell with more than three live neighbours dies, as if by overpopulation.
    4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
    """
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # Словарь для хранения возраста клеток
    if len(AGE_MAP) == 0:
        for row in range(rows):
            for col in range(cols):
                if grid[row][col] == 1:
                    AGE_MAP[(row, col)] = 1

    for row in range(rows):
        for col in range(cols):
            live_nb = live_neighbors(grid, row, col)

            # Rule 1: Underpopulation
            if grid[row][col] == 1 and live_nb < 2:
                new_grid[row][col] = 0
                if (row, col) in AGE_MAP:
                    del AGE_MAP[(row, col)]

            # Rule 2: Survival
            elif grid[row][col] == 1 and (live_nb == 2 or live_nb == 3):
                new_grid[row][col] = 1
                if (row, col) in AGE_MAP:
                    AGE_MAP[(row, col)] += 1
                else:
                    AGE_MAP[(row, col)] = 1

            # Rule 3: Overpopulation
            elif grid[row][col] == 1 and live_nb > 3:
                new_grid[row][col] = 0
                if (row, col) in AGE_MAP:
                    del AGE_MAP[(row, col)]

            # Rule 4: Reproduction
            elif grid[row][col] == 0 and live_nb == 3:
                new_grid[row][col] = 1
                AGE_MAP[(row, col)] = 1

            else:
                new_grid[row][col] = 0
                if (row, col) in AGE_MAP:
                    del AGE_MAP[(row, col)]

    return new_grid


def read_input(filename):
    """
    Чтение начальной конфигурации из файла.
    Формат файла: каждая строка содержит значения ячеек, разделенные запятыми
    """
    grid = []
    with open(filename, "r") as input_file:
        lines = input_file.readlines()
        if DEBUG:
            print(f"File contents: {lines}")

        for line in lines:
            line = line.strip()
            # Убираем возможные пробелы и разделяем по запятым
            cells = line.split(',')
            cells = [int(item.strip()) for item in cells if item.strip()]

            if cells:  # Добавляем только непустые строки
                grid.append(cells)

    # Проверяем, что все строки имеют одинаковую длину
    if grid:
        first_len = len(grid[0])
        for i, row in enumerate(grid):
            if len(row) != first_len:
                print(f"Warning: Row {i} has different length ({len(row)} vs {first_len})")

    return grid


def write_output(grid, filename, generation_num):
    """
    Запись в CSV файл
    """
    with open(f"{generation_num}_{filename}", "w") as output_file:
        for row in grid:
            line = ','.join(str(cell) for cell in row)
            output_file.write(line + '\n')


def write_png(grid, filename, generation_num, base_color=BASE_COLOR):
    """
    Создание PNG
    """
    rows = len(grid)
    cols = len(grid[0])

    # Размер
    width = cols * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
    height = rows * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH

    # Создаем изображение
    im = Image.new('RGB', (width, height), color=(240, 240, 240))
    draw = ImageDraw.Draw(im)

    # Сетка и клетки
    for row in range(rows):
        for col in range(cols):
            # Координаты клетки
            x1 = col * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
            y1 = row * (CELL_SIZE + BORDER_WIDTH) + BORDER_WIDTH
            x2 = x1 + CELL_SIZE
            y2 = y1 + CELL_SIZE
            if grid[row][col] == 1:
                # Возраст клетки
                age = AGE_MAP.get((row, col), 1)

                # Цвет: Чем старше клетка, тем темнее цвет
                factor = min(0.3 + (age * 0.1), 0.9)  # От 30% до 90% яркости
                color = tuple(int(c * factor) for c in base_color)

                # Живая клетка
                draw.rectangle([x1, y1, x2, y2], fill=color, outline=(200, 200, 200))

            else:

                # Мертвая клетка
                draw.rectangle([x1, y1, x2, y2], fill=(255, 255, 255), outline=(200, 200, 200))

    # Границы сетки
    for i in range(cols + 1):
        x = i * (CELL_SIZE + BORDER_WIDTH)

        draw.line([(x, 0), (x, height)], fill=(150, 150, 150), width=1)

    for i in range(rows + 1):
        y = i * (CELL_SIZE + BORDER_WIDTH)

        draw.line([(0, y), (width, y)], fill=(150, 150, 150), width=1)

    # Изображение в файл
    output_filename = f"{generation_num}_{filename}"
    im.save(output_filename)

    if DEBUG:
        print(f"Image saved as {output_filename}")


def main():
    """
    Основная функция игры "Жизнь"
    """

    # Обработка аргументов командной строки
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = INPUT_FILE

    if len(sys.argv) > 2:
        try:
            generations = int(sys.argv[2])
        except ValueError:
            print(f"Invalid generations value: {sys.argv[2]}, using default: {GENERATIONS}")
            generations = GENERATIONS
    else:
        generations = GENERATIONS

    if len(sys.argv) > 3:
        try:
            # Парсим цвет
            color_parts = sys.argv[3].split(',')

            if len(color_parts) == 3:
                base_color = tuple(int(c) for c in color_parts)
            else:
                raise ValueError

        except (ValueError, IndexError):
            print(f"Invalid color format: {sys.argv[3]}, using default: {BASE_COLOR}")
            base_color = BASE_COLOR
    else:
        base_color = BASE_COLOR

    # Читаем начальную конфигурацию
    grid = read_input(input_file)
    if not grid:
        print("Error: Empty grid or invalid input file")
        return

    if DEBUG:
        print(f"Initial grid ({len(grid)}x{len(grid[0])}):")
        for row in grid:
            print(row)
        print(f"\nSimulating {generations} generations...\n")

    # Сохраняем начальное состояние
    write_output(grid, OUTPUT_FILE_CSV, 0)
    write_png(grid, OUTPUT_FILE_PNG, 0, base_color)

    # Выполняем симуляцию
    for generation in range(1, generations + 1):
        grid = model(grid)

        # Сохраняем текущее состояние
        write_output(grid, OUTPUT_FILE_CSV, generation)
        write_png(grid, OUTPUT_FILE_PNG, generation, base_color)

        if DEBUG:
            print(f"Generation {generation} completed")
            alive_count = sum(sum(row) for row in grid)
            print(f"  Alive cells: {alive_count}")

    if DEBUG:
        print(f"\nSimulation completed. Results saved with prefixes 0-{generations}.")


main()
