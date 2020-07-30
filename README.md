# GpxProcessor

This project contains a set of tools to parse GPX data, calculate statistics and render an HTML report.


### Environment Setup
```
# Clone repo
git clone https://github.com/ervbrian/GpxProcessor
cd GpxProcessor

# Setup virtual environment
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt

# Create data directories
mkdir images
mkdir data
```

## Execution
```
(GpxProcessor)$ python process.py -h
usage: process.py [-h] [-p PATH] [-r] [-c COMBINE [COMBINE ...]]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  list of files to process
  -r, --render_only     render html only
  -c COMBINE [COMBINE ...], --combine COMBINE [COMBINE ...]
                        list of input files to combine
```

### Populated:
```
(GpxProcessor)$ python process.py -p ./
Found 15 GPX files in path...
Processing 0 files after removing hikes already populated in HikeDB
Total hikes stored in HikeDB database: 15
Generated HTML page: html/index.html
```

### Unpopulated:
```
(GpxProcessor)$ python process.py -p ./
Found 15 GPX files in path...
Processing 15 files after removing hikes already populated in HikeDB
Processing 20170723_Lake_Valhalla_Janus_1.GPX...
Processing 20170820_Lake_Colchuck_to_TH.GPX...
Processing 20170701_Church_Mountain_RT.GPX...
Processing 20170728_Mt_Pilchuck.GPX...
Processing 20170624_Tuscohatchie_Kaleetan_RT.GPX...
Processing 20170823_Park_Butte_Lookout_to_TH.GPX...
Processing 20170625_Tuscohatchie_TalapusTH.GPX...
Processing 20170826_Pear_Lake_to_Stevens_Pass_TH.GPX...
Processing 20170729_Silver_Abiel_Tinkham.GPX...
Processing 20170617_Lake_Serene_Bridal_Veil_Falls.GPX...
Processing 20170825_Stevens_Pass_TH_to_Pear_Lake.GPX...
Processing 20170819_Lake_Colchuck_TH_to_Core_Enchantments.GPX...
Processing 20170722_Sauk_Mountain.GPX...
Processing 20170822_Park_Butte_Lookout.GPX...
Processing 20170821_TH_to_Park_Butte.GPX...
Total hikes stored in HikeDB database: 15
Generated HTML page: html/index.html
```

### HTML Render Only
The example below contains output from an HTML render only execution and assumes the HikeDB database already exists.
```
(GpxProcessor)$ python process.py --render_only
Generated HTML page: html/index.html
```

### Combine Multiple GPX Files
```
(GpxProcessor)$ python process.py -p data/ -c 20200619_Snow_Lake.GPX 20200619_Snow_Lake_Return.GPX
Found 27 GPX files in path...
Combining the following: ['20200619_Snow_Lake.GPX', '20200619_Snow_Lake_Return.GPX']
Removed 20200619_Snow_Lake.GPX from processing in favor of 20200619_Snow_Lake.GPX_combined.GPX
Removed 20200619_Snow_Lake_Return.GPX from processing in favor of 20200619_Snow_Lake.GPX_combined.GPX
Processing 26 files after removing hikes already populated in HikeDB
...
```

## Versioning

v0.1 - Initial Release

## Authors

**Brian Ervin** - *Initial work* - [ervbrian](https://github.com/ervbrian)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

