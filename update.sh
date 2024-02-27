rm /usr/bin/scanner_pi_usb
rm -r /usr/bin/scanner_pi
git clone https://github.com/AWT-Trent/scanner_pi.git
cp -r ./scanner_pi ../
cp ./scanner_pi/scanner_pi_usb /usr/bin/scanner_pi_usb
mv ./scanner_pi /usr/bin/scanner_pi
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
pip install -r ./requirements.txt
rm -r ./scanner_pi

