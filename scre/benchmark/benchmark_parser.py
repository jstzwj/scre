
import time
import tqdm

from scre.parser.parser import Parser

def benchmark_parser(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
    char_count = len(text)
    print(f"总字符数量：{char_count}")
    start_time = time.time()
    for i in tqdm.tqdm(range(10), total=10):
        parser = Parser(text)
        ast = parser.parse()
    end_time = time.time()
    print(f"Time used：{end_time - start_time}s\nChar Speed：{char_count/(end_time - start_time)} c/s")

