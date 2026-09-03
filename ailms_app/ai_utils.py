import os
import re
import json
import random
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = None
if os.getenv("OPENAI_API_KEY"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------------------------
# Curated Domain Quiz Banks (100% Chapter-Aligned & Logical)
# ---------------------------------------------------------------------------

PYTHON_QUIZZES = {
    "easy": [
        {
            "question": "Who created Python, and in which year was it first released to the public?",
            "options": [
                "Guido van Rossum in 1991",
                "James Gosling in 1995",
                "Dennis Ritchie in 1972",
                "Bjarne Stroustrup in 1985"
            ],
            "answer": "Guido van Rossum in 1991"
        },
        {
            "question": "Which document contains the 19 guiding principles of Python's design philosophy?",
            "options": [
                "PEP 20 (The Zen of Python)",
                "PEP 8 (Style Guide for Python Code)",
                "PEP 484 (Type Hints)",
                "PEP 517 (Build System Interface)"
            ],
            "answer": "PEP 20 (The Zen of Python)"
        },
        {
            "question": "What is the return value of type(3.14) in Python?",
            "options": [
                "<class 'float'>",
                "<class 'int'>",
                "<class 'double'>",
                "<class 'decimal'>"
            ],
            "answer": "<class 'float'>"
        },
        {
            "question": "By standard Python convention (PEP 8), how should variable names be formatted?",
            "options": [
                "snake_case (e.g., total_price)",
                "camelCase (e.g., totalPrice)",
                "PascalCase (e.g., TotalPrice)",
                "kebab-case (e.g., total-price)"
            ],
            "answer": "snake_case (e.g., total_price)"
        },
        {
            "question": "What data type does the built-in input() function always return?",
            "options": [
                "str (string)",
                "int (integer)",
                "float (floating-point)",
                "bool (boolean)"
            ],
            "answer": "str (string)"
        },
        {
            "question": "Which arithmetic operator performs floor division (truncating decimals) in Python?",
            "options": [
                "//",
                "/",
                "%",
                "**"
            ],
            "answer": "//"
        },
        {
            "question": "What is the output of len(['apple', 'banana', 'cherry'])?",
            "options": [
                "3",
                "2",
                "4",
                "0"
            ],
            "answer": "3"
        },
        {
            "question": "How are code blocks defined in Python instead of using curly braces {}?",
            "options": [
                "4-space indentation",
                "Semicolons at line ends",
                "Parentheses around blocks",
                "End block statements"
            ],
            "answer": "4-space indentation"
        },
        {
            "question": "Which string formatting style introduced in Python 3.6 allows embedding expressions with f'...'?",
            "options": [
                "F-strings (Formatted String Literals)",
                "Raw strings (r-strings)",
                "Percent formatting (% s)",
                "str.format() method"
            ],
            "answer": "F-strings (Formatted String Literals)"
        },
        {
            "question": "What official central repository hosts over 450,000 third-party Python packages?",
            "options": [
                "PyPI (Python Package Index)",
                "NPM",
                "Maven Central",
                "Docker Hub"
            ],
            "answer": "PyPI (Python Package Index)"
        }
    ],
    "medium": [
        {
            "question": "What is the output of the list comprehension [x**2 for x in range(1, 4)]?",
            "options": [
                "[1, 4, 9]",
                "[1, 2, 3]",
                "[0, 1, 4]",
                "[2, 4, 6]"
            ],
            "answer": "[1, 4, 9]"
        },
        {
            "question": "What is the LEGB rule order for variable scope resolution in Python?",
            "options": [
                "Local, Enclosing, Global, Built-in",
                "Local, Extended, Global, Base",
                "Logical, Enclosing, General, Built-in",
                "Linear, Execution, Global, Binding"
            ],
            "answer": "Local, Enclosing, Global, Built-in"
        },
        {
            "question": "Which dictionary method safely fetches a value without throwing a KeyError if the key is missing?",
            "options": [
                "dict.get(key, default)",
                "dict.fetch(key)",
                "dict.pop(key)",
                "dict.lookup(key)"
            ],
            "answer": "dict.get(key, default)"
        },
        {
            "question": "In Python function definitions, what data structure collects extra positional arguments into *args?",
            "options": [
                "Tuple",
                "List",
                "Dictionary",
                "Set"
            ],
            "answer": "Tuple"
        },
        {
            "question": "Which statement accurately describes Python tuples?",
            "options": [
                "Tuples are immutable ordered sequences.",
                "Tuples can be modified using append().",
                "Tuples are unordered sets of unique items.",
                "Tuples cannot contain mixed data types."
            ],
            "answer": "Tuples are immutable ordered sequences."
        },
        {
            "question": "In Object-Oriented Python, what does the first parameter 'self' in an instance method represent?",
            "options": [
                "The current instance of the class",
                "The parent class definition",
                "The global module workspace",
                "The static constructor method"
            ],
            "answer": "The current instance of the class"
        },
        {
            "question": "What is the primary function of the @property decorator in Python classes?",
            "options": [
                "It turns a method into a read-only attribute.",
                "It makes a class private across modules.",
                "It speeds up arithmetic operations.",
                "It automatically validates method input types."
            ],
            "answer": "It turns a method into a read-only attribute."
        },
        {
            "question": "Which dunder method serves as the constructor when instantiating a new object?",
            "options": [
                "__init__",
                "__new__",
                "__construct__",
                "__create__"
            ],
            "answer": "__init__"
        },
        {
            "question": "What keyword is used inside a function to make it a generator that produces values lazily?",
            "options": [
                "yield",
                "return",
                "generate",
                "emit"
            ],
            "answer": "yield"
        },
        {
            "question": "Why is using the 'with' statement (context manager) recommended when opening files in Python?",
            "options": [
                "It guarantees file resources are automatically closed even if exceptions occur.",
                "It compresses file size during read operations.",
                "It prevents other programs from accessing the file system.",
                "It reads entire files into GPU memory automatically."
            ],
            "answer": "It guarantees file resources are automatically closed even if exceptions occur."
        }
    ],
    "hard": [
        {
            "question": "What role does the Global Interpreter Lock (GIL) play in CPython?",
            "options": [
                "It prevents multiple native threads from executing Python bytecode in parallel.",
                "It prevents unauthorized users from modifying system files.",
                "It optimizes memory allocation for floating-point arrays.",
                "It encrypts source code during bytecode compilation."
            ],
            "answer": "It prevents multiple native threads from executing Python bytecode in parallel."
        },
        {
            "question": "Which concurrency approach in Python uses a single-threaded event loop with async/await?",
            "options": [
                "Asyncio",
                "Multiprocessing",
                "Threading",
                "Subprocess"
            ],
            "answer": "Asyncio"
        },
        {
            "question": "What algorithm does Python use to resolve Method Resolution Order (MRO) in multiple inheritance?",
            "options": [
                "C3 Linearization algorithm",
                "Dijkstra's Shortest Path algorithm",
                "Depth-First Search (DFS) with backtracking",
                "Breadth-First Search (BFS) graph traversal"
            ],
            "answer": "C3 Linearization algorithm"
        },
        {
            "question": "What is the primary function of functools.wraps when building custom decorators?",
            "options": [
                "It preserves the original function's docstring, name, and parameter metadata.",
                "It compiles the wrapped function into C bytecode.",
                "It suppresses all runtime exceptions inside the wrapper.",
                "It enables automatic multi-threading for the decorated function."
            ],
            "answer": "It preserves the original function's docstring, name, and parameter metadata."
        },
        {
            "question": "How does CPython perform automatic memory management for objects?",
            "options": [
                "Reference counting supplemented by a cyclic garbage collector",
                "Manual allocation and deallocation via free()",
                "Generational mark-and-sweep collection exclusively",
                "Static stack allocation at compilation time"
            ],
            "answer": "Reference counting supplemented by a cyclic garbage collector"
        },
        {
            "question": "In pytest, what decorator is used to supply reusable test dependencies and setup logic?",
            "options": [
                "@pytest.fixture",
                "@pytest.setup",
                "@pytest.dependency",
                "@pytest.mock"
            ],
            "answer": "@pytest.fixture"
        },
        {
            "question": "In Python 3.7+, what built-in function provides a portable entry point to the interactive debugger?",
            "options": [
                "breakpoint()",
                "sys.debug()",
                "pdb.set()",
                "trace.inspect()"
            ],
            "answer": "breakpoint()"
        },
        {
            "question": "Which file format is designated by PEP 517/518 as standard build configuration for modern Python packages?",
            "options": [
                "pyproject.toml",
                "setup.cfg",
                "requirements.txt",
                "Pipfile"
            ],
            "answer": "pyproject.toml"
        },
        {
            "question": "Which technique is recommended for efficient string concatenation when building long text from lists?",
            "options": [
                "''.join(string_list)",
                "Iterative concatenation with +=",
                "functools.reduce with string addition",
                "str(string_list)"
            ],
            "answer": "''.join(string_list)"
        },
        {
            "question": "What decorator from functools memoizes function call results to optimize repetitive computations?",
            "options": [
                "@functools.lru_cache",
                "@functools.memoize",
                "@functools.cache_function",
                "@functools.fast_call"
            ],
            "answer": "@functools.lru_cache"
        }
    ]
}

AIML_QUIZZES = {
    "easy": [
        {
            "question": "When and where was Artificial Intelligence officially launched as a scientific field?",
            "options": [
                "Dartmouth Summer Research Project in 1956",
                "Turing Institute in 1950",
                "MIT AI Lab in 1965",
                "Stanford AI Lab in 1970"
            ],
            "answer": "Dartmouth Summer Research Project in 1956"
        },
        {
            "question": "Who coined the term 'Artificial Intelligence' at the 1956 Dartmouth conference?",
            "options": [
                "John McCarthy",
                "Alan Turing",
                "Geoffrey Hinton",
                "Claude Shannon"
            ],
            "answer": "John McCarthy"
        },
        {
            "question": "Which historic event in 2012 ignited the modern Deep Learning revolution?",
            "options": [
                "AlexNet winning the ImageNet competition by a wide margin",
                "DeepBlue defeating Garry Kasparov at chess",
                "AlphaGo defeating Lee Sedol",
                "The initial release of ChatGPT"
            ],
            "answer": "AlexNet winning the ImageNet competition by a wide margin"
        },
        {
            "question": "What category describes AI systems designed for a single dedicated task (e.g., spam detection)?",
            "options": [
                "Narrow AI (Weak AI)",
                "General AI (AGI)",
                "Superintelligence",
                "Autonomous Consciousness"
            ],
            "answer": "Narrow AI (Weak AI)"
        },
        {
            "question": "In Supervised Machine Learning, what does the training dataset contain?",
            "options": [
                "Input feature vectors paired with ground-truth target labels",
                "Unlabeled text documents with no correct outputs",
                "Environment state-action reward records only",
                "Random noise arrays"
            ],
            "answer": "Input feature vectors paired with ground-truth target labels"
        },
        {
            "question": "Predicting continuous values like real estate prices or temperature is an example of what task?",
            "options": [
                "Regression",
                "Classification",
                "Clustering",
                "Dimensionality Reduction"
            ],
            "answer": "Regression"
        },
        {
            "question": "Which unsupervised learning task groups similar data points without using target labels?",
            "options": [
                "Clustering",
                "Supervised Classification",
                "Reinforcement Learning",
                "Deep Q-Learning"
            ],
            "answer": "Clustering"
        },
        {
            "question": "Which matrix displays True Positives, True Negatives, False Positives, and False Negatives?",
            "options": [
                "Confusion Matrix",
                "Covariance Matrix",
                "Hessian Matrix",
                "Scatter Matrix"
            ],
            "answer": "Confusion Matrix"
        },
        {
            "question": "Which Python toolkit is the standard library for classical Machine Learning algorithms?",
            "options": [
                "Scikit-Learn",
                "Flask",
                "Django",
                "BeautifulSoup"
            ],
            "answer": "Scikit-Learn"
        },
        {
            "question": "What is the primary objective of a Reinforcement Learning agent?",
            "options": [
                "To learn a policy that maximizes cumulative reward over time",
                "To calculate Euclidean distances between samples",
                "To compress high-dimensional matrices to 2D",
                "To classify images into predefined discrete labels"
            ],
            "answer": "To learn a policy that maximizes cumulative reward over time"
        }
    ],
    "medium": [
        {
            "question": "What issue occurs when an ML model overfits (suffers from high variance)?",
            "options": [
                "It memorizes training data noise and fails to generalize to new test data.",
                "It is too simple to capture the underlying pattern in the data.",
                "It achieves uniform 50% accuracy on all datasets.",
                "It executes with zero loss on test data."
            ],
            "answer": "It memorizes training data noise and fails to generalize to new test data."
        },
        {
            "question": "Which activation function maps any real-valued number into a probability range of (0, 1)?",
            "options": [
                "Sigmoid function",
                "ReLU function",
                "Linear identity function",
                "Step function"
            ],
            "answer": "Sigmoid function"
        },
        {
            "question": "How does a Random Forest ensemble make its final decision for classification tasks?",
            "options": [
                "By taking a majority vote across all individual decision trees",
                "By picking the output of the deepest single tree",
                "By averaging tree depths",
                "By selecting the tree trained on the newest sample"
            ],
            "answer": "By taking a majority vote across all individual decision trees"
        },
        {
            "question": "Which gradient boosting library is famous for dominating competitive tabular ML on Kaggle?",
            "options": [
                "XGBoost",
                "AlexNet",
                "Word2Vec",
                "K-Means"
            ],
            "answer": "XGBoost"
        },
        {
            "question": "What metric is commonly used by Decision Trees to select the optimal feature split at a node?",
            "options": [
                "Gini Impurity or Information Gain (Entropy)",
                "Mean Squared Error (MSE)",
                "R-squared coefficient",
                "Cosine Distance"
            ],
            "answer": "Gini Impurity or Information Gain (Entropy)"
        },
        {
            "question": "Which calculus rule is used during Backpropagation to compute loss gradients across layers?",
            "options": [
                "Chain rule",
                "Product rule",
                "L'Hopital's rule",
                "Quotient rule"
            ],
            "answer": "Chain rule"
        },
        {
            "question": "Which non-linear activation function is defined as f(x) = max(0, x)?",
            "options": [
                "ReLU (Rectified Linear Unit)",
                "Sigmoid",
                "Tanh",
                "Softmax"
            ],
            "answer": "ReLU (Rectified Linear Unit)"
        },
        {
            "question": "In classification evaluation, how is Precision calculated?",
            "options": [
                "True Positives / (True Positives + False Positives)",
                "True Positives / (True Positives + False Negatives)",
                "(True Positives + True Negatives) / Total",
                "False Positives / (False Positives + True Negatives)"
            ],
            "answer": "True Positives / (True Positives + False Positives)"
        },
        {
            "question": "How does the Kernel Trick enable Support Vector Machines (SVMs) to handle non-linear decision boundaries?",
            "options": [
                "It implicitly projects data into a higher-dimensional space where linear separation is possible.",
                "It removes outliers from the training set before modeling.",
                "It converts multi-class targets into regression values.",
                "It applies PCA compression down to two dimensions."
            ],
            "answer": "It implicitly projects data into a higher-dimensional space where linear separation is possible."
        },
        {
            "question": "Which optimization algorithm combining momentum and adaptive learning rates is standard for deep learning?",
            "options": [
                "Adam optimizer",
                "Standard Mini-Batch SGD",
                "L-BFGS",
                "Adagrad"
            ],
            "answer": "Adam optimizer"
        }
    ],
    "hard": [
        {
            "question": "Which key architectural component introduced in 'Attention Is All You Need' (2017) powers Transformers?",
            "options": [
                "Self-Attention mechanism",
                "Recurrent hidden state connections",
                "Convolutional pooling filters",
                "K-nearest neighbor distance matrices"
            ],
            "answer": "Self-Attention mechanism"
        },
        {
            "question": "What is the structural difference between LSTM and GRU recurrent networks?",
            "options": [
                "LSTM utilizes 3 gates (forget, input, output); GRU utilizes 2 gates (update, reset).",
                "LSTM relies on max pooling; GRU relies on spectral convolutions.",
                "GRU processes image pixels; LSTM processes tabular numbers.",
                "LSTM cannot process sequential time-series data."
            ],
            "answer": "LSTM utilizes 3 gates (forget, input, output); GRU utilizes 2 gates (update, reset)."
        },
        {
            "question": "Which object detection model processes an entire image in a single pass at real-time speeds (30-100+ FPS)?",
            "options": [
                "YOLO (You Only Look Once)",
                "Faster R-CNN",
                "Mask R-CNN",
                "U-Net"
            ],
            "answer": "YOLO (You Only Look Once)"
        },
        {
            "question": "How do Generative Adversarial Networks (GANs) operate?",
            "options": [
                "A Generator network creates fake samples while a Discriminator network tries to detect them.",
                "A single linear model fits a line over multi-dimensional points.",
                "An encoder compresses images into 1D text labels.",
                "A decision tree generates text words sequentially."
            ],
            "answer": "A Generator network creates fake samples while a Discriminator network tries to detect them."
        },
        {
            "question": "What architecture pairs an LLM with a vector database to retrieve facts before generating answers?",
            "options": [
                "Retrieval-Augmented Generation (RAG)",
                "Reinforcement Learning from Human Feedback (RLHF)",
                "Supervised Fine-Tuning (SFT)",
                "Model Quantization"
            ],
            "answer": "Retrieval-Augmented Generation (RAG)"
        },
        {
            "question": "Which Policy Gradient algorithm is widely used in ChatGPT's RLHF alignment process?",
            "options": [
                "PPO (Proximal Policy Optimization)",
                "Deep Q-Network (DQN)",
                "SARSA",
                "Actor-Critic with Experience Replay"
            ],
            "answer": "PPO (Proximal Policy Optimization)"
        },
        {
            "question": "What component in production MLOps serves as a central repository for computed features across training and serving?",
            "options": [
                "Feature Store",
                "Model Registry",
                "Artifact Repository",
                "CI/CD Pipeline"
            ],
            "answer": "Feature Store"
        },
        {
            "question": "Which explainable AI (XAI) frameworks provide interpretability for complex black-box machine learning models?",
            "options": [
                "LIME and SHAP",
                "PyTorch and TensorFlow",
                "BERT and GPT",
                "NumPy and Pandas"
            ],
            "answer": "LIME and SHAP"
        },
        {
            "question": "What modern generative model family surpassed GANs by learning to iteratively denoise Gaussian noise into images?",
            "options": [
                "Diffusion Models",
                "Variational Autoencoders",
                "Decision Forests",
                "Hidden Markov Models"
            ],
            "answer": "Diffusion Models"
        },
        {
            "question": "Which landmark European regulatory framework categorizes AI systems by risk level and enforces strict compliance?",
            "options": [
                "EU AI Act",
                "HIPAA Privacy Rule",
                "Sarbanes-Oxley Act",
                "ISO 27001"
            ],
            "answer": "EU AI Act"
        }
    ]
}

FULLSTACK_QUIZZES = {
    "easy": [
        {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "HighTech Machine Language", "Hyperlink Text Mode Logic", "Home Tool Markup Language"], "answer": "HyperText Markup Language"},
        {"question": "Which HTTP status code indicates a successful HTTP request?", "options": ["200 OK", "404 Not Found", "500 Server Error", "301 Redirect"], "answer": "200 OK"},
        {"question": "Which CSS layout module enables one-dimensional flexible alignment of elements?", "options": ["Flexbox", "Grid", "Float", "Table"], "answer": "Flexbox"},
        {"question": "What keyword in JavaScript ES6 declares a block-scoped variable that can be reassigned?", "options": ["let", "const", "var", "static"], "answer": "let"},
        {"question": "What does REST stand for in web API design?", "options": ["Representational State Transfer", "Remote Execution Service Protocol", "Responsive Enterprise State Tracking", "Realtime Execution System Transfer"], "answer": "Representational State Transfer"},
        {"question": "Which HTTP method is typically used to create a new resource on the server?", "options": ["POST", "GET", "DELETE", "OPTIONS"], "answer": "POST"},
        {"question": "What is the primary role of the Client in Client-Server architecture?", "options": ["To display the UI and send user requests to the server", "To store all database records permanently", "To execute back-end cron jobs", "To compile server-side C code"], "answer": "To display the UI and send user requests to the server"},
        {"question": "Which HTML tag is used to embed JavaScript code directly in an HTML file?", "options": ["<script>", "<js>", "<javascript>", "<code>"], "answer": "<script>"},
        {"question": "What is Node.js?", "options": ["A JavaScript runtime built on Chrome's V8 engine", "A CSS framework for styling web applications", "A relational database management system", "A web browser extensions manager"], "answer": "A JavaScript runtime built on Chrome's V8 engine"},
        {"question": "Which package manager is installed by default alongside Node.js?", "options": ["NPM", "Pip", "Maven", "Composer"], "answer": "NPM"}
    ],
    "medium": [
        {"question": "How does React's Virtual DOM improve application rendering performance?", "options": ["By diffing state changes in memory and batching minimal updates to the real DOM", "By bypassing browser rendering engines completely", "By compiling JavaScript into native machine assembly", "By storing all web pages in local storage"], "answer": "By diffing state changes in memory and batching minimal updates to the real DOM"},
        {"question": "What are the three dot-separated parts of a JSON Web Token (JWT)?", "options": ["Header, Payload, Signature", "Client, Server, Database", "Key, Value, Hash", "Request, Response, Error"], "answer": "Header, Payload, Signature"},
        {"question": "Which browser security mechanism restricts web pages from requesting resources from a different domain?", "options": ["CORS (Cross-Origin Resource Sharing)", "DOM Isolation", "CSP Header", "SSL Handshake"], "answer": "CORS (Cross-Origin Resource Sharing)"},
        {"question": "In Express.js middleware functions, what is the role of the next() function?", "options": ["To pass control to the next middleware in the request-response cycle", "To restart the HTTP server automatically", "To terminate the client connection immediately", "To compile templates to HTML"], "answer": "To pass control to the next middleware in the request-response cycle"},
        {"question": "What architecture pattern separates front-end code completely from back-end logic via APIs?", "options": ["Decoupled (Headless) Architecture", "Monolithic Architecture", "Peer-to-Peer Protocol", "Server-Side Includes"], "answer": "Decoupled (Headless) Architecture"},
        {"question": "Which React hook is specifically used for managing side effects in functional components?", "options": ["useEffect", "useState", "useContext", "useReducer"], "answer": "useEffect"},
        {"question": "In relational full-stack apps, what does ORM stand for?", "options": ["Object-Relational Mapping", "Operational Resource Management", "Open Request Model", "Optimized Routing Mechanism"], "answer": "Object-Relational Mapping"},
        {"question": "Which HTTP status code signifies an Unauthorized request due to missing or invalid authentication credentials?", "options": ["401 Unauthorized", "403 Forbidden", "400 Bad Request", "502 Bad Gateway"], "answer": "401 Unauthorized"},
        {"question": "What mechanism enables asynchronous non-blocking I/O operations in Node.js?", "options": ["Event Loop and Thread Pool (libuv)", "Multi-threaded process execution", "Synchronous blocking queues", "GPU acceleration"], "answer": "Event Loop and Thread Pool (libuv)"},
        {"question": "What is the main benefit of Single Page Applications (SPAs)?", "options": ["Dynamic content updates without reloading the entire web page", "No JavaScript required on the browser", "Automatic offline deployment without servers", "Zero network requests"], "answer": "Dynamic content updates without reloading the entire web page"}
    ],
    "hard": [
        {"question": "How can you prevent memory leaks when returning a clean-up function inside React's useEffect hook?", "options": ["Return a cleanup callback function that unsubscribes from listeners or clears timers", "Set dependency array to null", "Call process.exit()", "Use useLayoutEffect without dependencies"], "answer": "Return a cleanup callback function that unsubscribes from listeners or clears timers"},
        {"question": "Which protocol provides full-duplex, persistent, real-time communication between client and server over a single TCP connection?", "options": ["WebSocket Protocol", "HTTP/1.1 Polling", "REST Over HTTP", "GraphQL Query"], "answer": "WebSocket Protocol"},
        {"question": "How does Server-Side Rendering (SSR) in frameworks like Next.js differ from Client-Side Rendering (CSR)?", "options": ["SSR renders HTML on the server for each request, improving initial load speed and SEO", "SSR executes only inside the user's web browser", "CSR generates static PDF files on the server", "SSR eliminates the need for database storage"], "answer": "SSR renders HTML on the server for each request, improving initial load speed and SEO"},
        {"question": "How does a server verify the integrity of an incoming JWT token without querying a database?", "options": ["By hashing header+payload with the secret key and comparing it against the incoming signature", "By decrypting the token with the client's password", "By sending a ping back to the authorization server", "By checking local storage cookies"], "answer": "By hashing header+payload with the secret key and comparing it against the incoming signature"},
        {"question": "Why is database connection pooling essential in high-throughput full-stack backend servers?", "options": ["It reuses a fixed set of open connections, avoiding the overhead of creating connections per request", "It encrypts database tables on disk", "It automatically writes SQL queries without developer input", "It converts SQL queries into React components"], "answer": "It reuses a fixed set of open connections, avoiding the overhead of creating connections per request"},
        {"question": "What is the purpose of Database Migrations in web framework backends like Django or Prisma?", "options": ["To version-control and incrementally propagate database schema changes safely", "To transfer user passwords into local storage", "To convert SQL tables into JSON files automatically", "To compress image uploads"], "answer": "To version-control and incrementally propagate database schema changes safely"},
        {"question": "Which HTTP security header mitigates Cross-Site Scripting (XSS) by restricting sources of executable scripts?", "options": ["Content-Security-Policy (CSP)", "Access-Control-Allow-Origin", "X-Frame-Options", "Strict-Transport-Security"], "answer": "Content-Security-Policy (CSP)"},
        {"question": "What is the primary role of a Reverse Proxy like Nginx in web application architecture?", "options": ["To handle SSL termination, load balancing, and route client traffic to backend servers", "To render React components on client devices", "To store user passwords in plain text", "To act as a primary database engine"], "answer": "To handle SSL termination, load balancing, and route client traffic to backend servers"},
        {"question": "In REST API design, what makes an HTTP method idempotent?", "options": ["Making multiple identical requests produces the exact same server state as a single request", "The request executes in less than 1 millisecond", "The method returns an empty JSON payload", "The request is executed on the front-end only"], "answer": "Making multiple identical requests produces the exact same server state as a single request"},
        {"question": "What design technique delays component loading until it is actually needed, optimizing initial bundle size?", "options": ["Lazy Loading / Code Splitting", "Eager Evaluation", "Synchronous Import", "Server Polling"], "answer": "Lazy Loading / Code Splitting"}
    ]
}

