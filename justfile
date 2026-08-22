icon:
    rc executor\windows.rc

exe:
    cl /std:c++17 /O2 executor\windows.cpp executor\windows.res /Fe:src\kivo\resources\executor\kivo.exe /link /SUBSYSTEM:WINDOWS