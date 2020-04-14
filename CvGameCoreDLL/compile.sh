#!/bin/bash
#Addition to nmake, as nmake doesn't seem to work with wine.
#Made by bluepotato. The code is released into the public domain.
#(not that this could really be considered creative work anyways, I just found the copyright notice in the original Makefile dumb)

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
#OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
#OTHER DEALINGS IN THE SOFTWARE.

#set -x

#You might want to change these variables here:
wine17="$HOME/.wine_versions/linux-amd64/1.7.55/bin/wine" #Your wine 1.7.55 installation directory.
PSDK="C:\Program Files\Microsoft Platform SDK"
VCTOOLKIT="C:\Program Files\Microsoft Visual C++ Toolkit 2003"
DLLOUTPUT="../Assets/CvGameCoreDLL.dll"

#You probably don't have to change these:
ARGS=$#
#Default to Release.
if (( $ARGS<1 )); then
	TARGET=Release
elif test $1 = "Release" || test $1 = "Debug"; then
	TARGET=$1
else
	echo "Invalid target: $1"
	exit 2
fi

echo "TARGET: $TARGET"

#Your wineprefix for compilation.
export WINEPREFIX="$HOME/compile_linux"

#Clean mode.
if test "$2" = "clean"; then
	rm -rf ./"$TARGET"
fi

#Use nmake to compile the files.
$wine17 "$PSDK\Bin\nmake" $TARGET

##TODO
#List files to compile.
#COMPILEFILES=""
#DLLEXISTS=$(test -f $DLLOUTPUT)
#if $DLLEXISTS; then
#	LASTCOMPILE=$(date -r $DLLOUTPUT +%s)
#fi
#for COMPILEFILE in $(ls)
#do
#	if ([[ $COMPILEFILE == *.cpp ]] || [[ $COMPILEFILE == *.h ]]) && (! $DLLEXISTS || [ "$LASTCOMPILE" -lt "$(date -r $COMPILEFILE +%s)" ]); then
#		COMPILEFILES="$COMPILEFILES $COMPILEFILE"
#	fi
#done

#echo "Files:" $COMPILEFILES

#Compiles the files.
#for COMPILEFILE in $COMPILEFILES
#do
#	rm $TARGET/${COMPILEFILE%.*}.obj
#	$wine17 "$VCTOOLKIT\bin\cl.exe" /nologo /MD /O2 /Oy /Oi /G7 /DNDEBUG /DFINAL_RELEASE /Fp"$TARGET\CvGameCoreDLL.pch" /GR /Gy /W3 /EHsc /Gd /Gm- /DWIN32 /D_WINDOWS /D_USRDLL /DCVGAMECOREDLL_EXPORTS /Yu"CvGameCoreDLL.h" /IBoost-1.32.0/include /IPython24/include /I"$VCTOOLKIT/include" /I"$PSDK/Include" /I"$PSDK/Include/mfc" /I".\CvGameCoreDLL\Boost-1.32.0/include" /I".\CvGameCoreDLL\Python24/include" "/Fo$TARGET\\${COMPILEFILE%.*}.obj" /c $COMPILEFILE
#done

#Make a list of files to link.
FILES=""
for FILE in $(ls $TARGET)
do
	if [[ $FILE == *.obj ]]; then
		FILES="$FILES $TARGET/$FILE"
	fi
done

echo "FILES: $FILES"

PDB=$TARGET"\CvGameCoreDLL.pdb"
IMPLIB=$TARGET"\CvGameCoreDLL.lib"

GLOBALFLAGS="$FILES /SUBSYSTEM:WINDOWS /LARGEADDRESSAWARE /TLBID:1 /DLL /NOLOGO /PDB:$PDB"
DEBUGFLAGS="$GLOBALFLAGS /DEBUG /INCREMENTAL /IMPLIB:$IMPLIB"
RELEASEFLAGS="$GLOBALFLAGS /INCREMENTAL:NO /OPT:REF /OPT:ICF"


#Create a DLL.
if test $TARGET = "Release"; then #For Release:
	$wine17 "$VCTOOLKIT\bin\link.exe" /LIBPATH:Python24/libs /LIBPATH:"boost-1.32.0/libs" /LIBPATH:"$VCTOOLKIT\lib" /LIBPATH:"$PSDK\Lib" /out:"../Assets/CvGameCoreDLL.dll" "boost-1.32.0\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "Python24\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" $RELEASEFLAGS
elif test $TARGET = "Debug"; then #For Debug:
	$wine17 "$VCTOOLKIT/bin/link.exe" /LIBPATH:"boost-1.32.0\libs" /LIBPATH:"$VCTOOLKIT\lib" /LIBPATH:"$PSDK\Lib" /out:"../Assets/CvGameCoreDLL.dll" "boost-1.32.0\libs\boost_python-vc71-mt-1_32.lib" winmm.lib user32.lib "$VCTOOLKIT\lib\msvcprt.lib" "$VCTOOLKIT\lib\msvcrt.lib" "Python24\libs\python24.lib" "$VCTOOLKIT\lib\OLDNAMES.lib" "$PSDK\Lib\AMD64\msvcprtd.lib" $DEBUGFLAGS
else #We should never get here.
	echo "ERROR: Wrong target " $TARGET
	exit 2
fi

echo "Done!"