JAVADEV_QUIZZES = {
    "easy": [
        {"question": "What does JVM stand for in the Java ecosystem?", "options": ["Java Virtual Machine", "Java Verified Module", "Java Variable Manager", "Java Visual Mechanism"], "answer": "Java Virtual Machine"},
        {"question": "What is the core slogan representing Java's cross-platform portability?", "options": ["Write Once, Run Anywhere (WORA)", "Code Fast, Deploy Daily", "Compile Once, Execute Everywhere", "Universal Bytecode Language"], "answer": "Write Once, Run Anywhere (WORA)"},
        {"question": "Which entry point method signature is required for executing a standalone Java application?", "options": ["public static void main(String[] args)", "public void main(String args)", "static main(String[] args)", "void main()"], "answer": "public static void main(String[] args)"},
        {"question": "Which keyword is used in Java to define a class that cannot be subclassed?", "options": ["final", "static", "abstract", "private"], "answer": "final"},
        {"question": "What is the default initial value of an uninitialized int field in a Java class?", "options": ["0", "null", "1", "undefined"], "answer": "0"},
        {"question": "Which Java keyword is used to inherit properties and methods from a parent class?", "options": ["extends", "implements", "inherits", "super"], "answer": "extends"},
        {"question": "Which key feature makes Java Strings immutable?", "options": ["Once created, their internal character array cannot be modified", "They can only be read by single-threaded code", "They are stored exclusively in stack memory", "They are automatically converted to integers"], "answer": "Once created, their internal character array cannot be modified"},
        {"question": "Which compiler tool converts Java source code (.java) into bytecode (.class)?", "options": ["javac", "java", "javadoc", "jar"], "answer": "javac"},
        {"question": "What interface keyword is used by a Java class to promise implementations for abstract methods?", "options": ["implements", "extends", "uses", "override"], "answer": "implements"},
        {"question": "Which package containing core classes like String and System is imported automatically into every Java file?", "options": ["java.lang", "java.util", "java.io", "java.net"], "answer": "java.lang"}
    ],
    "medium": [
        {"question": "What is the internal difference between ArrayList and LinkedList in Java?", "options": ["ArrayList uses a resizable array; LinkedList uses a doubly-linked node structure", "ArrayList allows duplicates; LinkedList does not", "LinkedList is thread-safe by default; ArrayList is not", "ArrayList is stored on stack; LinkedList on heap"], "answer": "ArrayList uses a resizable array; LinkedList uses a doubly-linked node structure"},
        {"question": "When storing custom objects in a Java HashMap, which two methods MUST be overridden together?", "options": ["equals() and hashCode()", "toString() and clone()", "compareTo() and equals()", "serialize() and deserialize()"], "answer": "equals() and hashCode()"},
        {"question": "What feature introduced in Java 7 automatically closes resources like streams when exiting the block?", "options": ["Try-with-resources statement", "AutoCloseable interface annotation", "Garbage Collection finalizer", "Resource pooling manager"], "answer": "Try-with-resources statement"},
        {"question": "In Java Spring Boot, what annotation is used to inject dependencies automatically into a class field or constructor?", "options": ["@Autowired", "@Injectable", "@Bean", "@Service"], "answer": "@Autowired"},
        {"question": "What does the 'transient' keyword indicate when applied to a class field in Java?", "options": ["The field should be ignored during object serialization", "The field value can never be modified", "The field is shared across all threads without locking", "The field is saved directly in SQL database"], "answer": "The field should be ignored during object serialization"},
        {"question": "What intermediate operation in Java Streams API filters elements based on a given Predicate?", "options": ["filter()", "map()", "collect()", "reduce()"], "answer": "filter()"},
        {"question": "What exception is thrown when attempting to invoke a method on an object variable pointing to null?", "options": ["NullPointerException", "IllegalArgumentException", "ClassCastException", "IllegalStateException"], "answer": "NullPointerException"},
        {"question": "In Spring Boot, which annotation marks a class as a RESTful controller returning JSON responses?", "options": ["@RestController", "@Controller", "@Component", "@Repository"], "answer": "@RestController"},
        {"question": "What is the purpose of the Java Garbage Collector (GC)?", "options": ["To automatically reclaim memory occupied by unreferenced objects on the heap", "To clean up unused source code files", "To delete temporary files from hard drive", "To close open network sockets"], "answer": "To automatically reclaim memory occupied by unreferenced objects on the heap"},
        {"question": "What is the difference between Checked and Unchecked exceptions in Java?", "options": ["Checked exceptions must be declared or caught at compile-time; Unchecked exceptions inherit from RuntimeException", "Unchecked exceptions crash the JVM immediately; Checked exceptions do not", "Checked exceptions are written in C++; Unchecked in Java", "There is no difference in Java"], "answer": "Checked exceptions must be declared or caught at compile-time; Unchecked exceptions inherit from RuntimeException"}
    ],
    "hard": [
        {"question": "What guarantee does the 'volatile' keyword provide for variable access across threads in Java?", "options": ["Guarantees read/write visibility directly from main memory, preventing CPU cache staleness", "Guarantees atomic execution of multi-step operations", "Guarantees thread-safe lock acquisitions", "Guarantees immutable variable state"], "answer": "Guarantees read/write visibility directly from main memory, preventing CPU cache staleness"},
        {"question": "How does the G1 (Garbage-First) Collector differ from legacy Parallel GC implementations?", "options": ["It divides the heap into equal region blocks and collects regions with the most garbage first to minimize pause times", "It stops the application for hours to defragment memory", "It runs exclusively on single-core CPUs", "It bypasses heap memory and collects stack frames"], "answer": "It divides the heap into equal region blocks and collects regions with the most garbage first to minimize pause times"},
        {"question": "In Spring Data JPA, what does the @Transactional(propagation = Propagation.REQUIRES_NEW) setting do?", "options": ["Suspends the current transaction and executes code in a newly created independent transaction", "Joins the existing active transaction without creating a new one", "Throws an exception if a transaction already exists", "Executes the database query asynchronously without transactions"], "answer": "Suspends the current transaction and executes code in a newly created independent transaction"},
        {"question": "What class in java.util.concurrent represents an asynchronous computation that can be chained with completion callbacks?", "options": ["CompletableFuture", "Thread", "FutureTask", "Runnable"], "answer": "CompletableFuture"},
        {"question": "What is Type Erasure in Java Generics?", "options": ["Generic type parameters are removed by the compiler, enforcing type safety at compile time and using raw types in bytecode", "Generics convert primitive int values to Objects at runtime", "Type hints are appended to class names at runtime", "Generics delete unused classes during compilation"], "answer": "Generic type parameters are removed by the compiler, enforcing type safety at compile time and using raw types in bytecode"},
        {"question": "Which design pattern is implemented by the Spring IoC (Inversion of Control) Container?", "options": ["Dependency Injection Pattern", "Singleton Pattern", "Observer Pattern", "Factory Method Pattern"], "answer": "Dependency Injection Pattern"},
        {"question": "How does Java memory allocation split between Stack and Heap?", "options": ["Stack holds primitive local variables and method call frames; Heap holds objects and instance variables", "Heap holds method code; Stack holds database tables", "Stack holds all global objects; Heap holds thread execution loops", "Stack and Heap share the same unsegmented memory pool"], "answer": "Stack holds primitive local variables and method call frames; Heap holds objects and instance variables"},
        {"question": "What causes a java.lang.OutOfMemoryError: Java heap space?", "options": ["The application allocated more objects on the heap than the maximum allowed JVM memory (-Xmx)", "Stack overflow due to deep recursion", "Missing .jar library dependencies", "Syntax error in main method"], "answer": "The application allocated more objects on the heap than the maximum allowed JVM memory (-Xmx)"},
        {"question": "What is the function of the ConcurrentHashMap class over Hashtable or synchronizedMap?", "options": ["It allows concurrent reads and bucket-level lock granularity for high-throughput thread-safe access", "It locks the entire map on every read operation", "It disables multi-threading to prevent race conditions", "It stores entries on disk instead of RAM"], "answer": "It allows concurrent reads and bucket-level lock granularity for high-throughput thread-safe access"},
        {"question": "What method on the Thread class allows one thread to wait until another thread completes its execution?", "options": ["join()", "yield()", "sleep()", "wait()"], "answer": "join()"}
    ]
}

