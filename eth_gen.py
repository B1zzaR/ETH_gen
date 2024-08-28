import os
import multiprocessing
import time
from eth_keys import keys
from eth_utils import decode_hex

def generate_vanity_address(prefix, attempts=10000000):
    """
    Функция генерирует Ethereum-адреса, пока не найдет адрес, начинающийся с заданного префикса.
    
    :param prefix: Строка, с которой должен начинаться адрес (например, '0x1234')
    :param attempts: Количество попыток для одного процесса
    :return: Кортеж (адрес, приватный ключ) или None, если не найден
    """
    for _ in range(attempts):
        private_key = keys.PrivateKey(os.urandom(32))
        public_key = private_key.public_key
        address = public_key.to_checksum_address()

        if address.lower().startswith(prefix.lower()):
            return address, private_key.to_hex()
    return None

def worker(prefix, queue, attempts):
    """
    Функция, запускаемая в отдельном процессе. Проверяет адреса и передает результат через очередь.
    
    :param prefix: Строка, с которой должен начинаться адрес
    :param queue: Очередь для передачи результатов между процессами
    :param attempts: Количество попыток для одного процесса
    """
    result = generate_vanity_address(prefix, attempts)
    if result:
        queue.put(result)

def find_vanity_address(prefix, attempts_per_process=10000000, workers=None):
    """
    Функция запускает несколько процессов для поиска адреса с заданным префиксом.
    
    :param prefix: Строка, с которой должен начинаться адрес
    :param attempts_per_process: Количество попыток для каждого процесса
    :param workers: Количество процессов (по умолчанию количество ядер процессора)
    :return: Найденный адрес и приватный ключ
    """
    if workers is None:
        workers = multiprocessing.cpu_count()

    queue = multiprocessing.Queue()
    processes = []

    for _ in range(workers):
        process = multiprocessing.Process(target=worker, args=(prefix, queue, attempts_per_process))
        processes.append(process)
        process.start()

    address, priv_key = queue.get()  # Ожидаем результат от одного из процессов

    for process in processes:
        process.terminate()  # Останавливаем все процессы

    return address, priv_key

if __name__ == "__main__":
    inp = str(input("Префикс >> 0x"))
    prefix = f"0x{inp}"  # Задайте здесь ваш префикс
    print(f"Поиск адреса, начинающегося с '{prefix}'...")

    start_time = time.time()
    address, priv_key = find_vanity_address(prefix)
    end_time = time.time()

    print(f"Найден адрес: {address}")
    print(f"Приватный ключ: {priv_key}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    input()