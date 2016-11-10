all:
	@echo "iBrew setup (linux & mac)"
	@echo use \"make setup\" to fetch requirements
	@echo use \"make cleanlin\" to clean temp files
	@echo use \"make cleanmac\" to clean temp files
	@echo use \"make cleanwin\" to clean temp files
	@echo use \"make mac\" to make a mac release
	@echo use \"make readme\" to create a new README.md
	@echo use \"make bonjour\" to download bonjour
	@echo use \"make pyinstaller\" to download already patched osx pyinstaller

mac:	cleanlin buildmac cleanmac diskimage

readme:
	@python ibrew license > LICENSE
	@echo iBrew: Generating README.md
	@python ibrew usage > usage.tmp
	@python ibrew examples > examples.tmp
	@python ibrew commands > console.tmp
	@python ibrew notes > notes.tmp
	@python ibrew structure > protocol.tmp
	@cat distro/README.md_parts/README_part1.md usage.tmp distro/README.md_parts/README_part2.md console.tmp distro/README.md_parts/README_part3.md examples.tmp distro/README.md_parts/README_part4.md LICENSE > README.md

setup:
	@echo iBrew: Fetching python requirements
	@pip install -q -r requirements.txt

cleanlin:
	@echo iBrew: Cleaning up
	@rm -f *.pyc smarter/*.pyc
	@rm -f *.tmp
	@rm -f *.spec 
	@rm -rf build
	@rm -rf test

windows:
	@pip install win-inet-pton

bonjour:
	@curl https://storage.googleapis.com/google-code-archive-downloads/v2/code.google.com/pybonjour/pybonjour-1.1.1.zip > pybonjour-1.1.1.zip

pyinstaller:
	@git clone https://github.com/Tristan79/pyinstaller.git

cleanwin:
	@echo iBrew: Cleaning up [Windows]
	@del *.pyc 
	@del smarter\*.pyc
	@del *.tmp
	@del *.spec 

cleanmac:
	@echo iBrew: Cleaning up [MacOS]
	@rm -rf ~/Library/Application\ Support/iBrew/logs 
	@rm -f *.pyc smarter/*.pyc
	@rm -f *.tmp
	@rm -f *.spec 
	@rm -rf build
	@rm -rf dist/iBrew
	@rm -rf dist/iBrewConsole
	
buildmac:
	@echo iBrew: Building MacOS package
	@pip install -q -r distro/mac/requirements-mac.txt
	@rm -rf build     
	@echo Please install upx with: brew install upx
	@pyinstaller iBrewUI.py -s -w -n iBrew --noupx
	@pyinstaller ibrew -s -w -n iBrewConsole --noupx
	@cp -a resources dist/iBrew.app/Contents/MacOS
	@cp -a web dist/iBrew.app/Contents/MacOS
	@cp distro/mac/Info.plist dist/iBrew.app/Contents/
	@mv dist/iBrewConsole.app/Contents/MacOS/iBrewConsole dist/iBrew.app/Contents/MacOS
	@cp distro/mac/iBrew.icns dist/iBrew.app/Contents/Resources/icon-windowed.icns
	@rm -rf dist/iBrewConsole.app
	@mkdir -p test
	@mv dist/iBrew.app test
	@rm -rf dist

diskimage:
	#Set up disk image staging folder
	@rm -rf dmg/iBrew
	mkdir -p dmg/iBrew
	cp LICENSE dmg/iBrew
	ln -s /Applications dmg/iBrew/Applications
	cp -a test/iBrew.app dmg/iBrew
	cp distro/mac/iBrew.icns dmg/iBrew/.VolumeIcon.icns
	SetFile -c icnC dmg/iBrew/.VolumeIcon.icns
	
	##generate raw disk image
	rm -f iBrew.dmg
	hdiutil create -srcfolder dmg/iBrew -volname iBrew-0.4.4 -format UDRW -ov raw-iBrew.dmg	

	#remove working files and folders
	rm -rf dmg/iBrew
	
	# we now have a raw DMG file.
	
	# remount it so we can set the volume icon properly
	mkdir -p dmg/iBrew
	hdiutil attach raw-iBrew.dmg -mountpoint dmg/iBrew
	SetFile -a C dmg/iBrew
	
	hdiutil detach dmg/iBrew
	rm -rf dmg
	
	# convert the raw image
	rm -f iBrew.dmg
	hdiutil convert raw-iBrew.dmg -format UDZO -o iBrew.dmg
	rm -f raw-iBrew.dmg
	
	#move finished product to release folder
	mkdir -p release
	mv iBrew.dmg release
	
