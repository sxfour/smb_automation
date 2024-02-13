@echo off

REM "Set following backup parameters to take backup"
SET PGPASSWORD=SOME VALUE
SET db_name=SOME VALUE
SET file_format=c
SET host_name=localhost
SET user_name=postgres
SET pg_dump_path="C:\Program Files\PostgreSQL\16\bin\pg_dump.exe"  
SET target_backup_path=C:\Backups\
SET target_backup_path_bot=C:\Backups\Bot\
SET other_pg_dump_flags=--blobs --verbose -c 

REM Fetch Current System Date and set month,day and year variables
for /f "tokens=1-3 delims=- " %%i in ("%date%") do (
	set month=%%j
	set day=%%i
	set year=%%k
)
for /f "tokens=1-3 delims=: " %%i in ("%time%") do (
	set hour=%%i
	set min=%%j
	set sec=%%k
)


REM Creating string for backup file name
for /f "delims=" %%i in ('dir "%target_backup_path%" /b/a-d ^| find /v /c "::"') do set count=%%i
set /a count=%count%+1 
set datestr=backup_%year%_%month%_%day%_%hour%_%min%

REM Backup File name
set BACKUP_FILE=%db_name%_%datestr%.backup
set BACKUP_FILE_TG_BOT=%db_name%.backup

REM :> Executing command to backup database 1
%pg_dump_path% --host=%host_name% -U %user_name% --format=%file_format%  %other_pg_dump_flags% -f %target_backup_path%%BACKUP_FILE%  %db_name% 

REM :> Executing command to backup database 2
%pg_dump_path% --host=%host_name% -U %user_name% --format=%file_format%  %other_pg_dump_flags% -f %target_backup_path_bot%%BACKUP_FILE_TG_BOT%  %db_name% 