DATASCIENCE_QUIZZES = {
    "easy": [
        {"question": "What is the primary data structure provided by Pandas for handling 2D tabular data with labeled axes?", "options": ["DataFrame", "Series", "NDArray", "DataList"], "answer": "DataFrame"},
        {"question": "In statistics, what is the middle value of a sorted dataset called?", "options": ["Median", "Mean", "Mode", "Variance"], "answer": "Median"},
        {"question": "Which Python library is foundational for scientific computing and n-dimensional array operations?", "options": ["NumPy", "Flask", "Pygame", "Requests"], "answer": "NumPy"},
        {"question": "What type of chart is ideal for visualizing the relationship and correlation between two continuous numeric variables?", "options": ["Scatter Plot", "Bar Chart", "Pie Chart", "Histogram"], "answer": "Scatter Plot"},
        {"question": "In hypothesis testing, what standard threshold (alpha level) is commonly used to determine statistical significance?", "options": ["0.05", "0.50", "0.10", "1.00"], "answer": "0.05"},
        {"question": "Which Pandas method is used to remove missing or null (NaN) rows from a DataFrame?", "options": ["dropna()", "fillna()", "clearna()", "remove_null()"], "answer": "dropna()"},
        {"question": "What metric measures the spread or dispersion of data points around their mean?", "options": ["Standard Deviation", "Median", "Mode", "Skewness"], "answer": "Standard Deviation"},
        {"question": "Which data visualization library in Python is built on top of Matplotlib and offers high-level statistical graphics?", "options": ["Seaborn", "Bokeh", "Plotly", "OpenCV"], "answer": "Seaborn"},
        {"question": "What is the process of transforming raw data into meaningful features for machine learning models?", "options": ["Feature Engineering", "Data Scraping", "Model Compilation", "Hyperparameter Tuning"], "answer": "Feature Engineering"},
        {"question": "Which metric evaluates regression model performance by averaging the absolute differences between predictions and actual values?", "options": ["Mean Absolute Error (MAE)", "Accuracy Score", "Precision", "Log-Loss"], "answer": "Mean Absolute Error (MAE)"}
    ],
    "medium": [
        {"question": "What does the groupby() method in Pandas return before an aggregation function is applied?", "options": ["A DataFrameGroupBy object", "A numpy array", "A sorted list", "A boolean mask"], "answer": "A DataFrameGroupBy object"},
        {"question": "What is the difference between StandardScaler and MinMaxScaler in data preprocessing?", "options": ["StandardScaler rescales data to mean=0 and std=1; MinMaxScaler rescales data to a fixed range (typically 0 to 1)", "StandardScaler converts text to numbers; MinMaxScaler removes outliers", "MinMaxScaler is for categorical data; StandardScaler is for images", "StandardScaler doubles the dataset size"], "answer": "StandardScaler rescales data to mean=0 and std=1; MinMaxScaler rescales data to a fixed range (typically 0 to 1)"},
        {"question": "What statistic measures the strength and direction of a linear relationship between two numerical variables?", "options": ["Pearson Correlation Coefficient (r)", "Chi-Square statistic", "Standard Error", "Gini Index"], "answer": "Pearson Correlation Coefficient (r)"},
        {"question": "In exploratory data analysis, what does a Box Plot display?", "options": ["The 5-number summary: minimum, first quartile (Q1), median, third quartile (Q3), and maximum", "The density distribution of text word counts", "The confusion matrix of a classifier", "The loss curve over training epochs"], "answer": "The 5-number summary: minimum, first quartile (Q1), median, third quartile (Q3), and maximum"},
        {"question": "Which technique evaluates model generalization by splitting data into K subsets and iteratively training/testing on each?", "options": ["K-Fold Cross-Validation", "Bootstrapping", "Holdout Testing", "Grid Search"], "answer": "K-Fold Cross-Validation"},
        {"question": "What problem occurs when independent variables in a regression model are highly correlated with each other?", "options": ["Multicollinearity", "Heteroscedasticity", "Autocorrelation", "Overfitting"], "answer": "Multicollinearity"},
        {"question": "Which metric is best suited for assessing class imbalance in binary classification tasks over simple Accuracy?", "options": ["ROC-AUC or F1-Score", "Mean Squared Error", "R-Squared", "Cosine Similarity"], "answer": "ROC-AUC or F1-Score"},
        {"question": "In Pandas, what does the merge() function perform?", "options": ["Database-style join operations (inner, outer, left, right) on DataFrames", "Concatenation of DataFrames along rows", "Exporting data to Excel files", "Deleting duplicate rows"], "answer": "Database-style join operations (inner, outer, left, right) on DataFrames"},
        {"question": "What is Central Limit Theorem (CLT) in statistics?", "options": ["The distribution of sample means approaches a normal distribution as sample size grows, regardless of population shape", "The mean of any dataset is always zero", "All random variables follow a uniform distribution", "Outliers increase sample size automatically"], "answer": "The distribution of sample means approaches a normal distribution as sample size grows, regardless of population shape"},
        {"question": "What technique reduces high-dimensional feature spaces while preserving maximum data variance?", "options": ["Principal Component Analysis (PCA)", "Linear Regression", "One-Hot Encoding", "K-Means Clustering"], "answer": "Principal Component Analysis (PCA)"}
    ],
    "hard": [
        {"question": "How is Variance Inflation Factor (VIF) used in statistical data analysis?", "options": ["To detect and quantify the severity of multicollinearity among predictor variables", "To measure the accuracy of deep learning neural networks", "To compute memory allocation of DataFrames", "To normalize audio frequency signals"], "answer": "To detect and quantify the severity of multicollinearity among predictor variables"},
        {"question": "What statistical test is used to check whether a time series dataset is stationary?", "options": ["Augmented Dickey-Fuller (ADF) Test", "Student's t-test", "Chi-Square Test of Independence", "Mann-Whitney U Test"], "answer": "Augmented Dickey-Fuller (ADF) Test"},
        {"question": "How does Principal Component Analysis (PCA) derive its orthogonal principal components?", "options": ["By computing the eigenvectors and eigenvalues of the data covariance matrix", "By running gradient descent on classification loss", "By calculating K-nearest neighbor distances", "By applying random decision tree splits"], "answer": "By computing the eigenvectors and eigenvalues of the data covariance matrix"},
        {"question": "What is the difference between Type I and Type II errors in statistical hypothesis testing?", "options": ["Type I error is rejecting a true null hypothesis (false positive); Type II error is failing to reject a false null hypothesis (false negative)", "Type I error occurs in Python 2; Type II in Python 3", "Type I error is low variance; Type II error is high bias", "Type I error occurs only in regression models"], "answer": "Type I error is rejecting a true null hypothesis (false positive); Type II error is failing to reject a false null hypothesis (false negative)"},
        {"question": "In Time Series analysis, what are the three components of an ARIMA(p, d, q) model?", "options": ["p: Auto-Regressive order, d: Differencing degree, q: Moving-Average order", "p: Polynomial degree, d: Data dimension, q: Quantile cut", "p: Precision, d: Density, q: Quality", "p: Penalty factor, d: Decay rate, q: Queue size"], "answer": "p: Auto-Regressive order, d: Differencing degree, q: Moving-Average order"},
        {"question": "What technique addresses data imbalance by generating synthetic minority class samples?", "options": ["SMOTE (Synthetic Minority Over-sampling Technique)", "Random Undersampling", "One-Hot Encoding", "MinMax Scaling"], "answer": "SMOTE (Synthetic Minority Over-sampling Technique)"},
        {"question": "What does R-squared (Coefficient of Determination) quantify in a regression model?", "options": ["The proportion of variance in the dependent variable predictable from the independent variables", "The exact count of correct classifications", "The probability of hypothesis significance", "The execution time of model training"], "answer": "The proportion of variance in the dependent variable predictable from the independent variables"},
        {"question": "How does Bayesian Inference differ from Frequentist statistical inference?", "options": ["Bayesian updates prior probability beliefs with observed data to form a posterior distribution; Frequentist treats parameters as fixed unknown constants", "Bayesian relies exclusively on neural networks", "Frequentist requires Markov Chain Monte Carlo sampling", "There is no mathematical difference"], "answer": "Bayesian updates prior probability beliefs with observed data to form a posterior distribution; Frequentist treats parameters as fixed unknown constants"},
        {"question": "Which algorithm framework uses Bayesian optimization to tune hyperparameter spaces efficiently?", "options": ["Optuna / Hyperopt", "GridSearchCV", "RandomSearch", "Manual Tuning"], "answer": "Optuna / Hyperopt"},
        {"question": "In A/B testing, what is the purpose of computing Statistical Power (1 - beta)?", "options": ["The probability of correctly detecting a true effect when one actually exists", "The percentage of users assigned to treatment group A", "The speed of web page load rendering", "The maximum allowed sample size"], "answer": "The probability of correctly detecting a true effect when one actually exists"}
    ]
}

