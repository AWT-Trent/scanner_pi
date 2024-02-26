rm /usr/bin/scanner_pi_usb
rm -r /usr/bin/scanner_pi/
git clone https://github.com/AWT-Trent/scanner_pi.git
cp -r ../scanner_pi /usr/bin/scanner_pi
cp ./scanner_pi_usb /usr/bin/scanner_pi_usb
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
rm -r ./scanner_pi
reboot