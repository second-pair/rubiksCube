build:
	pyinstaller.exe --onefile --specpath build --distpath bin rubiksCube.py
	
clean:
	rm -rf bin build __pycache__

all:  clean build
