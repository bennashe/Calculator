import tkinter as tk
from tkinter import ttk
import math

class AdvancedCalculator:
    def __init__(self, master):
        self.master = master
        master.title("高级多功能计算器")
        master.geometry("600x400")

        self.notebook = ttk.Notebook(master)
        self.notebook.pack(expand=1, fill="both")

        self.standard_frame = ttk.Frame(self.notebook)
        self.scientific_frame = ttk.Frame(self.notebook)
        self.unit_converter_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.standard_frame, text="标准")
        self.notebook.add(self.scientific_frame, text="科学")
        self.notebook.add(self.unit_converter_frame, text="单位转换")
        self.notebook.add(self.history_frame, text="历史")

        self.create_standard_calculator()
        self.create_scientific_calculator()
        self.create_unit_converter()
        self.create_history_view()

        self.history = []

    def create_standard_calculator(self):
        self.standard_display = tk.Entry(self.standard_frame, width=40, justify='right')
        self.standard_display.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', 'C', '+'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.standard_click(x)
            tk.Button(self.standard_frame, text=button, command=cmd, width=10, height=2).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 3:
                col = 0
                row += 1

        tk.Button(self.standard_frame, text='=', command=self.standard_calculate, width=43, height=2).grid(row=row, column=0, columnspan=4, padx=2, pady=2)

    def create_scientific_calculator(self):
        self.scientific_display = tk.Entry(self.scientific_frame, width=60, justify='right')
        self.scientific_display.grid(row=0, column=0, columnspan=6, padx=5, pady=5)

        buttons = [
            '7', '8', '9', '/', 'sin', 'asin',
            '4', '5', '6', '*', 'cos', 'acos',
            '1', '2', '3', '-', 'tan', 'atan',
            '0', '.', 'C', '+', 'sqrt', 'x^2',
            '(', ')', '=', 'log', 'ln', 'x^y'
        ]

        row = 1
        col = 0
        for button in buttons:
            cmd = lambda x=button: self.scientific_click(x)
            tk.Button(self.scientific_frame, text=button, command=cmd, width=7, height=2).grid(row=row, column=col, padx=2, pady=2)
            col += 1
            if col > 5:
                col = 0
                row += 1

    def create_unit_converter(self):
        units = {
            "长度": ["米", "厘米", "英寸", "英尺"],
            "重量": ["千克", "克", "磅", "盎司"],
            "温度": ["摄氏度", "华氏度", "开尔文"]
        }

        self.unit_type = tk.StringVar()
        self.unit_type.set("长度")
        self.from_unit = tk.StringVar()
        self.to_unit = tk.StringVar()

        ttk.Label(self.unit_converter_frame, text="转换类型:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Combobox(self.unit_converter_frame, textvariable=self.unit_type, values=list(units.keys()), state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(self.unit_converter_frame, text="从:").grid(row=1, column=0, padx=5, pady=5)
        self.from_unit_combo = ttk.Combobox(self.unit_converter_frame, textvariable=self.from_unit, state="readonly")
        self.from_unit_combo.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(self.unit_converter_frame, text="到:").grid(row=2, column=0, padx=5, pady=5)
        self.to_unit_combo = ttk.Combobox(self.unit_converter_frame, textvariable=self.to_unit, state="readonly")
        self.to_unit_combo.grid(row=2, column=1, padx=5, pady=5)

        self.unit_type.trace('w', self.update_unit_options)

        self.value_entry = tk.Entry(self.unit_converter_frame)
        self.value_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

        ttk.Button(self.unit_converter_frame, text="转换", command=self.convert_units).grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.result_label = ttk.Label(self.unit_converter_frame, text="")
        self.result_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    def create_history_view(self):
        self.history_listbox = tk.Listbox(self.history_frame, width=60, height=20)
        self.history_listbox.pack(padx=5, pady=5)
        
        # 添加清除历史按钮
        clear_button = tk.Button(self.history_frame, text="清除历史", command=self.clear_history)
        clear_button.pack(pady=5)

    def standard_click(self, key):
        if key == 'C':
            self.standard_display.delete(0, tk.END)
        else:
            self.standard_display.insert(tk.END, key)

    def scientific_click(self, key):
        if key == 'C':
            self.scientific_display.delete(0, tk.END)
        elif key in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sqrt', 'log', 'ln']:
            self.scientific_display.insert(tk.END, key + '(')
        elif key == 'x^2':
            self.scientific_display.insert(tk.END, '**2')
        elif key == 'x^y':
            self.scientific_display.insert(tk.END, '**')
        elif key == '=':
            self.scientific_calculate()
        else:
            self.scientific_display.insert(tk.END, key)

    def standard_calculate(self):
        try:
            expression = self.standard_display.get()
            result = eval(expression)
            self.standard_display.delete(0, tk.END)
            self.standard_display.insert(tk.END, str(result))
            self.add_to_history(expression, result)
        except:
            self.standard_display.delete(0, tk.END)
            self.standard_display.insert(tk.END, "错误")

    def scientific_calculate(self):
        try:
            expression = self.scientific_display.get()
            # 替换数学函数
            for old, new in [('sin', 'math.sin'), ('cos', 'math.cos'), ('tan', 'math.tan'),
                             ('asin', 'math.asin'), ('acos', 'math.acos'), ('atan', 'math.atan'),
                             ('sqrt', 'math.sqrt'), ('log', 'math.log10'), ('ln', 'math.log')]:
                expression = expression.replace(old, new)
            
            result = eval(expression)
            self.scientific_display.delete(0, tk.END)
            self.scientific_display.insert(tk.END, str(result))
            self.add_to_history(self.scientific_display.get(), result)
        except:
            self.scientific_display.delete(0, tk.END)
            self.scientific_display.insert(tk.END, "错误")

    def update_unit_options(self, *args):
        units = {
            "长度": ["米", "厘米", "英寸", "英尺"],
            "重量": ["千克", "克", "磅", "盎司"],
            "温度": ["摄氏度", "华氏度", "开尔文"]
        }
        unit_type = self.unit_type.get()
        self.from_unit_combo['values'] = units[unit_type]
        self.to_unit_combo['values'] = units[unit_type]
        self.from_unit.set(units[unit_type][0])
        self.to_unit.set(units[unit_type][1])

    def convert_units(self):
        try:
            value = float(self.value_entry.get())
            from_unit = self.from_unit.get()
            to_unit = self.to_unit.get()
            result = self.perform_conversion(value, from_unit, to_unit)
            self.result_label.config(text=f"{value} {from_unit} = {result:.4f} {to_unit}")
            self.add_to_history(f"{value} {from_unit} = {result:.4f} {to_unit}")
        except ValueError as e:
            self.result_label.config(text=str(e))

    def perform_conversion(self, value, from_unit, to_unit):
        # 长度转换
        length_units = {
            "米": 1,
            "厘米": 0.01,
            "英寸": 0.0254,
            "英尺": 0.3048
        }
        
        # 重量转换
        weight_units = {
            "千克": 1,
            "克": 0.001,
            "磅": 0.453592,
            "盎司": 0.0283495
        }
        
        # 温度转换
        def c_to_f(c):
            return c * 9/5 + 32
        
        def f_to_c(f):
            return (f - 32) * 5/9
        
        def c_to_k(c):
            return c + 273.15
        
        def k_to_c(k):
            return k - 273.15

        if from_unit == to_unit:
            return value

        if from_unit in length_units and to_unit in length_units:
            return value * length_units[from_unit] / length_units[to_unit]
        
        if from_unit in weight_units and to_unit in weight_units:
            return value * weight_units[from_unit] / weight_units[to_unit]
        
        if from_unit == "摄氏度" and to_unit == "华氏度":
            return c_to_f(value)
        if from_unit == "华氏度" and to_unit == "摄氏度":
            return f_to_c(value)
        if from_unit == "摄氏度" and to_unit == "开尔文":
            return c_to_k(value)
        if from_unit == "开尔文" and to_unit == "摄氏度":
            return k_to_c(value)
        if from_unit == "华氏度" and to_unit == "开尔文":
            return c_to_k(f_to_c(value))
        if from_unit == "开尔文" and to_unit == "华氏度":
            return c_to_f(k_to_c(value))

        # 如果没有匹配的转换
        raise ValueError(f"无法转换 {from_unit} 到 {to_unit}")

    def add_to_history(self, expression, result):
        entry = f"{expression} = {result}"
        self.history.append(entry)
        self.history_listbox.insert(tk.END, entry)

    def clear_history(self):
        self.history = []
        self.history_listbox.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = AdvancedCalculator(root)
    root.mainloop()

