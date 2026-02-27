SET versionValue=1.0.0
call version_specific.bat --create "Creating Version File (Should be used for First Time only)"
call version_specific.bat --newversion "Setting Default Version" %versionValue%