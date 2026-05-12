import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ailms_project.settings')
django.setup()

from ailms_app.models import Course, Quiz, Result, Resume
from ailms_app.pdf_utils import segment_into_chapters
import fitz  # PyMuPDF


def make_pdf_multipage(chapters_list, pdf_path):
    """Generate a multi-page PDF  -  one page per chapter."""
    doc = fitz.open()
    for chapter_text in chapters_list:
        page = doc.new_page(width=595, height=842)
        rect = fitz.Rect(50, 50, 545, 800)
        page.insert_textbox(rect, chapter_text, fontsize=10, fontname="helv", color=(0, 0, 0), align=0)
    doc.save(pdf_path)
    doc.close()


# ===========================================================================
# PYTHON COURSE  -  5 CHAPTERS (Introduction -> Basics -> Core -> Advanced -> Expert)
# ===========================================================================
PYTHON_CHAPTERS = [

# --- Chapter 1: Introduction -----------------------------------------------
"""Chapter 1: Introduction to Python

What Is Python?
Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum and first released to the public in 1991. Its name is a nod to the British comedy group Monty Python, reflecting the language's spirit of fun and approachability. Today Python is one of the most widely used programming languages in the world, consistently ranking in the top three of every major language popularity index, including TIOBE, PYPL, and the Stack Overflow Developer Survey.

The Design Philosophy
Python's guiding principles are documented in 'PEP 20  -  The Zen of Python', a collection of 19 aphorisms written by Tim Peters. Central ideas include: "Beautiful is better than ugly", "Explicit is better than implicit", "Simple is better than complex", "Readability counts", and "There should be one  -  and preferably only one  -  obvious way to do it." These principles explain why Python code tends to look clean, structured, and almost like English prose compared to other languages.

A Brief History
Guido van Rossum began designing Python in the late 1980s while working at Centrum Wiskunde & Informatica (CWI) in the Netherlands, as a successor to the ABC language. Python 1.0 was released in January 1994. Python 2.0 arrived in 2000, adding list comprehensions, garbage collection, and Unicode support. Python 3.0, released in December 2008, was a deliberate backward-incompatible revision that cleaned out years of technical debt. Python 2 reached its official end-of-life in January 2020.

Key Features
Python is dynamically typed: you do not declare variable types  -  the interpreter infers them at runtime. Python is garbage-collected, meaning memory is managed automatically. It is multi-paradigm, supporting procedural, object-oriented, and functional programming styles. The language ships with a huge "batteries included" standard library and enjoys an even larger ecosystem of third-party packages on the Python Package Index (PyPI), which hosts over 450,000 projects.

Where Python Is Used
Data Science and Machine Learning: Libraries like NumPy, Pandas, Scikit-Learn, TensorFlow, and PyTorch have made Python the dominant language for AI research and production ML systems. Web Development: Frameworks like Django and Flask power millions of websites. Scripting and Automation: Python scripts replace manual repetitive tasks in system administration, testing pipelines, and DevOps workflows. Scientific Computing: Researchers in physics, biology, and astronomy rely on SciPy, Matplotlib, and Jupyter Notebooks. Cybersecurity: Penetration testers and security researchers write exploit scripts and analysis tools in Python.

Major Companies Using Python
Google, Instagram, Spotify, Dropbox, Netflix, NASA, CERN, Reddit, and YouTube all use Python extensively in their production systems. Google even employs a dedicated "Python team" that maintains CPython (the reference implementation) and contributes upstream.

Getting Started
Python is free and open-source. You can download the latest version from python.org. The REPL (Read-Eval-Print Loop) lets you type Python statements interactively and see results immediately  -  ideal for experimentation. After installing, try: print("Hello, Python!")  -  that single line is a complete, runnable Python program. No semicolons. No curly braces. No class declarations just to print text. That simplicity is Python's signature.

Why Learn Python First?
Python is often the recommended first language for beginners because its syntax is forgiving and readable, the feedback loop is instant, and the same language scales all the way to complex production systems. Whether you want to build websites, analyze data, train machine learning models, or automate boring tasks, Python is the right tool for the job.
""",


# --- Chapter 2: Basics -------------------------------------------------------
"""Chapter 2: Python Basics  -  Variables, Types, and Operators

Variables and Assignment
In Python, a variable is simply a name that points to an object in memory. You create a variable with an assignment statement: x = 42. Unlike C, Java, or C++, you never write int x = 42  -  the type is inferred automatically. Python is dynamically typed, meaning one variable can hold an integer, then be reassigned to a string in the very next line. Variable names are case-sensitive (age and Age are different), and by convention use snake_case (total_price, user_name).

Core Data Types
int  -  Whole numbers of arbitrary size. Python 3 integers have no overflow: 2 ** 100 is computed exactly. float  -  IEEE 754 double-precision floating-point numbers. Be aware of floating-point rounding: 0.1 + 0.2 == 0.30000000000000004. str  -  Immutable sequences of Unicode code points. Strings can be written with single quotes, double quotes, or triple quotes for multi-line text. bool  -  A subclass of int. True and False are the only two boolean values. NoneType  -  The None singleton represents the absence of a value, similar to null in other languages.

Type Checking and Conversion
Use the built-in type() function to check a variable's type: type(3.14) returns <class 'float'>. Convert between types with int(), float(), str(), and bool(): int("42") returns the integer 42. Implicit conversion (coercion) is minimal in Python; you must be explicit, which prevents surprising bugs.

Strings in Depth
Strings are defined with 'single', "double", or """triple""" quotes. Escape sequences like \\n (newline), \\t (tab), and \\\\ (literal backslash) work inside strings. Raw strings (r"C:\\Users\\name") suppress escape processing  -  useful for file paths and regular expressions. F-strings (formatted string literals), introduced in Python 3.6, allow embedding expressions directly: name = "Alice"; print(f"Hello, {name}!")  -  this is the modern, preferred formatting method.

Arithmetic Operators
Python supports all standard arithmetic: + (addition), - (subtraction), * (multiplication), / (true division, always returns float), // (floor division, truncates toward negative infinity), % (modulo, returns remainder), ** (exponentiation). The divide-and-assign operator /= and friends (+=, -=, *=, //=, **=, %=) update a variable in place.

Comparison and Logical Operators
Comparison operators return booleans: == (equal), != (not equal), < (less than), > (greater than), <= (less than or equal to), >= (greater than or equal to). Logical operators combine boolean expressions: and returns True if both sides are True, or returns True if at least one side is True, not negates. Python also supports chained comparisons: 0 < x < 100 is valid and idiomatic.

The print() Function
print() outputs to standard output and automatically adds a newline. Multiple arguments are separated by a space by default: print("Score:", 95). You can customize with sep and end parameters: print("a", "b", "c", sep="-", end="!\\n") prints a-b-c! on one line.

The input() Function
input() reads a line of text from the user and returns it as a string: name = input("Enter your name: "). Always convert with int() or float() if you expect a number: age = int(input("Age: ")).

Comments and Documentation
Single-line comments start with #. Multi-line docstrings use triple quotes and are attached to functions, classes, or modules: they are accessible via help() and form the backbone of Python's documentation ecosystem.
""",


# --- Chapter 3: Core Concepts -----------------------------------------------
"""Chapter 3: Core Python  -  Control Flow, Functions, and Data Structures

Control Flow
The if statement selects which block to execute based on a condition. In Python, indentation (4 spaces by convention) defines the block  -  there are no curly braces. The elif (else-if) and else clauses handle additional and default cases. You can chain as many elif branches as needed.

Example:
score = 85
if score >= 90:
    grade = "A"
elif score >= 75:
    grade = "B"
else:
    grade = "C"

Loops
The for loop iterates over any iterable: a list, string, range, tuple, dict, or file. range(start, stop, step) generates a lazy sequence of integers  -  range(0, 10, 2) gives 0, 2, 4, 6, 8. The while loop repeats as long as a condition is True. break exits the loop immediately; continue skips the rest of the current iteration and jumps to the next; the else clause on a loop runs only if the loop ended normally (no break).

List Comprehensions
A list comprehension is one of Python's most loved features: [expression for item in iterable if condition]. squares = [x**2 for x in range(1, 11)] creates [1, 4, 9, 16, 25, 36, 49, 64, 81, 100] in a single, readable line. Dictionary and set comprehensions follow the same pattern.

Functions
def is the keyword to define a function. A function encapsulates a reusable block of logic. Parameters can have default values: def greet(name, greeting="Hello"). Keyword arguments let you pass values by name in any order: greet(greeting="Hi", name="Bob"). *args collects extra positional arguments as a tuple; **kwargs collects extra keyword arguments as a dict. Functions always return a value; without an explicit return statement they return None.

Scope and the LEGB Rule
Python looks up variables in this order: Local -> Enclosing -> Global -> Built-in. A variable created inside a function is local and not accessible outside. Use the global keyword to modify a global variable from inside a function (discouraged  -  prefer returning values).

Lists
Lists are mutable, ordered sequences: fruits = ["apple", "banana", "cherry"]. Access by zero-based index: fruits[0] == "apple". Negative indices count from the end: fruits[-1] == "cherry". Slices create sub-lists: fruits[1:3] == ["banana", "cherry"]. Key methods: append(), extend(), insert(), remove(), pop(), sort(), reverse(), index(), count().

Dictionaries
Dicts are mutable key-value maps: person = {"name": "Alice", "age": 30}. Access: person["name"]. Safe access with default: person.get("city", "Unknown"). Iteration: for key, value in person.items(). Dicts preserve insertion order in Python 3.7+. Dict comprehensions: {k: v**2 for k, v in data.items()}.

Tuples and Sets
Tuples are immutable, ordered sequences  -  useful for fixed data. Sets are unordered collections of unique elements with O(1) membership testing. Set operations: union |, intersection &, difference -, symmetric difference ^.

Exception Handling
try / except catches runtime errors gracefully. Multiple except clauses handle different exception types. finally always runs (cleanup). raise re-raises or throws a new exception. Custom exception classes inherit from Exception.
""",


# --- Chapter 4: Advanced Python ---------------------------------------------
"""Chapter 4: Advanced Python  -  OOP, Modules, Iterators, and Decorators

Object-Oriented Programming (OOP)
Python is fully object-oriented. Every value is an object  -  even integers and functions. A class is a blueprint; an object is an instance of that blueprint. The class keyword defines a class. The __init__ method is the constructor, called automatically when you create an instance. The first parameter of every instance method is self  -  a reference to the current object.

Inheritance
A child class inherits attributes and methods from its parent: class Dog(Animal). super() calls the parent's implementation. Python supports multiple inheritance: class C(A, B). The MRO (Method Resolution Order) determines which parent's method is called when both have the same name.

Dunder (Magic) Methods
Methods named __method__ are called "dunder" (double-underscore) or "magic" methods. They let you customize how objects behave with built-in operations. __repr__ and __str__ control string representation. __len__ makes len(obj) work. __add__ enables the + operator. __iter__ and __next__ make an object iterable. __enter__ and __exit__ enable the with statement (context managers).

Properties and Encapsulation
@property turns a method into a read-only attribute. @attribute.setter adds a setter. Name mangling: attributes prefixed with __ (double underscore) are made class-private by the interpreter (e.g., __balance becomes _ClassName__balance). Convention: a single underscore prefix (_x) means "internal use"  -  do not access from outside.

Generators and Iterators
An iterator is any object with __iter__ and __next__. Generators are a simpler way to create iterators using yield: def countdown(n): while n > 0: yield n; n -= 1. Generator expressions are like list comprehensions but lazy: (x**2 for x in range(1000000)) does not build a list in memory.

Decorators
A decorator is a function that takes another function and returns a modified version. The @ syntax is syntactic sugar: @timer def my_func(): ... is equivalent to my_func = timer(my_func). Decorators are used everywhere: Flask and Django use @app.route() and @login_required(). functools.wraps preserves the decorated function's metadata.

Context Managers
The with statement guarantees cleanup code runs even if an exception occurs. with open("file.txt") as f: is the canonical way to handle files  -  f.close() is called automatically. You can write custom context managers with __enter__/__exit__ or with the @contextmanager decorator from contextlib.

Modules and Packages
A module is a .py file. import math; math.sqrt(16). from datetime import datetime. Packages are directories with __init__.py. Virtual environments (python -m venv env) isolate dependencies per project. pip install package-name installs from PyPI.

Comprehensions and Functional Tools
map(fn, iterable) applies fn lazily. filter(fn, iterable) filters lazily. functools.reduce() accumulates a result. itertools provides combinatorial generators: combinations(), permutations(), product(), chain(), groupby(), islice().

Type Hints
Python 3.5+ supports optional type annotations: def add(a: int, b: int) -> int. These are not enforced at runtime but are used by static type checkers like mypy and editors for autocomplete and early error detection.
""",


# --- Chapter 5: Expert Python ---------------------------------------------
"""Chapter 5: Expert Python  -  Concurrency, Performance, Testing, and Ecosystem

Concurrency and Parallelism
Python has three main concurrency models. Threading (threading module): OS threads share memory. The Global Interpreter Lock (GIL) prevents multiple threads from executing Python bytecode simultaneously, limiting CPU-bound parallelism. Threading is effective for I/O-bound tasks (network requests, file reads). Multiprocessing (multiprocessing module): spawns separate processes, each with its own interpreter and memory space, bypassing the GIL. Ideal for CPU-bound workloads. Asyncio: a single-threaded event loop for cooperative multitasking using async/await syntax. Best for high-throughput I/O-bound servers (hundreds of thousands of network connections).

async / await
async def defines a coroutine. await suspends the coroutine until its target is ready. asyncio.run() is the entry point. aiohttp is an async HTTP client/server. FastAPI is built on asyncio for ultra-high-performance REST APIs. Understanding when to use threads vs. processes vs. async is a hallmark of expert Python.

Performance Optimization
Profile before optimizing: python -m cProfile my_script.py. For numerical code, NumPy operations vectorized in C are orders of magnitude faster than Python loops. Cython compiles annotated Python to C. Numba JIT-compiles numerical functions. PyPy is an alternative Python interpreter using JIT compilation for up to ~10x speedups on many workloads. functools.lru_cache / @cache memoizes expensive function results. Avoid repeated string concatenation  -  use "".join(parts) instead.

Memory Management
Python uses reference counting combined with a cyclic garbage collector. The del statement removes a name binding; the object is freed when its reference count reaches zero. The sys module exposes ref counts and memory usage. tracemalloc profiles memory allocations. For data-heavy work, use NumPy arrays (typed, contiguous memory) instead of Python lists of objects.

Testing
pytest is the industry standard. Write test functions prefixed with test_. pytest auto-discovers them. Fixtures provide reusable setup/teardown. Parametrize runs one test with multiple inputs. unittest is the built-in alternative. coverage.py measures what percentage of your code is covered by tests. TDD (Test-Driven Development): write the test first, then the implementation.

Logging and Debugging
Use logging instead of print for production code. Set levels: DEBUG, INFO, WARNING, ERROR, CRITICAL. Configure handlers to write to files, rotate logs, and format output as JSON for log aggregation systems. pdb (Python Debugger): import pdb; pdb.set_trace() opens an interactive REPL at that line. In Python 3.7+ use breakpoint()  -  it respects the PYTHONBREAKPOINT environment variable.

Packaging and Distribution
A modern Python package uses pyproject.toml (PEP 517/518) as the build configuration. Tools: Poetry, Hatch, and setuptools. Publish to PyPI with twine upload dist/*. Semantic versioning (MAJOR.MINOR.PATCH) communicates the impact of changes to users.

The Ecosystem at a Glance
Web: Django (batteries-included), Flask (micro), FastAPI (async, auto-docs). Data: NumPy, Pandas, Polars (Rust-backed DataFrame library). ML: Scikit-Learn, XGBoost, LightGBM. Deep Learning: PyTorch (research), TensorFlow/Keras (production). Visualization: Matplotlib, Seaborn, Plotly, Altair. ORMs: SQLAlchemy, Django ORM. CLI: Click, Typer. Configuration: Pydantic (data validation with type hints).

Pythonic Code Principles
Idiomatic Python ("Pythonic") means using the language's features naturally: prefer list comprehensions over map/filter, use enumerate instead of manual index counters, unpack tuples rather than indexing, use context managers for resources, and rely on duck typing rather than isinstance() checks. Code reviewed by seasoned Python developers will consistently return to readability, explicitness, and simplicity.
""",
]


