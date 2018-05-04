class Testable(object):
    """Builds a student's project, then runs tests from the appropriate .dll"""

    # buildPath = '"C:/Program Files (x86)/MSBuild/12.0/Bin/MSBuild.exe" ' + slnPath
# def buildAndTest(slnPath, dllPath, name):
#     build = subprocess.Popen(buildPath, shell=True,
#                              stdout=subprocess.PIPE).stdout.read()
#     if not "Build FAILED." in build:
#         print "\ntesting...\n"
#         testPath = '"C:/Program Files (x86)/Microsoft Visual Studio 12.0/Common7/IDE/MSTest.exe" /testcontainer:' + \
#             dllPath + ' /detail:errormessage'
#         output = subprocess.Popen(
#             testPath, stdout=subprocess.PIPE, shell=True).stdout.read()
#         exportTests(output, name)
#         results = cleanResults(output)
#     else:
#         print "NO BUILD"
#         exportTests(build, name)
#         results = {'passed': 0, 'failed': 99}
#     return results
