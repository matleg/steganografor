# steganografor2000

This repository is aimed as a demonstration of how to hide an image inside another using steganography.
We show the influence of significant bits by changing their number.

## Project setup

- Only one file : steganograformerge.py.

- No OOP.


## Prerequisites

```python
python3.8 -m pip install -r requirements.txt
```

## Use

```python
python steganograformerge.py
```

### Description

The aim is to hide this image of a written text   
![this text](/text_foobar.jpg)  
into this picture 
![this image](/Tower.jpg)


Increasing progressively the number of significant bits, we see the text
and the white background appearing more and more.

![GIF](/animation_1_to_8_sb.gif)


## Author

matleg

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

