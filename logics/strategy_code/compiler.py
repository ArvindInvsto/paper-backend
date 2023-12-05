from fastapi import FastAPI, HTTPException, status
import ast
import os, io
import sys
import traceback
import tempfile
from multiprocessing import Process,Queue,Event
from atom import Atom
from importlib.machinery import SourceFileLoader

app = FastAPI() 

allowed_packages = ['numpy', 'pandas','math', 'random', 'x', 'square', 'tal', 'threading', 'time', 'importlib.machinery', 'SourceFileLoader', 'os', 'datetime', 'atom']

class OutputRedirector:
    def __init__(self):
        self.output = ''

    def write(self, text):
        self.output += text

    def flush(self):
        pass

    def get_output(self):
        return self.output.strip()

class ErrorCollector(ast.NodeVisitor):
    def __init__(self):
        self.errors = []

    def visit_ExceptHandler(self, node):
        self.errors.append(node.lineno)

class ImportVisitor(ast.NodeVisitor):
    unallowed = []

    def visit_Import(self, node):
        for alias in node.names:
            if alias.name not in allowed_packages:
                self.unallowed.append(alias.name)

    def visit_ImportFrom(self, node):
        if node.module not in allowed_packages:
            self.unallowed.append(node.module)

class StrategyProcess(Process):
    def __init__(self, file_path, strategy_timeout_seconds, output_queue,completion_event):
        super().__init__()
        self.file_path = file_path
        self.stdout_redirector = OutputRedirector()
        self.output_queue = output_queue
        self.strategy_timeout_seconds = strategy_timeout_seconds
        self.completion_event = completion_event

    def run(self):
        self.execute_atom_strategy(self.file_path, self.strategy_timeout_seconds)

    def execute_atom_strategy(self, file_path, strategy_timeout_seconds):
        try:
            settings = {
            "strategy_id": "S005",
            "strategy": "GoldenCrossOver",
            "market": "India",
            "instruments": ["SBIN.NS"],
            "qty": 1,
            "exchange": "NSE",
            "instrument_type": "equity",
            "broker": "paper",
            "runType": "Debug",
            "data_source": "yfinance",
            }

            user_strategy_module = SourceFileLoader('user_strategy_module', file_path).load_module()
            user_strategy_class = user_strategy_module.UserStrategy
            print(user_strategy_class)

            at = Atom(strategy=user_strategy_class, setting=settings)
            sys.stdout = self.stdout_redirector
            at.run()
            sys.stdout = sys.__stdout__
        except Exception as ex:
            return {"status": "Error", "output": f"Syntax error at line {ex}"}
            

        # print("Here",self.stdout_redirector.get_output())
        output = self.stdout_redirector.get_output()
        self.completion_event.set()
        self.output_queue.put(output)
        # print("out", self.output_queue.get())

def compile_code(code, process_timeout_seconds=59, strategy_timeout_seconds=59):
    try:
        tree = ast.parse(code)
    except SyntaxError as ex:
        return {"status": "Error", "output": f"Syntax error at line {ex.lineno}: {ex.msg}"}
    
    visitor = ImportVisitor()
    
    visitor.visit(tree)
    
    if len(visitor.unallowed) > 0:
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                            detail=f" These packages are not allowed. {visitor.unallowed}")

    error_collector = ErrorCollector()
    error_collector.visit(tree)

    if error_collector.errors:
        return {"status": "Error", "output": f"Error in code at line {error_collector.errors[0]}"}

    try:
        compiled_code = compile(tree, filename='', mode='exec')
        output_stream = io.StringIO()
        sys.stdout = output_stream
        try:
            exec(compiled_code)
        except Exception as ex:
            _, _, tb = sys.exc_info()
            line_number = traceback.extract_tb(tb)[-1][1]
            error_message = f"Error at line {line_number}: {ex}"
            return {"status": "Error", "message": error_message}
    finally:
        # Restore the standard output
        sys.stdout = sys.__stdout__
        
    script_dir = os.path.dirname(os.path.abspath(__file__))

    def run_with_timeout():
        sys.stdout = sys.__stdout__
        captured_output = output_stream.getvalue()
        print("Captured Output:", captured_output)
        output = captured_output
        print(code)
        try:

            with tempfile.NamedTemporaryFile(dir=script_dir,delete=False, suffix=".py") as temp_file:
                temp_filename = temp_file.name
                temp_file.write(code.encode('utf-8'))
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), temp_filename)
            print(file_path)

            output_queue = Queue()
            completion_event = Event()
            strategy_process = StrategyProcess(file_path,strategy_timeout_seconds, output_queue, completion_event)
            strategy_process.start()
            completion_event.wait(process_timeout_seconds)
            
            if not completion_event.is_set():
                strategy_process.terminate()
                strategy_process.join()
                return {"status": "Strategy Compilation TimedOut", "output": ""}

            
            output = output + output_queue.get()
            print("out",output)

            return {"status": "Strategy compiled successfully", "output": output}
        except:
            print(traceback.format_exc())
            output += {"status": "Error", "output": traceback.format_exc()}
        finally:
            try:
                os.remove(temp_filename)
                print("Temporary file deleted successfully")
            except Exception as e:
                print(f"Error deleting temporary file: {e}")

    try:
        output = run_with_timeout()
        return output
    except Exception as ex:
        print(traceback.format_exc())
        return {"status": "Error", "output": traceback.format_exc()}

