@echo off

setlocal ENABLEDELAYEDEXPANSION
set SCRIPTDIR=%~dp0

echo TOOL VALIDTOR UTILTIY
echo.

:setOption
set /p choice= Enter Tool file location:

if not exist %choice% (
  echo File location is not valid
  echo.
  goto setOption
)

if exist %choice% (
 goto runToolTest
)

:runToolTest
python "%SCRIPTDIR%\main.py" --file %choice%
echo.
pause

goto setOption

:end
@REM pause


