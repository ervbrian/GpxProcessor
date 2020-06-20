# GpxApp

This project contains a set of tools to parse GPX data, calculate statistics and render an HTML report.


## Execution
```
186590d2efe7:GpxApp ervbrian$ python3 process.py -h
usage: process.py [-h] [-p PATH] [-r]

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH  list of files to process
  -r, --render_only     render html only
```

### Populated:
```
186590d2efe7:GpxApp ervbrian$ python3 process.py -p ./
Found 15 GPX files in path...
Processing 0 files after removing hikes already populated in HikeDB
Total hikes stored in HikeDB database: 15
Generated HTML page: html/index.html
```

### Unpopulated:
```
186590d2efe7:GpxApp ervbrian$ python3 process.py -p ./
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
The example below contains output from an HTML render only execution:
```
186590d2efe7:GpxApp ervbrian$ python3 process.py --render_only
Generated HTML page: html/index.html
```

## Versioning

v0.1 - Initial Release

## Authors

* **Brian Ervin** - *Initial work* - [ervbrian](https://github.com/ervbrian)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

