# Box.com PDF Downloader

This application can scrape and download protected docx, pdf files in box.com and save it as an editable PDF file.

### Installation

This app requires [Python](https://python.org/) 3 to run.

Clone the repository and install the dependencies.

```cmd
> git clone https://github.com/aebibtech/box.com-downloader
> cd box.com-downloader
> call setup.cmd
> call BoxDL.cmd
```

### Initial Setup
Note: This requires chrome selenium driver in order to work, you can download and install it from [here](http://chromedriver.chromium.org/downloads)

1. Run `BoxDL.cmd`
2. Enter a default path for box.com downloads.

### Example Usage
```pwsh
> sf 'Test'
> dl https://app.box.com/s/hs5de51wub2htrcl0hxn1wir4zpmf3wj
```

### Development

Want to contribute? Great!
Make a change in your file and instantanously see your updates!

### Todos
 - Write MORE Tests
 - Checkout the source code to know more

### Did you find this useful?
[![ko-fi](https://www.ko-fi.com/img/donate_sm.png)](https://ko-fi.com/A362BEU)

License
----
GNU General Public License v3.0
