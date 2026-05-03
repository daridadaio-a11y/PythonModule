from abc import ABC, abstractmethod
from typing import Any


class DataProcessor(ABC):
    def __init__(self):
        self.data_store = []
        self.rank_counter = 0

    @abstractmethod
    def validate(self, data: Any) -> bool:
        pass

    @abstractmethod
    def ingest(self, data: Any) -> None:
        pass

    def output(self) -> tuple[int, str]:
        if not self.data_store:
            raise IndexError("No data to output")
        oldest_data = self.data_store.pop(0)
        current_rank = self.rank_counter
        self.rank_counter += 1
        return (current_rank, oldest_data)


class NumericProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return True
        elif isinstance(data, list):
            for num in data:
                if not isinstance(num, (int, float)):
                    return False
            return True
        else:
            return False

    def ingest(self, data: int | float | list[int | float]) -> None:
        if not self.validate(data):
            raise ValueError("Improper numeric data")
        if isinstance(data, (int, float)):
            str_num = str(data)
            self.data_store.append(str_num)
        else:
            for num in data:
                str_num = str(num)
                self.data_store.append(str_num)


class TextProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, str):
            return True
        elif isinstance(data, list):
            for text in data:
                if not isinstance(text, str):
                    return False
            return True
        else:
            return False

    def ingest(self, data: str | list[str]) -> None:
        if not self.validate(data):
            raise ValueError("Improper text data")
        if isinstance(data, str):
            self.data_store.append(data)
        else:
            for text in data:
                self.data_store.append(text)


class LogProcessor(DataProcessor):
    def validate(self, data: Any) -> bool:
        if isinstance(data, dict):
            for key, value in data.items():
                if not (isinstance(key, str) and isinstance(value, str)):
                    return False
            return True
        elif isinstance(data, list):
            for log in data:
                if not isinstance(log, dict):
                    return False
                for key, value in log.items():
                    if not (isinstance(key, str) and isinstance(value, str)):
                        return False
            return True
        else:
            return False

    def ingest(self, data: dict[str, str] | list[dict[str, str]]) -> None:
        if not self.validate(data):
            raise ValueError("Improper log data")
        if isinstance(data, dict):
            level = data["log_level"]
            message = data["log_message"]
            new_str = f"{level}: {message}"
            self.data_store.append(new_str)
        else:
            for cdict in data:
                level = cdict["log_level"]
                message = cdict["log_message"]
                new_str = f"{level}: {message}"
                self.data_store.append(new_str)


class Datastream:
    def __init__(self):
        self.processors = []

    def register_processor(self, proc: DataProcessor) -> None:
        self.processors.append(proc)

    def process_stream(self, stream: list[Any]) -> None:
        for data in stream:
            is_proccessed = False
            for proc in self.processors:
                if proc.validate(data):
                    proc.ingest(data)
                    is_proccessed = True
                    break
            if not is_proccessed:
                print("DataStream error: Can't process element in stream:"
                      f" {data}")

    def print_processors_stats(self) -> None:
        if not self.processors:
            print("No processor found, no data")
            return
        for proc in self.processors:
            name = proc.__class__.__name__
            total = len(proc.data_store) + proc.rank_counter
            remaining_data = len(proc.data_store)
            print(f"{name}: total {total} items processed, remaining"
                  f" {remaining_data} on processor")


if __name__ == '__main__':
    print("=== Code Nexus Data Stream ===\n")
    stream = Datastream()
    num_pro = NumericProcessor()
    text_pro = TextProcessor()
    log_pro = LogProcessor()
    print("Initialize Data Stream...")
    print("== DataStream statistics ==")
    stream.print_processors_stats()
    print()
    stream.register_processor(num_pro)
    print("Registering Numuric Pricessor...\n")
    test_data = ['Hello world', [3.14, 1, 2.71],
                 [{'log_level': 'WARNING',
                   'log_message': 'Telnet access! Use ssh instead'},
                  {'log_level': 'INFO',
                   'log_message': 'User will is connected'}],
                 42, ['Hi', 'five']]
    print(f"Send first batch of data on stream: {test_data}")
    stream.process_stream(test_data)
    print("== DataStream statistics ==")
    stream.print_processors_stats()
    print()
    print("Registering other data processors")
    print("Send the same batch again")
    stream.register_processor(text_pro)
    stream.register_processor(log_pro)
    stream.process_stream(test_data)
    stream.print_processors_stats()
    print()
    num_range = 3
    text_range = 2
    log_range = 1
    for _ in range(num_range):
        num_rank, num_data = num_pro.output()
    for _ in range(text_range):
        text_rank, text_data = text_pro.output()
    for _ in range(log_range):
        log_rank, log_data = log_pro.output()
    print("Consume some elements from the data processors:"
          f" Numric {num_range}, Text {text_range}, Log {log_range}")
    print("== DataStream statistics ==")
    stream.print_processors_stats()
    