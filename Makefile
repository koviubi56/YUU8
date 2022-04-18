install:
	@echo "\n\nWARNING! THE OUTPUT OF THE COMMAND(S) MAY CONTAIN FAST FLASHING IMAGES! IT MAY CAUSE DISCOMFORT AND TRIGGER SEIZURES FOR PEOPLE WITH PHOTOSENSITIVE EPILEPSY!"
	python3 -m pip install -U pip setuptools wheel
	python3 -m pip install -vvvvvvvvvvvvvvvvvU -r requirements.txt -r f8pl.txt