BLOCKCHAIN_QUIZZES = {
    "easy": [
        {"question": "What is a Blockchain?", "options": ["A decentralized, distributed, immutable public ledger of blocks containing cryptographically signed transactions", "A centralized SQL database hosted by a single bank", "A cloud storage drive for backing up personal files", "A web browser plugin for downloading video files"], "answer": "A decentralized, distributed, immutable public ledger of blocks containing cryptographically signed transactions"},
        {"question": "Which cryptographic hash algorithm is famously used in Bitcoin's Proof of Work algorithm?", "options": ["SHA-256", "MD5", "AES-128", "RSA-2048"], "answer": "SHA-256"},
        {"question": "Who published the Bitcoin whitepaper in 2008 under a pseudonym?", "options": ["Satoshi Nakamoto", "Vitalik Buterin", "Nick Szabo", "Gavin Gavin"], "answer": "Satoshi Nakamoto"},
        {"question": "What key component of asymmetric cryptography is shared publicly to receive crypto funds?", "options": ["Public Key (or Wallet Address)", "Private Key", "Seed Phrase", "Password"], "answer": "Public Key (or Wallet Address)"},
        {"question": "What is a Smart Contract?", "options": ["A self-executing contract with terms directly written into immutable code on a blockchain", "A legal PDF document signed with a stylus", "A cloud server contract with AWS", "A trade agreement between two countries"], "answer": "A self-executing contract with terms directly written into immutable code on a blockchain"},
        {"question": "Which programming language is primarily used for writing Ethereum smart contracts?", "options": ["Solidity", "Python", "Java", "Ruby"], "answer": "Solidity"},
        {"question": "What unit represents computational fee cost required to execute transactions on Ethereum?", "options": ["Gas", "Watt", "Byte", "Satoshi"], "answer": "Gas"},
        {"question": "What token standard defines interchangeable fungible tokens on the Ethereum network?", "options": ["ERC-20", "ERC-721", "ERC-1155", "ZIP-20"], "answer": "ERC-20"},
        {"question": "What token standard defines non-fungible tokens (NFTs) representing unique digital assets?", "options": ["ERC-721", "ERC-20", "ERC-200", "HTTP-404"], "answer": "ERC-721"},
        {"question": "What is the process of validating transactions and proposing new blocks to a blockchain called?", "options": ["Mining or Validating", "Scraping", "Compiling", "Rendering"], "answer": "Mining or Validating"}
    ],
    "medium": [
        {"question": "How does Proof of Stake (PoS) differ from Proof of Work (PoW)?", "options": ["PoS validators lock up collateral tokens (stake) to propose blocks, replacing energy-intensive hash computations", "PoS requires supercomputers running GPUs continuously", "PoW has zero transaction fees", "PoS cannot support smart contracts"], "answer": "PoS validators lock up collateral tokens (stake) to propose blocks, replacing energy-intensive hash computations"},
        {"question": "What data structure allows efficient, secure verification of contents in large blocks using cryptographic hashes?", "options": ["Merkle Tree (Hash Tree)", "Binary Search Tree", "Linked List", "Stack"], "answer": "Merkle Tree (Hash Tree)"},
        {"question": "What is the Ethereum Virtual Machine (EVM)?", "options": ["The sandboxed runtime environment that executes smart contract bytecode across all Ethereum nodes", "A physical server located at Ethereum foundation headquarters", "A desktop wallet application", "A mining rig GPU"], "answer": "The sandboxed runtime environment that executes smart contract bytecode across all Ethereum nodes"},
        {"question": "What attack occurs if an entity controls more than 50% of a blockchain network's mining hash rate?", "options": ["51% Attack", "Reentrancy Attack", "Sybil Attack", "Man-in-the-Middle Attack"], "answer": "51% Attack"},
        {"question": "What does DeFi stand for in the blockchain ecosystem?", "options": ["Decentralized Finance", "Definite Financial Instrument", "Digital Encryption Framework", "Direct Electronic Fund Transfer"], "answer": "Decentralized Finance"},
        {"question": "How does a Hard Fork differ from a Soft Fork in blockchain governance?", "options": ["A Hard Fork is a non-backward-compatible software upgrade splitting the chain; a Soft Fork is backward-compatible", "A Soft Fork deletes the transaction history completely", "A Hard Fork requires hardware replacement", "Soft Forks can only happen on private chains"], "answer": "A Hard Fork is a non-backward-compatible software upgrade splitting the chain; a Soft Fork is backward-compatible"},
        {"question": "What is an Automated Market Maker (AMM) in decentralized exchanges like Uniswap?", "options": ["A smart contract protocol that uses mathematical liquidity pools to price assets without order books", "A human trader matching orders manually", "A centralized bank clearing house", "A high-frequency trading algorithm on Wall Street"], "answer": "A smart contract protocol that uses mathematical liquidity pools to price assets without order books"},
        {"question": "In Solidity, what modifier restricts a function so it can only be executed by the contract owner?", "options": ["onlyOwner (custom modifier)", "private", "pure", "view"], "answer": "onlyOwner (custom modifier)"},
        {"question": "What is the function of a Blockchain Oracle (e.g., Chainlink)?", "options": ["To feed off-chain real-world data (e.g., asset prices, weather) into on-chain smart contracts securely", "To predict future cryptocurrency prices", "To mine blocks faster", "To compress blockchain storage"], "answer": "To feed off-chain real-world data (e.g., asset prices, weather) into on-chain smart contracts securely"},
        {"question": "What is IPFS (InterPlanetary File System)?", "options": ["A peer-to-peer decentralized media storage protocol using content addressing hashes", "A NASA satellite network protocol", "A proprietary cloud server product by Google", "A relational database engine"], "answer": "A peer-to-peer decentralized media storage protocol using content addressing hashes"}
    ],
    "hard": [
        {"question": "How does a Reentrancy Attack work in Solidity smart contracts?", "options": ["An external malicious contract repeatedly calls back into a withdraw function before the vulnerable contract updates state balances", "An attacker guesses the private key using brute force", "An attacker overloads the network with spam gas", "An attacker modifies historical block hashes"], "answer": "An external malicious contract repeatedly calls back into a withdraw function before the vulnerable contract updates state balances"},
        {"question": "What pattern protects Solidity contracts against Reentrancy vulnerabilities?", "options": ["Checks-Effects-Interactions pattern or ReentrancyGuard mutex lock", "Making all functions public", "Disabling gas limits", "Using assembly code for transfers"], "answer": "Checks-Effects-Interactions pattern or ReentrancyGuard mutex lock"},
        {"question": "What scaling solution executes transactions off-chain in batches and posts cryptographic proof back to Layer 1?", "options": ["Rollups (Optimistic & Zero-Knowledge Rollups)", "Sidechains", "State Channels", "Sharding"], "answer": "Rollups (Optimistic & Zero-Knowledge Rollups)"},
        {"question": "What cryptographic technique allows one party to prove to another that a statement is true without revealing any underlying data?", "options": ["Zero-Knowledge Proofs (ZK-SNARKs / ZK-STARKs)", "Diffie-Hellman Key Exchange", "Elliptic Curve Digital Signature", "Homomorphic Encryption"], "answer": "Zero-Knowledge Proofs (ZK-SNARKs / ZK-STARKs)"},
        {"question": "How does MEV (Maximal Extractable Value) impact blockchain transaction ordering?", "options": ["Miners/validators reorder, insert, or censor transactions within a block to extract arbitrage or front-running profit", "Validators double total coin supply", "Transactions become instantly free of gas fees", "Network bandwidth drops to zero"], "answer": "Miners/validators reorder, insert, or censor transactions within a block to extract arbitrage or front-running profit"},
        {"question": "In Solidity, what is the difference between 'memory' and 'storage' location data keywords?", "options": ["'storage' persists data permanently on blockchain state; 'memory' holds temporary data during function execution", "'memory' costs more gas than 'storage'", "'storage' data is erased when transaction ends", "There is no functional difference"], "answer": "'storage' persists data permanently on blockchain state; 'memory' holds temporary data during function execution"},
        {"question": "What consensus mechanism is used by enterprise private permissioned blockchains like Hyperledger Fabric?", "options": ["Practical Byzantine Fault Tolerance (PBFT) or Raft", "Proof of Work", "Proof of Burn", "Proof of Elapsed Time"], "answer": "Practical Byzantine Fault Tolerance (PBFT) or Raft"},
        {"question": "What is the purpose of the ERC-4337 standard in Ethereum development?", "options": ["Enables Account Abstraction, converting user wallets into smart contracts with social recovery and gasless transactions", "Defines mandatory KYC rules for all wallets", "Standardizes NFT metadata images", "Replaces EVM bytecode with WebAssembly"], "answer": "Enables Account Abstraction, converting user wallets into smart contracts with social recovery and gasless transactions"},
        {"question": "How does an Unspent Transaction Output (UTXO) model used by Bitcoin differ from Ethereum's Account model?", "options": ["UTXO tracks discrete coin chunks spent as inputs to create new outputs; Account model maintains global account balance states", "UTXO model requires smart contracts for simple transfers", "Account model prevents double-spending without consensus", "UTXO stores balances in SQL databases"], "answer": "UTXO tracks discrete coin chunks spent as inputs to create new outputs; Account model maintains global account balance states"},
        {"question": "What mechanism prevents infinite loops from hanging nodes during EVM smart contract execution?", "options": ["Gas limit enforcement — transactions revert when gas runs out", "Max execution time clock of 5 seconds", "Static analysis at compile time", "Manual supervisor node termination"], "answer": "Gas limit enforcement — transactions revert when gas runs out"}
    ]
}

CYBERSECURITY_QUIZZES = {
    "easy": [
        {"question": "What does the CIA Triad represent in cybersecurity fundamentals?", "options": ["Confidentiality, Integrity, Availability", "Control, Inspection, Authorization", "Centralized Information Architecture", "Cyber Inspection Agency"], "answer": "Confidentiality, Integrity, Availability"},
        {"question": "What tool or hardware device inspects and filters incoming/outgoing network traffic based on security rules?", "options": ["Firewall", "Router", "Switch", "Modem"], "answer": "Firewall"},
        {"question": "What social engineering attack uses deceptive emails or messages to trick users into revealing sensitive credentials?", "options": ["Phishing", "Man-in-the-Middle", "SQL Injection", "Buffer Overflow"], "answer": "Phishing"},
        {"question": "Which network port is the standard default for secure HTTPS web traffic?", "options": ["443", "80", "22", "21"], "answer": "443"},
        {"question": "What is Malware?", "options": ["Malicious software designed to infiltrate, damage, or compromise computer systems", "Antivirus security software", "A network routing protocol", "An encrypted database file"], "answer": "Malicious software designed to infiltrate, damage, or compromise computer systems"},
        {"question": "Which security measure requires users to provide two distinct authentication factors to gain access?", "options": ["Multi-Factor Authentication (MFA / 2FA)", "Single Sign-On (SSO)", "Biometric Scan only", "Password Reset Link"], "answer": "Multi-Factor Authentication (MFA / 2FA)"},
        {"question": "What type of attack floods a web server with artificial traffic to render it unavailable to legitimate users?", "options": ["Denial of Service (DoS / DDoS)", "Eavesdropping", "Cross-Site Scripting", "Privilege Escalation"], "answer": "Denial of Service (DoS / DDoS)"},
        {"question": "Which protocol secures remote command-line login access over port 22?", "options": ["SSH (Secure Shell)", "Telnet", "FTP", "HTTP"], "answer": "SSH (Secure Shell)"},
        {"question": "What is Ransomware?", "options": ["Malware that encrypts victim files and demands payment for the decryption key", "Software that displays pop-up ads", "A utility that cleans browser history", "A hardware firewall appliance"], "answer": "Malware that encrypts victim files and demands payment for the decryption key"},
        {"question": "What organization maintains the widely recognized OWASP Top 10 list of web application security risks?", "options": ["Open Web Application Security Project (OWASP)", "Open Source Security Initiative", "Online Web Protection System", "Operational Web Advisory Group"], "answer": "Open Web Application Security Project (OWASP)"}
    ],
    "medium": [
        {"question": "How do Prepared Statements (Parameterized Queries) prevent SQL Injection attacks?", "options": ["They separate SQL code structure from user input parameters, preventing input from executing as SQL commands", "They encrypt database credentials stored in config files", "They disable HTTP POST requests", "They limit SQL queries to 10 rows"], "answer": "They separate SQL code structure from user input parameters, preventing input from executing as SQL commands"},
        {"question": "What is the difference between Stored XSS and Reflected XSS attacks?", "options": ["Stored XSS permanently saves malicious script into the database; Reflected XSS reflects script off immediate server requests", "Reflected XSS affects mobile phones only; Stored XSS affects servers", "Stored XSS uses SQL; Reflected XSS uses C++", "There is no technical difference"], "answer": "Stored XSS permanently saves malicious script into the database; Reflected XSS reflects script off immediate server requests"},
        {"question": "How does Asymmetric Encryption differ from Symmetric Encryption?", "options": ["Asymmetric uses a key pair (Public/Private key); Symmetric uses a single shared secret key for encryption and decryption", "Symmetric encryption is uncrackable; Asymmetric is easily broken", "Asymmetric encryption does not use mathematics", "Symmetric uses RSA exclusively"], "answer": "Asymmetric uses a key pair (Public/Private key); Symmetric uses a single shared secret key for encryption and decryption"},
        {"question": "What security issue is caused by Cross-Site Request Forgery (CSRF)?", "options": ["Tricking an authenticated victim browser into submitting unauthorized requests to a trusted web application", "Stealing user passwords directly from RAM", "Encrypting victim hard drives remotely", "Listening to unencrypted Wi-Fi packets"], "answer": "Tricking an authenticated victim browser into submitting unauthorized requests to a trusted web application"},
        {"question": "What key exchange algorithm allows two parties to establish a shared secret key over an insecure channel?", "options": ["Diffie-Hellman Key Exchange", "AES-256", "MD5 Hashing", "Base64 Encoding"], "answer": "Diffie-Hellman Key Exchange"},
        {"question": "What is the purpose of an Intrusion Detection System (IDS) vs an Intrusion Prevention System (IPS)?", "options": ["IDS monitors and alerts on suspicious activity; IPS actively blocks or mitigates detected threats inline", "IDS deletes infected files; IPS generates weekly audit PDFs", "IPS operates only on physical hardware; IDS operates in software", "IDS requires manual virus scans"], "answer": "IDS monitors and alerts on suspicious activity; IPS actively blocks or mitigates detected threats inline"},
        {"question": "What technique is used by network engineers to capture and analyze live network packets on an interface?", "options": ["Packet Sniffing / Analysis (e.g., Wireshark)", "Port Knocking", "Reverse Shell Execution", "DNS Poisoning"], "answer": "Packet Sniffing / Analysis (e.g., Wireshark)"},
        {"question": "What is a Zero-Day Vulnerability?", "options": ["A software security flaw that is unknown to the vendor and has no available security patch", "A security flaw that takes 0 days to patch", "An attack launched on January 1st", "A bug in open-source software older than 10 years"], "answer": "A software security flaw that is unknown to the vendor and has no available security patch"},
        {"question": "In Public Key Infrastructure (PKI), what role does a Certificate Authority (CA) serve?", "options": ["Issues digital certificates validating the cryptographic identity of domain owners", "Stores all client passwords in plain text", "Generates daily network backups", "Monitors employee web browsing logs"], "answer": "Issues digital certificates validating the cryptographic identity of domain owners"},
        {"question": "What is the principle of Least Privilege (PoLP)?", "options": ["Granting users and processes only the minimum access privileges necessary to perform their legitimate job tasks", "Disabling admin accounts permanently", "Allowing all employees read access to all files", "Setting all file permissions to 777"], "answer": "Granting users and processes only the minimum access privileges necessary to perform their legitimate job tasks"}
    ],
    "hard": [
        {"question": "What is the core philosophical axiom of Zero Trust Architecture (ZTA)?", "options": ["'Never Trust, Always Verify' — assume breach and verify every request regardless of origin", "Trust internal corporate network traffic implicitly", "Encrypt only external email messages", "Require passwords to be updated every 24 hours"], "answer": "'Never Trust, Always Verify' — assume breach and verify every request regardless of origin"},
        {"question": "How does a Buffer Overflow vulnerability occur in C/C++ applications?", "options": ["Writing more data to a fixed memory buffer than it can hold, overwriting adjacent stack memory and execution pointers", "Allocating too much memory on the heap", "Running out of CPU clock cycles during loops", "Sending oversized HTTP GET requests"], "answer": "Writing more data to a fixed memory buffer than it can hold, overwriting adjacent stack memory and execution pointers"},
        {"question": "What mechanism in PKI allows clients to verify if a TLS digital certificate has been revoked before expiration?", "options": ["OCSP (Online Certificate Status Protocol) or CRL (Certificate Revocation List)", "DNSSEC lookup", "BGP Route Inspection", "SSH Fingerprint check"], "answer": "OCSP (Online Certificate Status Protocol) or CRL (Certificate Revocation List)"},
        {"question": "In SIEM (Security Information and Event Management) platforms, what is Event Correlation?", "options": ["Analyzing and cross-referencing disparate log events across systems to detect multi-stage attack patterns", "Deleting duplicate log lines automatically", "Converting system logs into Excel charts", "Filtering out all INFO severity log messages"], "answer": "Analyzing and cross-referencing disparate log events across systems to detect multi-stage attack patterns"},
        {"question": "How does a Kerberos Ticket-Granting Ticket (TGT) operate in enterprise Active Directory networks?", "options": ["Provides single sign-on authentication by issuing encrypted tickets proving client identity to network services", "Stores domain passwords in browser cookies", "Encrypts internal hard drives with BitLocker", "Filters outgoing network traffic on port 80"], "answer": "Provides single sign-on authentication by issuing encrypted tickets proving client identity to network services"},
        {"question": "What attack technique corrupts local DNS cache records to redirect web users to spoofed malicious websites?", "options": ["DNS Cache Poisoning / Spoofing", "ARP Cache Poisoning", "BGP Hijacking", "Session Hijacking"], "answer": "DNS Cache Poisoning / Spoofing"},
        {"question": "What is the purpose of Address Space Layout Randomization (ASLR) in operating system security?", "options": ["Randomizes memory location addresses of process key data areas to impede buffer overflow exploitation", "Encrypts virtual machine disk files", "Randomizes user passwords on system boot", "Generates random IP addresses for network adapters"], "answer": "Randomizes memory location addresses of process key data areas to impede buffer overflow exploitation"},
        {"question": "How does Perfect Forward Secrecy (PFS) protect past encrypted TLS communication sessions?", "options": ["Generates unique ephemeral session keys per connection; compromise of server long-term private key cannot decrypt past recorded sessions", "Stores past session keys on read-only optical disks", "Encrypts network cables with hardware shielding", "Changes domain names every week"], "answer": "Generates unique ephemeral session keys per connection; compromise of server long-term private key cannot decrypt past recorded sessions"},
        {"question": "What is the difference between Red Team and Blue Team in cybersecurity exercises?", "options": ["Red Team acts as offensive attackers testing defenses; Blue Team acts as defensive security defenders protecting assets", "Red Team builds firewall software; Blue Team writes Python code", "Red Team manages databases; Blue Team manages network routers", "Red Team handles legal compliance; Blue Team handles public relations"], "answer": "Red Team acts as offensive attackers testing defenses; Blue Team acts as defensive security defenders protecting assets"},
        {"question": "What framework categorized by MITRE maps out adversary tactics, techniques, and procedures (TTPs)?", "options": ["MITRE ATT&CK Framework", "NIST SP 800-53", "ISO/IEC 27001", "CIS Critical Controls"], "answer": "MITRE ATT&CK Framework"}
    ]
}

