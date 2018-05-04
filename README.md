# Documention for EECS 214 Auto Grader
#### Last Upated Spring 2018 by Ethan Robison

## Configuration
1. It's in Python3. If this bothers you because Python, then I justify my choice by saying accessibility. If this bothers you because "3," I say fuck right off Python 3 or b u s t.
2. You'll need a Canvas API key, and you'll need to put in in a file named "secret" in the same directory as `main.py`. I self-authenticated for this thing since I'm the only one who needs to run it. Presumably, you're doing the same.

## Overview of System

First, we configure the system to look at the right course and assignment.
Then we get a list of all of the students and make representations of each.
Then, we download each individual student's submission.
Then, we need to run our testing framework (MSTEST at the time of this writing; hopefully NUNIT in the future since it's cross-platform) on each submission solution.
We serialize out the results of the previous step.
Last, we need to take our test results (grades + comments) and upload them to Canvas. 

## Pathing Troubles
I'm using Windows' broken-ass "Bash on Ubuntu on Windows," so my life is suffering. I'm going to outline, generally, the steps that I take to call a Windows executable from the shell. If you are running all of this from the command prompt (for some reason), then you're presumably enough of a Windows hacker to figure this shit out on your own. Don't @ me, sorry.

### Calling an Executable
As an example, let's start with the path that my shell thinks points to `MSBuild`: `/mnt/c/Windows/Microsoft.NET/Framework64/v4.0.30319/MSBuild.exe`

Running this in the shell produces results similar to what I get if I run it in the command prompt:

> `Microsoft (R) Build Engine, versión 4.7.2556.0`
> `[Microsoft .NET Framework, versión 4.0.30319.42000]`
> `Copyright (C) Microsoft Corporation. Todos los derechos reservados.`
> 
> `MSBUILD : error MSB1003: Especifique un archivo de proyecto o de solución. El directorio de trabajo actual no contiene un archivo de proyecto ni de solución.`

(translation: specify a project or solution file; the current directory does not have any project or solution [Sorry for the Spanish - Ethan])

#### Notes:
- no space in `\testcontainer:$ARG`
- linux path vs windows path

- find MSTest and MSBuild in your Visual Studios program folder

# "/mnt/c/Program Files (x86)/Microsoft Visual Studio/2017/Community/MSBuild/15.0/Bin/MSBuild.exe" ./EECS\ 214\ Assignment\ 1.sln # to build the damn thing
# "/mnt/c/Program Files (x86)/Microsoft Visual Studio/2017/Community/Common7/IDE/MSTest.exe" "/testcontainer:QueueTests/bin/Debug/QueueTests.dll" "/detail:errormessage" # to run the damn unit tests