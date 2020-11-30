#!/bin/sh
#Author: bluepotato
#This script is released into the public domain.
#USAGE: ./compile.sh [Release/Debug] [clean]
#nmake doesn't work too great with wine, so this is intended to replace it on
#Linux. This should be POSIX-compliant. As to why I made this: firstly it's
#less hacky than nmake.sh, secondly it doesn't spam the console like nmake.sh
#does, and thirdly it's usually faster, or at least isn't slower. It also
#supports multiprocessing for Release builds, which makes it way faster on my
#system - you may want to disable it if yours has a low amount of cores/threads.

#You might want to change some of these variables here:
wine17="$HOME/.wine_versions/linux-x86/1.7.55/bin/wine" #Path to your wine 1.7.55 binary.
PSDK="C:/Program Files/Microsoft Platform SDK"
VCTOOLKIT="C:/Program Files/Microsoft Visual C++ Toolkit 2003"
DLLOUTPUT="../Assets/CvGameCoreDLL.dll"
OWINEPREFIX="$HOME/compile_linux"
PYTHON="./Python24"
BOOST="./Boost-1.32.0"
#Spawn a bunch of child processes in release mode. true - on, false - off
PARALLEL=true
#Generate compile_commands.json for the clangd language server. true - on, false - off
#TODO: this doesn't work yet
CLANGD=false

#You probably won't have to change anything below
set -e

error() {
	echo "ERROR: $*" >&2
	exit 2
}

CLEAN=false

tolower() {
	printf '%s\n' "$1" | tr '[:upper:]' '[:lower:]'
}

toupper() {
	printf '%s\n' "$1" | tr '[:lower:]' '[:upper:]'
}

dec() {
	printf '%d\n' $(($1-1))
}

if test $# -lt 1; then
	error "Unspecified target. USAGE: ./compile.sh [release/debug] [clean]"
else #iterate over arguments
	for arg in "$@"; do
		larg="$(tolower "$arg")"
		if test "$larg" = "release" || test "$larg" = "debug"; then
			TARGET="$(toupper "$(printf '%s\n' "$arg" | head -c1)")$(tolower "$(printf '%s\n' "$arg" | tail -c+2)")"
		elif test "$larg" = "clean"; then
			CLEAN=true
		else
			error "Invalid argument $arg"
		fi
	done
fi

export WINEDEBUG=-all
PID="$$"
WINEPWD="$(winepath -w "$PWD")"

if $CLEAN && $CLANGD; then
	printf '[\n' > ./compile_commands.json.new
fi

if test "$TARGET"; then
	echo "TARGET: $TARGET"
fi

#Clean mode.
if $CLEAN; then
	if test "$TARGET"; then
		if test -e "$TARGET"; then
			echo "CLEAN: cleaning $TARGET"
			rm -r ./"$TARGET"
		else
			echo "CLEAN: nothing to clean"
		fi
	else
		echo "CLEAN: cleaning Release and Debug"
		if test -e Release; then
			rm -r ./Release/
		fi
		if test -e Debug; then
			rm -r ./Debug/
		fi
		exit 0
	fi
fi

if ! test -e "$TARGET"; then
	mkdir "$TARGET"
fi


owine() { #wine 1.7.55
	WINEPREFIX="$OWINEPREFIX" $wine17 "$@"
}

generate_compile_command() {
	printf \
'{
"directory": "%s",
"command": "%s",
"file": "%s"
},\n' "$WINEPWD" "$(printf '"%s" ' "$@" | sed 's/"\/G7" //g' | sed 's/"/\\"/g')" "$WINEPWD/$2" >> compile_commands.json.new
}

cl() {
	if ! owine "$VCTOOLKIT/bin/cl.exe" "$@"; then
		echo "Failed to compile $1" >&2
		#Yes this is quite brutal but I'm not aware of any better methods to do this
		kill -9 "$PID"
		exit 1
	fi
	if $CLEAN && $CLANGD; then
		generate_compile_command "c++" "$@"
	fi
}

link() {
	owine "$VCTOOLKIT/bin/link.exe" "$@"
}

should_compile() {
	if test $# -gt 2; then
		compiled="$TARGET/$3"
	else
		compiled="$TARGET/${1%.*}.obj"
	fi

	if ! test -f "$compiled" || test "$(date -r "$compiled" +%s)" -lt "$(date -r "$1" +%s)"; then
		return 0
	fi

	set -- $(echo "$DEPENDS" | sed "${2}q;d")
	shift
	test "$(date -r "$compiled" +%s)" -lt "$(date -r "$(ls -rt $(find . -maxdepth 1 | grep -Eio "$(echo "$@" | sed "s/ /\|/g")") | tail -1)" +%s)"
}