CLOUD_QUIZZES = {
    "easy": [
        {"question": "What are the three main service models of cloud computing defined by NIST?", "options": ["IaaS, PaaS, SaaS", "AWS, Azure, GCP", "Public, Private, Hybrid", "Compute, Storage, Network"], "answer": "IaaS, PaaS, SaaS"},
        {"question": "What does IaaS stand for in cloud computing?", "options": ["Infrastructure as a Service", "Integration as a Service", "Information as a Service", "Intelligence as a Service"], "answer": "Infrastructure as a Service"},
        {"question": "Which cloud service model provides fully hosted end-user applications managed entirely by the vendor (e.g., Google Workspace, Office 365)?", "options": ["SaaS (Software as a Service)", "PaaS (Platform as a Service)", "IaaS (Infrastructure as a Service)", "FaaS (Function as a Service)"], "answer": "SaaS (Software as a Service)"},
        {"question": "What type of cloud deployment combines public cloud resources with on-premises private infrastructure?", "options": ["Hybrid Cloud", "Public Cloud", "Community Cloud", "Air-Gapped Cloud"], "answer": "Hybrid Cloud"},
        {"question": "Which AWS cloud storage service provides highly durable scalable Object Storage?", "options": ["Amazon S3 (Simple Storage Service)", "Amazon EBS", "Amazon EFS", "Amazon EC2"], "answer": "Amazon S3 (Simple Storage Service)"},
        {"question": "What is an Virtual Private Cloud (VPC)?", "options": ["An isolated virtual network dedicated to your cloud account within a public cloud provider", "A VPN software client installed on laptops", "A physical data center facility", "A private fiber optic cable"], "answer": "An isolated virtual network dedicated to your cloud account within a public cloud provider"},
        {"question": "What fundamental cloud property allows infrastructure capacity to scale up or down automatically based on demand?", "options": ["Elasticity", "Fixed Capacity", "Immutability", "Latency"], "answer": "Elasticity"},
        {"question": "What feature automatically adjusts the number of virtual compute instances running in response to server load?", "options": ["Auto-Scaling Group", "Static Load Balancer", "Manual Provisioning", "Cron Job"], "answer": "Auto-Scaling Group"},
        {"question": "What cloud paradigm executes code in response to events without requiring developers to manage virtual servers?", "options": ["Serverless Computing (FaaS)", "Bare-Metal Hosting", "Virtual Machine Cluster", "Monolithic Hosting"], "answer": "Serverless Computing (FaaS)"},
        {"question": "Which cloud platform is owned and operated by Microsoft?", "options": ["Microsoft Azure", "Amazon Web Services", "Google Cloud Platform", "IBM Cloud"], "answer": "Microsoft Azure"}
    ],
    "medium": [
        {"question": "Under the Cloud Shared Responsibility Model, what is the cloud customer typically responsible for?", "options": ["Customer data security, user IAM permissions, OS patches (IaaS), and application code", "Physical security of server data center buildings", "Hypervisor virtualization software updates", "Replacement of broken physical hard drives"], "answer": "Customer data security, user IAM permissions, OS patches (IaaS), and application code"},
        {"question": "In Infrastructure as Code (IaC), what is the primary benefit of tools like Terraform?", "options": ["Allows infrastructure to be defined, version-controlled, and provisioned using declarative configuration files", "Renders web pages faster in user browsers", "Automatically writes application business logic", "Eliminates network bandwidth charges"], "answer": "Allows infrastructure to be defined, version-controlled, and provisioned using declarative configuration files"},
        {"question": "What component distributes incoming web application traffic across multiple target virtual machines to ensure high availability?", "options": ["Load Balancer (e.g., ALB / ELB)", "DNS Resolver", "Internet Gateway", "NAT Gateway"], "answer": "Load Balancer (e.g., ALB / ELB)"},
        {"question": "What is the difference between Object Storage (e.g., S3) and Block Storage (e.g., EBS)?", "options": ["Object Storage treats data as discrete units with metadata accessed via API; Block Storage acts as raw unformatted disk volumes attached to compute", "Block Storage is accessible from anywhere over public internet without keys", "Object Storage is strictly for database log files", "There is no performance difference"], "answer": "Object Storage treats data as discrete units with metadata accessed via API; Block Storage acts as raw unformatted disk volumes attached to compute"},
        {"question": "In cloud IAM, what is the difference between a Role and a User?", "options": ["A User represents a person or application with permanent credentials; a Role is assumed temporarily by identities needing specific permissions", "Roles cannot have policies attached", "Users can only be created by root AWS accounts", "Roles are stored on local hard drives"], "answer": "A User represents a person or application with permanent credentials; a Role is assumed temporarily by identities needing specific permissions"},
        {"question": "What does a Content Delivery Network (CDN, e.g., Cloudflare, CloudFront) do?", "options": ["Caches static website assets at edge locations worldwide to reduce latency for end users", "Runs database queries in parallel", "Compiles C code on cloud servers", "Generates SSL certificates automatically"], "answer": "Caches static website assets at edge locations worldwide to reduce latency for end users"},
        {"question": "What cloud service allows private subnets without public IPs to access the internet for outbound updates?", "options": ["NAT Gateway", "Internet Gateway", "VPC Peering", "Route Table"], "answer": "NAT Gateway"},
        {"question": "What is the purpose of AWS KMS (Key Management Service)?", "options": ["To create, manage, and control cryptographic keys used to encrypt data across cloud services", "To manage domain name DNS records", "To monitor server CPU usage percentage", "To store user credit card numbers"], "answer": "To create, manage, and control cryptographic keys used to encrypt data across cloud services"},
        {"question": "What metric defines the maximum acceptable data loss measured in time following a cloud service outage?", "options": ["Recovery Point Objective (RPO)", "Recovery Time Objective (RTO)", "Mean Time Between Failures (MTBF)", "Service Level Agreement (SLA)"], "answer": "Recovery Point Objective (RPO)"},
        {"question": "What metric defines the maximum acceptable downtime duration allowed to restore business operations after an outage?", "options": ["Recovery Time Objective (RTO)", "Recovery Point Objective (RPO)", "Service Level Indicator (SLI)", "Mean Time to Repair (MTTR)"], "answer": "Recovery Time Objective (RTO)"}
    ],
    "hard": [
        {"question": "How does Terraform manage and track existing cloud infrastructure state?", "options": ["Via a state file (terraform.tfstate) that maps real-world cloud resources to configuration declarations", "By querying browser cookies", "By scanning git commit logs on every run", "By storing plain text passwords in cloud memory"], "answer": "Via a state file (terraform.tfstate) that maps real-world cloud resources to configuration declarations"},
        {"question": "What mechanism prevents concurrent Terraform runs from corrupting the remote state file?", "options": ["State Locking (e.g., using AWS DynamoDB table or S3 native locking)", "Deleting the state file after every apply", "Disabling multi-threading in Terraform CLI", "Encrypting the git repository"], "answer": "State Locking (e.g., using AWS DynamoDB table or S3 native locking)"},
        {"question": "How does Envelope Encryption work in cloud security (e.g., KMS)?", "options": ["Plaintext data is encrypted with a Data Key (DEK); the Data Key itself is encrypted with a Master Key (KMS KEK)", "Data is encrypted twice with the user's password", "Keys are sent over unencrypted HTTP GET parameters", "Encryption occurs only on physical hardware tape drives"], "answer": "Plaintext data is encrypted with a Data Key (DEK); the Data Key itself is encrypted with a Master Key (KMS KEK)"},
        {"question": "What is the difference between VPC Peering and AWS Transit Gateway for multi-VPC networking?", "options": ["VPC Peering establishes point-to-point non-transitive connections; Transit Gateway acts as a central hub for transitive routing", "VPC Peering works across different cloud providers; Transit Gateway does not", "Transit Gateway requires physical cable installation", "VPC Peering cannot cross AWS regions"], "answer": "VPC Peering establishes point-to-point non-transitive connections; Transit Gateway acts as a central hub for transitive routing"},
        {"question": "What is Chaos Engineering in cloud resilience testing (pioneered by Netflix Chaos Monkey)?", "options": ["Intentionally introducing infrastructure failures into production to test system self-healing resilience", "Writing random unformatted code during sprints", "Deleting database backups to save money", "Disabling firewalls during load tests"], "answer": "Intentionally introducing infrastructure failures into production to test system self-healing resilience"},
        {"question": "How does an Active-Active Multi-Region Cloud Architecture achieve high availability?", "options": ["Traffic is routed across fully operational infrastructure stacks running concurrently in multiple geographic regions", "One region is kept powered off until disaster strikes", "All user requests are processed by single master database", "Data is synced once per year over FTP"], "answer": "Traffic is routed across fully operational infrastructure stacks running concurrently in multiple geographic regions"},
        {"question": "What issue occurs if a Lambda function suffers from a 'Cold Start'?", "options": ["Latency delay occurring when a new container environment must be initialized before processing a request", "The server freezing due to low data center temperatures", "The Lambda execution failing due to syntax errors", "The function executing twice simultaneously"], "answer": "Latency delay occurring when a new container environment must be initialized before processing a request"},
        {"question": "What design pattern prevents a failing downstream service from repeatedly crashing an entire cloud microservice pipeline?", "options": ["Circuit Breaker Pattern", "Bulkhead Pattern", "Saga Pattern", "Strangler Fig Pattern"], "answer": "Circuit Breaker Pattern"},
        {"question": "In cloud cost optimization, what is the trade-off of AWS Reserved Instances or Savings Plans over On-Demand?", "options": ["Commitment to specific usage terms (1 or 3 years) yields steep discounts in exchange for reduced flexibility", "Reserved Instances can be canceled at any hour with zero fee", "On-Demand instances run faster than Reserved Instances", "Savings Plans apply only to storage, not compute"], "answer": "Commitment to specific usage terms (1 or 3 years) yields steep discounts in exchange for reduced flexibility"},
        {"question": "What is the role of an Egress-Only Internet Gateway in cloud IPv6 networking?", "options": ["Allows outbound IPv6 traffic from VPC instances to the internet while preventing inbound connections from internet", "Blocks all outgoing HTTPS requests", "Translates IPv6 addresses to IPv4 addresses", "Encrypts VPC peering connections"], "answer": "Allows outbound IPv6 traffic from VPC instances to the internet while preventing inbound connections from internet"}
    ]
}

DEVOPS_QUIZZES = {
    "easy": [
        {"question": "What is the primary objective of DevOps methodology?", "options": ["To shorten the software development lifecycle while delivering continuous high-quality features and stability", "To replace software developers with automated robots", "To eliminate the need for software testing", "To enforce strict manual release approval phases"], "answer": "To shorten the software development lifecycle while delivering continuous high-quality features and stability"},
        {"question": "What command line tool is the industry standard for distributed version control?", "options": ["Git", "SVN", "Mercurial", "CVS"], "answer": "Git"},
        {"question": "What is a Docker Container?", "options": ["A lightweight, standalone, executable package that includes code, runtime, libraries, and settings", "A physical shipping container used for hardware transport", "A virtual machine running a full guest OS kernel", "A cloud data center rack"], "answer": "A lightweight, standalone, executable package that includes code, runtime, libraries, and settings"},
        {"question": "What does CI/CD stand for in modern DevOps pipelines?", "options": ["Continuous Integration / Continuous Deployment (or Delivery)", "Centralized Inspection / Code Distribution", "Computer Infrastructure / Data Center", "Continuous Installation / Custom Design"], "answer": "Continuous Integration / Continuous Deployment (or Delivery)"},
        {"question": "Which popular open-source automation server uses Jenkinsfiles to define build pipelines?", "options": ["Jenkins", "Docker", "Kubernetes", "GitLab"], "answer": "Jenkins"},
        {"question": "What file in a Git repository specifies intentional untracked files to ignore?", "options": [".gitignore", "Dockerfile", "README.md", "package.json"], "answer": ".gitignore"},
        {"question": "What command creates a new git branch and switches to it immediately?", "options": ["git checkout -b <branch_name>", "git branch create", "git switch new", "git commit -b"], "answer": "git checkout -b <branch_name>"},
        {"question": "What Docker instruction sets the base parent image in a Dockerfile?", "options": ["FROM", "RUN", "CMD", "EXPOSE"], "answer": "FROM"},
        {"question": "What is Kubernetes (K8s)?", "options": ["An open-source container orchestration system for automating application deployment, scaling, and management", "A programming language developed by Google", "A database engine for JSON files", "A web browser testing framework"], "answer": "An open-source container orchestration system for automating application deployment, scaling, and management"},
        {"question": "What Git command uploads local repository commits to a remote server like GitHub?", "options": ["git push", "git pull", "git fetch", "git commit"], "answer": "git push"}
    ],
    "medium": [
        {"question": "What is the difference between RUN and CMD instructions in a Dockerfile?", "options": ["RUN executes commands during image build time; CMD specifies default commands when the container starts", "CMD builds the container; RUN exports it to tar", "RUN runs only in background; CMD runs in foreground", "There is no difference in Docker"], "answer": "RUN executes commands during image build time; CMD specifies default commands when the container starts"},
        {"question": "What smallest deployable compute unit in Kubernetes contains one or more tightly coupled containers?", "options": ["Pod", "Node", "Cluster", "Deployment"], "answer": "Pod"},
        {"question": "How do Docker Volumes differ from bind mounts for data persistence?", "options": ["Volumes are stored in a part of the host filesystem managed entirely by Docker, isolated from host OS structure", "Bind mounts are stored on remote cloud servers only", "Volumes are deleted automatically when containers stop", "Bind mounts require root access to create"], "answer": "Volumes are stored in a part of the host filesystem managed entirely by Docker, isolated from host OS structure"},
        {"question": "What Kubernetes Service type exposes a workload externally on a static port of each Cluster Node?", "options": ["NodePort", "ClusterIP", "LoadBalancer", "ExternalName"], "answer": "NodePort"},
        {"question": "Where should GitHub Actions workflow YAML files be stored in a repository?", "options": [".github/workflows/", ".git/actions/", "src/workflows/", "config/github/"], "answer": ".github/workflows/"},
        {"question": "What is Infrastructure as Code (IaC) tool Ansible primarily known for?", "options": ["Agentless configuration management and automation via SSH using YAML playbooks", "Compiling Java applications into native binaries", "Running browser end-to-end tests", "Managing cloud billing reports"], "answer": "Agentless configuration management and automation via SSH using YAML playbooks"},
        {"question": "In Kubernetes, what is the role of an Ingress Controller?", "options": ["Manages external HTTP/HTTPS routing rules into services within the cluster", "Performs automatic node disk cleanup", "Allocates IP addresses to physical hardware", "Compiles Docker images inside pods"], "answer": "Manages external HTTP/HTTPS routing rules into services within the cluster"},
        {"question": "What open-source monitoring tool collects metric time-series data using a pull model via HTTP endpoints?", "options": ["Prometheus", "Logstash", "Grafana", "Kibana"], "answer": "Prometheus"},
        {"question": "What tool visualizes Prometheus metrics time-series data using customizable interactive dashboards?", "options": ["Grafana", "Jenkins", "Helm", "ArgoCD"], "answer": "Grafana"},
        {"question": "What does GitOps paradigm use as the single source of truth for declarative infrastructure and application state?", "options": ["A Git repository", "A SQL database", "A Redis cache", "An Excel spreadsheet"], "answer": "A Git repository"}
    ],
    "hard": [
        {"question": "How does a Kubernetes RollingUpdate Deployment strategy update pods without application downtime?", "options": ["Gradually replaces old pods with new version pods one-by-one, maintaining capacity during rollout", "Deletes all old pods immediately, causing 5-minute downtime", "Duplicates the entire cluster infrastructure", "Updates pod source code in-place inside running containers"], "answer": "Gradually replaces old pods with new version pods one-by-one, maintaining capacity during rollout"},
        {"question": "What is the difference between Blue-Green Deployment and Canary Deployment strategies?", "options": ["Blue-Green switches 100% traffic between two identical environments; Canary routes a small percentage of user traffic to the new version first", "Canary requires manual physical server swaps", "Blue-Green deployment works only with mobile apps", "Canary deployment deletes all database records"], "answer": "Blue-Green switches 100% traffic between two identical environments; Canary routes a small percentage of user traffic to the new version first"},
        {"question": "In Site Reliability Engineering (SRE), how is Error Budget calculated?", "options": ["100% minus the Service Level Objective (SLO) percentage (e.g., 99.9% SLO yields 0.1% Error Budget)", "Total dev salary divided by downtime hours", "Number of failed git commits per week", "Total server RAM size minus usage"], "answer": "100% minus the Service Level Objective (SLO) percentage (e.g., 99.9% SLO yields 0.1% Error Budget)"},
        {"question": "What package manager for Kubernetes uses Charts to define, install, and upgrade complex cluster applications?", "options": ["Helm", "Kustomize", "Pip", "Chocolatey"], "answer": "Helm"},
        {"question": "In Docker Multi-stage builds, how do developer optimization goals get achieved?", "options": ["By copying build artifacts from intermediate build stages into a minimal final production runtime image", "By combining 5 OS kernels into one container", "By compressing files into zip archives", "By building images on external cloud GPUs"], "answer": "By copying build artifacts from intermediate build stages into a minimal final production runtime image"},
        {"question": "What Kubernetes component runs on every worker node, watching for assigned PodSpecs and running containers?", "options": ["kubelet", "kube-apiserver", "kube-scheduler", "etcd"], "answer": "kubelet"},
        {"question": "What consistent distributed key-value store stores the complete cluster state configuration in Kubernetes?", "options": ["etcd", "Redis", "MongoDB", "Cassandra"], "answer": "etcd"},
        {"question": "In Continuous Delivery, what Git branching model uses short-lived feature branches merged frequently into main?", "options": ["Trunk-Based Development", "GitFlow", "Release Branching", "Forking Workflow"], "answer": "Trunk-Based Development"},
        {"question": "What Git command rewrites commit history by moving local commits onto a new base parent commit?", "options": ["git rebase", "git merge", "git reset", "git revert"], "answer": "git rebase"},
        {"question": "In Prometheus monitoring architecture, what utility pushes short-lived batch job metrics to Prometheus?", "options": ["Pushgateway", "Alertmanager", "Node Exporter", "Blackbox Exporter"], "answer": "Pushgateway"}
    ]
}

