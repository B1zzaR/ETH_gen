import os
import multiprocessing
import time
from eth_keys import keys
from eth_utils import decode_hex

def generate_vanity_address(prefix, attempts=10000000):
    for _ in range(attempts):
        private_key = keys.PrivateKey(os.urandom(32))
        public_key = private_key.public_key
        address = public_key.to_checksum_address()

        if address.lower().startswith(prefix.lower()):
            return address, private_key.to_hex()
    return None

def worker(prefix, queue, attempts):
    result = generate_vanity_address(prefix, attempts)
    if result:
        queue.put(result)

def find_vanity_address(prefix, attempts_per_process=10000000, workers=None):
    if workers is None:
        workers = multiprocessing.cpu_count()

    queue = multiprocessing.Queue()
    processes = []

    for _ in range(workers):
        process = multiprocessing.Process(target=worker, args=(prefix, queue, attempts_per_process))
        processes.append(process)
        process.start()

    address, priv_key = queue.get()

    for process in processes:
        process.terminate()

    return address, priv_key

if __name__ == "__main__":
    inp = str(input("Префикс >> 0x"))
    prefix = f"0x{inp}"
    print(f"Поиск адреса, начинающегося с '{prefix}'...")

    start_time = time.time()
    address, priv_key = find_vanity_address(prefix)
    end_time = time.time()

    print(f"Найден адрес: {address}")
    print(f"Приватный ключ: {priv_key}")
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    input()
