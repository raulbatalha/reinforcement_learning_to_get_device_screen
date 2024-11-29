from setuptools import setup, find_packages

setup(
    name="Reinforcement Learning to Get Device Screen!",
    version="1.0.0",
    author="Engº Raul Batalha",
    author_email="raulbatalh@gmail.com",
    description="This is a Python codebase that includes several classes and functions for a reinforcement learning agent that learns to navigate an environment. The agent learns to navigate from a starting position to a goal position in the grid by updating its Q-values based on the rewards obtained through interactions with the environment. Here's a breakdown of the main components and functionalities:",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/raulbatalha/reinforcement_learning_to_get_device_screen",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "matplotlib==3.4.3",
        "numpy==1.21.0",
        "Pillow==8.3.1",
        "requests==2.26.0",
        "adb==1.3.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    entry_points={
        "console_scripts": [
            "meu_comando=src.main:main",
        ]
    },
)
