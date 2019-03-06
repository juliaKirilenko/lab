
from parserecho3 import ParserEcho
from concurrent.futures import ThreadPoolExecutor

if __name__ == '__main__':
    
    days = 180
    exec = ThreadPoolExecutor(max_workers=30)
    filename =  'parserEcho8.csv'
    parser = ParserEcho(filename)
    exec.map(parser.get_page_by_day, range(days))
