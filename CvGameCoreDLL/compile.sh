#!/bin/bash
#Author: bluepotato
#This script is released into the public domain.
#USAGE: ./compile.sh [Release/Debug] [clean]
#nmake doesn't work too great with wine, so this is intended to replace it
#on Linux. This should be POSIX-compliant, the only "extra" it needs is awk.
#As to why I made this: firstly it's less hacky, secondly it doesn't spam the
#console like nmake.sh, and thirdly it's usually faster, or at least isn't
#slower. It also supports multiprocessing for Release builds, which makes it
#way faster. Here's a small benchmark (for the RFGW DLL):
#				compile.sh	nmake.sh
#Release (Changed 1 cpp file):	24s		24s
#Debug (Changed 1 cpp file):	9s		9s
#Release (Changed CvGlobals.h)	1m8s		2m41
#Debug (Changed CvGlobals.h)	1m43s		2m8s
#Clean Release:			1m8s		2m42s
#Clean Debug:			1m37s		2m12s


#You might want to change some of these variables here:
wine17="$HOME/.wine_versions/linux-x86/1.7.55/bin/wine" #Your wine 1.7.55 installation directory.
PSDK="C:\Program Files\Microsoft Platform SDK"
VCTOOLKIT="C:\Program Files\Microsoft Visual C++ Toolkit 2003"
DLLOUTPUT="../Assets/CvGameCoreDLL.dll"
OWINEPREFIX="$HOME/compile2"
PYTHON=".\Python24"
BOOST=".\Boost-1.32.0"

#You probably won't have to change anything below
set -e
error() {
	echo "ERROR: $*"
	exit 1
}

export WINEDEBUG=-all
CLEAN=1

if [ $# -lt 1 ]; then
	error "Unspecified target. USAGE: ./compile.sh [Release/Debug] [clean]" 
else #iterate over arguments
	for arg in "$@"; do
		if test "$arg" = "Release" || test $arg = "Debug"; then
			TARGET=$arg
		elif test "$arg" = "clean"; then
			CLEAN=0
		fi
	done
fi

echo "TARGET: $TARGET"

owine() { #wine 1.7.55
	WINEPREFIX="$OWINEPREFIX" $wine17 "$@"
}

cl() {
	owine "$VCTOOLKIT\bin\cl.exe" "$@"
}

link() {
	owine "$VCTOOLKIT\bin\link.exe" "$@"
}

disable_ifs() {
	PREV_IFS="$IFS"
	IFS=""
}

enable_ifs() {
	IFS="$PREV_IFS"
}

echo "Finding dependencies..."
owine bin/fastdep.exe --objectextension=pch -q -O "$TARGET" CvGameCoreDLL.cpp > depends
for file in $(ls *.cpp); do
	owine bin/fastdep.exe --objectextension=obj -q -O "$TARGET" "$file" >> depends
done

DEPENDS="$(awk '{gsub(/\.\\/," ")}1' depends)" #A hacky way for getting fastdep to cooperate. For some reason .\.\ nukes the entire variable.
DEPENDS=$(echo "$DEPENDS" | sed ':a;N;$!ba;s/\\\r\n\t //g')
DEPENDS=$(echo "$DEPENDS" | sed ':a;N;$!ba;s/\r//g')
echo "$DEPENDS" > depends

should_compile() {
	if test $# -gt 2; then
		compiled="$TARGET/$3"
	else
		compiled="$TARGET/${1%.*}.obj"
	fi
	c_index=$2
	if ! [ -f "$compiled" ]; then
		return 0
	elif [ "$(date -r $compiled +%s)" -lt "$(date -r $1 +%s)" ]; then
		return 0
	fi
	
	set $(echo "$DEPENDS" | sed "${c_index}q;d")
	shift
	pattern=$(echo "$@" | sed "s/ /\|/g")
	ELEMS=$(find . -maxdepth 1 | ack -io $pattern)
	if test "$LASTCOMPILE" -lt "$(date -r $(ls -rt $ELEMS | tail -1) +%s)"; then
		return 0
	fi
	return 1
}

PCH="$TARGET\CvGameCoreDLL.pch"
PDB="$TARGET\CvGameCoreDLL.pdb"
IMPLIB="$TARGET\CvGameCoreDLL.lib"

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
	fi
fi

if test -f "$DLLOUTPUT"; then
	LASTCOMPILE=$(date -r $DLLOUTPUT +%s)
else
	LASTCOMPILE=0
fi

if ! test -e "$TARGET"; then
	mkdir "$TARGET"
fi

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
	cl $@ "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/YcCvGameCoreDLL.h" "/Fo$TARGET\_precompile.obj" "/c" "_precompile.cpp"
fi

#Compile the files
if test "$TARGET" = "Release"; then
	for COMPILEFILE in $(ls); do
		if test $(echo "$COMPILEFILE" | awk -F . '{print $NF}') = "cpp" && test "$COMPILEFILE" != "_precompile.cpp"; then
			ci=$((ci+1))
			(
			if should_compile "$COMPILEFILE" $ci; then
				cl $@ "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" "/c" "$COMPILEFILE"
			fi
			)&
		fi
	done
	wait
elif test "$TARGET" = "Debug"; then
	for COMPILEFILE in $(ls); do
		if test $(echo "$COMPILEFILE" | awk -F . '{print $NF}') = "cpp" && test "$COMPILEFILE" != "_precompile.cpp"; then
			ci=$((ci+1))
			if should_compile "$COMPILEFILE" $ci; then
				cl $@ "/I$VCTOOLKIT/include" "/I$PSDK/Include" "/I$PSDK/Include/mfc" "/I$BOOST/include" "/I$PYTHON/include" "/I$BOOST/include/" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" "/c" "$COMPILEFILE"
			fi
		fi
	done
	wait
fi

LINKFILES="$(find $TARGET/*.obj)"

GLOBALFLAGS="$LINKFILES /SUBSYSTEM:WINDOWS /LARGEADDRESSAWARE /TLBID:1 /DLL /NOLOGO /PDB:$PDB"
DEBUGFLAGS="$GLOBALFLAGS /DEBUG /INCREMENTAL /IMPLIB:$IMPLIB"
RELEASEFLAGS="$GLOBALFLAGS /INCREMENTAL:NO /OPT:REF /OPT:ICF"

#Create a DLL.
if test "$TARGET" = "Release"; then #For Release:
	link $RELEASEFLAGS "/LIBPATH:$PSDK\Lib" "$BOOST\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "$PYTHON\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" /out:"../Assets/CvGameCoreDLL.dll"
elif test "$TARGET" = "Debug"; then #For Debug:
	link $DEBUGFLAGS "/LIBPATH:$PSDK\Lib" "$BOOST\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "$PYTHON\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" "$PSDK\Lib\AMD64\msvcprtd.lib" /out:"../Assets/CvGameCoreDLL.dll"
fi

echo "Done!"
