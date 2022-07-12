# Box.com PDF Downloader

This application can scrape and download protected docx, pdf files in box.com and save it as an editable PDF file.

### Installation

This app requires [Python 3](https://python.org/), [Google Chrome](https://chrome.google.com), and Selenium Chrome Web Driver to run.

Clone the repository and install the dependencies.

```cmd
> git clone https://github.com/aebibtech/box.com-downloader
> cd box.com-downloader
> call setup.cmd
> call BoxDL.cmd
```

### Initial Setup
Note: Chrome Selenium driver is installed by setup.cmd. If it does not install, you can download and install it from [here](http://chromedriver.chromium.org/downloads)

1. Run `BoxDL.cmd`
2. Enter a default path for box.com downloads.

### Example Usage

To Change your subfolder for downloads, use `sf` command:
`sf 'Test'`

To download a box document, use the `dl` command:
`dl https://app.box.com/s/hs5de51wub2htrcl0hxn1wir4zpmf3wj`


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
