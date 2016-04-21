[![Build Status](https://travis-ci.org/acouch/csv-testing-tools.svg?branch=master)](https://travis-ci.org/acouch/csv-testing-tools)

# CSV Testing Examples 
CSV files are still a standard for sharing open data as they are easy read and parse and not part of a proprietary toolchain. It is common to extract data from less open formats like PDF and XLSX files into CSVs. When parsing large numbers of files into CSVs I have found myself wanting to test the outputs for obvious reasons. This repo collects two of those strategies. 

### Validation Tests

1. Tests to validate the CSV output using <a href="https://github.com/dhcole/csv-test">csv-test</a>. To test:
```bash
npm install
node_modules/csv-test/bin/csv-test tests/csv-test-config.yml '2014/*' tests/csv-test-validators.yml
```
### Sampling Tests

2. Tests to validate a sampling of results. These use behave and follow the format:
```yml
Examples: 20150929__wi__general_ward.csv
  | candidate                   | office   | ward                           | votes  | total |
  | Cindi Duchow                | Assembly | Village of Hartland Wards 1-13 | 117    | 140   |
  | Thomas D. Hibbard (Write-In)| ASSEMBLY | Village of Wales Wards 1-4     | 10     | 106   |
```

To run those tests ``cd tests; behave``  