UIUX_QUIZZES = {
    "easy": [
        {"question": "What is the core distinction between UI (User Interface) and UX (User Experience)?", "options": ["UI focuses on visual elements and layout; UX focuses on overall user journey, usability, and satisfaction", "UI is for mobile phones; UX is for desktop computers", "UI requires writing Python code; UX requires SQL", "UI and UX are exact identical terms with no difference"], "answer": "UI focuses on visual elements and layout; UX focuses on overall user journey, usability, and satisfaction"},
        {"question": "Which design software is widely considered the industry standard for collaborative vector interface design?", "options": ["Figma", "Photoshop", "MS Paint", "Blender"], "answer": "Figma"},
        {"question": "What is a Wireframe in UI/UX design?", "options": ["A low-fidelity structural blueprint representing page layout and content structure without final styling", "A high-resolution marketing poster", "The backend database schema diagram", "A working front-end JavaScript file"], "answer": "A low-fidelity structural blueprint representing page layout and content structure without final styling"},
        {"question": "What is a User Persona?", "options": ["A semi-fictional representation of an ideal user based on research and demographic data", "A real user's social media profile", "The lead designer's personal avatar", "An automated chatbot character"], "answer": "A semi-fictional representation of an ideal user based on research and demographic data"},
        {"question": "In visual design, what does White Space (Negative Space) refer to?", "options": ["Unmarked empty area around and between UI layout elements", "Background areas painted strictly with #FFFFFF white hex color", "Empty browser windows", "Deleted layers in Figma"], "answer": "Unmarked empty area around and between UI layout elements"},
        {"question": "What term describes a clickable, interactive representation of a design used for usability testing?", "options": ["Prototype", "Moodboard", "Site Map", "Blueprint"], "answer": "Prototype"},
        {"question": "Which primary colors make up the additive RGB color model used by digital displays?", "options": ["Red, Green, Blue", "Red, Yellow, Blue", "Cyan, Magenta, Yellow", "Black, White, Gray"], "answer": "Red, Green, Blue"},
        {"question": "What concept ensures UI elements respond visually to user actions (e.g., hover states, button click feedback)?", "options": ["Visual Feedback / Micro-interactions", "Backend Validation", "Database Triggers", "Static Styling"], "answer": "Visual Feedback / Micro-interactions"},
        {"question": "Which design principle arranges visual elements to guide the viewer's eye in order of importance?", "options": ["Visual Hierarchy", "Symmetry", "Randomization", "Skewing"], "answer": "Visual Hierarchy"},
        {"question": "What standard guidelines ensure web content is accessible to people with disabilities?", "options": ["WCAG (Web Content Accessibility Guidelines)", "ISO 9001", "IEEE 802.11", "RFC 2616"], "answer": "WCAG (Web Content Accessibility Guidelines)"}
    ],
    "medium": [
        {"question": "What is Nielsen's Usability Heuristic regarding 'Visibility of System Status'?", "options": ["The design should always keep users informed about what is happening through appropriate feedback within reasonable time", "All system source code must be published open source", "The UI must display server CPU temperature", "Users must see the full database schema"], "answer": "The design should always keep users informed about what is happening through appropriate feedback within reasonable time"},
        {"question": "What UX research method involves users organizing content topics into groups to inform Information Architecture?", "options": ["Card Sorting", "Tree Testing", "A/B Testing", "Eye Tracking"], "answer": "Card Sorting"},
        {"question": "What is Fitts's Law in UI interaction design?", "options": ["The time required to rapidly move to a target area is a function of the ratio between distance to target and target width", "Users spend most of their time on other websites", "Decision time increases logarithmically with the number of choices", "Designs must use no more than 3 colors"], "answer": "The time required to rapidly move to a target area is a function of the ratio between distance to target and target width"},
        {"question": "What contrast ratio is required by WCAG 2.1 AA guidelines for normal body text against background?", "options": ["At least 4.5:1", "At least 2.0:1", "At least 10.0:1", "Exactly 1.0:1"], "answer": "At least 4.5:1"},
        {"question": "In Design Systems, what are Design Tokens?", "options": ["Agreed key-value pairs (colors, typography, spacing values) stored as platform-agnostic variables", "Cryptocurrency tokens awarded to designers", "Security passwords for Figma files", "Badges earned in design quizzes"], "answer": "Agreed key-value pairs (colors, typography, spacing values) stored as platform-agnostic variables"},
        {"question": "What UX methodology maps out step-by-step actions and emotions a user experiences while completing a task?", "options": ["Customer Journey Mapping", "Card Sorting", "Heuristic Evaluation", "A/B Testing"], "answer": "Customer Journey Mapping"},
        {"question": "What is the 'Mobile-First' design strategy?", "options": ["Designing the mobile UI experience first, then progressively expanding features for larger desktop viewports", "Building apps exclusively for Android devices", "Disabling web applications on desktop computers", "Testing apps on mobile phones without internet"], "answer": "Designing the mobile UI experience first, then progressively expanding features for larger desktop viewports"},
        {"question": "In web accessibility, what attribute provides text descriptions for screen readers on non-decorative images?", "options": ["alt attribute (alt text)", "title attribute", "src attribute", "href attribute"], "answer": "alt attribute (alt text)"},
        {"question": "What visual design principle uses proximity to group related interface items together?", "options": ["Law of Proximity (Gestalt Principles)", "Law of Similarity", "Law of Closure", "Law of Continuity"], "answer": "Law of Proximity (Gestalt Principles)"},
        {"question": "What is an A/B Test in UX design optimization?", "options": ["Comparing two variants (A and B) live to determine which yields better conversion or user performance", "Testing UI in two different browsers", "Designing two pages in Adobe Illustrator", "Conducting interviews with two users"], "answer": "Comparing two variants (A and B) live to determine which yields better conversion or user performance"}
    ],
    "hard": [
        {"question": "What mathematical principle of Hick's Law governs UI menu design?", "options": ["The time it takes to make a decision increases logarithmically with the number and complexity of choices (T = b * log2(n + 1))", "Decision time doubles for every red button", "Users choose option A 90% of the time", "Interface complexity decreases as features grow"], "answer": "The time it takes to make a decision increases logarithmically with the number and complexity of choices (T = b * log2(n + 1))"},
        {"question": "In accessible UI development, how should aria-label or aria-labelledby be utilized?", "options": ["To provide accessible string names for interactive elements that lack visible text labels for assistive tech", "To change CSS background color on click", "To store tracking analytics IDs", "To disable keyboard tab navigation"], "answer": "To provide accessible string names for interactive elements that lack visible text labels for assistive tech"},
        {"question": "What Information Architecture framework organizes content according to Location, Alphabet, Time, Category, or Hierarchy?", "options": ["LATCH Method (Wurman's principles)", "CARD Framework", "GOMS Model", "SUS System"], "answer": "LATCH Method (Wurman's principles)"},
        {"question": "What standard standardized questionnaire yields a System Usability Scale (SUS) score ranging from 0 to 100?", "options": ["A 10-item Likert scale survey measuring subjective usability and learnability", "A 50-item technical quiz", "An automated browser speed test", "A 5-star app store review rating"], "answer": "A 10-item Likert scale survey measuring subjective usability and learnability"},
        {"question": "What is the difference between Skeuomorphic Design and Flat Design?", "options": ["Skeuomorphism mimics real-world textures and 3D shadows; Flat design uses minimalist 2D elements and solid colors", "Flat design requires 3D graphics cards; Skeuomorphism uses plain text", "Skeuomorphism is for mobile; Flat design is for TV", "There is no difference in interface styling"], "answer": "Skeuomorphism mimics real-world textures and 3D shadows; Flat design uses minimalist 2D elements and solid colors"},
        {"question": "What Gestalt law explains why humans perceive complete shapes even when parts of the line are missing?", "options": ["Law of Closure", "Law of Common Fate", "Law of Figure/Ground", "Law of Symmetry"], "answer": "Law of Closure"},
        {"question": "In usability testing, what is the difference between Formative and Summative Evaluation?", "options": ["Formative evaluation is done during design to guide iteration; Summative evaluation assesses finished products against benchmarks", "Formative is done with forms; Summative uses math", "Formative tests 1000 users; Summative tests 1 user", "Summative testing is conducted by developers exclusively"], "answer": "Formative evaluation is done during design to guide iteration; Summative evaluation assesses finished products against benchmarks"},
        {"question": "What design strategy prevents user input errors by restricting invalid actions beforehand (Poka-Yoke principle)?", "options": ["Defensive Design / Error Prevention", "Error Recovery Messages", "Form Validation On Submit", "User Apology Modals"], "answer": "Defensive Design / Error Prevention"},
        {"question": "How does Jakob's Law of User Experience influence platform UI design decisions?", "options": ["Users spend most time on other sites, preferring your site to work similarly to existing familiar conventions", "All web apps must look like Microsoft Word", "New designs must change standard icon meanings", "UI designers must invent original navigation patterns"], "answer": "Users spend most time on other sites, preferring your site to work similarly to existing familiar conventions"},
        {"question": "What design token category specifies elevation depth using CSS drop-shadow variables?", "options": ["Elevation / Shadow Tokens", "Color Tokens", "Spatial Tokens", "Motion Tokens"], "answer": "Elevation / Shadow Tokens"}
    ]
}

C_QUIZZES = {
    "easy": [
        {"question": "Who created the C programming language at Bell Labs in 1972?", "options": ["Dennis Ritchie", "Bjarne Stroustrup", "Ken Thompson", "Linus Torvalds"], "answer": "Dennis Ritchie"},
        {"question": "Which compiler tool is standard for compiling C source code files on Linux systems?", "options": ["gcc", "javac", "python", "node"], "answer": "gcc"},
        {"question": "What format specifier is used in printf() to print a signed integer in C?", "options": ["%d", "%f", "%s", "%c"], "answer": "%d"},
        {"question": "What operator in C is used to obtain the memory address of a variable?", "options": ["& (Address-of operator)", "* (Dereference operator)", "-> (Arrow operator)", ". (Dot operator)"], "answer": "& (Address-of operator)"},
        {"question": "What character marks the mandatory termination of statements in C?", "options": ["; (Semicolon)", ": (Colon)", ". (Period)", "} (Right brace)"], "answer": "; (Semicolon)"},
        {"question": "What header file must be included to use standard input/output functions like printf() and scanf()?", "options": ["<stdio.h>", "<stdlib.h>", "<string.h>", "<math.h>"], "answer": "<stdio.h>"},
        {"question": "What value is returned by main() to signal successful program execution to the operating system?", "options": ["0", "1", "-1", "NULL"], "answer": "0"},
        {"question": "Which data type keyword is used to store floating-point numbers in C?", "options": ["float", "int", "char", "void"], "answer": "float"},
        {"question": "What is a Pointer in C?", "options": ["A variable that stores the memory address of another variable", "A function that prints text to terminal", "A loop counter statement", "A file handling stream"], "answer": "A variable that stores the memory address of another variable"},
        {"question": "What character is automatically appended to terminate strings in C?", "options": ["'\\0' (Null terminator)", "'\\n' (Newline)", "'\\t' (Tab)", "' ' (Space)"], "answer": "'\\0' (Null terminator)"}
    ],
    "medium": [
        {"question": "What is the key difference between malloc() and calloc() in dynamic memory allocation?", "options": ["malloc() allocates uninitialized memory; calloc() allocates and initializes memory to zero", "calloc() is faster than malloc()", "malloc() works on stack; calloc() on heap", "calloc() frees memory automatically"], "answer": "malloc() allocates uninitialized memory; calloc() initializes memory to zero"},
        {"question": "What function in <stdlib.h> deallocates dynamically allocated memory block back to the heap?", "options": ["free()", "delete()", "clear()", "release()"], "answer": "free()"},
        {"question": "How does memory allocation differ between a struct and a union in C?", "options": ["struct members each have separate memory space; union members share the exact same memory space", "union members are private; struct members are public", "struct size is always 4 bytes; union is 100 bytes", "union cannot contain integer variables"], "answer": "struct members each have separate memory space; union members share the exact same memory space"},
        {"question": "What is a Dangling Pointer in C?", "options": ["A pointer pointing to a memory location that has been freed or deallocated", "A pointer initialized to NULL", "A pointer pointing to an active array", "A pointer used in global scope"], "answer": "A pointer pointing to a memory location that has been freed or deallocated"},
        {"question": "What operator returns the exact size in bytes of a data type or object in C?", "options": ["sizeof", "lengthof", "countof", "bytesize"], "answer": "sizeof"},
        {"question": "What happens if a program attempts to dereference a NULL pointer in C?", "options": ["A Segmentation Fault (SIGSEGV) runtime crash occurs", "The program returns 0 cleanly", "The pointer converts to 1 automatically", "The compiler fixes it"], "answer": "A Segmentation Fault (SIGSEGV) runtime crash occurs"},
        {"question": "In pointer arithmetic, if ptr points to an int array (4 bytes per int), what does ptr + 1 point to?", "options": ["The memory address 4 bytes ahead (the next integer element)", "The memory address 1 byte ahead", "The value 1", "The start of the array"], "answer": "The memory address 4 bytes ahead (the next integer element)"},
        {"question": "What preprocessor directive is used to define macro constants in C?", "options": ["#define", "#include", "#pragma", "#ifdef"], "answer": "#define"},
        {"question": "What is the function of the typedef keyword in C?", "options": ["Creates an alias/synonym for an existing data type", "Defines a new binary file format", "Allocates heap memory", "Converts floats to integers"], "answer": "Creates an alias/synonym for an existing data type"},
        {"question": "What function opens a file stream in C, returning a FILE pointer?", "options": ["fopen()", "open()", "file_open()", "fread()"], "answer": "fopen()"}
    ],
    "hard": [
        {"question": "What is a Memory Leak in C systems programming?", "options": ["Failing to free dynamically allocated heap memory after it is no longer needed, reducing available RAM over time", "Reading memory beyond array bounds", "Writing code without using variables", "Printing passwords to standard error"], "answer": "Failing to free dynamically allocated heap memory after it is no longer needed, reducing available RAM over time"},
        {"question": "What does the 'volatile' qualifier tell the C compiler about a variable?", "options": ["Prevents the compiler from optimizing out reads/writes, indicating the variable value can change unexpectedly outside code control", "Enforces read-only constant access", "Stores the variable in CPU register", "Encrypts the variable in RAM"], "answer": "Prevents the compiler from optimizing out reads/writes, indicating the variable value can change unexpectedly outside code control"},
        {"question": "What are the four discrete stages of the C compilation pipeline in order?", "options": ["Preprocessing -> Compilation -> Assembly -> Linking", "Compiling -> Building -> Executing -> Cleaning", "Parsing -> Translating -> Binding -> Running", "Linking -> Assembling -> Preprocessing -> Executing"], "answer": "Preprocessing -> Compilation -> Assembly -> Linking"},
        {"question": "What occurs during undefined behavior (UB) in C specification?", "options": ["The C standard places no requirements on execution; the program may crash, produce garbage, or work sporadically", "The compiler issues a mandatory red alert error", "The operating system catches it cleanly and resumes", "The variable defaults to zero"], "answer": "The C standard places no requirements on execution; the program may crash, produce garbage, or work sporadically"},
        {"question": "What POSIX library function creates a new execution thread in C?", "options": ["pthread_create()", "fork()", "thread_start()", "spawn_process()"], "answer": "pthread_create()"},
        {"question": "How does the system call fork() behave in Unix C programming?", "options": ["Duplicates the calling process, creating a child process with an exact copy of address space", "Forks the git code repository", "Allocates 1GB of memory", "Terminates current thread"], "answer": "Duplicates the calling process, creating a child process with an exact copy of address space"},
        {"question": "In C, what is the difference between pass-by-value and pass-by-reference (simulated via pointers)?", "options": ["Pass-by-value copies the argument value; pass-by-reference passes the memory address allowing function modification of caller state", "Pass-by-value is only for float data types", "Pass-by-reference is slower in C than in Python", "Pass-by-value allows direct modification of original variables"], "answer": "Pass-by-value copies the argument value; pass-by-reference passes the memory address allowing function modification of caller state"},
        {"question": "What bitwise operator performs an XOR (exclusive OR) operation between two integer operands in C?", "options": ["^", "&", "|", "~"], "answer": "^"},
        {"question": "What is the purpose of header guards (#ifndef HEADER_H / #define HEADER_H / #endif) in C header files?", "options": ["Prevents double inclusion of header file contents during compilation", "Enforces strict private class access", "Encrypts header files on disk", "Accelerates file I/O speed"], "answer": "Prevents double inclusion of header file contents during compilation"},
        {"question": "What C function reallocates previously allocated heap memory to a new size while preserving content?", "options": ["realloc()", "resize()", "calloc()", "remalloc()"], "answer": "realloc()"}
    ]
}

