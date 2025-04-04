from setuptools import setup, find_packages

setup(
    name="zkom-mcp-server",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.103.1",
        "uvicorn==0.23.2",
        "requests==2.31.0",
        "pydantic==2.4.2",
        "python-dotenv==1.0.0",
        "httpx==0.25.0"
    ],
    entry_points={
        "console_scripts": [
            "zkom-mcp-server=app.main:run_server",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A Model Context Protocol server for cryptocurrency prices",
    keywords="mcp, cryptocurrency, prices, api",
    python_requires=">=3.8",
) 