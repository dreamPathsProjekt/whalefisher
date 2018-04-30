from setuptools import setup, find_packages

setup(
    name="whalefisher-data_provider",
    version="0.5",
    packages=find_packages(),


    install_requires=[
        "pyaml",
        "flask==1.0.1",
        "pyinstaller",
        "docker",
        "eventlet",
        "flask_socketio",
        "socketIO_client"
    ],

    # package_data={
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst'],
    #     # And include any *.msg files found in the 'hello' package, too:
    #     'hello': ['*.msg'],
    # },

    # metadata for upload to PyPI
    author="Ioannis Dritsas",
    author_email="dream.paths.projekt@gmail.com",
    description="A Logging Api for Docker Swarm",
    license="MIT",
    keywords="",
    # url="http://example.com/HelloWorld/",
)
