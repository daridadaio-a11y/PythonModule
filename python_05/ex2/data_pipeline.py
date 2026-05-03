from abc import ABC, abstractmethod
from typing import Any
from typing import Protocol


class ExportPlugin(Protocol):
    def process_output(self, data: list[tuple[int, str]]) -> None:
        pass


class CSVExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        str_list = []
        rank = 0
        if not data:
            return
        print("CSV Output:")
        for put_data in data:
            rank, put_str = put_data
            str_list.append(put_str)
        join_list = ', '.join(str_list)
        print(join_list)


class JSONExportPlugin:
    def process_output(self, data: list[tuple[int, str]]) -> None:
        json_parts = []
        if not data:
            return
        print("JSON Output:")
        for put_data in data:
            rank, put_str = put_data
            part_str = f'"item_{rank}": "{put_str}"'
            json_parts.append(part_str)
        final_string = "{" + ', '.join(json_parts) + "}"
        print(final_string)

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

    def output_pipeline(self, nb: int, plugin: ExportPlugin) -> None:
        for proc in self.processors:
            str_data = []
            for _ in range(nb):
                try:
                    data_tuple = proc.output()
                    str_data.append(data_tuple)
                except IndexError:
                    break
            if str_data:
                plugin.process_output(str_data)


if __name__ == "__main__":
    print("=== Code Nexus - Data Pipeline ===\n")
    print("Registering Processors\n")
    test_data = ['Hello world', [3.14, -1, 2.71],
                 [{'log_level': 'WARNING',
                   'log_message': 'Telnet access! Use ssh instead'},
                  {'log_level': 'INFO',
                   'log_message': 'User wil isconnected'}], 42, ['Hi', 'five']]
    print(f"Send first batch of data on stream: {test_data}\n")
    print("== DataStream statistics ==")
    stream = Datastream()
    numpro = NumericProcessor()
    textpro = TextProcessor()
    logpro = LogProcessor()
    stream.register_processor(numpro)
    stream.register_processor(textpro)
    stream.register_processor(logpro)
    stream.process_stream(test_data)
    stream.print_processors_stats()
    print()
    nb = 3
    csv = CSVExportPlugin()
    json = JSONExportPlugin()
    print(f"Send {nb} processed data from each processor to a CSV plugin:")
    stream.output_pipeline(nb, csv)
    print()
    print("== DataStream statistics ==")
    stream.print_processors_stats()
    print()
    test_data2 = [21, ['I love AI', 'LLMs are wonderful', 'Stay healthy'],
                      [{'log_level': 'ERROR',
                        'log_message': '500 server crash'},
                       {'log_level': 'NOTICE',
                        'log_message': 'Certificate expires in 10 days'}],
                      [32, 42, 64, 84, 128, 168], 'World hello']
    print(f"Send another batch of data: {test_data2}\n")
    print("== DataStream statistics ==")
    stream.process_stream(test_data2)
    stream.print_processors_stats()
    print()
    nb = 5
    print(f"Send {nb} processed data from each processor to a JSON plugin:")
    stream.output_pipeline(nb, json)
    print()
    print("== DataStream statistics ==")
    stream.print_processors_stats()