PCH="$TARGET/CvGameCoreDLL.pch"

echo "Finding dependencies..."
owine bin/fastdep.exe --objectextension=pch -q -O "$TARGET" CvGameCoreDLL.cpp > depends
for file in *.cpp; do
	owine bin/fastdep.exe --objectextension=obj -q -O "$TARGET" "$file" >> depends
done

DEPENDS="$(awk '{gsub(/\.\\/," ")}1' depends | sed ':a;N;$!ba;s/\\\r\n\t //g' | sed ':a;N;$!ba;s/\r//g')" #A hacky way for getting fastdep to cooperate. For some reason .\.\ nukes the entire variable.
#echo "$DEPENDS" > depends

#Set flags for compilation
GLOBAL_CFLAGS="/MD /nologo /GR /Gy /W3 /EHsc /Gd /Gm- /DWIN32 /D_WINDOWS /D_USRDLL /DCVGAMECOREDLL_EXPORTS /YuCvGameCoreDLL.h /c /Fp$PCH"
if test "$TARGET" = "Release"; then
	set -- "/O2" "/Oy" "/Oi" "/G7" "/DNDEBUG" "/DFINAL_RELEASE" $GLOBAL_CFLAGS
elif test "$TARGET" = "Debug"; then
	set -- "/Zi" "/Od" "/D_DEBUG" "/RTC1" $GLOBAL_CFLAGS
fi

#Generate precompiled header
ci=1
if should_compile "_precompile.cpp" $ci "CvGameCoreDLL.pch"; then
	echo "Generating precompiled header..."
	cl "_precompile.cpp" "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/YcCvGameCoreDLL.h" "/Fo$TARGET/_precompile.obj"
fi

#Compile the files
if test "$TARGET" = "Release"; then
	if $PARALLEL; then
		PIDS=""
		for COMPILEFILE in *.cpp; do
			if test "$COMPILEFILE" != "_precompile.cpp"; then
				ci=$((ci+1))
				(
				if should_compile "$COMPILEFILE" $ci; then
					cl "$COMPILEFILE" "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET/${COMPILEFILE%.*}.obj"
				fi
				)&
				PIDS="$PIDS $!"
			fi
		done
		for p in $PIDS; do
			if ! wait $p; then
				test -z "$(jobs -p)" || kill $(jobs -p)
				exit 1
			fi
		done
	else
		for COMPILEFILE in *.cpp; do
			if test "$COMPILEFILE" != "_precompile.cpp"; then
				ci=$((ci+1))
				if should_compile "$COMPILEFILE" $ci; then
					cl "$COMPILEFILE" "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET/${COMPILEFILE%.*}.obj"
				fi
			fi
		done
	fi
elif test "$TARGET" = "Debug"; then
	for COMPILEFILE in *.cpp; do
		if test "$COMPILEFILE" != "_precompile.cpp"; then
			ci=$((ci+1))
			if should_compile "$COMPILEFILE" $ci; then
				cl "$COMPILEFILE" "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET/${COMPILEFILE%.*}.obj"
			fi
		fi
	done
fi

#Link resulting files
LINKFILES="$(find "$TARGET"/*.obj)"

GLOBALFLAGS="$LINKFILES /SUBSYSTEM:WINDOWS /LARGEADDRESSAWARE /TLBID:1 /DLL /NOLOGO /PDB:$TARGET/CvGameCoreDLL.pdb"
if test "$TARGET" = "Release"; then
	FLAGS="$GLOBALFLAGS /INCREMENTAL:NO /OPT:REF /OPT:ICF"
	set -- ""
else
	FLAGS="$GLOBALFLAGS /DEBUG /INCREMENTAL /IMPLIB:$TARGET/CvGameCoreDLL.lib"
	set -- " " "$PSDK/Lib/AMD64/msvcprtd.lib"
fi

link $FLAGS "/LIBPATH:$PSDK/Lib" "$BOOST/libs/boost_python-vc71-mt-1_32.lib" "winmm.lib" "user32.lib" "$VCTOOLKIT/lib/msvcprt.lib" "$VCTOOLKIT/lib/msvcrt.lib" "$PYTHON/libs/python24.lib" "$VCTOOLKIT/lib/OLDNAMES.lib" "/out:$DLLOUTPUT""$@"

if $CLEAN && $CLANGD; then
	cat compile_commands.json.new | head -n$(dec $(cat compile_commands.json.new | wc -l)) > compile_commands.json
	rm compile_commands.json.new
	printf '}\n]\n' >> compile_commands.json
fi

echo "Done!"
