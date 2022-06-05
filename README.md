# Save book summary from lit charts.

Just give this module the litcharts book link, and it will fetch summary from there. 
Saves it in <it>'book_file_name</it>.html'.

[Here](/The_White_Tiger_by_Aravind_Adiga.html) is the summary of book "The White Tiger" by Arvind Adiga from [this URL](https://www.litcharts.com/lit/the-white-tiger).
---

## Install

Clone this repository using

```sh
cd ~
git clone -b master --depth 1 https://github.com/HritwikSinghal/litcharts-summary
```

Enter the directory and install all the requirements using

```sh
cd litcharts-summary/
pip3 install -r requirements.txt
```

Run the app and paste the book link.

```sh
chmod +x main.py
./main.py
```

---

## License

[GPLv3](/LICENSE)