DATABASE_QUIZZES = {
    "easy": [
        {"question": "What does SQL stand for in database management?", "options": ["Structured Query Language", "Standard Query Logic", "Sequential Quantitative Language", "System Quick Lookup"], "answer": "Structured Query Language"},
        {"question": "What column or set of columns uniquely identifies every single row in a relational database table?", "options": ["Primary Key", "Foreign Key", "Index Key", "Candidate Key"], "answer": "Primary Key"},
        {"question": "Which SQL command is used to retrieve data from database tables?", "options": ["SELECT", "FETCH", "GET", "EXTRACT"], "answer": "SELECT"},
        {"question": "What column establishes a link between data in two tables by referencing the Primary Key of another table?", "options": ["Foreign Key", "Secondary Key", "Composite Key", "Super Key"], "answer": "Foreign Key"},
        {"question": "Which SQL clause is used to filter records based on specified conditions?", "options": ["WHERE", "HAVING", "GROUP BY", "ORDER BY"], "answer": "WHERE"},
        {"question": "Which SQL command adds new data rows into a table?", "options": ["INSERT INTO", "ADD ROW", "APPEND", "CREATE DATA"], "answer": "INSERT INTO"},
        {"question": "What category of databases stores data in document-based or key-value formats rather than tables?", "options": ["NoSQL (Non-Relational Databases)", "RDBMS", "Flat File Systems", "Spreadsheets"], "answer": "NoSQL (Non-Relational Databases)"},
        {"question": "Which SQL keyword sorts returned query result sets in ascending or descending order?", "options": ["ORDER BY", "GROUP BY", "SORT BY", "ALIGN BY"], "answer": "ORDER BY"},
        {"question": "What command removes a table structure and all its data permanently from a database?", "options": ["DROP TABLE", "DELETE TABLE", "REMOVE TABLE", "TRUNCATE SCHEMA"], "answer": "DROP TABLE"},
        {"question": "Which popular open-source relational database management system uses SQL?", "options": ["PostgreSQL / MySQL", "MongoDB", "Redis", "Neo4j"], "answer": "PostgreSQL / MySQL"}
    ],
    "medium": [
        {"question": "What is the difference between INNER JOIN and LEFT JOIN in SQL?", "options": ["INNER JOIN returns matching rows in both tables; LEFT JOIN returns all rows from left table plus matching rows from right", "LEFT JOIN excludes matching rows", "INNER JOIN works only on numbers", "There is no difference in result output"], "answer": "INNER JOIN returns matching rows in both tables; LEFT JOIN returns all rows from left table plus matching rows from right"},
        {"question": "What rule defines Third Normal Form (3NF) in database normalization?", "options": ["It is in 2NF and has no transitive functional dependencies (non-key attributes depend only on the primary key)", "It contains no duplicate table names", "All columns are stored as text", "It allows multi-valued attributes"], "answer": "It is in 2NF and has no transitive functional dependencies (non-key attributes depend only on the primary key)"},
        {"question": "In SQL, what is the difference between WHERE and HAVING clauses?", "options": ["WHERE filters rows before aggregation; HAVING filters aggregated groups created by GROUP BY", "HAVING is for primary keys only", "WHERE works only on text strings", "WHERE cannot be used with SELECT"], "answer": "WHERE filters rows before aggregation; HAVING filters aggregated groups created by GROUP BY"},
        {"question": "What does the ACID acronym stand for in transaction processing?", "options": ["Atomicity, Consistency, Isolation, Durability", "Authentication, Control, Integrity, Data", "Automated Creation, Insertion, Deletion", "Asynchronous Cache Invalidation Strategy"], "answer": "Atomicity, Consistency, Isolation, Durability"},
        {"question": "What database indexing structure speeds up data retrieval by maintaining a balanced search tree?", "options": ["B-Tree Index", "Hash Table only", "Linear Array", "Linked List"], "answer": "B-Tree Index"},
        {"question": "What SQL aggregate function counts the total number of rows matching a criteria?", "options": ["COUNT()", "SUM()", "TOTAL()", "NUM()"], "answer": "COUNT()"},
        {"question": "What is a Database View?", "options": ["A virtual table based on the result set of an underlying SQL query", "A screenshot of database administrative console", "A physical backup file on disk", "A user access role permission"], "answer": "A virtual table based on the result set of an underlying SQL query"},
        {"question": "Which SQL statement modifies existing record values in a table?", "options": ["UPDATE", "MODIFY", "CHANGE", "ALTER"], "answer": "UPDATE"},
        {"question": "What command permanently saves all transaction changes made during a session to the database?", "options": ["COMMIT", "SAVEPOINT", "ROLLBACK", "PERSIST"], "answer": "COMMIT"},
        {"question": "What command undoes uncommitted transaction changes made during a session?", "options": ["ROLLBACK", "COMMIT", "UNDO", "REVERT"], "answer": "ROLLBACK"}
    ],
    "hard": [
        {"question": "What are the four SQL Standard Transaction Isolation Levels in order of increasing isolation strength?", "options": ["Read Uncommitted, Read Committed, Repeatable Read, Serializable", "Low, Medium, High, Extreme", "Dirty, Non-Repeatable, Phantom, Strict", "Shared, Exclusive, Intent, Update"], "answer": "Read Uncommitted, Read Committed, Repeatable Read, Serializable"},
        {"question": "What concurrency anomaly is prevented by Repeatable Read isolation level?", "options": ["Non-Repeatable Read (reading different values for the same row in one transaction)", "Dirty Read", "Phantom Read", "Write Skew"], "answer": "Non-Repeatable Read (reading different values for the same row in one transaction)"},
        {"question": "How does Database Sharding scale high-traffic database infrastructure?", "options": ["Horizontally partitions rows of database tables across multiple independent database server nodes", "Runs SQL queries in parallel threads on single server", "Compresses database tables into zip archives", "Stores all data in RAM cache exclusively"], "answer": "Horizontally partitions rows of database tables across multiple independent database server nodes"},
        {"question": "What mechanism does Write-Ahead Logging (WAL) use to ensure Durability and Crash Recovery?", "options": ["Changes are recorded sequentially to a log file on non-volatile disk before being written to database pages", "Log files are deleted before commits", "Transactions are held in CPU cache until reboot", "Data is synced over FTP to secondary cloud"], "answer": "Changes are recorded sequentially to a log file on non-volatile disk before being written to database pages"},
        {"question": "In database query execution plans, what does a Full Table Scan indicate?", "options": ["The database engine must read every block of the table sequentially due to missing or unused indexes", "The query executed instantly using B-Tree index lookup", "The database table is corrupted", "The table contains zero rows"], "answer": "The database engine must read every block of the table sequentially due to missing or unused indexes"},
        {"question": "What issue is caused by a Deadlock in relational database locking?", "options": ["Two or more transactions are stuck in a circular wait condition where each holds a lock the other needs", "The database engine runs out of hard drive space", "The SQL query returns negative numbers", "The server loses power"], "answer": "Two or more transactions are stuck in a circular wait condition where each holds a lock the other needs"},
        {"question": "What high-performance in-memory key-value data store is widely used for database caching and session storage?", "options": ["Redis", "PostgreSQL", "SQLite", "MariaDB"], "answer": "Redis"},
        {"question": "What is Boyce-Codd Normal Form (BCNF)?", "options": ["A stricter version of 3NF where for every functional dependency X -> Y, X must be a super key", "A database without any foreign keys", "A NoSQL document schema standard", "A table with exactly 5 columns"], "answer": "A stricter version of 3NF where for every functional dependency X -> Y, X must be a super key"},
        {"question": "How does an In-Memory Database (e.g., Redis / Memcached) differ from disk-backed RDBMS?", "options": ["Primary data operations execute directly in RAM, offering sub-millisecond latency at the cost of volatile storage", "In-Memory databases cannot handle JSON data", "Disk-backed databases do not support SQL", "In-Memory databases require no power"], "answer": "Primary data operations execute directly in RAM, offering sub-millisecond latency at the cost of volatile storage"},
        {"question": "What does a Database Trigger do?", "options": ["Automatically executes a defined SQL procedural block when specific event actions (INSERT/UPDATE/DELETE) occur", "Triggers a full system reboot automatically", "Sends SMS messages to database admins", "Deletes orphan rows every midnight"], "answer": "Automatically executes a defined SQL procedural block when specific event actions (INSERT/UPDATE/DELETE) occur"}
    ]
}

SYSADMIN_QUIZZES = {
    "easy": [
        {"question": "What user account possesses supreme administrative system control privileges in Linux/Unix operating systems?", "options": ["root", "admin", "administrator", "superuser"], "answer": "root"},
        {"question": "What command allows authorized non-root users to execute individual commands with administrative root privileges?", "options": ["sudo", "su", "runas", "chmod"], "answer": "sudo"},
        {"question": "What command is used to change file and directory access permissions in Linux?", "options": ["chmod", "chown", "chgrp", "ls"], "answer": "chmod"},
        {"question": "What command lists directory contents in Linux terminal environments?", "options": ["ls", "dir", "cat", "pwd"], "answer": "ls"},
        {"question": "What system and service manager is the default init system in modern Linux distributions (e.g., Ubuntu, RHEL)?", "options": ["systemd", "sysvinit", "upstart", "initd"], "answer": "systemd"},
        {"question": "What command is used to manage and inspect systemd service statuses?", "options": ["systemctl", "service", "init", "daemonctl"], "answer": "systemctl"},
        {"question": "What Linux command displays real-time running system processes and CPU/RAM resource usage?", "options": ["top (or htop)", "ps", "df", "free"], "answer": "top (or htop)"},
        {"question": "What scheduled task daemon automatically executes commands at specified dates and time intervals in Linux?", "options": ["cron", "at", "systemd-timer", "sched"], "answer": "cron"},
        {"question": "What command prints the absolute current working directory path in Linux?", "options": ["pwd", "cd", "whereami", "path"], "answer": "pwd"},
        {"question": "What command changes the owner and group ownership of a file in Linux?", "options": ["chown", "chmod", "useradd", "chgrp"], "answer": "chown"}
    ],
    "medium": [
        {"question": "In numeric octal notation, what file permissions does 'chmod 755 file.txt' grant?", "options": ["Owner: Read/Write/Execute (7); Group & Others: Read/Execute (5)", "Owner: Read only; Others: Write only", "Full public permission to all users", "Owner & Group: Read/Write; Others: None"], "answer": "Owner: Read/Write/Execute (7); Group & Others: Read/Execute (5)"},
        {"question": "What is the function of Logical Volume Manager (LVM) in Linux disk management?", "options": ["Provides flexible storage management by creating virtual logical volumes across physical hard drives", "Compresses log files automatically", "Encrypts network traffic over SSH", "Formats hard drives into FAT32"], "answer": "Provides flexible storage management by creating virtual logical volumes across physical hard drives"},
        {"question": "What command line tool queries and views logs generated by the systemd journal service?", "options": ["journalctl", "dmesg", "syslog", "logcat"], "answer": "journalctl"},
        {"question": "In a 5-field Cron expression '* * * * *', what do the five position fields represent in order?", "options": ["Minute, Hour, Day of Month, Month, Day of Week", "Second, Minute, Hour, Day, Year", "Hour, Minute, Day, Month, Year", "Day of Week, Month, Day, Hour, Minute"], "answer": "Minute, Hour, Day of Month, Month, Day of Week"},
        {"question": "What command displays file system disk space usage in human-readable format?", "options": ["df -h", "du -sh", "ls -l", "free -m"], "answer": "df -h"},
        {"question": "What network utility replaces netstat for inspecting active sockets, ports, and network connections in modern Linux?", "options": ["ss", "ip", "ifconfig", "ping"], "answer": "ss"},
        {"question": "What file in /etc/ directory maps local IP addresses to hostnames before querying DNS servers?", "options": ["/etc/hosts", "/etc/resolv.conf", "/etc/nsswitch.conf", "/etc/sysconfig/network"], "answer": "/etc/hosts"},
        {"question": "What SSH configuration hardening practice prevents remote automated password brute-force attacks?", "options": ["Disabling PasswordAuthentication and enforcing SSH Key Pair Authentication", "Changing SSH port to 80", "Disabling root user login only", "Updating Linux kernel"], "answer": "Disabling PasswordAuthentication and enforcing SSH Key Pair Authentication"},
        {"question": "What command displays memory (RAM and swap) usage statistics in Linux?", "options": ["free -m", "meminfo", "ramstat", "vmstat"], "answer": "free -m"},
        {"question": "What signal does 'kill -9 <PID>' send to forcefully terminate a stubborn process immediately?", "options": ["SIGKILL", "SIGTERM", "SIGINT", "SIGHUP"], "answer": "SIGKILL"}
    ],
    "hard": [
        {"question": "What is the difference between SELinux Enforcing mode and Permissive mode?", "options": ["Enforcing blocks and logs security policy violations; Permissive logs violations without blocking actions", "Permissive mode turns off Linux kernel entirely", "Enforcing mode works only on Ubuntu; Permissive on Debian", "Permissive mode deletes log files"], "answer": "Enforcing blocks and logs security policy violations; Permissive logs violations without blocking actions"},
        {"question": "How does Rsync command perform efficient incremental file backups across servers?", "options": ["Transfers only the differences (delta) between source and destination files using a rolling checksum algorithm", "Copies the entire hard drive on every run", "Compresses files into zip archives without checksums", "Sends plain text FTP streams"], "answer": "Transfers only the differences (delta) between source and destination files using a rolling checksum algorithm"},
        {"question": "What configuration tool dynamically updates Linux kernel parameters at runtime without requiring a reboot?", "options": ["sysctl", "modprobe", "lsmod", "grub2-mkconfig"], "answer": "sysctl"},
        {"question": "In LVM architecture, what are the three abstraction layers in order from bottom physical hardware to top file system?", "options": ["Physical Volumes (PV) -> Volume Groups (VG) -> Logical Volumes (LV)", "Logical Volumes -> Physical Volumes -> Hard Disk", "Drive Partition -> File System -> Mount Point", "RAID 0 -> RAID 1 -> RAID 5"], "answer": "Physical Volumes (PV) -> Volume Groups (VG) -> Logical Volumes (LV)"},
        {"question": "What command line tool is used to monitor real-time disk I/O performance per storage device?", "options": ["iostat", "top", "netstat", "vmstat"], "answer": "iostat"},
        {"question": "What system file configures static file system mount points mounted automatically during system boot?", "options": ["/etc/fstab", "/etc/mtab", "/etc/exports", "/etc/filesystems"], "answer": "/etc/fstab"},
        {"question": "What security mechanism restricts process access to system resources by running processes inside isolated namespaces and cgroups?", "options": ["Containers (Linux Namespaces and Control Groups / cgroups)", "SELinux User Roles", "PAM Modules", "TCP Wrappers"], "answer": "Containers (Linux Namespaces and Control Groups / cgroups)"},
        {"question": "What command extracts detailed hardware information from system DMI / BIOS tables in Linux?", "options": ["dmidecode", "lshw", "lscpu", "lspci"], "answer": "dmidecode"},
        {"question": "What command changes user password expiration, aging, and account expiration policies in Linux?", "options": ["chage", "passwd", "usermod", "shadow"], "answer": "chage"},
        {"question": "What Linux kernel feature allows temporary memory space (Swap) to be used when physical RAM fills up?", "options": ["Virtual Memory Swapping (swappiness tuning)", "Page Table Lock", "RAM Cache Flushing", "Memory Compaction"], "answer": "Virtual Memory Swapping (swappiness tuning)"}
    ]
}


