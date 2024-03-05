echo "removing old installation" | sudo tee -a /log.log
rm /usr/bin/scanner_pi_usb
rm -r /usr/bin/scanner_pi
echo "cloning new install" | sudo tee -a /log.log
git clone https://github.com/AWT-Trent/scanner_pi.git
#cp -r ./scanner_pi ../
cp ./scanner_pi/scanner_pi_usb /usr/bin/scanner_pi_usb
mv ./scanner_pi /usr/bin/scanner_pi
chmod +x /usr/bin/scanner_pi/scanner_pi_usb
echo "Install finished.....installing requirements" | sudo tee -a /log.log
pip install -r /usr/bin/scanner_pi/requirements.txt
echo "Finished upgrade....rebooting" | sudo tee -a /log.log
reboot