# ===========================================================================
# AI & ML COURSE  -  5 CHAPTERS
# ===========================================================================
AI_CHAPTERS = [

# --- Chapter 1: Introduction -----------------------------------------------
"""Chapter 1: Introduction to Artificial Intelligence

What Is Artificial Intelligence?
Artificial Intelligence (AI) is the science and engineering of creating intelligent machines  -  systems that can perform tasks that normally require human intelligence. These tasks include understanding natural language, recognizing objects in images, making decisions under uncertainty, translating between languages, generating creative content, and learning from experience. AI is not a single technology but a collection of overlapping disciplines including machine learning, natural language processing, computer vision, robotics, and knowledge representation.

A Brief History of AI
The formal birth of AI as a scientific discipline is attributed to the Dartmouth Summer Research Project of 1956, organized by John McCarthy (who coined the term "artificial intelligence"), Marvin Minsky, Nathaniel Rochester, and Claude Shannon. They believed that "every aspect of learning or any other feature of intelligence can in principle be so precisely described that a machine can be made to simulate it." Early AI research produced impressive - but narrow - results: programs that played checkers, proved theorems, and solved algebra word problems.

Two AI Winters
After periods of optimism and investment, the field experienced two "AI winters" (1974-1980 and 1987-1993) when progress stalled, funding dried up, and expectations went unmet. Researchers had underestimated the difficulty of common-sense reasoning, perception, and general intelligence.

The Deep Learning Revolution
Everything changed after 2012 when Geoffrey Hinton's team at the University of Toronto won the ImageNet image classification challenge by a massive margin using a deep convolutional neural network (AlexNet), trained on GPUs. This ignited the deep learning revolution. Since then, AI has achieved superhuman performance in image recognition, speech recognition, Go (DeepMind's AlphaGo), protein folding prediction (AlphaFold), and natural language tasks (GPT-4, Claude, Gemini).

Types of AI by Capability
Narrow AI (Weak AI): AI that is designed for a specific task  -  a chess engine, a spam filter, a face recognition system. All current commercial AI is narrow AI. General AI (AGI): A hypothetical AI that could perform any intellectual task a human can. Timelines and feasibility are hotly debated. Superintelligence: A hypothetical AI far beyond human-level intelligence across all domains. Both AGI and superintelligence remain speculative.

Core Branches of AI
Machine Learning: Systems that learn patterns from data. Natural Language Processing (NLP): Understanding and generating human language. Computer Vision: Interpreting images and video. Robotics: Perceiving and acting in the physical world. Knowledge Representation and Reasoning: Encoding facts and logical inference. Planning and Search: Finding sequences of actions to achieve goals.

Why AI Matters Now
Three forces converged to make AI practical at scale: massive datasets (the internet, social media, digitized records), powerful hardware (GPUs, TPUs, specialized AI chips), and algorithmic breakthroughs (deep learning, attention mechanisms, reinforcement learning from human feedback). The result is that AI is now embedded in everyday life  -  in smartphones, search engines, recommendation systems, medical devices, and financial markets.

Ethical Considerations from the Start
As AI becomes more capable and pervasive, ethical questions become urgent: How do we ensure AI systems are fair and unbiased? Who is accountable when an AI makes a harmful decision? How do we preserve privacy? What happens to employment? These questions are not afterthoughts  -  they must be built into the design process from day one.
""",


# --- Chapter 2: Basics -------------------------------------------------------
"""Chapter 2: Basics of Machine Learning

What Is Machine Learning?
Machine learning (ML) is a subfield of AI that focuses on building systems capable of learning from data and improving their performance on a task without being explicitly programmed with rules. Instead of writing if-then rules by hand, you provide the algorithm with examples (data) and a measure of success (a loss function), and the algorithm figures out the rules on its own.

The Machine Learning Pipeline
A typical ML project follows these stages: (1) Problem Definition  -  what exactly do you want to predict or decide? (2) Data Collection  -  gather labeled or unlabeled examples from real-world sources. (3) Data Preprocessing  -  clean, normalize, encode categorical variables, handle missing values, and split into training, validation, and test sets. (4) Feature Engineering  -  select and transform the raw variables into informative inputs for the model. (5) Model Selection  -  choose an algorithm appropriate for the problem. (6) Training  -  fit the model to the training data. (7) Evaluation  -  measure performance on held-out data using appropriate metrics. (8) Deployment  -  serve the model in production and monitor its behavior over time.

Supervised Learning
In supervised learning, the training data consists of (input, output) pairs where the correct output is known. The model learns a function f such that f(input) - output. Regression: the output is a continuous number (e.g., predicting house prices, stock returns, temperature). Classification: the output is a discrete category (e.g., spam/not-spam, cat/dog/bird, malignant/benign). Common supervised algorithms: Linear Regression, Logistic Regression, Decision Trees, Random Forests, Support Vector Machines, k-Nearest Neighbors, and Neural Networks.

Unsupervised Learning
In unsupervised learning, there are no labels. The algorithm must find structure in the data on its own. Clustering: group similar data points (K-Means, DBSCAN, Hierarchical Clustering). Dimensionality Reduction: compress high-dimensional data into fewer dimensions while preserving structure (PCA, t-SNE, UMAP). Association Rule Mining: discover relationships between variables (Apriori algorithm  -  used in market basket analysis).

Reinforcement Learning
A reinforcement learning (RL) agent learns by interacting with an environment. At each step, it chooses an action, observes the resulting state, and receives a reward (positive) or penalty (negative). The goal is to learn a policy  -  a mapping from states to actions  -  that maximizes cumulative reward over time. RL has achieved landmark results: AlphaGo, OpenAI Five (Dota 2), and robotic locomotion.

Key Metrics
Regression: Mean Absolute Error (MAE), Mean Squared Error (MSE), Root Mean Squared Error (RMSE), R- (coefficient of determination). Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC. Understanding which metric to optimize depends on the business context  -  a spam filter cares more about precision; a cancer screening system cares more about recall.

Bias-Variance Tradeoff
Underfitting (high bias): the model is too simple to capture the true patterns. Overfitting (high variance): the model memorizes the training data, including noise, and fails to generalize. The goal is to find the sweet spot. Regularization techniques (L1/Lasso, L2/Ridge), cross-validation, and proper train/validation/test splits are the primary tools for managing this tradeoff.

Tools and Libraries
Python is the dominant language for ML. Scikit-Learn provides a consistent API for classical ML algorithms. NumPy and Pandas handle numerical computation and data manipulation. Matplotlib and Seaborn visualize data and results. Jupyter Notebooks enable interactive experimentation and communication of results.
""",


# --- Chapter 3: Core Concepts -----------------------------------------------
"""Chapter 3: Core ML Algorithms  -  Regression, Classification, and Trees

Linear Regression in Depth
Linear regression models the relationship between input features X and a continuous output Y as: Y = -- + --X- + --X- + ... + --X- + -. The parameters - are estimated using Ordinary Least Squares (OLS), which minimizes the Sum of Squared Residuals (SSR). Gradient Descent is an iterative alternative used when the normal equations are computationally expensive for large datasets. Ridge Regression adds an L2 penalty (-||-||-) to shrink coefficients toward zero, reducing overfitting. Lasso Regression uses an L1 penalty (-||-||-), which can shrink some coefficients to exactly zero, effectively performing feature selection.

Logistic Regression
Logistic Regression is the go-to algorithm for binary classification. Despite its name, it outputs a probability using the sigmoid function: -(z) = 1 / (1 + e^(-z)). The decision boundary is linear: the model separates two classes with a hyperplane. The model is trained by maximizing the log-likelihood (equivalently, minimizing binary cross-entropy loss). Multi-class classification is handled by the One-vs-Rest or Softmax (multinomial logistic regression) strategies.

Decision Trees
A decision tree recursively partitions the feature space by asking yes/no questions. At each node, it chooses the split that maximizes information gain (the reduction in entropy) or minimizes Gini impurity. Advantages: highly interpretable ("CART" trees can be plotted and explained to non-technical stakeholders), no feature scaling required, handles mixed data types. Disadvantages: prone to overfitting, sensitive to small changes in the data.

Random Forests
A Random Forest trains hundreds of decision trees on different bootstrap samples of the data (bagging) and uses a random subset of features at each split. The final prediction is the majority vote (classification) or average (regression) of all trees. This reduces variance dramatically without sacrificing much bias. Feature importance scores are a valuable byproduct: they rank which input features contribute most to predictions. Random Forests are robust, accurate, and one of the best "off-the-shelf" algorithms.

Gradient Boosting Machines (GBMs)
Gradient Boosting builds trees sequentially: each new tree corrects the residual errors of all previous trees. XGBoost, LightGBM, and CatBoost are highly optimized GBM implementations that consistently win tabular data competitions (Kaggle). They support regularization, handle missing values natively, and train fast on CPU. They typically outperform Random Forests on structured/tabular data.

Support Vector Machines (SVMs)
SVMs find the maximum-margin hyperplane  -  the decision boundary that maximizes the distance (margin) to the nearest data points (support vectors). The "kernel trick" implicitly maps data into a higher-dimensional space where linear separation is possible, enabling SVMs to handle non-linear boundaries. Common kernels: linear, polynomial, and Radial Basis Function (RBF). SVMs work well in high-dimensional spaces (text classification) but scale poorly to very large datasets.

k-Nearest Neighbors (kNN)
kNN is a non-parametric, lazy learning algorithm. To classify a new point, it finds the k closest training points (by Euclidean or Manhattan distance) and returns the majority class. No explicit training phase. k is a critical hyperparameter: small k = high variance, large k = high bias. Feature scaling is essential because kNN is distance-based.

Evaluating Classifiers Beyond Accuracy
The confusion matrix shows True Positives, True Negatives, False Positives, and False Negatives. Precision = TP/(TP+FP): how many predicted positives are actually positive. Recall = TP/(TP+FN): how many actual positives are correctly identified. F1 = harmonic mean of precision and recall. The ROC curve plots True Positive Rate vs. False Positive Rate across all thresholds; AUC (Area Under Curve) summarizes it in a single number. A random classifier has AUC = 0.5; a perfect classifier has AUC = 1.0.
""",


# --- Chapter 4: Advanced AI -------------------------------------------------
"""Chapter 4: Advanced AI  -  Neural Networks and Deep Learning Architectures

Artificial Neural Networks (ANNs)
A neural network is a computational graph of layers of neurons. Each neuron computes: output = activation(W - input + b), where W is a weight matrix, b is a bias vector, and activation is a non-linear function. Stacking layers allows the network to learn hierarchical representations of data. A feedforward network (also called a Multi-Layer Perceptron or MLP) has an input layer, one or more hidden layers, and an output layer.

Activation Functions
Sigmoid: -(x) = 1/(1+e^(-x)), output in (0,1). Suffers from vanishing gradients. Tanh: output in (-1,1), zero-centered. Also suffers from vanishing gradients. ReLU (Rectified Linear Unit): f(x) = max(0, x). The most widely used activation. Fast, sparse, avoids vanishing gradient for positive inputs. Leaky ReLU / ELU: address the "dying ReLU" problem where neurons get stuck at zero. Softmax: used in the output layer for multi-class classification to produce a probability distribution that sums to 1.

Backpropagation and Gradient Descent
Training a neural network means finding weights that minimize the loss function. Backpropagation computes the gradient of the loss with respect to every weight using the chain rule of calculus. Gradient Descent updates weights in the opposite direction of the gradient: W - W - --L. - is the learning rate  -  too large and training diverges, too small and it crawls. Stochastic Gradient Descent (SGD) updates weights after each example. Mini-batch SGD (the standard) updates after a batch of 32-512 examples. Adam (Adaptive Moment Estimation) combines momentum and adaptive learning rates and is the default optimizer for most deep learning.

Convolutional Neural Networks (CNNs)
CNNs are specialized for grid-structured data (images, spectrograms, time series). A convolutional layer applies learned filters across the input, detecting local patterns like edges and textures. Pooling layers (Max Pooling, Average Pooling) downsample feature maps, providing spatial invariance. Landmark CNNs: LeNet (1998) for handwritten digit recognition; AlexNet (2012) that triggered the deep learning revolution; VGGNet (2014) with deep uniform architecture; ResNet (2015) introduced residual skip connections enabling training of 100+ layer networks; EfficientNet scales depth, width, and resolution optimally.

Recurrent Neural Networks (RNNs)
RNNs process sequential data (text, audio, time series) by maintaining a hidden state that acts as memory of previous inputs. Vanilla RNNs suffer from vanishing/exploding gradients for long sequences. Long Short-Term Memory (LSTM, 1997): uses three gates (forget, input, output) to selectively remember or discard information over long time horizons. Gated Recurrent Unit (GRU): a simpler variant of LSTM with two gates, often performing comparably with fewer parameters.

The Transformer Architecture
The Transformer (2017, "Attention Is All You Need"  -  Vaswani et al.) replaced recurrence with Self-Attention. Each token in a sequence attends to every other token, capturing long-range dependencies directly. Key components: Multi-Head Self-Attention, Positional Encoding, Feed-Forward sublayers, Layer Normalization, and Residual connections. Transformers train faster (fully parallelizable) and scale better than RNNs.

Large Language Models (LLMs)
BERT (2018): bidirectional Transformer pre-trained with Masked Language Modeling. Excellent at understanding tasks (question answering, classification). GPT (2018-2024): autoregressive Transformer pre-trained to predict the next token. Scales to billions of parameters. GPT-4, Claude, and Gemini are state-of-the-art LLMs capable of reasoning, coding, creative writing, and multi-modal understanding. Fine-tuning with Reinforcement Learning from Human Feedback (RLHF) aligns these models with human preferences.

Regularization in Deep Learning
Dropout: randomly zeroes out a fraction of neurons during training, preventing co-adaptation. Batch Normalization: normalizes activations within each mini-batch, stabilizing and accelerating training. L2 Weight Decay: penalizes large weights. Early Stopping: stops training when validation loss stops improving. Data Augmentation: artificially expands the training set by applying label-preserving transformations (flips, crops, color jitter for images).
""",


# --- Chapter 5: Expert AI -------------------------------------------------
"""Chapter 5: Expert AI  -  Computer Vision, NLP, RL, and Ethics

Computer Vision at an Expert Level
Object Detection goes beyond classification to locate and label multiple objects in a single image. Two-stage detectors (Faster R-CNN) first propose candidate regions, then classify them  -  high accuracy but slower. Single-stage detectors (YOLO  -  You Only Look Once, SSD) process the entire image in a single forward pass, enabling real-time performance (30-100+ FPS). Semantic Segmentation assigns a class label to every pixel (U-Net for medical imaging). Instance Segmentation also distinguishes individual instances of the same class (Mask R-CNN). Depth Estimation and 3D reconstruction are critical for autonomous driving and augmented reality.

Generative Models
Generative Adversarial Networks (GANs, Goodfellow et al. 2014): A generator network creates fake data; a discriminator tries to distinguish real from fake. Adversarial training drives both to improve. Trained GANs produce photorealistic faces, artwork, and data augmentation samples. Variational Autoencoders (VAEs): learn a latent representation of data enabling controlled generation and interpolation. Diffusion Models (2020-): learn to iteratively denoise Gaussian noise back into structured data. Stable Diffusion, DALL-E 2/3, Midjourney, and Imagen use diffusion models to generate stunning images from text prompts. Diffusion models have surpassed GANs in image quality and diversity.

Advanced NLP
Word Embeddings (Word2Vec, GloVe, FastText): represent words as dense vectors where semantic similarity corresponds to geometric proximity. The king - man + woman - queen analogy demonstrated that these vectors capture meaningful structure. Contextual Embeddings (ELMo, BERT): the same word gets different vector representations depending on context  -  solving the polysemy problem. Retrieval-Augmented Generation (RAG): combine an LLM with a vector database of documents; the LLM retrieves relevant passages before generating an answer, grounding responses in facts and reducing hallucinations. Instruction Fine-tuning and RLHF: fine-tune base LLMs on curated instruction-response pairs, then use reinforcement learning with human feedback to align outputs with human preferences.

Reinforcement Learning  -  Advanced Topics
Policy Gradient Methods (REINFORCE, PPO  -  Proximal Policy Optimization): directly optimize the policy by computing gradients of expected reward. PPO is the algorithm behind ChatGPT's RLHF fine-tuning. Q-Learning and Deep Q-Networks (DQN): learn a value function Q(s,a) estimating future reward. DQN with experience replay and target networks achieved superhuman Atari game play. Multi-Agent Reinforcement Learning (MARL): multiple agents learn to cooperate or compete. Used in autonomous vehicle swarms and game AI. Model-Based RL: the agent learns a world model and plans using it, dramatically improving sample efficiency.

MLOps  -  Taking Models to Production
MLOps (Machine Learning Operations) is the discipline of deploying, monitoring, and maintaining ML models in production. Key components: Feature Stores (centralized feature computation and serving), Model Registry (version control for trained models), CI/CD Pipelines for automated testing and deployment, A/B Testing and Canary Releases for gradual rollout, Monitoring for data drift and model degradation. Tools: MLflow, Kubeflow, Weights & Biases, SageMaker, Vertex AI, Azure ML.

AI Ethics and Responsible AI
Bias and Fairness: ML models trained on historically biased data perpetuate discrimination. Auditing for demographic parity, equalized odds, and individual fairness is essential. Explainability: high-stakes decisions (loan approvals, medical diagnosis, criminal justice) require justification. LIME and SHAP provide local and global explanations for black-box models. Privacy: Federated Learning trains models across distributed devices without centralizing raw data. Differential Privacy adds mathematically calibrated noise to protect individual records. Safety and Alignment: as models become more capable, ensuring they pursue intended goals becomes critical. Constitutional AI, debate, and scalable oversight are active research areas. Governance: the EU AI Act classifies AI systems by risk and mandates transparency, accountability, and conformity assessment for high-risk applications.

The Road Ahead
Foundation Models pre-trained on internet-scale data (images, text, code, audio, video) and then adapted to downstream tasks with minimal fine-tuning are reshaping AI development. Multimodal models (GPT-4V, Claude 3, Gemini) process and generate text, images, audio, and video together. Neuromorphic computing and quantum machine learning are experimental frontiers. The decade ahead will bring AI systems of unprecedented capability  -  shaping every industry from healthcare and education to climate science and space exploration.
""",
]


