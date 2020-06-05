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
PSDK="C:\Program Files\Microsoft Platform SDK"
VCTOOLKIT="C:\Program Files\Microsoft Visual C++ Toolkit 2003"
DLLOUTPUT="../Assets/CvGameCoreDLL.dll"
OWINEPREFIX="$HOME/compile_linux"
PYTHON=".\Python24"
BOOST=".\Boost-1.32.0"
PARALLEL=1 #Spawn a bunch of child processes in release mode. 1 - on, 0 - off 

#You probably won't have to change anything below
set -e
export WINEDEBUG=-all

error() {
	echo "ERROR: $*"
	exit 1
}

CLEAN=1

if [ $# -lt 1 ]; then
	error "Unspecified target. USAGE: ./compile.sh [Release/Debug] [clean]" 
else #iterate over arguments
	for arg in "$@"; do
		if test "$arg" = "Release" || test "$arg" = "Debug"; then
			TARGET=$arg
		elif test "$arg" = "clean"; then
			CLEAN=0
		fi
	done
fi

if test "$TARGET" != ""; then
	echo "TARGET: $TARGET"
fi

#Clean mode.
if test $CLEAN = 0; then
	if test "$TARGET" != ""; then
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

cl() {
	owine "$VCTOOLKIT\bin\cl.exe" "$@"
}

link() {
	owine "$VCTOOLKIT\bin\link.exe" "$@"
}

should_compile() {
	if test $# -gt 2; then
		compiled="$TARGET/$3"
	else
		compiled="$TARGET/${1%.*}.obj"
	fi
	c_index=$2
	if ! test -f "$compiled"; then
		return 0
	elif [ "$(date -r "$compiled" +%s)" -lt "$(date -r "$1" +%s)" ]; then
		return 0
	fi
	
	set $(echo "$DEPENDS" | sed "${c_index}q;d")
	shift
	pattern=$(echo "$@" | sed "s/ /\|/g")
	latest_elem=$(ls -rt $(find . -maxdepth 1 | grep -Eio "$pattern") | tail -1)
	if test "$(date -r "$compiled" +%s)" -lt "$(date -r "$latest_elem" +%s)"; then
		return 0
	fi
	return 1
}

PCH="$TARGET\CvGameCoreDLL.pch"

echo "Finding dependencies..."
owine bin/fastdep.exe --objectextension=pch -q -O "$TARGET" CvGameCoreDLL.cpp > depends
for file in *.cpp; do
	owine bin/fastdep.exe --objectextension=obj -q -O "$TARGET" "$file" >> depends
done

DEPENDS="$(awk '{gsub(/\.\\/," ")}1' depends)" #A hacky way for getting fastdep to cooperate. For some reason .\.\ nukes the entire variable.
DEPENDS=$(echo "$DEPENDS" | sed ':a;N;$!ba;s/\\\r\n\t //g')
DEPENDS=$(echo "$DEPENDS" | sed ':a;N;$!ba;s/\r//g')
echo "$DEPENDS" > depends

#Set flags for compilation
GLOBAL_CFLAGS="/nologo /GR /Gy /W3 /EHsc /Gd /Gm- /DWIN32 /D_WINDOWS /D_USRDLL /DCVGAMECOREDLL_EXPORTS /YuCvGameCoreDLL.h /Fp$PCH"
if test "$TARGET" = "Release"; then
	set "/MD" "/O2" "/Oy" "/Oi" "/G7" "/DNDEBUG" "/DFINAL_RELEASE" $GLOBAL_CFLAGS
elif test "$TARGET" = "Debug"; then
	set "/MD" "/Zi" "/Od" "/D_DEBUG" "/RTC1" $GLOBAL_CFLAGS
fi

#Generate precompiled header
ci=1
if should_compile "_precompile.cpp" $ci "CvGameCoreDLL.pch"; then
	echo "Generating precompiled header..."
	cl "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/YcCvGameCoreDLL.h" "/Fo$TARGET\_precompile.obj" "/c" "_precompile.cpp"
fi

#Compile the files
if test "$TARGET" = "Release"; then
	if test "$PARALLEL" -eq 1; then
		for COMPILEFILE in *; do
			if test "$(echo "$COMPILEFILE" | awk -F . '{print $NF}')" = "cpp" && test "$COMPILEFILE" != "_precompile.cpp"; then
				ci=$((ci+1))
				(
				if should_compile "$COMPILEFILE" $ci; then
					cl "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" "/c" "$COMPILEFILE"
				fi
				)&
			fi
		done
		wait
	elif test "$PARALLEL" -eq 0; then
		for COMPILEFILE in *; do
			if test "$(echo "$COMPILEFILE" | awk -F . '{print $NF}')" = "cpp" && test "$COMPILEFILE" != "_precompile.cpp"; then
				ci=$((ci+1))
				if should_compile "$COMPILEFILE" $ci; then
					cl "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" "/c" "$COMPILEFILE"
				fi
			fi
		done
	else
		error "PARALLEL not set to a valid value"
	fi
elif test "$TARGET" = "Debug"; then
	for COMPILEFILE in *; do
		if test "$(echo "$COMPILEFILE" | awk -F . '{print $NF}')" = "cpp" && test "$COMPILEFILE" != "_precompile.cpp"; then
			ci=$((ci+1))
			if should_compile "$COMPILEFILE" $ci; then
				cl "$@" "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" "/c" "$COMPILEFILE"
			fi
		fi
	done
fi

LINKFILES="$(find "$TARGET"/*.obj)"

PDB="$TARGET\CvGameCoreDLL.pdb"
IMPLIB="$TARGET\CvGameCoreDLL.lib"
GLOBALFLAGS="$LINKFILES /SUBSYSTEM:WINDOWS /LARGEADDRESSAWARE /TLBID:1 /DLL /NOLOGO /PDB:$PDB"
DEBUGFLAGS="$GLOBALFLAGS /DEBUG /INCREMENTAL /IMPLIB:$IMPLIB"
RELEASEFLAGS="$GLOBALFLAGS /INCREMENTAL:NO /OPT:REF /OPT:ICF"

#Create a DLL.
if test "$TARGET" = "Release"; then #For Release:
	link $RELEASEFLAGS "/LIBPATH:$PSDK\Lib" "$BOOST\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "$PYTHON\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" "/out:$DLLOUTPUT"
elif test "$TARGET" = "Debug"; then #For Debug:
	link $DEBUGFLAGS "/LIBPATH:$PSDK\Lib" "$BOOST\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "$PYTHON\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" "$PSDK\Lib\AMD64\msvcprtd.lib" "/out:$DLLOUTPUT"
fi

echo "Done!"
