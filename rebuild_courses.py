# -*- coding: utf-8 -*-
"""
Repopulate - safe ASCII-only version
Run with: python rebuild_courses.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ailms_project.settings')
django.setup()

import fitz
from ailms_app.models import Course, Quiz, Result, Resume
from ailms_app.pdf_utils import segment_into_chapters

# ---------------------------------------------------------------------------
# Chapter content (plain ASCII, no special characters)
# ---------------------------------------------------------------------------

PY = [
    # Chapter 1 - Introduction
    (
        "Chapter 1: Introduction to Python\n\n"
        "What Is Python?\n"
        "Python is a high-level, interpreted, general-purpose programming language created by Guido van Rossum"
        " and first released in 1991. Its name is a nod to the British comedy group Monty Python. Today Python"
        " is one of the most widely used languages in the world, ranking in the top 3 of TIOBE, PYPL, and the"
        " Stack Overflow Developer Survey every year.\n\n"
        "Design Philosophy\n"
        "Python's guiding principles are documented in PEP 20 (The Zen of Python). Core ideas include: Beautiful"
        " is better than ugly. Explicit is better than implicit. Simple is better than complex. Readability counts."
        " There should be one obvious way to do it. These principles explain why Python code looks clean and"
        " readable compared to other languages.\n\n"
        "A Brief History\n"
        "Guido van Rossum began designing Python in the late 1980s at CWI in the Netherlands as a successor to"
        " the ABC language. Python 1.0 was released in January 1994. Python 2.0 added list comprehensions,"
        " garbage collection, and Unicode support in 2000. Python 3.0, released in December 2008, was a"
        " backward-incompatible revision that cleaned up years of technical debt. Python 2 reached its official"
        " end-of-life in January 2020. The latest stable release is Python 3.12.\n\n"
        "Key Features\n"
        "Dynamically typed: you do not declare variable types. Garbage-collected: memory is managed automatically."
        " Multi-paradigm: supports procedural, object-oriented, and functional programming. Batteries included:"
        " Python ships with a massive standard library plus access to 450,000 third-party packages on PyPI.\n\n"
        "Where Python Is Used\n"
        "Data Science and Machine Learning: NumPy, Pandas, Scikit-Learn, TensorFlow, PyTorch have made Python"
        " the dominant language for AI research and production ML. Web Development: Django and Flask power"
        " millions of websites worldwide. Scripting and Automation: Python replaces manual repetitive tasks in"
        " DevOps, testing, and system administration. Scientific Computing: SciPy, Matplotlib, and Jupyter"
        " Notebooks are standard tools in academic research. Cybersecurity: penetration testers write exploit"
        " scripts and analysis tools in Python.\n\n"
        "Companies Using Python\n"
        "Google, Instagram, Spotify, Dropbox, Netflix, NASA, CERN, Reddit, and YouTube all use Python extensively."
        " Google maintains CPython (the reference implementation) and contributes regularly to the language.\n\n"
        "Getting Started\n"
        "Download Python from python.org. The REPL (Read-Eval-Print Loop) lets you type statements interactively"
        " and see results immediately. Run: print('Hello, Python!') -- that is a complete Python program."
        " No semicolons, no curly braces, no class declarations required. That simplicity is Python's hallmark.\n\n"
        "Why Learn Python First?\n"
        "Python is the recommended first language because its syntax is forgiving and readable, the feedback loop"
        " is instant, and the same language scales all the way to complex production systems. Whether you want to"
        " build websites, analyze data, train machine learning models, or automate boring tasks, Python is the"
        " right tool for the job."
    ),

    # Chapter 2 - Basics
    (
        "Chapter 2: Python Basics - Variables, Types, and Operators\n\n"
        "Variables and Assignment\n"
        "A variable is a name that points to an object in memory. Create one with assignment: x = 42."
        " No type declaration is needed -- Python infers the type automatically. Python is dynamically typed:"
        " one variable can hold an integer, then be reassigned to a string on the next line. Variable names are"
        " case-sensitive (age and Age are different) and use snake_case by convention (total_price, user_name).\n\n"
        "Core Data Types\n"
        "int -- Whole numbers of arbitrary size. Python 3 integers never overflow: 2**100 computes exactly.\n"
        "float -- IEEE 754 double-precision. Be aware: 0.1 + 0.2 equals 0.30000000000000004 due to binary representation.\n"
        "str -- Immutable sequences of Unicode code points. Defined with single, double, or triple quotes.\n"
        "bool -- True and False are the only two boolean values. bool is a subclass of int.\n"
        "NoneType -- The None singleton represents the absence of a value, similar to null in other languages.\n\n"
        "Type Checking and Conversion\n"
        "Use type() to inspect a variable: type(3.14) returns float. Convert with int(), float(), str(), bool()."
        " Python requires explicit conversion -- no hidden coercion -- which prevents surprising bugs.\n\n"
        "Strings in Depth\n"
        "Escape sequences: \\n is newline, \\t is tab, \\\\ is a literal backslash. Raw strings (r'path') suppress"
        " escape processing -- useful for file paths and regular expressions. F-strings (Python 3.6+) embed"
        " expressions: name = 'Alice'; print(f'Hello, {name}!') -- this is the modern preferred format method.\n\n"
        "Arithmetic Operators\n"
        "+ addition, - subtraction, * multiplication, / true division (always float), // floor division,"
        " % modulus (remainder), ** exponentiation. Augmented assignment: +=, -=, *=, /=, //=, **=, %=.\n\n"
        "Comparison and Logical Operators\n"
        "Comparison: == (equal), != (not equal), < (less than), > (greater than), <=, >=. All return bool."
        " Logical: and returns True if both sides are True. or returns True if at least one is True. not negates."
        " Chained comparisons work: 0 < x < 100 is valid and idiomatic Python.\n\n"
        "The print() and input() Functions\n"
        "print() writes to stdout with an automatic newline. Customize: print('a', 'b', sep='-', end='!')."
        " input() reads a string from the user. Always convert if you need a number: age = int(input('Age: ')).\n\n"
        "Comments and Docstrings\n"
        "Single-line comments start with #. Triple-quoted strings serve as docstrings for functions, classes,"
        " and modules. Docstrings are accessible via the built-in help() function."
    ),

    # Chapter 3 - Core Concepts
    (
        "Chapter 3: Core Python - Control Flow, Functions, and Data Structures\n\n"
        "Control Flow\n"
        "The if statement selects which block to execute based on a condition. Python uses 4-space indentation to"
        " define blocks -- there are no curly braces. elif and else handle additional and default cases.\n\n"
        "Example:\n"
        "score = 85\n"
        "if score >= 90:\n"
        "    grade = 'A'\n"
        "elif score >= 75:\n"
        "    grade = 'B'\n"
        "else:\n"
        "    grade = 'C'\n\n"
        "Loops\n"
        "The for loop iterates over any iterable: list, string, range, tuple, dict, or file object."
        " range(start, stop, step) generates integers lazily -- range(0,10,2) gives 0,2,4,6,8."
        " The while loop repeats as long as a condition is True. break exits immediately. continue"
        " skips to the next iteration. The else clause on a loop runs only when no break occurred.\n\n"
        "List Comprehensions\n"
        "A list comprehension is [expression for item in iterable if condition]."
        " squares = [x**2 for x in range(1, 11)] creates [1,4,9,16,25,36,49,64,81,100] in one readable line."
        " Dictionary and set comprehensions follow the same pattern. Generator expressions are lazy versions.\n\n"
        "Functions\n"
        "def defines a function. Parameters can have default values: def greet(name, greeting='Hello')."
        " Keyword arguments pass values by name in any order: greet(greeting='Hi', name='Bob')."
        " *args collects extra positional arguments as a tuple."
        " **kwargs collects extra keyword arguments as a dict."
        " Without an explicit return statement a function returns None.\n\n"
        "Scope: LEGB Rule\n"
        "Python resolves names in this order: Local, Enclosing, Global, Built-in."
        " Variables created inside a function are local and inaccessible outside."
        " The global keyword lets you modify a global from inside a function (use sparingly).\n\n"
        "Lists\n"
        "Mutable ordered sequences: fruits = ['apple', 'banana', 'cherry']."
        " Zero-based indexing: fruits[0] is 'apple'. Negative: fruits[-1] is the last item."
        " Slicing: fruits[1:3] returns ['banana', 'cherry']."
        " Methods: append(), extend(), insert(), remove(), pop(), sort(), reverse(), index(), count().\n\n"
        "Dictionaries\n"
        "Mutable key-value maps: person = {'name': 'Alice', 'age': 30}."
        " Access: person['name']. Safe access: person.get('city', 'Unknown')."
        " Iteration: for key, value in person.items()."
        " Dict comprehensions: {k: v**2 for k, v in data.items()}.\n\n"
        "Tuples and Sets\n"
        "Tuples are immutable ordered sequences -- useful for fixed data and as dict keys."
        " Sets are unordered collections of unique elements with O(1) membership testing."
        " Set operations: union |, intersection &, difference -, symmetric difference ^.\n\n"
        "Exception Handling\n"
        "try / except catches runtime errors. Multiple except clauses handle different types."
        " finally always runs for cleanup (closing files, connections)."
        " raise throws or re-raises exceptions. Custom exceptions inherit from Exception."
    ),

    # Chapter 4 - Advanced
    (
        "Chapter 4: Advanced Python - OOP, Modules, Generators, and Decorators\n\n"
        "Object-Oriented Programming (OOP)\n"
        "Every value in Python is an object. The class keyword defines a blueprint."
        " __init__ is the constructor invoked automatically when creating an instance."
        " self is the first parameter of every instance method -- it references the current object.\n\n"
        "Inheritance\n"
        "A child class inherits attributes and methods from its parent: class Dog(Animal)."
        " super() calls the parent's implementation. Python supports multiple inheritance."
        " The MRO (Method Resolution Order) uses the C3 linearization algorithm to determine"
        " which parent method is called when names conflict.\n\n"
        "Dunder (Magic) Methods\n"
        "__repr__ and __str__ control string representation. __len__ enables len(obj)."
        " __add__ enables the + operator. __iter__ and __next__ make an object iterable."
        " __enter__ and __exit__ enable the with statement (context managers).\n\n"
        "Properties and Encapsulation\n"
        "@property turns a method into a read-only attribute. @attribute.setter adds a setter."
        " Double-underscore prefix (__x) triggers name mangling: becomes _ClassName__x, making"
        " the attribute class-private. Single underscore (_x) means internal use by convention.\n\n"
        "Generators and Iterators\n"
        "An iterator implements __iter__ and __next__. Generators use yield to produce values one at a time:"
        " def countdown(n): while n > 0: yield n; n -= 1. Generator expressions are lazily evaluated:"
        " (x**2 for x in range(1000000)) consumes almost no memory.\n\n"
        "Decorators\n"
        "A decorator wraps a function to modify its behavior without changing its source code."
        " @timer before a function definition is sugar for func = timer(func)."
        " Flask uses @app.route(). Django uses @login_required. functools.wraps preserves metadata.\n\n"
        "Context Managers\n"
        "The with statement guarantees cleanup even if exceptions occur."
        " with open('file.txt') as f: automatically calls f.close()."
        " Custom context managers use __enter__/__exit__ or @contextmanager from contextlib.\n\n"
        "Modules and Packages\n"
        "A module is a .py file. import math; math.sqrt(16). from datetime import datetime."
        " Packages are directories with __init__.py. Virtual environments (python -m venv env)"
        " isolate dependencies per project. pip install name fetches from PyPI.\n\n"
        "Type Hints\n"
        "Python 3.5+ supports optional type annotations: def add(a: int, b: int) -> int."
        " Not enforced at runtime but used by static checkers (mypy) and IDEs for autocomplete."
    ),

    # Chapter 5 - Expert
    (
        "Chapter 5: Expert Python - Concurrency, Performance, Testing, and Ecosystem\n\n"
        "Concurrency Models\n"
        "Python has three main concurrency approaches. Threading (threading module): OS threads share memory."
        " The Global Interpreter Lock (GIL) prevents true CPU parallelism in CPython -- best for I/O-bound tasks"
        " (network requests, file reads). Multiprocessing: separate processes with own interpreter and memory,"
        " bypassing the GIL -- ideal for CPU-bound work (image processing, numerical computation)."
        " Asyncio: a single-threaded event loop using async/await for cooperative multitasking -- best for"
        " high-concurrency I/O like web servers handling thousands of connections simultaneously.\n\n"
        "async / await\n"
        "async def defines a coroutine. await suspends it until the target completes. asyncio.run() is the entry"
        " point. aiohttp provides async HTTP. FastAPI is an async REST framework achieving very high throughput.\n\n"
        "Performance Optimization\n"
        "Always profile before optimizing: python -m cProfile my_script.py. NumPy operations in C are orders of"
        " magnitude faster than Python loops. Cython compiles annotated Python to C. Numba JIT-compiles numerical"
        " functions at runtime. PyPy is an alternative interpreter with JIT compilation. functools.lru_cache"
        " memoizes expensive function calls. For string building, use ''.join(parts) not + concatenation.\n\n"
        "Memory Management\n"
        "Python uses reference counting plus a cyclic garbage collector. del removes a name binding; the object"
        " is freed when its reference count reaches zero. sys.getsizeof() measures object size. tracemalloc"
        " profiles memory allocation. Use NumPy typed arrays instead of Python lists for large numeric data.\n\n"
        "Testing\n"
        "pytest is the industry standard. Test functions are prefixed test_. pytest auto-discovers them."
        " Fixtures provide reusable setup/teardown via @pytest.fixture. Parametrize runs one test with many"
        " inputs. coverage.py measures what percentage of code is covered. TDD: write tests before implementation.\n\n"
        "Logging and Debugging\n"
        "Use the logging module instead of print in production. Configure levels: DEBUG, INFO, WARNING, ERROR,"
        " CRITICAL. Direct output to files, rotate logs, format as JSON for log aggregation systems."
        " pdb is the built-in interactive debugger. Python 3.7+: use breakpoint() as a portable entry point."
        " Static analysis: pylint, flake8 check style; mypy checks types.\n\n"
        "Packaging and Distribution\n"
        "Modern Python packages use pyproject.toml (PEP 517/518) as build configuration. Tools: Poetry, Hatch,"
        " setuptools. Publish to PyPI with twine upload dist/*. Follow semantic versioning: MAJOR.MINOR.PATCH.\n\n"
        "The Python Ecosystem\n"
        "Web: Django (batteries-included), Flask (micro), FastAPI (async, auto-docs)."
        " Data: NumPy, Pandas, Polars (Rust-backed DataFrames)."
        " ML: Scikit-Learn, XGBoost, LightGBM."
        " Deep Learning: PyTorch (research), TensorFlow/Keras (production)."
        " Visualization: Matplotlib, Seaborn, Plotly."
        " ORMs: SQLAlchemy, Django ORM."
        " CLI: Click, Typer. Config/Validation: Pydantic.\n\n"
        "Pythonic Code Principles\n"
        "List comprehensions over map/filter. enumerate() over manual index counters. Tuple unpacking over"
        " indexing. Context managers for resources. Duck typing over isinstance() checks. The goal is always"
        " readability, explicitness, and simplicity -- the true Python way."
    ),
]

AI = [
    # Chapter 1 - Introduction
    (
        "Chapter 1: Introduction to Artificial Intelligence\n\n"
        "What Is Artificial Intelligence?\n"
        "Artificial Intelligence (AI) is the science and engineering of creating intelligent machines -- systems"
        " that can perform tasks normally requiring human intelligence. These include understanding natural"
        " language, recognizing images, making decisions under uncertainty, translating between languages,"
        " generating creative content, and learning from experience. AI is not one technology but a collection"
        " of disciplines: machine learning, NLP, computer vision, robotics, and knowledge representation.\n\n"
        "A Brief History\n"
        "The formal birth of AI was the Dartmouth Summer Research Project of 1956, organized by John McCarthy"
        " (who coined the term 'artificial intelligence'), Marvin Minsky, Nathaniel Rochester, and Claude Shannon."
        " Their goal was to simulate every aspect of intelligence in a machine. Early AI produced programs that"
        " played checkers, proved mathematical theorems, and solved algebra word problems -- impressive but narrow.\n\n"
        "Two AI Winters\n"
        "After periods of optimism and investment, the field experienced two AI winters (1974-1980 and 1987-1993)"
        " when progress stalled, funding dried up, and overly optimistic expectations went unmet. Researchers had"
        " underestimated the difficulty of common-sense reasoning, perception, and general intelligence.\n\n"
        "The Deep Learning Revolution\n"
        "Everything changed in 2012 when Geoffrey Hinton's team at the University of Toronto won the ImageNet"
        " challenge by a massive margin using AlexNet, a deep convolutional neural network trained on GPUs."
        " Since then AI has achieved superhuman performance in image recognition, speech recognition,"
        " the game of Go (AlphaGo), protein structure prediction (AlphaFold), and language tasks"
        " (GPT-4, Claude, Gemini).\n\n"
        "Types of AI\n"
        "Narrow AI (Weak AI): AI designed for one specific task. All current commercial AI is narrow."
        " General AI (AGI): a hypothetical AI that can perform any intellectual task a human can."
        " Superintelligence: a hypothetical AI far beyond human level. Both AGI and superintelligence"
        " remain speculative and their timelines are hotly debated by researchers.\n\n"
        "Core Branches of AI\n"
        "Machine Learning: systems that learn patterns from data."
        " Natural Language Processing: understanding and generating human language."
        " Computer Vision: interpreting images and video."
        " Robotics: perceiving and acting in the physical world."
        " Knowledge Representation: encoding facts and logical inference."
        " Planning and Search: finding action sequences to achieve goals.\n\n"
        "Why AI Matters Now\n"
        "Three forces converged to make AI practical at scale: massive datasets (the internet, social media,"
        " digitized records), powerful hardware (GPUs, TPUs, specialized AI chips), and algorithmic breakthroughs"
        " (deep learning, Transformer attention, RLHF). AI is now embedded in smartphones, search engines,"
        " recommendation systems, medical devices, and financial markets.\n\n"
        "Ethics from the Start\n"
        "Fairness, accountability, transparency, and privacy must be built into AI design from day one."
        " Bias in training data, lack of explainability, and impact on employment are urgent concerns"
        " that the field must address proactively."
    ),

    # Chapter 2 - Basics
    (
        "Chapter 2: Basics of Machine Learning\n\n"
        "What Is Machine Learning?\n"
        "Machine learning (ML) is the subfield of AI focused on building systems that learn from data and improve"
        " without being explicitly programmed with rules. Rather than hand-coding logic, you provide labeled"
        " examples and a measure of success (a loss function), and the algorithm discovers patterns on its own.\n\n"
        "The ML Pipeline\n"
        "Step 1: Problem Definition -- what exactly do you want to predict or decide?\n"
        "Step 2: Data Collection -- gather labeled or unlabeled examples from real-world sources.\n"
        "Step 3: Data Preprocessing -- clean, normalize, encode categorical variables, handle missing values,"
        " and split into training, validation, and test sets.\n"
        "Step 4: Feature Engineering -- transform raw variables into informative model inputs.\n"
        "Step 5: Model Selection -- choose an algorithm appropriate for the problem.\n"
        "Step 6: Training -- fit the model to the training data by minimizing the loss function.\n"
        "Step 7: Evaluation -- measure performance on held-out test data using appropriate metrics.\n"
        "Step 8: Deployment -- serve the model in production and monitor for drift and degradation.\n\n"
        "Supervised Learning\n"
        "Training data consists of (input, output) pairs. The model learns f(input) = output."
        " Regression predicts continuous values: house prices, stock returns, temperature forecasting."
        " Classification predicts discrete categories: spam/not-spam, cat/dog/bird, malignant/benign."
        " Common algorithms: Linear Regression, Logistic Regression, Decision Trees, Random Forests,"
        " Support Vector Machines, k-Nearest Neighbors, and Neural Networks.\n\n"
        "Unsupervised Learning\n"
        "No labels. The algorithm finds hidden structure in data."
        " Clustering groups similar data points: K-Means, DBSCAN, Hierarchical Clustering."
        " Dimensionality Reduction compresses high-dimensional data: PCA, t-SNE, UMAP."
        " Association Rule Mining discovers relationships: Apriori algorithm in market basket analysis.\n\n"
        "Reinforcement Learning\n"
        "An agent interacts with an environment, chooses actions, observes the resulting state, and receives"
        " rewards or penalties. The goal is to learn a policy maximizing cumulative reward over time."
        " RL achieved remarkable results: AlphaGo, OpenAI Five (Dota 2), and robotic locomotion.\n\n"
        "Key Evaluation Metrics\n"
        "Regression: Mean Absolute Error (MAE), Mean Squared Error (MSE), RMSE, R-squared."
        " Classification: Accuracy, Precision, Recall, F1-Score, ROC-AUC."
        " The right metric depends on business context: spam filters prioritize precision;"
        " cancer screening prioritizes recall to minimize missed cases.\n\n"
        "Bias-Variance Tradeoff\n"
        "Underfitting (high bias): the model is too simple and misses real patterns."
        " Overfitting (high variance): the model memorizes noise and fails to generalize."
        " Balance with regularization (L1 Lasso, L2 Ridge), cross-validation, and proper data splits.\n\n"
        "Tools for ML\n"
        "Scikit-Learn provides a consistent API for classical algorithms."
        " NumPy and Pandas handle numerical computation and data manipulation."
        " Matplotlib and Seaborn visualize data and results."
        " Jupyter Notebooks enable interactive experimentation."
        " Python is the dominant language for machine learning."
    ),

    # Chapter 3 - Core Concepts
    (
        "Chapter 3: Core ML Algorithms - Regression, Classification, and Ensemble Methods\n\n"
        "Linear Regression\n"
        "Models Y = B0 + B1*X1 + B2*X2 + ... + Bn*Xn + error. Parameters estimated by Ordinary Least Squares,"
        " which minimizes the sum of squared residuals. Gradient Descent is the iterative alternative for large"
        " datasets. Ridge Regression (L2 penalty) shrinks coefficients toward zero. Lasso Regression (L1 penalty)"
        " can shrink some coefficients to exactly zero, performing automatic feature selection.\n\n"
        "Logistic Regression\n"
        "Binary classifier using the sigmoid function: sigma(z) = 1 / (1 + exp(-z)), which maps any real number"
        " to (0,1). Predicts probability of the positive class. The decision boundary is linear."
        " Trained by minimizing binary cross-entropy loss. Multi-class handled by One-vs-Rest or Softmax.\n\n"
        "Decision Trees\n"
        "Recursively partitions the feature space using optimal yes/no splits. At each node, the split"
        " maximizing information gain (entropy reduction) or minimizing Gini impurity is chosen."
        " Highly interpretable -- the tree can be visualized and explained to non-technical stakeholders."
        " Prone to overfitting on training data without pruning.\n\n"
        "Random Forests\n"
        "Trains many decision trees on different bootstrap samples of the data with different random feature"
        " subsets at each split. Final prediction: majority vote (classification) or average (regression)."
        " Dramatically reduces variance while maintaining low bias."
        " Feature importance scores rank which inputs matter most for predictions."
        " Robust, accurate, and one of the best general-purpose algorithms.\n\n"
        "Gradient Boosting: XGBoost, LightGBM, CatBoost\n"
        "Builds trees sequentially -- each new tree corrects the residual errors of all previous trees."
        " XGBoost, LightGBM, and CatBoost are highly optimized implementations that consistently win"
        " tabular data competitions on Kaggle. They support regularization, handle missing values natively,"
        " and train fast on CPU. They typically outperform Random Forests on structured data.\n\n"
        "Support Vector Machines (SVMs)\n"
        "Find the maximum-margin hyperplane separating the two classes."
        " The kernel trick implicitly maps data into higher-dimensional space where linear separation is possible."
        " Common kernels: linear, polynomial, RBF. Work well in high dimensions (text classification)."
        " Scale poorly to very large datasets (millions of examples).\n\n"
        "k-Nearest Neighbors (kNN)\n"
        "Classifies a new point by the majority class of its k nearest training neighbors."
        " No explicit training phase -- lazy learning. Feature scaling is essential since kNN is distance-based."
        " k is a critical hyperparameter: small k = high variance; large k = high bias.\n\n"
        "Evaluation Beyond Accuracy\n"
        "Confusion matrix: TP, TN, FP, FN. Precision = TP/(TP+FP). Recall = TP/(TP+FN)."
        " F1 = harmonic mean of precision and recall."
        " The ROC curve plots True Positive Rate vs False Positive Rate across all thresholds."
        " AUC of 0.5 equals random guessing; AUC of 1.0 equals a perfect classifier."
    ),

    # Chapter 4 - Advanced
    (
        "Chapter 4: Advanced AI - Neural Networks and Deep Learning\n\n"
        "Artificial Neural Networks (ANNs)\n"
        "A neural network is a directed graph of layers of neurons. Each neuron computes:"
        " output = activation(W * input + b) where W is a weight matrix and b is a bias vector."
        " Stacking layers allows the network to learn hierarchical representations."
        " A feedforward network (Multi-Layer Perceptron) has input, hidden, and output layers.\n\n"
        "Activation Functions\n"
        "Sigmoid: maps input to (0,1); suffers from vanishing gradients in deep networks."
        " Tanh: output in (-1,1), zero-centered; also has vanishing gradient issues."
        " ReLU (Rectified Linear Unit): f(x) = max(0,x) -- most widely used, avoids vanishing gradients."
        " Leaky ReLU and ELU fix the dying ReLU problem where neurons get stuck at zero."
        " Softmax: used in the output layer for multi-class classification, produces a valid probability distribution.\n\n"
        "Backpropagation and Gradient Descent\n"
        "Backpropagation computes the gradient of the loss with respect to every weight using the chain rule."
        " Weight update: W = W - learning_rate * gradient_of_loss."
        " Mini-batch SGD (standard): updates weights after 32-512 examples."
        " Adam optimizer combines momentum and adaptive learning rates -- the default for most deep learning.\n\n"
        "Convolutional Neural Networks (CNNs)\n"
        "Specialized for grid-structured data (images, spectrograms). Convolutional layers apply learned filters"
        " across the input, detecting local patterns like edges and textures regardless of position."
        " Pooling layers downsample feature maps for spatial invariance."
        " Landmark architectures: LeNet (1998), AlexNet (2012 ImageNet winner), VGGNet, ResNet (residual"
        " connections enabling 100+ layer networks), EfficientNet (optimally scaled).\n\n"
        "Recurrent Neural Networks (RNNs)\n"
        "Process sequential data (text, speech, time series) maintaining a hidden state as memory."
        " Vanilla RNNs suffer vanishing/exploding gradients for long sequences."
        " LSTM (Long Short-Term Memory, 1997): uses forget, input, and output gates for long-range memory."
        " GRU (Gated Recurrent Unit): simpler LSTM variant with two gates, comparable performance.\n\n"
        "The Transformer Architecture\n"
        "Introduced in 'Attention Is All You Need' (Vaswani et al., 2017). Replaces recurrence with"
        " Self-Attention: each token attends to every other token in the sequence, directly capturing"
        " long-range dependencies. Components: Multi-Head Self-Attention, Positional Encoding,"
        " Feed-Forward sublayers, Layer Normalization, Residual connections. Fully parallelizable"
        " during training, scales to billions of parameters.\n\n"
        "Large Language Models (LLMs)\n"
        "BERT (2018): bidirectional Transformer pre-trained with Masked Language Modeling."
        " GPT series: autoregressive next-token prediction, scaling to billions of parameters."
        " GPT-4, Claude, Gemini: state-of-the-art LLMs capable of complex reasoning, coding,"
        " and multi-modal understanding. RLHF (Reinforcement Learning from Human Feedback) aligns outputs.\n\n"
        "Regularization for Deep Learning\n"
        "Dropout: zeroes random neurons during training to prevent co-adaptation."
        " Batch Normalization: normalizes activations within each mini-batch, stabilizes training."
        " L2 Weight Decay: penalizes large weights. Early Stopping: halts training when validation"
        " loss stops improving. Data Augmentation: label-preserving transformations expand training data."
    ),

    # Chapter 5 - Expert
    (
        "Chapter 5: Expert AI - Computer Vision, NLP, Reinforcement Learning, and Ethics\n\n"
        "Computer Vision at Expert Level\n"
        "Object Detection locates and classifies multiple objects in one image."
        " Two-stage detectors (Faster R-CNN): propose candidate regions, then classify them -- accurate but slow."
        " Single-stage detectors (YOLO, SSD): process the entire image in one forward pass -- real-time at 30-100 FPS."
        " Semantic Segmentation labels every pixel (U-Net is standard for medical imaging)."
        " Instance Segmentation also separates individual object instances (Mask R-CNN)."
        " 3D Vision, Depth Estimation, and SLAM are critical for autonomous vehicles and robotics.\n\n"
        "Generative AI Models\n"
        "GANs (Generative Adversarial Networks, 2014): a generator creates synthetic data; a discriminator"
        " tries to identify fakes. Adversarial training drives both networks to improve."
        " VAEs (Variational Autoencoders): learn a structured latent space enabling controlled generation."
        " Diffusion Models (2020+): learn to iteratively denoise Gaussian noise back into structured data."
        " Stable Diffusion, DALL-E 3, Midjourney, and Imagen use diffusion for text-to-image generation."
        " Diffusion models have surpassed GANs in image quality and diversity.\n\n"
        "Advanced NLP\n"
        "Word2Vec, GloVe, FastText: dense word vectors encoding semantic similarity."
        " BERT, ELMo: contextual embeddings where the same word gets different vectors in different contexts."
        " Instruction Fine-tuning: train base LLMs on curated instruction-response pairs."
        " Retrieval-Augmented Generation (RAG): LLM retrieves relevant documents before generating an answer,"
        " grounding responses in facts and reducing hallucinations. Vision-Language Models (CLIP, Flamingo)"
        " align image and text representations enabling zero-shot image classification and visual question answering.\n\n"
        "Advanced Reinforcement Learning\n"
        "PPO (Proximal Policy Optimization): the policy gradient algorithm behind ChatGPT's RLHF fine-tuning."
        " DQN (Deep Q-Network): achieved superhuman Atari performance using experience replay and target networks."
        " AlphaZero: combined MCTS with deep RL, mastering chess, shogi, and Go from self-play alone."
        " Multi-Agent RL (MARL): multiple agents cooperate or compete -- used in autonomous vehicle swarms."
        " Model-Based RL: agent learns a world model and plans within it, dramatically improving sample efficiency.\n\n"
        "MLOps: Taking Models to Production\n"
        "Feature Stores: centralized feature computation and serving for consistency between training and inference."
        " Model Registry: version control and lifecycle management for trained models."
        " CI/CD Pipelines: automated testing and deployment of model updates."
        " A/B Testing and Canary Releases: gradual traffic shifting for safe rollouts."
        " Monitoring: detecting data drift (input distribution shift) and model degradation over time."
        " Tools: MLflow, Kubeflow, Weights and Biases, SageMaker, Vertex AI, Azure ML.\n\n"
        "AI Ethics and Responsible AI\n"
        "Bias and Fairness: models trained on historically biased data perpetuate discrimination."
        " Audit for demographic parity, equalized odds, and individual fairness."
        " Explainability: LIME and SHAP provide local and global explanations for black-box models, essential"
        " for high-stakes decisions in healthcare, finance, and criminal justice."
        " Privacy: Federated Learning trains across distributed devices without centralizing raw data."
        " Differential Privacy adds mathematically calibrated noise to protect individual records."
        " Safety and Alignment: Constitutional AI, debate, and scalable oversight address misalignment risks."
        " Governance: the EU AI Act classifies systems by risk and mandates transparency for high-risk applications.\n\n"
        "The Road Ahead\n"
        "Foundation Models pre-trained on internet-scale data and adapted to downstream tasks with minimal"
        " fine-tuning are reshaping AI development. Multimodal models (GPT-4V, Claude 3, Gemini) process"
        " text, images, audio, and video together. Neuromorphic computing and quantum machine learning are"
        " experimental frontiers. The coming decade will bring AI of unprecedented capability across healthcare,"
        " climate science, education, and space exploration."
    ),
]


def make_pdf(chapters, path):
    doc = fitz.open()
    for ch in chapters:
        pg = doc.new_page(width=595, height=842)
        pg.insert_textbox(fitz.Rect(50, 50, 545, 800), ch, fontsize=10, fontname='helv', color=(0,0,0), align=0)
    doc.save(path)
    doc.close()


from ailms_app.ai_utils import generate_quiz

def run():
    print("Purging old data...")
    Result.objects.all().delete()
    Quiz.objects.all().delete()
    Resume.objects.all().delete()
    Course.objects.all().delete()

    media_path = 'media/courses'
    os.makedirs(media_path, exist_ok=True)

    courses = [
        {
            'title': 'Introduction to Python Programming',
            'domain': 'Python',
            'desc': 'A comprehensive journey from first principles to expert Python mastery, covering '
                    'syntax, OOP, concurrency, and the full ecosystem.',
            'chapters': PY,
        },
        {
            'title': 'AI and Machine Learning Foundations',
            'domain': 'AI and ML',
            'desc': 'A structured deep-dive into AI history, core ML algorithms, deep learning,'
                    ' computer vision, NLP, and responsible AI.',
            'chapters': AI,
        },
    ]

    for cd in courses:
        fname = cd['title'].lower().replace(' ', '_') + '.pdf'
        fpath = os.path.join(media_path, fname)
        print(f"Building PDF for: {cd['title']} ...")
        make_pdf(cd['chapters'], fpath)

        full_text = '\n\n'.join(cd['chapters'])
        c = Course.objects.create(
            title=cd['title'],
            domain=cd['domain'],
            description=cd['desc'],
            pdf_file='courses/' + fname,
        )
        c.extracted_content = full_text
        c.chapters = segment_into_chapters(full_text)
        c.save()
        print(f"  -> Course {c.id}: {len(c.chapters)} chapters indexed.")

        for diff in ['easy', 'medium', 'hard']:
            qs = generate_quiz(full_text, diff)
            Quiz.objects.create(course=c, difficulty=diff, questions=qs)
            print(f"     [+] Created {diff.title()} Quiz with {len(qs)} domain-aligned questions.")

    print("\nDone! All courses and domain quizzes rebuilt successfully.")



if __name__ == '__main__':
    run()
