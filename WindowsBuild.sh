nasm -f win64 forester_compiler.asm -o forester.obj
link forester.obj /subsystem:console /defaultlib:msvcrt.lib /out:forester.exe