# ---------------------------------------------------------------------------
# Intelligent Fallback Synthesizer for Custom PDFs / Courses
# ---------------------------------------------------------------------------

def _extract_key_sentences(text):
    """Extract clear, factual sentences from raw content."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    cleaned = []
    for s in sentences:
        s = s.strip()
        if 40 <= len(s) <= 220 and not s.isupper() and not s.startswith("http"):
            cleaned.append(s)
    return cleaned


def _generate_dynamic_fallback(content, difficulty="medium", count=10):
    """
    Construct high-quality, readable conceptual questions from generic text.
    """
    sentences = _extract_key_sentences(content)
    if not sentences:
        return PYTHON_QUIZZES.get(difficulty, PYTHON_QUIZZES["medium"])

    questions = []
    random.shuffle(sentences)

    for i, s in enumerate(sentences):
        if len(questions) >= count:
            break

        words = re.findall(r'\b[A-Z][a-zA-Z0-9_-]{2,}\b', s)
        if not words:
            continue

        target_concept = words[0]
        question_text = f"According to the course content: \"{s}\" — Which term or concept is directly referenced?"
        
        options = [target_concept]
        other_words = set(re.findall(r'\b[A-Z][a-zA-Z0-9_-]{2,}\b', content)) - {target_concept}
        distractors = list(other_words)[:3]
        
        fallback_distractors = ["General Domain Principle", "Secondary Standard Specification", "Auxiliary Execution Pipeline"]
        while len(distractors) < 3:
            distractors.append(fallback_distractors[len(distractors)])

        options.extend(distractors)
        random.shuffle(options)

        questions.append({
            "question": question_text,
            "options": options,
            "answer": target_concept
        })

    while len(questions) < count:
        q_idx = len(questions) + 1
        questions.append({
            "question": f"Question {q_idx}: Which core methodology best aligns with the overall principles described in this module?",
            "options": [
                "Domain-Driven Implementation Strategy",
                "Random Unstructured Approach",
                "Deprecated Legacy Protocol",
                "Non-Standard Execution Model"
            ],
            "answer": "Domain-Driven Implementation Strategy"
        })

    return questions[:count]


# ---------------------------------------------------------------------------
# OpenAI Helper
# ---------------------------------------------------------------------------

def get_ai_response(prompt, json_mode=False):
    if not client:
        return None
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"} if json_mode else None
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"AI Error: {e}")
        return None


# ---------------------------------------------------------------------------
# Public Quiz Generation API
# ---------------------------------------------------------------------------

def generate_quiz(content, difficulty="medium"):
    """
    Generate 10 MCQs from the provided course content.
    First checks curated domain question banks, then OpenAI, then intelligent fallback.
    """
    difficulty = difficulty.lower()
    if difficulty not in ["easy", "medium", "hard"]:
        difficulty = "medium"

    content_lower = (content or "").lower()

    # 1. Match Curated Domain Banks
    if "python" in content_lower and ("guido" in content_lower or "zen of python" in content_lower or "pep 20" in content_lower or "cpython" in content_lower):
        print(f"[ai_utils] Using curated Python quiz bank ({difficulty})")
        return PYTHON_QUIZZES.get(difficulty, PYTHON_QUIZZES["medium"])

    if ("artificial intelligence" in content_lower or "machine learning" in content_lower or "deep learning" in content_lower or "dartmouth" in content_lower or "scikit-learn" in content_lower):
        print(f"[ai_utils] Using curated AI & ML quiz bank ({difficulty})")
        return AIML_QUIZZES.get(difficulty, AIML_QUIZZES["medium"])

    if "full stack" in content_lower or "react" in content_lower or "express.js" in content_lower or "client-server architecture" in content_lower:
        print(f"[ai_utils] Using curated Full Stack quiz bank ({difficulty})")
        return FULLSTACK_QUIZZES.get(difficulty, FULLSTACK_QUIZZES["medium"])

    if "java development" in content_lower or ("java" in content_lower and ("jvm" in content_lower or "spring boot" in content_lower or "bytecode" in content_lower)):
        print(f"[ai_utils] Using curated Java Dev quiz bank ({difficulty})")
        return JAVADEV_QUIZZES.get(difficulty, JAVADEV_QUIZZES["medium"])

    if "data science" in content_lower or "predictive analytics" in content_lower or ("pandas" in content_lower and "dataframe" in content_lower):
        print(f"[ai_utils] Using curated Data Science quiz bank ({difficulty})")
        return DATASCIENCE_QUIZZES.get(difficulty, DATASCIENCE_QUIZZES["medium"])

    if "blockchain" in content_lower or "ethereum" in content_lower or "smart contract" in content_lower or "solidity" in content_lower:
        print(f"[ai_utils] Using curated Blockchain quiz bank ({difficulty})")
        return BLOCKCHAIN_QUIZZES.get(difficulty, BLOCKCHAIN_QUIZZES["medium"])

    if "cybersecurity" in content_lower or "cia triad" in content_lower or "owasp" in content_lower or "firewall" in content_lower:
        print(f"[ai_utils] Using curated Cybersecurity quiz bank ({difficulty})")
        return CYBERSECURITY_QUIZZES.get(difficulty, CYBERSECURITY_QUIZZES["medium"])

    if "cloud computing" in content_lower or "infrastructure as code" in content_lower or "aws" in content_lower or "virtual private cloud" in content_lower:
        print(f"[ai_utils] Using curated Cloud quiz bank ({difficulty})")
        return CLOUD_QUIZZES.get(difficulty, CLOUD_QUIZZES["medium"])

    if "devops" in content_lower or "kubernetes" in content_lower or "docker" in content_lower or "ci/cd" in content_lower:
        print(f"[ai_utils] Using curated DevOps quiz bank ({difficulty})")
        return DEVOPS_QUIZZES.get(difficulty, DEVOPS_QUIZZES["medium"])

    if "ui/ux" in content_lower or "user experience" in content_lower or "nielsen" in content_lower or "wireframing" in content_lower:
        print(f"[ai_utils] Using curated UI/UX quiz bank ({difficulty})")
        return UIUX_QUIZZES.get(difficulty, UIUX_QUIZZES["medium"])

    if "c programming" in content_lower or "dennis ritchie" in content_lower or "malloc" in content_lower or "format specifier" in content_lower:
        print(f"[ai_utils] Using curated C quiz bank ({difficulty})")
        return C_QUIZZES.get(difficulty, C_QUIZZES["medium"])

    if "database management" in content_lower or "relational data" in content_lower or "acid properties" in content_lower or "b-tree indexing" in content_lower:
        print(f"[ai_utils] Using curated Database quiz bank ({difficulty})")
        return DATABASE_QUIZZES.get(difficulty, DATABASE_QUIZZES["medium"])

    if "system administration" in content_lower or "linux server" in content_lower or "systemd" in content_lower or "chmod" in content_lower:
        print(f"[ai_utils] Using curated System Administration quiz bank ({difficulty})")
        return SYSADMIN_QUIZZES.get(difficulty, SYSADMIN_QUIZZES["medium"])

    # 2. OpenAI path if available
    if client:
        difficulty_instructions = {
            "easy": "Focus on basic definitions, key terms, and foundational concepts explicitly stated in the text.",
            "medium": "Focus on understanding and application of concepts described in the text.",
            "hard": "Focus on deep analysis, advanced concepts, technical details, and inter-relating multiple ideas from the text.",
        }
        instruction = difficulty_instructions.get(difficulty, difficulty_instructions["medium"])
        prompt = (
            f"You are an expert educator. Generate exactly 10 multiple-choice questions (MCQs) "
            f"strictly based on the following course material. {instruction} "
            f"Each question must be directly answerable from the provided text only. "
            f"Return JSON with a single key 'questions', which is a list of objects, each with: "
            f"'question' (string), 'options' (list of exactly 4 strings), 'answer' (string — must exactly match one option).\n\n"
            f"COURSE MATERIAL:\n{content[:6000]}"
        )
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                qs = data.get('questions', [])
                if qs and len(qs) == 10:
                    return qs
            except Exception:
                pass

    # 3. Dynamic Fallback
    print(f"[ai_utils] Using dynamic conceptual question synthesizer ({difficulty})")
    return _generate_dynamic_fallback(content, difficulty, count=10)


def parse_resume(text):
    if not text:
        return [], "Unknown"
    
    if client:
        prompt = f"Extract skills (list) and domain from this resume: {text[:4000]}. Format as JSON with keys 'skills', 'domain'."
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                skills = data.get('skills', [])
                domain = data.get('domain', 'Unknown')
                if skills:
                    return skills, domain
            except Exception:
                pass

    # Content-based fallback
    text_lower = text.lower()
    skills = []
    domain = "Software Engineering"
    
    if any(w in text_lower for w in ["ui", "ux", "figma", "sketch", "design", "wireframe", "prototype"]):
        skills.extend(["UI/UX Design", "Figma", "User Research", "Wireframing"])
        domain = "UI/UX Design"
    if any(w in text_lower for w in ["python", "django", "flask", "fastapi"]):
        skills.extend(["Python", "Backend Development"])
        domain = "Backend Engineering" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["javascript", "react", "angular", "vue", "html", "css", "frontend"]):
        skills.extend(["JavaScript", "Frontend Web", "HTML/CSS"])
        domain = "Frontend Engineering" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["machine learning", "ai", "data science", "tensorflow", "pytorch"]):
        skills.extend(["Machine Learning", "Data Analysis"])
        domain = "Data Science & AI" if domain == "Software Engineering" else domain
    if any(w in text_lower for w in ["sql", "database", "analytics", "tableau", "power bi"]):
        skills.extend(["SQL", "Data Analytics"])
        domain = "Data Analytics" if domain == "Software Engineering" else domain
        
    if not skills:
        skills = ["Problem Solving", "Software Development", "Communication"]
        
    return list(set(skills)), domain


def suggest_jobs(skills):
    if client:
        prompt = (
            f"Suggest exactly 4 realistic job roles based on these skills: {skills}. "
            f"For each role provide a clear career progression path. "
            f"Return JSON with 'jobs' as a list of objects with keys 'role' and 'path'."
        )
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                jobs = data.get('jobs', [])
                if jobs:
                    return jobs
            except Exception:
                pass

    skills_str = " ".join(skills).lower() if isinstance(skills, list) else str(skills).lower()

    if any(w in skills_str for w in ["python", "django", "flask", "fastapi"]):
        return [
            {"role": "Python Developer", "path": "Junior Dev → Senior Dev → Tech Lead"},
            {"role": "Backend Engineer", "path": "Engineer → Senior → Principal Engineer"},
            {"role": "ML Engineer", "path": "Junior ML → ML Engineer → Staff ML Engineer"},
            {"role": "Data Engineer", "path": "Analyst → Data Engineer → Architect"},
        ]
    elif any(w in skills_str for w in ["ui", "ux", "design", "figma", "wireframing"]):
        return [
            {"role": "UI/UX Designer", "path": "Junior Designer → Senior Designer → Design Lead"},
            {"role": "Product Designer", "path": "Designer → Senior Product Designer → Head of Design"},
            {"role": "UX Researcher", "path": "Junior Researcher → Senior Researcher → UX Director"},
            {"role": "Frontend Developer", "path": "Junior Dev → Frontend Engineer → Tech Lead"},
        ]
    elif any(w in skills_str for w in ["machine learning", "ai", "tensorflow", "pytorch", "deep learning"]):
        return [
            {"role": "ML Engineer", "path": "Junior ML Engineer → ML Engineer → Principal"},
            {"role": "AI Research Scientist", "path": "Research Engineer → Scientist → Director of AI"},
            {"role": "Data Scientist", "path": "Analyst → Data Scientist → Lead Scientist"},
            {"role": "NLP Engineer", "path": "Engineer → Senior NLP → Head of NLP"},
        ]
    elif any(w in skills_str for w in ["react", "javascript", "typescript", "vue", "angular"]):
        return [
            {"role": "Frontend Engineer", "path": "Junior → Senior → Lead Frontend"},
            {"role": "Full Stack Developer", "path": "Junior Dev → Full Stack → CTO"},
            {"role": "UI/UX Engineer", "path": "Designer → Engineer → Design Systems Lead"},
            {"role": "React Native Developer", "path": "Mobile Dev → Senior → Tech Lead"},
        ]
    elif any(w in skills_str for w in ["java", "spring", "kotlin"]):
        return [
            {"role": "Java Developer", "path": "Junior → Senior → Architect"},
            {"role": "Backend Engineer", "path": "Engineer → Senior → Principal"},
            {"role": "Android Developer", "path": "Junior → Senior → Lead Mobile"},
            {"role": "DevOps Engineer", "path": "Engineer → Senior → Platform Lead"},
        ]
    elif any(w in skills_str for w in ["sql", "data", "analytics", "tableau", "power bi"]):
        return [
            {"role": "Data Analyst", "path": "Junior Analyst → Senior Analyst → Manager"},
            {"role": "Business Intelligence Engineer", "path": "BI Developer → Senior → Director"},
            {"role": "Data Scientist", "path": "Analyst → Scientist → Lead Scientist"},
            {"role": "Database Administrator", "path": "DBA → Senior DBA → Data Architect"},
        ]
    else:
        return [
            {"role": "Software Engineer", "path": "Junior → Mid-Level → Senior → Staff"},
            {"role": "Product Manager", "path": "APM → PM → Senior PM → Director"},
            {"role": "Full Stack Developer", "path": "Junior Dev → Senior Dev → CTO"},
            {"role": "DevOps Engineer", "path": "Junior → Senior → Platform Lead"},
        ]


def recommend_courses_ai(skills):
    if client:
        prompt = f"Recommend courses for skills: {skills}. Format as JSON with 'recommendations' list."
        res = get_ai_response(prompt, json_mode=True)
        if res:
            try:
                data = json.loads(res)
                return data.get('recommendations', [])
            except Exception:
                pass
                
    skills_str = " ".join(skills).lower() if isinstance(skills, list) else str(skills).lower()
    
    if any(w in skills_str for w in ["ui", "ux", "design", "figma"]):
        return ["UI/UX Design & User Experience", "Digital Design Principles", "Advanced CSS"]
    elif any(w in skills_str for w in ["python", "django", "flask", "backend"]):
        return ["Introduction to Python Programming", "Backend Engineering with Django", "API Design"]
    elif any(w in skills_str for w in ["javascript", "react", "html", "frontend", "web"]):
        return ["Full Stack Web Development", "React Mastery", "JavaScript Advanced"]
    elif any(w in skills_str for w in ["data", "sql", "analytics"]):
        return ["Data Science & Predictive Analytics", "Database Management Systems & SQL", "Data Analytics"]
    elif any(w in skills_str for w in ["ai", "machine learning", "ml", "tensorflow"]):
        return ["AI & Machine Learning Foundations", "Deep Learning", "Neural Networks"]
    
    return ["Introduction to Python Programming", "Full Stack Web Development", "Database Management Systems & SQL"]
