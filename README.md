# SquirrelUno

SquirrelUno is a fun and engaging project by Dominik Krenn that aims to implement a unique version of the classic Uno card game. This project not only provides an enjoyable coding experience but also demonstrates the use of Sphinx for comprehensive documentation, including modules and submodules. Whether you're a developer looking to contribute or a gamer interested in exploring the code behind Uno, SquirrelUno has something for you!

## Installation

### Local Installation

To install the package locally from the source code, follow these steps:

1. Clone the repository:

    ```bash
    git clone https://github.com/MarvGMBH/SquirrelUno.git
    cd SquirrelUno
    ```

2. Install the package in editable mode:

    ```bash
    pip install -e .
    ```

### GitHub Installation

To install the package directly from GitHub without cloning the repository, run:

```bash
pip install git+https://github.com/MarvGMBH/SquirrelUno.git

```markdown
## Usage

### Running the Project

After installing the package, you can run the main entry point. The command differs slightly between Linux and Windows due to how Python handles module names and entry points on different operating systems.

#### On Linux

You can run the project using either of the following commands:

```bash
squirreluno
```

or

```bash
python -m uno
```

#### On Windows

On Windows, due to certain constraints, you should use the following command:

```bash
python -m uno
```
(Note: The `squirreluno` command may not work on Windows due to differences in how Python handles entry points and module names across platforms.)

### What You'll See

When you run the project, you should see the following output:

```plaintext
Welcome to the SquirrelUno project!
```

## Contribution

Contributions are welcome! If you'd like to contribute to SquirrelUno, please fork the repository and create a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.
