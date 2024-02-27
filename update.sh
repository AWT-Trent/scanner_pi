rm /usr/bin/scanner_pi_usb
cp -r /usr/bin/scanner_pi/config.ini ./config.ini
git clone https://github.com/AWT-Trent/scanner_pi.git
cp -r ./scanner_pi ../
cp ./scanner_pi/scanner_pi_usb /usr/bin/scanner_pi_usb
cp -r ./scanner_pi /usr/bin/
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
pip install -r ./scanner_pi/requirements.txt
rm -r ./scanner_pi
