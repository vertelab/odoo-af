all : module.tmp 
	@echo Complete

module.tmp: TestData_Config.xlsx
	@python read_file.py
	@touch module.tmp

clean:
	@rm -f *tmp
	@rm -f *csv
	@echo "Cleaned up"