def repopulate():
    print("Purging old data...")
    Result.objects.all().delete()
    Quiz.objects.all().delete()
    Resume.objects.all().delete()
    Course.objects.all().delete()

    media_path = 'media/courses'
    os.makedirs(media_path, exist_ok=True)

    courses_data = [
        {
            "title": "Introduction to Python Programming",
            "domain": "Python",
            "description": "A comprehensive journey through Python from first principles to expert-level mastery.",
            "chapters": PYTHON_CHAPTERS,
        },
        {
            "title": "AI & Machine Learning Foundations",
            "domain": "AI & ML",
            "description": "A structured deep-dive into AI theory, core ML algorithms, deep learning, and ethics.",
            "chapters": AI_CHAPTERS,
        },
    ]

    for c_data in courses_data:
        print(f"Creating Course: {c_data['title']}...")
        pdf_filename = c_data['title'].lower().replace(" ", "_").replace("&", "and") + ".pdf"
        pdf_path = os.path.join(media_path, pdf_filename)
        make_pdf_multipage(c_data['chapters'], pdf_path)

        course = Course.objects.create(
            title=c_data['title'],
            domain=c_data['domain'],
            description=c_data['description'],
            pdf_file=f"courses/{pdf_filename}",
        )

        full_text = "\n\n".join(c_data['chapters'])
        course.extracted_content = full_text
        course.chapters = segment_into_chapters(full_text)
        course.save()
        print(f"  -> Course {course.id}: {len(course.chapters)} chapters indexed.")

    print("\nRepopulation complete!")


if __name__ == "__main__":
    repopulate()
