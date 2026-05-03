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


if __name__ == '__main__':
    print("=== Code Nexus Data Processor ===")
    print("Testing Numric Processor")
    numeric_proc = NumericProcessor()
    true_num = 42
    is_valid = numeric_proc.validate(true_num)
    print(f"Trying to validate input '{true_num}' : {is_valid}")
    false_str = "Hello"
    is_valid = numeric_proc.validate(false_str)
    print(f"Trying to validate input '{false_str}' : {is_valid}")
    false_str = "foo"
    print("Test invalid ingestion of string"
          f" '{false_str}' without prior validation:")
    try:
        numeric_proc.ingest(false_str)  # type: ignore[arg-type]
    except Exception as e:
        print(f"Got exception: {e}")
    num_list: list[int | float] = [1, 2, 3, 4, 5]
    print(f"Processing data: {num_list}")
    numeric_proc.ingest(num_list)
    print("Extracting 3 values...")
    for _ in range(3):
        rank, val = numeric_proc.output()
        print(f"Numeric value {rank}: {val}")
    print()
    print("Testing Text Processor...")
    text_pro = TextProcessor()
    false_num = 42
    is_vaild = text_pro.validate(false_num)
    print(f"Trying to validate input '{false_num}: {is_valid}")
    true_list = ['Hello', 'Nexus', 'World']
    print(f"Processing data: {true_list}")
    text_pro.ingest(true_list)
    print("Extracting 1 value...")
    for _ in range(1):
        rank, val = text_pro.output()
        print(f"Text value {rank}: {val}")
    print()
    print("Testing Log Processer...")
    log_pro = LogProcessor()
    false_str = "Hello"
    is_valid = log_pro.validate(false_str)
    print(f"Trying to validate input '{false_str}' : {is_valid}")
    true_dict = [{'log_level': 'NOTICE',
                  'log_message': 'Connection to server'},
                 {'log_level': 'ERROR',
                  'log_message': 'Unauthorized access!!'}]
    print(f"Processing data: {true_dict}")
    log_pro.ingest(true_dict)
    print("Extracting 2 values...")
    for _ in range(2):
        rank, val = log_pro.output()
        print(f"Log entry {rank}: {val}")
