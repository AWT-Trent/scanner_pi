rm /usr/bin/scanner_pi_usb
git clone https://github.com/AWT-Trent/scanner_pi.git
rm ./update.sh
chmod +x ./update.sh
cp ./scanner_pi/update.sh ./update.sh
cp ./scanner_pi_usb /usr/bin/scanner_pi_usb
mv -f ./scanner_pi /usr/bin/
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
pip install -r ./scanner_pi/requirements.txt
reboot () { echo 'Reboot? (y/n)' && read x && [[ "$x" == "y" ]] && /sbin/reboot; }