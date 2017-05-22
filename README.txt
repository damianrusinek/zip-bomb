# ZipBomb

A zip bomb, also known as a zip of death or decompression bomb, is a malicious archive file designed to crash or render useless the program or system reading it.

This is a small script written in Python which generates such a zip bomb. It is based on [this repo](https://github.com/abdulfatir/ZipBomb) but it receives uncompressed size as input and provides two modes: nested and flat.

## Usage
```Usage: zip-bomb.py <mode> <size> <out_zip_file>

Creates ZIP bomb archive

<mode> - mode of compression
  nested - nested zip file (zip file of zip files of ...)
  flat   - flat file without nested zips
<size> - decompression size in MB
<out_zip_file> - path to destination file
```

## Sample Run - Flat mode 

`python zip-bomb.py flat 1024 out.zip`

### Output
```
Compressed File Size: 1020.36 KB
Size After Decompression: 1020 MB
Generation Time: 29.44s
```

## Sample Run - Nested mode 

`python zip-bomb.py nested 1024 out.zip`

### Output
```
Warning: Using nested mode. Actual size may differ from given.
Compressed File Size: 1.90 KB
Size After Decompression: 4590 MB
Generation Time: 5.82s
```


