import os
import sys

# 设置环境变量来禁用 PyQt5 的弃用警告
os.environ['PYTHONWARNINGS'] = 'ignore::DeprecationWarning'

import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

class MathProblemGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('小学数学题生成器')
        self.setGeometry(100, 100, 800, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 输入布局
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel('数字范围（1-1000）：'))
        self.rangeInput = QLineEdit()
        self.rangeInput.setText('100')
        input_layout.addWidget(self.rangeInput)
        
        input_layout.addWidget(QLabel('题目数量：'))
        self.problemCountInput = QLineEdit()
        self.problemCountInput.setText('20')
        input_layout.addWidget(self.problemCountInput)
        
        input_layout.addWidget(QLabel('混合题目数量：'))
        self.mixedCountInput = QLineEdit()
        self.mixedCountInput.setText('5')
        input_layout.addWidget(self.mixedCountInput)
        
        self.generateButton = QPushButton('生成题目')
        self.generateButton.clicked.connect(self.generate_problems)
        input_layout.addWidget(self.generateButton)
        
        layout.addLayout(input_layout)
        
        # 显示题目的文本框
        self.problemsText = QTextEdit()
        self.problemsText.setReadOnly(True)
        self.problemsText.setPlaceholderText('生成的题目将显示在这里...')
        layout.addWidget(self.problemsText)
        
        central_widget.setLayout(layout)

    def greet(self):
        print('Hello Python')
        print("Hi Python~")

    def generate_problems(self):
        try:
            max_number = int(self.rangeInput.text())
            if max_number < 1 or max_number > 1000:
                self.problemsText.setText('请输入1-1000之间的数字！')
                return
            
            # 读取题目数量
            problem_count = int(self.problemCountInput.text())
            if problem_count < 1 or problem_count > 100:
                self.problemsText.setText('请输入1-100之间的题目数量！')
                return
            
            # 读取混合题目数量
            mixed_count = int(self.mixedCountInput.text())
            if mixed_count < 0 or mixed_count > problem_count:
                self.problemsText.setText('混合题目数量不能超过总题目数量！')
                return
            
            # 分别生成普通题目和混合题目
            normal_problems = []
            mixed_problems = []
            
            # 生成普通题目
            normal_count = problem_count - mixed_count
            for i in range(normal_count):
                problem_index = i + 1  # 普通题目从1开始编号
                
                # 随机选择题目类型
                problem_type = random.choice(['result', 'addend', 'minuend', 'subtrahend'])
                
                if problem_type == 'result':
                    # 计算结果的题目
                    operation = random.choice(['+', '-'])
                    if operation == '+':
                        num1 = random.randint(1, max_number)
                        num2 = random.randint(1, max_number - num1)
                        problem = f"{problem_index}. {num1} + {num2} = "
                    else:
                        num1 = random.randint(1, max_number)
                        num2 = random.randint(1, num1)
                        problem = f"{problem_index}. {num1} - {num2} = "
                elif problem_type == 'addend':
                    # 计算加数的题目
                    num2 = random.randint(1, max_number - 1)
                    result = random.randint(num2 + 1, max_number)
                    problem = f"{problem_index}. ? + {num2} = {result}"
                elif problem_type == 'minuend':
                    # 计算被减数的题目
                    num2 = random.randint(1, max_number - 1)
                    result = random.randint(1, max_number - num2)
                    problem = f"{problem_index}. ? - {num2} = {result}"
                else:  # subtrahend
                    # 计算减数的题目
                    num1 = random.randint(2, max_number)
                    result = random.randint(1, num1 - 1)
                    problem = f"{problem_index}. {num1} - ? = {result}"
                
                normal_problems.append(problem)
            
            # 生成混合题目
            for i in range(mixed_count):
                problem_index = normal_count + i + 1  # 混合题目从普通题目数量+1开始编号
                
                # 连加或加减混合算式（限制为3个数，2个运算符）
                num_count = 3  # 固定为3个数
                nums = []
                operations = []
                
                # 随机决定是否生成缺少加数或减数的题目
                missing_part = random.choice(['none', 'addend', 'subtrahend'])
                
                if missing_part == 'none':
                    # 生成完整的混合算式
                    # 生成第一个数
                    current_num = random.randint(1, max_number // 2)
                    nums.append(current_num)
                    
                    # 生成后续的运算和数字（2个运算符，3个数）
                    for j in range(num_count - 1):
                        # 随机选择运算符
                        operation = random.choice(['+', '-'])
                        operations.append(operation)
                        
                        if operation == '+':
                            # 加法：确保和不超过最大值
                            next_num = random.randint(1, max_number - current_num)
                            current_num += next_num
                        else:
                            # 减法：确保结果不为负数
                            next_num = random.randint(1, current_num)
                            current_num -= next_num
                        
                        nums.append(next_num)
                    
                    # 构建混合算式
                    problem_parts = []
                    for k in range(len(nums)):
                        problem_parts.append(str(nums[k]))
                        if k < len(operations):
                            problem_parts.append(operations[k])
                    
                    problem = f"{problem_index}. {' '.join(problem_parts)} = "
                else:
                    # 生成缺少加数或减数的混合算式
                    # 首先生成完整的算式
                    current_num = random.randint(1, max_number // 2)
                    nums.append(current_num)
                    
                    for j in range(num_count - 1):
                        operation = random.choice(['+', '-'])
                        operations.append(operation)
                        
                        if operation == '+':
                            next_num = random.randint(1, max_number - current_num)
                            current_num += next_num
                        else:
                            next_num = random.randint(1, current_num)
                            current_num -= next_num
                        
                        nums.append(next_num)
                    
                    # 随机选择一个位置来替换为问号
                    # 对于3个数的算式，有3个数字位置
                    missing_index = random.randint(0, len(nums) - 1)
                    
                    # 构建混合算式，将选定位置替换为问号
                    problem_parts = []
                    for k in range(len(nums)):
                        if k == missing_index:
                            problem_parts.append('?')
                        else:
                            problem_parts.append(str(nums[k]))
                        if k < len(operations):
                            problem_parts.append(operations[k])
                    
                    # 计算结果
                    # 重新计算结果，确保正确
                    result = nums[0]
                    for j in range(len(operations)):
                        if operations[j] == '+':
                            result += nums[j+1]
                        else:
                            result -= nums[j+1]
                    
                    problem = f"{problem_index}. {' '.join(problem_parts)} = {result}"
                
                mixed_problems.append(problem)
            
            # 合并题目：普通题目在前，混合题目在后
            all_problems = normal_problems + mixed_problems
            
            # 按列排列，每列10个
            columns = []
            column_size = 10
            for i in range(0, len(all_problems), column_size):
                columns.append(all_problems[i:i+column_size])
            
            # 构建列布局
            max_rows = len(columns[0]) if columns else 0
            formatted_problems = []
            for row in range(max_rows):
                row_problems = []
                for col in columns:
                    if row < len(col):
                        # 确保每列宽度一致，调整为更紧凑的宽度
                        row_problems.append(col[row].ljust(25))
                formatted_problems.append(''.join(row_problems))
            
            # 显示题目
            self.problemsText.setText('\n'.join(formatted_problems))
        except ValueError:
            self.problemsText.setText('请输入有效的数字！')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MathProblemGenerator()
    window.show()
    sys.exit(app.exec_())